# MakerWorld upload kit — VEVOR YT60231 replacement wind vane

Do not include personal names, locations, or measurements attributed to a person. Use the files and text below.

## Title

VEVOR YT60231 Replacement Wind Vane

## Category

Household > Outdoor & Garden

(If MakerWorld offers “Replacement parts” or “Sports & Outdoors > Outdoor gadgets”, that is also fine.)

## Tags

weather station, VEVOR, YT60231, wind vane, wind direction, replacement part, anemometer, weathervane, outdoor, PETG, ASA

## License

Creative Commons Attribution (CC BY 4.0), same as the GitHub repo.

## Description

Copy this into the listing (plain text or MakerWorld’s editor):

```
A two-part 3D-printed replacement wind-direction vane for the VEVOR YT60231 7-in-1 weather station, and rebrands that use the same sensor head.

The hub is a cap that slides onto the 2.8 mm D-shaft and locks with a set screw. A bell-shaped skirt drops over the bearing boss and sheds water at a drip lip. The blade bolts to the cap with one M3 screw and nut. This is v5: no ballast nuts, a solid printed barbed arrow, and a slightly shorter tail. Overall length is 167.6 mm.

Print the small fit ring first. It is a 5-minute check that the skirt will drop 2 mm over your housing with a visible gap all around. If it binds, raise skirt_rim_clear in the OpenSCAD source and re-export the cap.

Parametric OpenSCAD source and STEP files are in the GitHub repo: https://github.com/lundy405/vevor-yt60231-wind-vane
```

## Print settings

- Material: PETG or ASA (UV and heat resistant; do not use PLA outdoors)
- 0.4 mm nozzle, 0.2 mm layers (0.12–0.16 mm gives a rounder bore)
- 2–3 walls, 4 top and 4 bottom layers, 30–40% gyroid infill
- No supports
- Cap: print upside down as exported (slot on the bed, skirt opening upward)
- Blade: print as exported, arm on the bed, fin standing up. A 3–5 mm brim is optional. Slow the top of the fin (minimum layer time about 8 s)
- Fit ring: print first, upright

## Hardware

- 1 × M3 × 14 screw (stainless)
- 1 × M3 hex nut
- 1 × M2 × 3 cup-point set screw (stainless; M2 × 4 also fits)

## Assembly (short)

1. Push the blade pad into the cap slot, then fasten with the M3 screw and nut.
2. Clean up the D-bore with a needle file or a 2.8–3.0 mm drill turned by hand if needed.
3. Start the set screw, slide the cap down until the shaft tip bottoms in the bore, line the screw up with the flat, and tighten. The vane must spin freely by hand.
4. Print and try the fit ring before the cap. If the skirt drags on the housing, increase `skirt_rim_clear` and re-export.
5. Mount the station level.

## Files to upload (print files)

Upload these three print-ready STLs. Do not upload the assembly STL as a printable part (it is a reference pose only). STEP and OpenSCAD can be added as “source” or “other files” if the form allows, or left on GitHub.

- `/workspace/publish/vevor-yt60231-wind-vane/stl/wind_vane_cap.stl`
- `/workspace/publish/vevor-yt60231-wind-vane/stl/wind_vane_blade.stl`
- `/workspace/publish/vevor-yt60231-wind-vane/stl/wind_vane_skirt_fit_ring.stl`

Optional extras (not required to print):

- `/workspace/publish/vevor-yt60231-wind-vane/step/wind_vane_cap.step`
- `/workspace/publish/vevor-yt60231-wind-vane/step/wind_vane_blade.step`
- `/workspace/publish/vevor-yt60231-wind-vane/source/wind_vane.scad`

## Cover images (upload in this order)

1. `/workspace/publish/vevor-yt60231-wind-vane/images/photo_installed_station.jpg` — main cover (printed vane on the station)
2. `/workspace/publish/vevor-yt60231-wind-vane/images/photo_installed_closeup.jpg` — close-up of the cap and blade joint
3. `/workspace/publish/vevor-yt60231-wind-vane/images/preview_iso_on_housing.png` — render on the housing
4. `/workspace/publish/vevor-yt60231-wind-vane/images/preview_cap_section_clearances.png` — dimensioned cap section
5. `/workspace/publish/vevor-yt60231-wind-vane/images/photo_shaft_housing.jpg` — shaft and housing the cap fits over

These photos are indoor workbench shots. They do not show a house exterior or other identifying background.

## Notes for the uploader

- Space this listing out from any other MakerWorld upload.
- Do not publish the house-number sign on MakerWorld (that repo is private).
- Profile name, if asked: Helm AI Strategy (as used on the earlier Printables attempt).
