"""v5 balance + pointing-authority report (no ballast; nothing to tune).

CG of the installed vane for normal FDM settings, using mass_model.fdm_mass on the
print-oriented STLs (blade_print / cap_print keep installed X, so x is measured from the shaft).
Side-area moments (projected XZ area x lever arm) for the nose (x>0) and tail (x<0).
usage: python balance.py   (exports the STLs it needs with openscad first)
"""
import subprocess
from mass_model import fdm_mass, side_area
HW = 1.35   # M3x14 screw ~1.0 g + M3 nut ~0.25 g + M2 set screw ~0.1 g, all on the axis
for part, out in (("blade_print", "/tmp/v5_blade_print.stl"), ("cap_print", "/tmp/v5_cap_print.stl")):
    subprocess.run(["openscad", "-o", out, "-D", f'part="{part}"', "wind_vane.scad"], check=True, capture_output=True)
print("settings              blade g   cap g  moment g*mm  CG plastic  CG with hardware")
for inf, w in ((0.30, 2), (0.35, 2), (0.40, 3), (1.0, 2)):
    b = fdm_mass("/tmp/v5_blade_print.stl", inf, w); c = fdm_mass("/tmp/v5_cap_print.stl", inf, w)
    mp = b["mass"] + c["mass"]
    print(f"{inf:4.0%} infill, {w} walls   {b['mass']:6.2f}  {c['mass']:6.2f}  {b['moment']:+9.1f}   {b['moment']/mp:+7.1f} mm   {b['moment']/(mp+HW):+7.1f} mm")
s = side_area("/tmp/v5_blade_print.stl")
(an, mn), (at, mt) = s["nose"], s["tail"]
print(f"side area: nose {an/100:.1f} cm2, moment {mn/1000:+.1f} cm3 | tail {at/100:.1f} cm2, moment {mt/1000:+.1f} cm3 | "
      f"tail:nose = {-mt/mn:.1f} : 1  (tail centroid {mt/at:.1f} mm, nose centroid {mn/an:.1f} mm)")
