# Replacement wind vane for the VEVOR YT60231 (v4)

**What's new in v4** (v3 is saved in `v3_final/`):
- **Teardrop ballast pod.** The round nose pod is now a streamlined teardrop: round nose forward (into the wind), tapering toward the shaft. It still holds 2 × M6 nuts and has a flat bottom, so the blade prints with no supports. The pod sits at **34.35 mm**.
- **Skirt extended down 2.0 mm** over the outside of the housing top. Its bottom inside diameter is **22.7 mm** (F − 0.5, no extra clearance, from the measured housing), and its bottom edge is the drip edge.
- **Self-locating cap.** The bore now ends exactly at the shaft tip (`bore_extra = 0`). Push the cap down until it stops and the 0.5 mm gap above the bearing sets itself. A shim can't be pulled out any more because the skirt now overlaps the housing.
- **New test print:** `wind_vane_skirt_fit_ring.stl`, the bottom 4 mm of the skirt, to try on the housing before printing the whole cap.

Since v3 the hub works like the original's: **a cap**. The arm sits on top of the hub. A bell-shaped skirt drops over the bearing boss and the small tab/post, and a drip lip at the rim sheds water off the edge before it can reach the shaft or bearing. The blade keeps the v2 profile measured from VEVOR's photos (small half-barb arrow, tall swept fin, about 171 mm long) and is still statically balanced by two M6 nuts, now in a teardrop pod (v4).

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
- **Model:** `wind_vane.scad` – parametric. `part=` can be `"assembly"`, `"cap_print"`, `"blade_print"`, `"cap"`, `"blade"`, `"fit_ring"`, `"housing"` (dummy of the sensor top), `"envelope"` or `"section"`.
- **STLs:**
  - `wind_vane_cap.stl` and `wind_vane_blade.stl` – print-ready, in print orientation, each watertight and one body
  - `wind_vane_assembly_installed.stl` – both parts in installed position, for reference only
  - `wind_vane_skirt_fit_ring.stl` – 4 mm tall test ring (skirt bottom ID 22.7, OD 25.5), 0.5 g
- **STEPs:** `wind_vane_cap.step`, `wind_vane_blade.step` and `wind_vane_assembly.step`, all in installed coordinates (z = 0 at the housing top). They're made by `wind_vane_cq.py` and their volumes match the STLs to within 0.2 %.
- **Previews:**
  - `preview_cap_section_clearances.png` – dimensioned cross-section of the cap over the boss and tab
  - `preview_iso.png`, `preview_side.png`, `preview_iso_on_housing.png`, `preview_teardrop_pod.png`
  - v3 previews (exploded, print layout, cap underside, top) are in `v3_final/`. The layout hasn't changed.
- `compare.png` – original vs. v4 at the same scale
- **Scripts:** `tune.py` (balance solver for the assembly), `clearance.py` (minimum clearance between the cap and the swept stationary parts), `check.py` (STL validation), `section_plot.py`
- `v3_final/` (v3 as printed), `v3_estimates/` (v3 built on photo estimates), `v2_flat_hub/` and `v1_big_arrow/` – earlier versions. `ref/` – manuals and photos.

## Sensor-top dimensions (caliper measurements of a VEVOR YT60231, 2026-11-20)
| Ref | Measurement | Parameter |
|---|---|---|
| A | across-flat 2.6 | `flat_depth = 0.2` (2.8 − 2.6). **Shallow flat**; see Notes. |
| B | boss OD 8.92 | `boss_d = 8.92` |
| C | far side of boss → tab outer edge 12.1 | `tab_outer_r = 12.1 − 8.92/2 = 7.64` |
| D | tab height 6.1 | `tab_h = 6.1` |
| E | shaft above bearing 15.35 | `shaft_protrusion = 15.35` |
| F | housing top Ø23.2 ("with room to spare"; the housing tapers, wider going down) | `housing_top_d = 23.2` → `skirt_bottom_id = 22.7` (F − 0.5), `skirt_overlap = 2.0` |
| G | boss height 3.9 | `boss_h = 3.9` |
| – | tab OD **not measured** (4 assumed) | `tab_d = 4`. This sets how far the tab reaches toward the shaft (r ≈ 3.64). |

