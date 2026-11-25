# Replacement wind vane for the VEVOR YT60231 (v2)

v2 follows the original VEVOR vane's side profile: a small half-barb arrow, a tall swept tail fin with a concave leading edge, and about 171 mm overall. v1 balanced itself with a big 28 × 32 × 12 mm plastic arrow head. v2 drops that and uses **two steel M6 nuts in a small pod** hidden behind the arrow head. The result is static balance (centre of mass on the shaft) with a slim nose, and the balance doesn't change with infill.

## Files
- `wind_vane.scad` – parametric OpenSCAD model
- `wind_vane.stl` – print-ready, default settings (watertight, 1 body)
- `wind_vane.step` – B-rep solid from `wind_vane_cq.py`. Its volume and centre of mass match the STL to within 0.1 %.
- `preview_iso/top/side.png`, `preview_hub_section.png` (D-bore and set-screw hole), `preview_ballast_pod_section.png`
- `compare.png` – original photo vs. new render at the same scale
- `tune.py` – balance solver (moves `ballast_x` until the CG is on the axis). `check.py` – STL validation.
- `ref/` – VEVOR manual PDFs, product photos and crops. Sources are listed in `ref/SOURCES.md`.
- `v1_big_arrow/` – the previous design, kept for reference

## What the original looks like (measured from the VEVOR photos)
Scale comes from the 408 mm sensor width in VEVOR's dimension drawing. Expect about ±10 % error from perspective.
| | Original (approx.) | v2 |
|---|---|---|
| Overall length | ~172–176 mm | 171 mm |
| Axis → arrow tip | ~72 mm | 72 mm |
| Axis → fin top trailing corner / boom end | ~100 / ~76 mm | 100 (98.6 after corner rounding) / 77 mm |
| Fin height above arm bottom | ~44 mm | 45 mm |
| Fin top chord | ~33 mm | 33 mm |
| Arrow | half-barb, ~18 mm long, ~7 mm above the arm | same |
| Arm | thin rib, ~4.6 mm tall | 3 × 5 mm rib |
| Hub | ~21 mm OD with a skirt; arm at the **top** of the hub | Ø11 × 14 mm; arm at the **bottom** of the hub (needed to print without supports) |
| Counterweight | **none visible**: thin rib and a small barb only | 2 × M6 nuts in a Ø14.3 × 11.4 mm pod at 37.3 mm |

**The original is not statically balanced. It's tail-heavy.** With this profile and no ballast (`ballast="none"`), the CG sits about **28 mm behind the shaft** (−218 g·mm in PETG). That's normal for cheap vanes and is harmless if the sensor is perfectly level. v2 is balanced instead. That lets it read correctly even if the mount is a little off level, and it puts less side load on the small bearing. `ballast="none"` reproduces the original's tail-heavy behaviour if you prefer it.

## Key dimensions (v2 defaults)
- **Bore:** Ø2.95 mm (2.8 + 0.15), D-flat 2.45 mm across-flat (assumes 2.3 mm shaft across-flat + 0.15), 11 mm deep. Blind, with a cone roof; 3 mm cap; 0.4 mm lead-in chamfer.
- **Hub:** Ø11 × 14 mm. Optional bottom recess (`hub_recess_d/h`, 45° cone roof) to clear a boss or tab on the housing.
- **Set screw:** M2, Ø1.6 mm teardrop tap hole, square to and centred on the flat, 5.5 mm up, 90° from the arrow. Options: `screw_size="M2.5"` (Ø2.05) and `nut_trap=true`.
- **Arm:** 3 mm wide × 5 mm tall rib. Barb: 18 mm long, 7 mm tall, 3 mm thick.
- **Fin:** 1.4 mm thick, 2 mm rounded corners, leading-edge curve exponent 1.3. Side area: tail 22.7 cm² vs. nose 5.3 cm². Turning moment is about **7 : 1** (v1 was about 5 : 1).
- **Ballast pod:** hex pocket 10.3 mm across flats × 10.4 mm deep for 2 × M6 nuts (DIN 934 / ISO 4032, ~2.5 g each). 1.2 mm wall, 1 mm floor, open top.

## Balance and mass (computed from the mesh plus the nuts)
- Plastic 6.77 cm³ = **8.6 g PETG** (≈7.2 g ASA), plus 5.0 g of steel = **13.6 g**. v1 was 15.4 g.
- Moments: tail plastic −274.8 g·mm, nose plastic +88.2 g·mm, nuts +186.5 g·mm. **Residual −0.02 g·mm (CG 0.001 mm behind the axis).**
- Moment of inertia about the shaft is about 24 400 g·mm², roughly a third of v1's 76 800, so the vane responds faster.
- **Infill doesn't matter for balance.** Everything off the axis is ≤3 mm thick (fin 1.4, rib and barb 3, pod wall 1.2, pod floor 1.0), so it slices as solid perimeters or solid top/bottom layers at any infill. Only the hub uses infill, and it sits on the axis. Use 30–40 % gyroid.
- Other nut options (run `python tune.py ballast_nut='"M5"' ballast_count=3` and so on, then put the reported `ballast_x` in the .scad):

| Ballast | `ballast_x` | Total mass |
|---|---|---|
| 2 × M6 (default) | 37.3 mm | 13.6 g |
| 3 × M5 | 48.5 mm | 12.3 g |
| 1 × M8 | 36.3 mm | 13.8 g |

  Real nut weights vary by about ±10 %. That's ±19 g·mm, or the CG within about 1.4 mm of the axis, which is still far better than the original's 28 mm. To fine-tune, weigh your nuts and edit `NUT_G` in `tune.py`.

## Print settings
- **Material:** PETG or ASA (UV-stable). Avoid PLA outdoors.
- **Orientation:** as modelled, bottom face on the bed. **No supports.** The bore opens downward with a cone roof, the set-screw hole is a teardrop, and the fin, rib, barb and pod are vertical walls.
- **Layers and nozzle:** 0.2 mm layers (0.12–0.16 for a rounder bore), 0.4 mm nozzle.
- **Walls and infill:** 4 perimeters, 5 top / 5 bottom layers, 30–40 % gyroid.
- **Brim:** optional, 3–5 mm, to hold down the long rib. Slow the top of the fin (minimum layer time ~8 s).

## Assembly
1. **Measure the shaft:** check its diameter and across-flat with calipers, set `shaft_d` and `flat_depth = shaft_d − across_flat`, and re-export. 2.3 mm across-flat is an assumption.
2. **Ream the bore** with a 2.8–3.0 mm drill bit turned by hand.
3. **Fit the ballast:** drop 2 × M6 steel nuts into the pod and fix them with a dab of silicone or epoxy, which also seals the top against water.
4. **Set screw:** thread an M2 × 3–4 mm stainless cup-point set screw into the side hole so it cuts its own thread. Slide the vane on, line the screw up with the shaft's flat ("align the screw holes with the flat, vertical side of the metal rod", as the manual says), and snug it down. Don't over-tighten.
5. **Check clearance:** the original's hub sits over the housing boss, and the new arm is lower (at the hub bottom). Make sure the vane spins clear of the housing and the tab/loop. If it rubs, set `hub_recess_d`/`hub_recess_h` to clear the boss, or raise the vane on the shaft if there's enough shaft length.
6. **Calibrate direction:** the flat and screw sit 90° from the arrow (`screw_angle`). Match the original if you can. Otherwise point the arrow north and compare with the console. Mount the sensor so the bubble level is centred and the rain collector faces north, per the manual.
