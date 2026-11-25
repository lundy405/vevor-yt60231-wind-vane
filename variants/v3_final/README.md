# Replacement wind vane for the VEVOR YT60231 (v3: weather-cap hub, fitted to caliper measurements)

In v3 the hub works like the original's: **a cap**. The arm sits on top of the hub. A bell-shaped skirt drops over the bearing boss and the small tab/post, and a drip lip at the rim sheds water off the edge before it can reach the shaft or bearing. The blade keeps the v2 profile measured from VEVOR's photos (small half-barb arrow, tall swept fin, about 171 mm long) and is still statically balanced by two M6 nuts.

## Why two printed parts
In the installed position the arm sits at the top of the cap and the fin rises above the arm, so no single orientation prints without supports:
- **Upright:** the 170 mm arm floats about 23 mm above the bed.
- **Upside down:** the fin would hang below the bed.
- **On its side:** the round cap and skirt need support, and the off-centre blade would unbalance it sideways.

So it splits into two parts, each printed in its natural support-free orientation:

| Part | File | Print orientation | Notes |
|---|---|---|---|
| **Cap** (hub, skirt, drip lip, bore, set screw) | `wind_vane_cap.stl` | **Upside down**: the cap top with its slot sits on the bed and the skirt opens upward | No supports. The skirt shoulder is 45°, the drip lip has a 45° flare, the bore is vertical, and the horizontal holes are teardrops. The slot floor is a 3.2 mm bridge. |
| **Blade** (arm, barb, fin, ballast pod, centre pad) | `wind_vane_blade.stl` | **Upright**: arm on the bed, fin standing up, same as v2 | No supports. The bolt hole through the pad is a teardrop. |

**Joint:** the blade's 3 mm centre pad drops 6 mm into a keyed slot across the cap top (along the arm), which fixes the angle. One **M3 × 14 screw and M3 nut** clamp it through both cheeks and the pad. The nut sits in a hex pocket on the −Y cheek; the head seats on a flat spot face on the +Y cheek. No glue is needed, though a drop of CA or epoxy in the slot is fine. This keeps the parts small and strong: the fin's layers stand vertical and the cap's skirt prints as clean walls.

## Files
- **Model:** `wind_vane.scad` – parametric. `part=` can be `"assembly"`, `"cap_print"`, `"blade_print"`, `"cap"`, `"blade"`, `"housing"` (dummy of the sensor top) or `"section"`.
- **STLs:**
  - `wind_vane_cap.stl` and `wind_vane_blade.stl` – print-ready, in print orientation, each watertight and one body
  - `wind_vane_assembly_installed.stl` – both parts in installed position, for reference only
- **STEPs:** `wind_vane_cap.step`, `wind_vane_blade.step` and `wind_vane_assembly.step`, all in installed coordinates (z = 0 at the housing top). They're made by `wind_vane_cq.py` and their volumes match the STLs to within 0.2 %.
- **Previews:**
  - `preview_cap_section_clearances.png` – dimensioned cross-section of the cap over the boss and tab
  - `preview_iso.png`, `preview_iso_on_housing.png`, `preview_side.png`, `preview_top.png`
  - `preview_exploded.png`, `preview_print_layout.png`, `preview_cap_underside.png`
- `compare.png` – original vs. v3 at the same scale
- **Scripts:** `tune.py` (balance solver for the assembly), `clearance.py` (minimum clearance between the cap and the swept stationary parts), `check.py` (STL validation), `section_plot.py`
- `v3_estimates/` (v3 built on photo estimates), `v2_flat_hub/` and `v1_big_arrow/` – earlier versions. `ref/` – manuals and photos.

## Sensor-top dimensions (caliper measurements of a VEVOR YT60231, 2026-11-20)
| Ref | Measurement | Parameter |
|---|---|---|
| A | across-flat 2.6 | `flat_depth = 0.2` (2.8 − 2.6). **Shallow flat**; see Notes. |
| B | boss OD 8.92 | `boss_d = 8.92` |
| C | far side of boss → tab outer edge 12.1 | `tab_outer_r = 12.1 − 8.92/2 = 7.64` |
| D | tab height 6.1 | `tab_h = 6.1` |
| E | shaft above bearing 15.35 | `shaft_protrusion = 15.35` |
| F | housing top Ø23.2 | `housing_top_d = 23.2` |
| G | boss height 3.9 | `boss_h = 3.9` |
| – | tab OD **not measured** (4 assumed) | `tab_d = 4`. This sets how far the tab reaches toward the shaft (r ≈ 3.64). |

After any change, re-export and run `python clearance.py` and `python tune.py` (commands at the end).

## Key dimensions (as built)
- **Cap:**
  - Neck Ø14, skirt Ø21.08 (ID 18.28), walls 1.4 mm.
  - **Drip lip Ø25.08**, which overhangs the Ø23.2 housing top by about 0.94 mm per side, so water drips off outside the top face.
  - Rim 1.5 mm above the housing top; cap top 29.2 mm above it. The cap is 27.7 mm tall.
- **Bore:**
  - Ø2.95 round with a D-flat at **2.65 mm across-flat** (2.6 + 0.05). The flat is 1.78 mm wide in the bore and 1.44 mm wide on the shaft.
  - 16.35 deep, closed top with a cone roof. It ends 1.5 mm above the shaft tip.
