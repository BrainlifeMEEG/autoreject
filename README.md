# Autoreject

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)

Brainlife App to automatically detect and repair bad epochs/channels in MEG/EEG epoched data using the [autoreject](https://autoreject.github.io/stable/index.html) package.

## Description

`autoreject` fits a cross-validated model that learns, per channel type, how many channels can be interpolated within an epoch and how many bad channels are tolerated before the epoch is dropped outright, rather than relying on a single fixed peak-to-peak amplitude threshold. This app:

- Loads MNE-compatible epoched data in FIF format
- Fits `autoreject.AutoReject` on the epochs via cross-validation
- Transforms the epochs: interpolates repairable channels and drops unrepairable epochs
- Generates a reject-log visualization and before/after comparison figures
- Creates an interactive HTML report for quality control

## Inputs

- **epo**: Path to MNE epochs data file in FIF format (.fif)

## Outputs

- **out_dir/epo.fif**: Cleaned epochs (bad epochs dropped, bad channels interpolated)
- **out_dir/info.txt**: Summary of dropped epochs and interpolated channels
- **out_figs/reject_log.png**: Visualization of the reject log (bad/interpolated/good per channel per epoch)
- **out_figs/epochs_before.png**, **out_figs/epochs_after.png**: Before/after comparison
- **out_report/report.html**: Interactive HTML report with reject-log and epochs visualizations
- **product.json**: Metadata file for Brainlife.io interface

## Configuration Parameters

All parameters are specified in `config.json`:

- **n_interpolate** (comma-separated integers, default: `1,4,32`): Candidate values for the number of channels to interpolate per epoch, tried during cross-validation.
- **consensus** (comma-separated floats, optional): Candidate values for the fraction of channels that must agree an epoch is bad. If empty, defaults to 11 evenly spaced values between 0 and 1.
- **cv** (integer, default: 10): Number of cross-validation folds.
- **picks** (string, optional): Channel type to run on (e.g. `eeg`, `meg`). If empty, autoreject infers channels from the data.
- **thresh_method** (string, default: `bayesian_optimization`): Threshold search strategy. Options: `bayesian_optimization`, `random_search`.
- **random_state** (integer, optional): Random seed for reproducibility. If empty, results will vary between runs.
- **n_jobs** (integer, default: 8): Number of parallel jobs for the cross-validated search. Should match the job's allocated CPU count.

## Usage

The app is typically run on the Brainlife.io platform through the web interface. To run locally:

```bash
python main.py
```

The `main.py` script reads the `config.json` file to get all parameters and data paths.

## Citation

Jas, M., Engemann, D., Bekhti, Y., Raimondo, F., & Gramfort, A. (2017). Autoreject: Automated artifact rejection for MEG and EEG data. *NeuroImage*, 159, 417-429. https://doi.org/10.1016/j.neuroimage.2017.06.030

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
