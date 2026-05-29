# HI Spectral Fitting Library
**Related file(s)**: [Analysis/SpectralAnalysis/spectral_fitting_lib.py](../SpectralAnalysis/spectral_fitting_lib.py)
**Date**: 2026-04-15 14:32:00

---

## Overview

`spectral_fitting_lib.py` provides the downstream spectral analysis utilities for the Local Group HI Survey pipeline. It wraps Gaussian profile fitting (via `scipy.optimize.curve_fit`) and computes moment maps from masked HI 21 cm spectral cubes.

This file handles **fitting and moment computation**. GaussPy+ parameter training and automated decomposition are handled separately in `Analysis/GaussDecomp/gaussdecomp_lib.py`.

---

## Inputs

- **Spectral cubes**: 3D NumPy arrays, shape `(n_channels, n_y, n_x)`, in brightness temperature [K]. Loaded from FITS via `astropy.io.fits` before calling library functions.
- **Velocity axis**: 1D array [km/s], one value per channel. Computed from FITS header (CRVAL3, CDELT3, CRPIX3) using `spectral-cube` or manually.
- **SNR mask**: 3D boolean array, True where a voxel has sufficient signal. Produced by `Analysis/CubePrep/masking_lib.py`.

---

## Outputs

- **Moment maps**: 2D arrays (moment 0 in K km/s, moment 1 and 2 in km/s). Saved as FITS in `Visualizations/moment_maps/`.
- **Fit parameters**: 1D arrays of best-fit [amplitude, centre, sigma] × n_components per spectrum. Saved as compressed NumPy archives (`.npz`) in `Analysis/SpectralAnalysis/`.
- **Quality mask**: 2D boolean array, saved alongside fit results.

---

## Dependencies

- `numpy`, `scipy.optimize.curve_fit`, `scipy.signal.find_peaks`
- `Analysis/CubePrep/masking_lib.py` — produces the SNR mask input
- `constants.py` — SNR and chi-squared quality thresholds (`SNR_MIN`, `CHI2_RED_MAX`)

---

## Key Assumptions

1. **Gaussian profiles**: HI spectra are modelled as sums of Gaussian components. This is well-justified for the warm neutral medium (WNM) but may underfit the cold neutral medium (CNM) where profiles can be non-Gaussian (see Haud & Kalberla 2007).

2. **Velocity axis uniformity**: The library assumes constant channel spacing (`np.median(np.diff(v))`). For cubes with non-uniform channels (rare, but possible after Hanning smoothing), pass `channel_width_kms` explicitly to `compute_moment_maps()`.

3. **Single-slab LTE**: No radiative transfer is assumed in this library; it operates purely on line profiles. Physical interpretation (column density, optical depth) is done downstream using `Analysis/ViralAnalysis/`.

4. **Noise stationarity**: `estimate_noise_rms()` assumes the noise RMS is constant across line-free channels. This is appropriate for VLA data after flagging; it may underestimate noise near the band edges.

---

## Physical Motivation

The key function `compute_moment_maps()` computes:

- **Moment 0** (W_HI): integrated intensity [K km/s] → proportional to N_HI (column density) in the optically thin regime.
- **Moment 1** (v_mean): intensity-weighted mean velocity [km/s] → traces the bulk gas kinematics.
- **Moment 2** (sigma_v): intensity-weighted velocity dispersion [km/s] → combines thermal and turbulent broadening. Note: for multi-component profiles, moment 2 captures the full blend, not individual component dispersions. Use GaussPy+ component sigmas for individual component analysis.

The SNR mask is applied *before* moment summation to avoid noise bias in the tails of the profile.

---

## Caveats and Limitations

- Auto-detection of initial Gaussian parameters (`_auto_initial_params`) uses `scipy.signal.find_peaks` with a 1% peak height threshold. For very broad, low-amplitude features (common in WNM), manual initial parameters may be needed.
- The chi-squared returned by `fit_single_spectrum()` is set to NaN; it must be computed externally after calling `estimate_noise_rms()`.
- For large cubes (>10 GB), do not load the full cube into memory. Use `spectral-cube`'s lazy-loading or process by channel slab.

---

## Pipeline Role

This library is called by:
1. `Analysis/SpectralAnalysis/run_moment_maps.py` — produces science moment maps for all targets
2. `Analysis/SpectralAnalysis/run_gaussfit_validation.py` — validates Gaussian fits against GaussPy+ decomposition

Unit tests: `Analysis/tests/test_moment_maps.py`
