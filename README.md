# Autoreject

[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.954-blue.svg)](https://doi.org/10.25663/brainlife.app.954)
[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)

## Description

`autoreject` fits a cross-validated model that learns, per channel type, how many channels can be interpolated within an epoch and how many bad channels are tolerated before the epoch is dropped outright, rather than relying on a single fixed peak-to-peak amplitude threshold. This app calls the [autoreject](https://autoreject.github.io/stable/index.html) package's `autoreject.AutoReject` to fit this model on MNE-Python epoched data and transform the epochs accordingly.

The app generates:
- Cleaned epochs with bad epochs dropped and repairable channels interpolated
- A reject-log visualization and before/after comparison figures
- An interactive HTML report for quality control

## Inputs

- **`epo`** (`neuro/meeg/mne/epochs`): epoched MEG/EEG data to clean (required)

## Outputs

- **`out_dir/meg-epo.fif`** (`neuro/meeg/mne/epochs`): cleaned epochs (bad epochs dropped, bad channels interpolated)
- **`out_dir/info.txt`**: summary of dropped epochs and interpolated channels
- **`out_figs/reject_log.png`**: visualization of the reject log (bad/interpolated/good per channel per epoch)
- **`out_figs/epochs_before.png`**, **`out_figs/epochs_after.png`**: before/after comparison
- **`out_report/report.html`**: interactive HTML report with the reject-log and epochs visualizations
- **`product.json`**: metadata about the cleaning, for the Brainlife.io interface

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `n_interpolate` | string (comma-separated integers) | `"1,4,32"` | Candidate values for the number of channels to interpolate per epoch, tried during cross-validation. |
| `consensus` | string (comma-separated floats) | `""` | Candidate values for the fraction of channels that must agree an epoch is bad. If empty, defaults to 11 evenly spaced values between 0 and 1. |
| `cv` | number | `10` | Number of cross-validation folds. |
| `picks` | string | `""` | Channel type to run on (e.g. `eeg`, `meg`). If empty, autoreject infers channels from the data. |
| `thresh_method` | string | `"bayesian_optimization"` | Threshold search strategy: `bayesian_optimization` or `random_search`. |
| `random_state` | number | `42` | Random seed for reproducibility. If empty, results will vary between runs. |
| `n_jobs` | number | `8` | Number of parallel jobs for the cross-validated search. Should match the job's allocated CPU count. |

## Usage

### Running on Brainlife.io

1. Select your epoched MEG/EEG dataset as the `epo` input.
2. Optionally adjust `n_interpolate`, `consensus`, `cv`, `picks`, `thresh_method`, `random_state`, and `n_jobs`.
3. Submit the process.
4. Review the reject-log and before/after figures, and the HTML report, once the task completes.

### Local Testing

```bash
# Update config.json with your epoched data path, then:
python main.py
```

## Authors

- Maximilien Chaumon (https://github.com/dnacombo)

## Citations

- Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
- Gramfort, A. et al. MEG and EEG data analysis with MNE-Python. Front. Neurosci. 7, 267 (2013). https://doi.org/10.3389/fnins.2013.00267
- Jas, M., Engemann, D., Bekhti, Y., Raimondo, F., & Gramfort, A. (2017). Autoreject: Automated artifact rejection for MEG and EEG data. NeuroImage, 159, 417-429. https://doi.org/10.1016/j.neuroimage.2017.06.030

## Funding Acknowledgement

brainlife.io is publicly funded. We kindly ask that you acknowledge the funding below in your code and publications.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

## License

Copyright (c) 2026 MEEG Brainlife team. Licensed under AGPL-3.0, see [license.txt](license.txt).
