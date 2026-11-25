"""Balance solver for wind_vane.scad (v3: cap + blade assembled, part="assembly").
Moves the ballast pod (ballast_x) until the centre of mass of plastic + steel
nuts sits on the shaft axis.  Plastic is treated as solid PETG. That's valid
because everything off the axis is <= 3 mm thick and slices as solid perimeters.
usage: python tune.py [-D name=value ...]      (same overrides you'd give openscad)
"""
import subprocess, sys, trimesh, re
RHO = 1.27e-3                                     # PETG g/mm^3 (ASA ~1.07e-3)
NUT_G = {"M4": 0.81, "M5": 1.25, "M6": 2.5, "M8": 5.2}   # DIN 934 steel hex nut, typical
extra = sys.argv[1:]
src = open("wind_vane.scad").read()
def param(name):
    for e in extra:
        if e.startswith(name + "="): return e.split("=", 1)[1].strip('"')
    return re.search(rf'^{name}\s*=\s*"?([^";]+)"?;', src, re.M).group(1)
nut, count, mode = param("ballast_nut"), int(param("ballast_count")), param("ballast")

def evaluate(x):
    args = ["openscad", "-o", "/tmp/tune.stl", "-D", 'part="assembly"', "-D", f"ballast_x={x}"]
    for e in extra: args += ["-D", e]
    subprocess.run(args + ["wind_vane.scad"], check=True, capture_output=True)
    m = trimesh.load("/tmp/tune.stl")
    mp = m.volume * RHO
    ms = NUT_G[nut] * count if mode == "nuts" else 0.0
    moment = mp * m.center_mass[0] + ms * x
    return moment, mp, ms, m

if mode != "nuts":
    mom, mp, ms, m = evaluate(0)
    print(f"no ballast: plastic {mp:.2f} g, moment {mom:.1f} g*mm, CG x = {mom/mp:.2f} mm")
    sys.exit()
lo, hi = 15.0, 70.0
for _ in range(22):
    mid = (lo + hi) / 2
    if evaluate(mid)[0] < 0: lo = mid
    else: hi = mid
x = round((lo + hi) / 2, 2)
mom, mp, ms, m = evaluate(x)
print(f"Y: plastic CG y = {m.center_mass[1]:+.3f} mm ({mp*m.center_mass[1]:+.2f} g*mm)")
print(f"{count}x {nut}: ballast_x = {x} mm  plastic {mp:.2f} g + steel {ms:.2f} g = {mp+ms:.2f} g  "
      f"residual {mom:+.2f} g*mm  (CG {mom/(mp+ms):+.3f} mm)")
