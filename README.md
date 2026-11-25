<h1 align="center">Autoreject</h1>

<p align="center">
  Cleans epoched MEG/EEG data with autoreject, learning per-channel rejection thresholds by cross-validation to interpolate bad channels and drop bad epochs, and outputs the cleaned epochs and QC figures.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.954"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.954-blue.svg" alt="Run on brainlife.io"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Cleans epoched MEG/EEG data with autoreject, learning per-channel rejection thresholds by cross-validation to interpolate bad channels and drop bad epochs, and outputs the cleaned epochs and QC figures.**

Fits autoreject with candidate n_interpolate and consensus values (cross-validated, Bayesian optimization or random search) and applies it, interpolating repairable channels within epochs and dropping epochs with too many bad channels. Use it after epoching as an automated alternative to fixed peak-to-peak rejection. It needs epochs with sensor positions; runs can take hours on large datasets.

| | |
|---|---|
| **Inputs** | `neuro/meeg/mne/epochs` |
| **Outputs** | `neuro/meeg/mne/epochs` |
| **Container** | `brainlifemeeg/mne:1.12.1` |
| **Resources** | 8 CPUs · 20 GB memory · 8 h walltime |
| **Run it** | [doi.org/10.25663/brainlife.app.954](https://doi.org/10.25663/brainlife.app.954) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `epo` | `neuro/meeg/mne/epochs` | yes | Epoched MEG/EEG data in MNE epochs .fif format. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/epochs` | Cleaned epochs after autoreject (bad epochs dropped, bad channels interpolated) |

<details>
<summary><b>Parameters</b> (7)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `n_interpolate` | string | `1,4,32` | Candidate values (comma-separated) for number of channels to interpolate per epoch, tried during cross-validation |
| `consensus` | string |  | Candidate consensus fractions (comma-separated). Empty = 11 evenly spaced values 0–1 |
| `cv` | number | `10` | Number of cross-validation folds |
| `picks` | string |  | Channel type to run on (e.g. eeg, meg). Empty = infer from data |
| `thresh_method` | string | `bayesian_optimization` | Threshold search strategy: bayesian_optimization or random_search |
| `random_state` | number | `42` | Random seed for reproducibility |
| `n_jobs` | number | `8` | Parallel jobs for cross-validated search; should match allocated CPUs (currently 8) |

</details>

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.954](https://doi.org/10.25663/brainlife.app.954), choose `neuro/meeg/mne/epochs` from your project, set the parameters and press **Execute**. The results are saved to your project as `neuro/meeg/mne/epochs`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `brainlifemeeg/mne:1.12.1`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "epo": "/path/to/epo/epo",
       "n_interpolate": "1,4,32",
       "consensus": "",
       "cv": 10,
       "picks": "",
       "thresh_method": "bayesian_optimization",
       "random_state": 42,
       "n_jobs": 8
   }
   ```

3. Run `./main`.

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

## Local Testing

```bash
# Update config.json with your epoched data path, then:
python main.py
```

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- Autoreject. brainlife.io App. [doi:10.25663/brainlife.app.954](https://doi.org/10.25663/brainlife.app.954)
- Gramfort A, et al. MEG and EEG data analysis with MNE-Python. Front Neurosci 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)
- Jas, M., Engemann, D., Bekhti, Y., Raimondo, F., & Gramfort, A. (2017). Autoreject: Automated artifact rejection for MEG and EEG data. NeuroImage, 159, 417-429. https://doi.org/10.1016/j.neuroimage.2017.06.030
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- Maximilien Chaumon (https://github.com/dnacombo)

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>