- **Stepped core:**
  - **New: the tab reaches in toward the shaft.** With a 4 mm OD and its outer edge at r 7.64, its inner side is at about r 3.64, and it stands 6.1 mm tall, above the 3.9 mm boss.
  - So the core is a **stem of r 2.64** (1.17 mm wall) from the bearing up to z 7.1, then widens to Ø8.
  - The stem bottom sits **0.5 mm above the bearing**.
- **Set screw:**
  - M2 **cup point**, at z 14.75 (4.5 mm below the shaft tip, 10.85 mm above the bearing), centred on the flat, 90° from the arrow.
  - The Ø2.6 access hole through the neck lines up with it.
  - Optional 2nd screw on the same flat: `second_screw_dz` (e.g. −3.5 → z 11.25). It needs the flat to run 8 mm down from the tip.
- **Clearances** (`clearance.py`, 360° sweep of the boss, bearing, tab and housing top; no contact anywhere):

| Gap | Clearance |
|---|---|
| Skirt to tab outer edge | 1.5 radial (≥1.0 at the shoulder corner) |
| Shoulder to tab top | ≥1.0 (1.41 vertical) |
| Stem to tab inner side | 1.0 |
| Stem to bearing | 0.5 |
| Rim to housing top | 1.5 |

- **Blade:** unchanged (72 mm nose, 100 mm tail, 45 mm fin, centre pad and M3 joint). Overall 170.6 mm long; the fin top is 68.2 mm above the housing top.

## Balance and mass
- **Plastic:** cap 3.94 g + blade 7.36 g = **11.30 g PETG**.
- **Hardware:** 2 × M6 nuts 5.0 g, plus an M3 × 14 screw and nut and an M2 set screw (≈1.5 g, on the axis). **Total about 17.8 g.**
- **Ballast pod** at **37.3 mm**. X residual **−0.02 g·mm** (CG 0.001 mm behind the axis). Y residual +0.15 g·mm.
- Alternatives: 3 × M5 at 48.5 mm, or 1 × M8 at 36.3 mm.
- Infill doesn't affect balance. Wind turning moment is about 7 : 1.

## Notes on the shallow 0.2 mm flat
- **The flat is only 1.44 mm wide.** An M2 **cup-point** set screw (point Ø ≈1.0 mm) fits on it. Don't use M2.5 (point too wide) or a flat-point screw.
- **Before final tightening,** mark the screw position and make a small **dimple, about 0.3 mm deep, on the flat with a Ø1.5 drill**, 4.5 mm below the shaft tip. The cup point then locks positively. Add a drop of medium threadlocker.
- **Alternatively, file the upper 6 mm of the flat** down to about 2.4 mm across-flat. Leave `flat_depth` at 0.2 so the bore still fits the untouched lower shaft.
- **Second screw option:** `second_screw_dz = -3.5` adds a second screw on the same flat if the flat runs far enough down.
- **The D-bore flat is snug (+0.05 mm).** Printed holes run slightly small. If the shaft won't go in, scrape the bore's flat side with a needle file or a 2.5 mm flat blade. If it's very loose, the set screw still does the locking.

## Print settings (both parts)
- **Material:** PETG or ASA, 0.4 mm nozzle, 0.2 mm layers (0.12–0.16 gives a rounder bore).
- **Walls and infill:** 4 perimeters, 5 top / 5 bottom layers, 30–40 % gyroid, **no supports**.
- **Cap:** upside down as exported. A brim isn't needed.
- **Blade:** as exported. A 3–5 mm brim is optional for the long arm. Slow the top of the fin (min layer time ~8 s).

## Assembly
1. **Ballast:** drop 2 × M6 steel nuts into the pod and seal the top with a dab of silicone or epoxy.
2. **Join the parts:** push the blade pad into the cap slot (arrow on the +X side). Put the M3 nut in the hex pocket and insert the M3 × 14 screw from the spot-face side. Snug it down.
3. **Clean up the bore** with a 2.8–3.0 mm drill turned by hand.
4. **Start the set screw:** thread an M2 × 3 cup-point stainless set screw (×3 seats it on the flat inside the core; ×4 also fits) through the neck access hole into the core so it cuts its own thread, then back it out to clear the bore.
5. **Fit it on the shaft:** lay a **slit 0.5 mm card shim** (2–3 layers of business card) on the bearing around the shaft. Slide the cap down until the core rests on the shim, turn it so the access hole faces the shaft flat, tighten the set screw, then pull the shim out under the rim. Spin it by hand to check nothing rubs.
6. **Calibrate direction:** the flat and screw sit 90° from the arrow (`screw_angle`). Calibrate against north or the original. Mount level, per the manual.

## Regenerate
```
openscad -o wind_vane_cap.stl   -D 'part="cap_print"'   wind_vane.scad
openscad -o wind_vane_blade.stl -D 'part="blade_print"' wind_vane.scad
openscad -o /tmp/v3_cap.stl -D 'part="cap"' wind_vane.scad; openscad -o /tmp/v3_envelope.stl -D 'part="envelope"' wind_vane.scad
python clearance.py && python tune.py && python wind_vane_cq.py
```
