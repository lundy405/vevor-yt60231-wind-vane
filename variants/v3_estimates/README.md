# Replacement wind vane for the VEVOR YT60231 (v3: weather-cap hub)

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
- `v2_flat_hub/` and `v1_big_arrow/` – earlier versions. `ref/` – manuals and photos.

## Sensor-top dimensions used (ESTIMATES from product photos – replace with caliper numbers)
| Parameter | Value | What to measure |
|---|---|---|
| `flat_depth` | 0.5 (across-flat 2.3) | shaft across-flat → `flat_depth = shaft_d − across_flat` |
| `shaft_d` | 2.8 | shaft diameter |
| `boss_d` | 12 | bearing boss OD (dummy only, not critical) |
| `boss_h` | 3.5 | boss / bearing top height above the housing top |
| `shaft_protrusion` | 16 | shaft length above the bearing top (sets the bore depth and cap height) |
| `tab_outer_r` | 10.5 | shaft axis → **outermost** edge of the tab/post (sets the skirt ID) |
| `tab_h` | 5.5 | tab height above the housing top (sets the shoulder height) |
| `housing_top_d` | 35 | flat top diameter. Just check that the lip OD (29.2) is smaller. |
| `screw_below_tip` | 4.5 | keeps the set screw on the flat. Check how far down from the tip the flat runs. |

After you change any of these, re-export, then run `python clearance.py` (after exporting the `cap` and `envelope` parts to `/tmp/v3_*.stl`; see the commands at the end) and `python tune.py`.

## Key dimensions (defaults)
- **Cap:** neck Ø14, skirt Ø26.8 (ID 24), drip lip Ø29.2, walls 1.4 mm. Rim 1.5 mm above the housing top; cap top 29.5 mm above the housing top. 28 mm tall.
- **Bore:** Ø2.95 D-bore (across-flat 2.45), 17 mm deep, closed top with a cone roof, in an Ø8 core. The core bottom sits **0.5 mm above the bearing top**, and the bore ends 1.5 mm above the shaft tip so the shaft never bottoms out. Height is set by the set screw.
- **Set screw:** M2 (Ø1.6 tap hole in the core), 15 mm above the housing top (4.5 mm below the shaft tip), centred on the flat, 90° from the arrow. There's a coaxial **Ø2.6 access hole through the neck**, so the screw and hex key go straight in. The arm sits at the top of the cap, nowhere near the screw path.
- **Clearances** (`clearance.py`, swept 360°):
  - skirt to tab outer edge: 1.5 mm radial
  - shoulder to tab top corner: ≥1.0 mm (1.41 mm vertical)
  - core to bearing: 0.5 mm
  - rim to housing top: 1.5 mm
  - no contact with any stationary part
- **Blade:** same as v2 (72 mm nose, 100 mm tail, 45 mm fin above the arm, 1.4 mm fin, 3 × 5 mm arm), plus a 14 × 8 × 3 mm centre pad with an M3 hole.
- **Overall:** 170.6 mm long; the fin top is 68.5 mm above the housing top.

## Balance and mass
- **Plastic:** cap 4.37 g + blade 7.36 g = 11.73 g PETG (≈9.9 g ASA).
- **Hardware:** 2 × M6 nuts 5.0 g, plus an M3 screw and nut and an M2 set screw (≈1.5 g, all on the axis). **Total about 18 g.**
- **Ballast pod** at **37.3 mm** from the axis. X residual **−0.02 g·mm** (CG 0.001 mm behind the axis). Y residual +0.16 g·mm. The M3 head and nut sit on opposite sides, which adds about 1 g·mm.
- **Alternatives:** 3 × M5 at `ballast_x=48.5`, or 1 × M8 at 36.3. Without ballast (`ballast="none"`) the CG would sit 20 mm behind the axis.
- **Infill doesn't matter for balance:** the cap is symmetric about the shaft, and everything on the blade away from the axis is ≤3 mm thick, so it prints solid.
- **Wind:** fin side area 22.7 cm² vs. nose 5.3 cm², about 7 : 1 turning moment.

## Print settings (both parts)
- **Material:** PETG or ASA, 0.4 mm nozzle, 0.2 mm layers (0.12–0.16 gives a rounder bore).
- **Walls and infill:** 4 perimeters, 5 top / 5 bottom layers, 30–40 % gyroid, **no supports**.
- **Cap:** upside down as exported. A brim isn't needed.
- **Blade:** as exported. A 3–5 mm brim is optional for the long arm. Slow the top of the fin (min layer time ~8 s).

## Assembly
1. **Ballast:** drop 2 × M6 steel nuts into the pod and seal the top with a dab of silicone or epoxy.
2. **Join the parts:** push the blade pad into the cap slot (arrow on the +X side). Put the M3 nut in the hex pocket and insert the M3 × 14 screw from the spot-face side. Snug it down.
3. **Clean up the bore** with a 2.8–3.0 mm drill turned by hand.
4. **Start the set screw:** thread an M2 × 3 (or × 4) cup-point stainless set screw through the neck access hole into the core so it cuts its own thread, then back it out to clear the bore.
5. **Fit it on the shaft:** lay a **slit 0.5 mm card shim** (2–3 layers of business card) on the bearing around the shaft. Slide the cap down until the core rests on the shim, turn it so the access hole faces the shaft flat, tighten the set screw, then pull the shim out under the rim. Spin it by hand to check nothing rubs.
6. **Calibrate direction:** the flat and screw sit 90° from the arrow (`screw_angle`). Calibrate against north or the original. Mount level, per the manual.

## Regenerate
```
openscad -o wind_vane_cap.stl   -D 'part="cap_print"'   wind_vane.scad
openscad -o wind_vane_blade.stl -D 'part="blade_print"' wind_vane.scad
openscad -o /tmp/v3_cap.stl -D 'part="cap"' wind_vane.scad; openscad -o /tmp/v3_envelope.stl -D 'part="envelope"' wind_vane.scad
python clearance.py && python tune.py && python wind_vane_cq.py
```
