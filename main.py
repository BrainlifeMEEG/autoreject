"""
Automatically detect and repair bad epochs/channels in MEG/EEG epoched data.

This app uses the autoreject package (Jas et al., 2017) to fit a
cross-validated model estimating, per channel type, how many channels can be
interpolated per epoch and how many bad channels are tolerated before an
epoch is dropped outright.

Inputs:
    - epo: Path to MNE epochs .fif file

Outputs:
    - out_dir/meg-epo.fif: Cleaned epochs (bad epochs dropped, bad channels interpolated)
    - out_dir/info.txt: Summary of dropped epochs / interpolated channels
    - out_figs/reject_log.png: Visualization of the reject log
    - out_figs/epochs_before.png, out_figs/epochs_after.png: Before/after comparison
    - out_report/report.html: MNE Report
    - product.json: Metadata about the cleaning
"""

# Copyright (c) 2026 brainlife.io
#
# Automated artifact rejection/repair on MNE epochs using autoreject.
#
# Authors:
# - Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne
import numpy as np
import matplotlib.pyplot as plt
from autoreject import AutoReject

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    require_config_keys
)

mne.set_log_level('WARNING')
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_figs', 'out_report')

# Load configuration
config = load_config()
require_config_keys(config, ['epo'])

# == LOAD DATA ==
epochs = mne.read_epochs(config['epo'], preload=True)
print(f'Loaded {len(epochs)} epochs', flush=True)

product_items = []

# == PARSE PARAMETERS ==
n_interpolate = [1, 4, 32]
if config.get('n_interpolate') not in (None, '', 'None'):
    try:
        n_interpolate = [int(x.strip()) for x in str(config['n_interpolate']).split(',') if x.strip()]
    except Exception as e:
        print(f'Warning: Could not parse n_interpolate "{config["n_interpolate"]}", using default {n_interpolate}: {e}')

consensus = list(np.linspace(0, 1.0, 11))
if config.get('consensus') not in (None, '', 'None'):
    try:
        consensus = [float(x.strip()) for x in str(config['consensus']).split(',') if x.strip()]
    except Exception as e:
        print(f'Warning: Could not parse consensus "{config["consensus"]}", using default: {e}')

cv = int(config.get('cv') or 10)
picks = config.get('picks') or None
thresh_method = config.get('thresh_method') or 'bayesian_optimization'
if thresh_method not in ('bayesian_optimization', 'random_search'):
    print(f'Warning: Unknown thresh_method "{thresh_method}", falling back to bayesian_optimization')
    thresh_method = 'bayesian_optimization'
random_state = config.get('random_state')
random_state = int(random_state) if random_state not in (None, '', 'None') else None
n_jobs = int(config.get('n_jobs') or 1)

add_info_to_product(
    product_items,
    f'n_interpolate={n_interpolate}, consensus={[round(c, 2) for c in consensus]}, cv={cv}'
)

# == PLOT BEFORE ==
fig = epochs.plot_image(picks='data', combine='gfp', show=False)
fig[0].savefig(os.path.join('out_figs', 'epochs_before.png'))
plt.close(fig[0])

# == FIT AUTOREJECT ==
# n_jobs defaults to 1 (AutoReject's own default) unless the caller passes
# a higher value matching the job's actual CPU allocation -- the CV grid
# search over n_interpolate x consensus candidates parallelizes across
# it, so leaving this at 1 wastes however many cores Slurm allocated.
# verbose=True (not the previous False): AutoReject has real per-candidate
# progress reporting by default: silencing it was making a genuinely
# multi-hour CV search (confirmed on the ICM cluster: still running past
# 4h with zero log output, eventually Slurm-walltime-killed) indistinguish-
# able from a hang, the exact same ambiguity already found+fixed for
# ICA-fit (see that app's own commit history for the pattern).
print(f'[{datetime.datetime.now().isoformat()}] Starting AutoReject fit '
      f'(n_interpolate={n_interpolate}, consensus={len(consensus)} values, '
      f'cv={cv}, n_jobs={n_jobs}) on {len(epochs)} epochs...', flush=True)
ar = AutoReject(
    n_interpolate=n_interpolate,
    consensus=consensus,
    cv=cv,
    picks=picks,
    thresh_method=thresh_method,
    random_state=random_state,
    n_jobs=n_jobs,
    verbose=True,
)
ar.fit(epochs)
print(f'[{datetime.datetime.now().isoformat()}] AutoReject fit done, '
      f'transforming...', flush=True)
epochs_clean, reject_log = ar.transform(epochs, return_log=True)

# == SUMMARY STATS ==
n_bad_epochs = int(reject_log.bad_epochs.sum())
pct_bad_epochs = 100 * n_bad_epochs / len(epochs)
n_interpolated = int((reject_log.labels == 2).sum())

msg = (f'Dropped {n_bad_epochs}/{len(epochs)} epochs ({pct_bad_epochs:.1f}%); '
       f'interpolated {n_interpolated} channel-epoch instances')
print(msg)
add_info_to_product(product_items, msg, 'success')

# == PLOT REJECT LOG ==
fig_log = reject_log.plot('horizontal', show=False)
reject_log_path = os.path.join('out_figs', 'reject_log.png')
fig_log.savefig(reject_log_path)
plt.close(fig_log)

# == PLOT AFTER ==
fig = epochs_clean.plot_image(picks='data', combine='gfp', show=False)
fig[0].savefig(os.path.join('out_figs', 'epochs_after.png'))
plt.close(fig[0])

# == SAVE CLEANED EPOCHS ==
out_epo_path = os.path.join('out_dir', 'meg-epo.fif')
epochs_clean.save(out_epo_path, overwrite=True)

# Validate round-trip before declaring success
_ = mne.read_epochs(out_epo_path, preload=False)
print(f'Verified {out_epo_path} reloads successfully')

# == SAVE INFO TEXT ==
info_text = (
    f'Epochs before: {len(epochs)}\n'
    f'Epochs dropped: {n_bad_epochs} ({pct_bad_epochs:.1f}%)\n'
    f'Epochs remaining: {len(epochs_clean)}\n'
    f'Channel-epoch instances interpolated: {n_interpolated}\n'
)
with open(os.path.join('out_dir', 'info.txt'), 'w') as f:
    f.write(info_text)

# == CREATE REPORT ==
report = mne.Report(title='Autoreject Report')
report.add_epochs(epochs=epochs, title='Original Epochs')
report.add_image(image=reject_log_path, title='Reject Log')
report.add_epochs(epochs=epochs_clean, title='Cleaned Epochs')
report.save(os.path.join('out_report', 'report.html'), overwrite=True, verbose=False)

# == CREATE PRODUCT.JSON ==
add_image_to_product(product_items, name='Reject log', filepath=reject_log_path)
add_image_to_product(product_items, name='Epochs before cleaning', filepath=os.path.join('out_figs', 'epochs_before.png'))
add_image_to_product(product_items, name='Epochs after cleaning', filepath=os.path.join('out_figs', 'epochs_after.png'))
create_product_json(product_items)
