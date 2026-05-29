# Project Background: Local Group HI Survey
**Generated**: 2026-04-05 13:00:00
**Last Updated**: 2026-05-10 09:45:00
**Source files**: literature/Warren+2004_LMC_HI.pdf, literature/Stanimirovic+1999_SMC.pdf,
    literature/Hunter+2012_LITTLE_THINGS.pdf, literature/Bolatto+2013_alpha_CO.pdf, my_notes.txt

*This file is automatically consulted by Claude at the start of each session.
Edit freely — Claude will not overwrite your changes. To regenerate from literature,
tell Claude: "Please re-read Background/ and update this summary."*

---

## Scientific Context

This project characterises the neutral hydrogen (HI) structure of five Local Group
dwarf irregular galaxies across a metallicity range 0.05–0.5 Z_sun: LMC, SMC, WLM,
NGC 6822, and IC 10. The overarching question is how HI morphology, kinematics, and
phase structure vary with metallicity and star formation activity, and what this implies
for the relationship between atomic gas and star formation efficiency in low-metallicity
environments.

The HI is observed in the 21 cm hyperfine transition. At the resolution of the VLA
D-array (~45"), we probe physical scales of 11 pc (LMC) to 200 pc (WLM), ranging
from individual cloud complexes to large-scale ISM structure.

---

## Key Results from the Literature

### HI in the LMC
- Total HI mass: ~4.8 × 10⁸ M_sun (Kim et al. 1998; 15" VLA + Parkes)
- Velocity range: ~220–310 km/s (LSR); kinematic disk inclined ~35° to line of sight
- Giant HI holes and shells are prominent: 100–1500 pc diameter, likely from OB
  association stellar feedback (Kim et al. 1999)
- Fraction of CNM (cold neutral medium): ~10–20% by mass; most HI is warm (WNM)
- HI column density: peaks of ~10²¹·⁵ cm⁻² in GMC-associated regions

### HI in the SMC
- Total HI mass: ~4.0 × 10⁸ M_sun (Stanimirović et al. 1999; ATCA + Parkes)
- The SMC Wing is a distinct kinematic feature; tidal interaction with the LMC
  drives the overall irregular morphology
- Velocity range ~90–220 km/s (LSR), with clear velocity gradient from NE to SW
- Higher CNM fraction than the LMC in some studies; disputed

### Local Group dwarfs (LITTLE THINGS survey, Hunter et al. 2012)
- 40 dwarf irregulars at D < 11 Mpc with VLA HI at ~6" resolution
- Typical HI morphologies: irregular, extended beyond stellar disk, often lopsided
- WLM: isolated, relatively undisturbed; good for baseline measurements
- IC 10: the most actively star-forming Local Group dwarf; starburst-like HI kinematics
- NGC 6822: isolated, low-metallicity; Hα–HI kinematic comparison well-studied

### Star formation thresholds
- The Kennicutt–Schmidt relation holds approximately in dwarfs but with larger scatter
  and lower normalisation than spirals (Bigiel et al. 2008; Leroy et al. 2008)
- HI-dominated ISM: star formation proceeds at lower efficiency per gas mass unit than
  in CO-dominated (H₂-rich) environments
- The HI-to-H₂ transition (Krumholz et al. 2009) shifts to higher column densities at
  lower metallicity — explaining why these dwarfs retain more HI per stellar mass

---

## Key Physical Reference Values

*These are the sanity-check anchors for Physics Cop and order-of-magnitude checks.*

| Parameter | Expected range | Notes |
|-----------|---------------|-------|
| N_HI | 10¹⁹–10²¹·⁵ cm⁻² | peaks in GMC regions; envelopes at 10¹⁹ |
| T_spin (WNM) | 3,000–10,000 K | bulk of HI mass in these galaxies |
| T_spin (CNM) | 30–300 K | minority phase; filamentary |
| HI linewidth (FWHM) | 5–30 km/s (cloud complexes) | includes turbulent + thermal |
| HI cloud mass | 10³–10⁷ M_sun | individual complexes |
| HI disk scale height | ~150–500 pc (LMC/SMC) | flared in outer disks |
| Metallicity | 0.05–0.5 Z_sun | across the 5 targets |
| Star formation efficiency | 0.5–5% per 100 Myr | lower than spirals |
| Distance modulus | LMC: 18.50 ± 0.02 (Pietrzyński+2019) | 50 kpc |

---

## Open Questions This Project Addresses

1. **Does the CNM fraction correlate with metallicity across Local Group dwarfs?**
   Predicted by theory (Wolfire et al. 2003), not systematically tested across this
   metallicity range with matched-resolution data.

2. **Do HI hole/shell populations scale with star formation history?**
   IC 10 (starburst) vs WLM (quiescent) provide the contrasting extremes.

3. **What is the turbulent velocity dispersion of HI at ~10–200 pc scales as a
   function of environment?** Relevant to turbulence driving mechanisms (stellar
   feedback vs. gravitational instability vs. accretion).

4. **Is there a consistent HI-to-star-formation threshold across metallicities?**
   Comparison with UV + Hα star formation maps.

---

## Key References

- **Kim et al. (1998, ApJ 503, 674)** — definitive LMC HI study at ~15" (VLA+Parkes)
- **Stanimirović et al. (1999, MNRAS 302, 417)** — SMC HI structure and kinematics
- **Hunter et al. (2012, AJ 144, 134)** — LITTLE THINGS survey; WLM, NGC 6822, IC 10
- **Bolatto et al. (2013, ARA&A 51, 207)** — alpha_CO review; CO-to-H2 conversion
- **Bigiel et al. (2008, AJ 136, 2846)** — HI-SFR relation in dwarf galaxies
- **Krumholz et al. (2009, ApJ 693, 216)** — HI-to-H2 transition theory
- **Wolfire et al. (2003, ApJ 587, 278)** — thermal equilibrium and CNM/WNM phases

---

## Notes from Anna (my_notes.txt)

- Priority target for first paper: LMC + SMC (data already in hand and reduced)
- WLM, NGC6822, IC10 need re-reduction from LITTLE THINGS archive — not started yet
- The Parkes single-dish data for LMC feathering is from the HIPASS survey at 14.4'
  resolution; we will combine with VLA D-array using the "feather" method in CASA
- Main competing analysis: Koch et al. (2018, MNRAS) did similar work on the LMC
  at ~75 pc resolution — we need to be clearly better or complementary at 11 pc