After any change, re-export and run `python clearance.py` and `python tune.py` (commands at the end).

## Key dimensions (v4, as built)
- **Cap:**
  - Neck Ø14, walls 1.4 mm.
  - **Skirt: bottom ID 22.70, OD 25.50, small 45° drip lip to Ø27.1** at the bottom edge.
  - The skirt is a straight cylinder from its bottom edge, **2.0 mm below the housing top plane**, up to 3.8 mm above it. From there a 45° shoulder runs in to the neck.
  - The cap top is 27.7 mm above the housing top. The cap is 29.7 mm tall.
- **Bore:**
  - Ø2.95 round, **2.65 across the flat**, 14.85 deep. The shaft tip seats on the bore end, which puts the stem bottom **0.5 mm above the bearing**.
  - Closed top with a cone roof.
- **Stepped core:** an r 2.64 stem up to z 7.1 (clears the tab's inner side), then Ø8.
- **Set screw:** M2 **cup point** at z 14.75 (4.5 mm below the shaft tip), centred on the flat. There's a Ø2.6 access hole through the neck. Optional second screw: `second_screw_dz`.
- **Clearances** (`clearance.py`, full 360° sweep of the boss, bearing, tab and tapered housing):

| Gap | Clearance |
|---|---|
| **Skirt bottom ID to housing side at −2 mm** | **0.00, line-to-line by spec.** The housing is assumed to be exactly Ø22.7 at that depth. See the warning below. |
| Skirt wall to housing top edge (z = 0) | 0.18 radial (with the assumed 0.18 mm/mm taper) |
| Skirt to tab outer edge | 3.7 radial |
| Shoulder to tab top corner | ≥1.0 |
| Stem to tab inner side | 1.0 |
| Stem to bearing | 0.5 |

- **Blade:** 72 mm nose, 100 mm tail, 45 mm fin, centre pad and M3 joint (unchanged). **Teardrop pod:** Ø14.3 round nose centred at **34.35 mm**, with a 20 mm taper toward the shaft (tail tip at 12.85 mm). It's 11.4 mm tall at the nose and slopes down to the 5 mm arm. The hex pocket is 10.3 mm across flats × 10.4 mm deep for 2 × M6 nuts, with a 1.2 mm wall and 1 mm floor.
- **Overall:** 170.6 mm long; the fin top is 66.7 mm above the housing top.

### ⚠ Skirt fit
A spinning vane must not touch anything stationary. A 22.7 mm skirt that touches the housing will add drag and make the vane stick in light wind.
- **Molding eccentricity and print tolerance:** printed holes usually come out 0.1–0.2 mm small, and the shaft is rarely perfectly concentric with the housing.
- **Taper:** the product photo suggests the housing grows about 0.18 mm in diameter per mm going down, but nobody has measured that.

**Before printing the cap, print `wind_vane_skirt_fit_ring.stl`** (5 min). Slip it over the housing top. It should drop 2 mm below the top edge with a visible gap all round. If it binds or is snug, raise `skirt_rim_clear` (e.g. 0.25 → ID 23.2) or reduce `skirt_overlap`, then re-export. Each 0.1 mm of `skirt_rim_clear` adds 0.2 mm to the ID.

## Balance and mass
- **Plastic:** cap 4.18 g + blade 8.09 g = **12.28 g PETG** (≈10.3 g ASA).
- **Hardware:** 2 × M6 nuts 5.0 g, plus an M3 × 14 screw and nut and an M2 set screw (≈1.5 g, on the axis). **Total about 18.8 g.**
- **Pod at 34.35 mm. Balance error +0.01 g·mm** (CG 0.001 mm off the axis, front-to-back). Side-to-side is +0.15 g·mm.
- The pod moved in from 37.3 mm because the teardrop's taper adds about 0.7 g of plastic ahead of the shaft.
- **Infill:** the cap is symmetric about the shaft, so its infill doesn't matter. The teardrop's taper is too thick to print solid from walls alone; about 0.24 cm³ of it gets sparse infill.
  - **At 100 % infill** the error stays at +0.01 g·mm.
  - **At 30–40 % infill** it shifts about −4.3 to −5.0 g·mm (CG about 0.3 mm behind the axis).
  - **Recommendation:** print the **blade at 100 % infill**, or use a 100 % modifier on the pod. It adds under 0.2 g.

## Notes on the shallow 0.2 mm flat
- **The flat is only 1.44 mm wide.** An M2 **cup-point** set screw (point Ø ≈1.0 mm) fits on it. Don't use M2.5 (point too wide) or a flat-point screw.
- **Before final tightening,** mark the screw position and make a small **dimple, about 0.3 mm deep, on the flat with a Ø1.5 drill**, 4.5 mm below the shaft tip. The cup point then locks positively. Add a drop of medium threadlocker.
- **Alternatively, file the upper 6 mm of the flat** down to about 2.4 mm across-flat. Leave `flat_depth` at 0.2 so the bore still fits the untouched lower shaft.
- **Second screw option:** `second_screw_dz = -3.5` adds a second screw on the same flat if the flat runs far enough down.
- **The D-bore flat is snug (+0.05 mm).** Printed holes run slightly small. If the shaft won't go in, scrape the bore's flat side with a needle file or a 2.5 mm flat blade. If it's very loose, the set screw still does the locking.

## Print settings
- **Material:** PETG or ASA, 0.4 mm nozzle, 0.2 mm layers (0.12–0.16 gives a rounder bore), 4 perimeters, 5 top / 5 bottom layers, **no supports**.
- **Cap:** upside down as exported, with 30–40 % gyroid. The skirt bottom edge and drip lip print last at the top: vertical wall plus a 45° flare.
- **Blade:** as exported, at **100 % infill** (see Balance). A 3–5 mm brim is optional. Slow the top of the fin (min layer time ~8 s).
- **Fit ring:** print it first, upright.

## Assembly
1. **Ballast:** drop 2 × M6 steel nuts into the pod and seal the top with a dab of silicone or epoxy.
2. **Join the parts:** push the blade pad into the cap slot (arrow on the +X side). Put the M3 nut in the hex pocket and insert the M3 × 14 screw from the spot-face side. Snug it down.
3. **Clean up the bore** with a 2.8–3.0 mm drill turned by hand.
4. **Start the set screw:** thread an M2 × 3 cup-point stainless set screw (×3 seats it on the flat inside the core; ×4 also fits) through the neck access hole into the core so it cuts its own thread, then back it out to clear the bore.
5. **Fit it on the shaft:** slide the cap down until the **shaft tip bottoms out in the bore**. That sets the 0.5 mm gap above the bearing and puts the skirt edge 2 mm below the housing top. Turn the cap so the access hole faces the shaft flat and tighten the set screw. Spin it by hand: it must turn freely and coast. If the skirt drags on the housing, see the skirt-fit warning above.
6. **Calibrate direction:** the flat and screw sit 90° from the arrow (`screw_angle`). Calibrate against north or the original. Mount level, per the manual.

## Regenerate
```
openscad -o wind_vane_cap.stl   -D 'part="cap_print"'   wind_vane.scad
openscad -o wind_vane_blade.stl -D 'part="blade_print"' wind_vane.scad
openscad -o wind_vane_skirt_fit_ring.stl -D 'part="fit_ring"' wind_vane.scad
openscad -o /tmp/v4_cap.stl -D 'part="cap"' wind_vane.scad; openscad -o /tmp/v4_envelope.stl -D 'part="envelope"' wind_vane.scad
python clearance.py && python tune.py && python wind_vane_cq.py
```
