# Data Inventory — Local Group HI Survey
**Related file(s)**: [Data/](../)
**Date**: 2026-04-02 11:00:00
**Last Updated**: 2026-05-10 09:30:00

*This document is generated and maintained by Claude after reviewing the Data/
directory (Step 4 of the ClaudeAstroVolpert setup). Update it whenever new data
is added. Ask Claude: "Please update Data/descriptions/data_inventory.md."*

---

## Summary

| Target | Dataset | Format | Location | Status |
|--------|---------|--------|----------|--------|
| LMC | VLA D-array HI cube | FITS | `Raw/LMC/` | ✓ In hand |
| LMC | Parkes HIPASS | FITS | `Raw/LMC/` | ✓ In hand |
| LMC | Mosaiced (VLA+Parkes feather) | FITS | `Mosaics/` | ✓ Complete |
| SMC | VLA D-array HI cube | FITS | `Raw/SMC/` | ✓ In hand |
| SMC | Parkes HIPASS | FITS | `Raw/SMC/` | ✓ In hand |
| WLM | LITTLE THINGS VLA cube | FITS | `Raw/WLM/` | ✓ Downloaded |
| NGC 6822 | LITTLE THINGS VLA cube | FITS | `Raw/NGC6822/` | ✓ Downloaded |
| IC 10 | LITTLE THINGS VLA cube | FITS | `Raw/IC10/` | Pending re-download |
| All | FIR dust maps (Herschel) | FITS | `Ancillary/dust/` | ✓ In hand |
| All | UV (GALEX) star formation | FITS | `Ancillary/UV/` | ✓ In hand |
| LMC/SMC | Hα (MCELS) | FITS | `Ancillary/Halpha/` | ✓ In hand |

---

## Raw Data (`Data/Raw/`)

### LMC — VLA D-array HI
**File**: `Raw/LMC/LMC_HI_VLA_Darray_v2.0_native.fits`
**Instrument**: VLA in D configuration, 1.4 GHz
**Pipeline version**: AIPS reduction, pipeline v2.0 (Kim et al. 1998 dataset; re-delivered 2025-01 from NRAO archive)
**Beam**: 63" × 56" (native, pre-convolution)
**Channel width**: 1.649 km/s (native)
**Velocity range**: 190–380 km/s LSR
**Noise (per channel)**: ~14 mJy/beam = ~0.18 K (Tb)
**Notes**: Negative bowls present at the 2–3 K level due to missing short spacings — feathering with Parkes is required before moment analysis. Do not use this cube alone for emission totals.

### LMC — Parkes HIPASS
**File**: `Raw/LMC/LMC_HI_Parkes_HIPASS_v1.0.fits`
**Instrument**: Parkes 64m, HIPASS survey
**Beam**: 14.4' FWHM
**Channel width**: 18.5 km/s
**Notes**: Used only for single-dish total power to fill in the short-spacing information missing from the VLA cube. NOT used alone for structure analysis.

### SMC — VLA D-array HI
**File**: `Raw/SMC/SMC_HI_VLA_Darray_v1.0_native.fits`
**Instrument**: VLA D-array, 1.4 GHz
**Source**: Stanimirović et al. (1999) dataset; downloaded from NRAO archive 2026-02
**Beam**: 98" × 98" (native)
**Channel width**: 1.649 km/s
**Noise**: ~22 mJy/beam = ~0.15 K (Tb)

### WLM, NGC 6822, IC 10 — LITTLE THINGS
**Files**: `Raw/{WLM,NGC6822,IC10}/{TARGET}_HI_LTTHINGS_robust0.fits`
**Source**: LITTLE THINGS survey, Hunter et al. (2012, AJ 144, 134)
**Downloaded from**: https://science.nrao.edu/science/surveys/littlethings
**Pipeline**: AIPS, LITTLE THINGS pipeline v1.2
**Beam**: varies per target; see FITS header BMAJ/BMIN
**Notes**: IC 10 cube was corrupted in the initial download (zeroed channels 45–67); pending re-download from archive. Do NOT use the current IC10 file for science.

---

## Mosaiced Data (`Data/Mosaics/`)

### LMC — Feathered cube (VLA + Parkes)
**File**: `Mosaics/LMC_HI_VLA_Parkes_feather_v1.0.fits`
**Method**: `CASA feather` task; see `Analysis/CubePrep/feather_lmc.py`
**Beam**: Convolved to 63" × 63" (circular; matched to VLA major axis)
**Pixel scale**: 15" (regridded from native 5"/pixel VLA grid)
**Channel width**: 1.649 km/s (preserved from VLA)
**Noise**: ~0.20 K per channel after feathering
**Status**: Used for all LMC science analysis

---

## Ancillary Data (`Data/Ancillary/`)

### FIR Dust Maps — Herschel
**File**: `Ancillary/dust/{TARGET}_Herschel_250um_v1.0.fits`
**Instrument**: Herschel PACS/SPIRE 250 μm
**Resolution**: 18" FWHM
**Source**: Herschel archive, ESA; processed by Gordon et al. (2014 pipeline)
**Notes**: Used for dust-based column density comparison and star-formation efficiency estimates. Not convolved to HI beam yet — see `Analysis/CubePrep/descriptions/beam_matching_info.md` for the convolution recipe.

### UV Star Formation — GALEX
**File**: `Ancillary/UV/{TARGET}_GALEX_FUV_v1.0.fits`
**Instrument**: GALEX FUV (153 nm)
**Resolution**: 4.5" FWHM
**Source**: MAST archive, downloaded 2026-01
**Notes**: FUV traces recent star formation (< 100 Myr); will be used for HI-SFR correlation analysis.

### Hα — MCELS (LMC/SMC only)
**File**: `Ancillary/Halpha/LMC_Halpha_MCELS_v1.fits`, `SMC_Halpha_MCELS_v1.fits`
**Instrument**: CTIO 0.9m; Magellanic Cloud Emission Line Survey
**Resolution**: ~2" FWHM
**Notes**: Hα traces ionised gas and HII regions; useful for identifying feedback-driven HI holes.

---

## Data to Acquire

| Dataset | Priority | Status | Notes |
|---------|----------|--------|-------|
| IC 10 VLA cube (re-download) | HIGH | Not started | Current file corrupted; re-request from NRAO |
| SMC Parkes for feathering | HIGH | Not started | Need HIPASS SMC tile |
| WLM THINGS 21cm (higher res) | MED | Not started | Optional: check if THINGS observed WLM |
| NGC 6822 CO (IRAM) | LOW | Not started | For HI-to-H2 transition study; deferred to paper 2 |

---

## Notes

- All FITS files use J2000 equatorial coordinates.
- Brightness temperatures are in K (main beam temperature scale, T_MB) unless the header says otherwise.
- CDELT3 is in m/s in some raw files and km/s in others — always check before assuming. The `Analysis/CubePrep/` scripts normalise to km/s.
- The `Data/` directory is in `.gitignore` and is never committed to the git repository.
