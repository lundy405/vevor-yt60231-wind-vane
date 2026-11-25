"""FDM mass / balance model for normal (non-solid) prints, plus side-area moments.

Slices a print-oriented STL in layers. Within each layer:
  * a perimeter band `walls * line_w` wide inside the outline is solid,
  * areas within `top_bottom` layers of a top or bottom skin are solid,
  * everything else is sparse infill at `infill` density.
Moments are taken about x = 0, i.e. the shaft axis (blade_print and cap_print keep installed X/Y).

usage: python mass_model.py part.stl [infill walls]   or import and call fdm_mass().
"""
import sys, numpy as np, trimesh
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

RHO = 1.27e-3          # PETG g/mm^3 (ASA ~1.07e-3)
LINE_W, LAYER_H, TOPBOT = 0.45, 0.2, 4

def _slices(mesh, h):
    zs = np.arange(h / 2, mesh.bounds[1][2], h)
    out = []
    for z in zs:
        s = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if s is None: out.append(Polygon()); continue
        p2, T = s.to_2D(to_2D=np.eye(4))          # keep world XY
        out.append(unary_union(p2.polygons_full).buffer(0))
    return zs, out

_cache = {}
def fdm_mass(path, infill=0.35, walls=2, topbot=TOPBOT, rho=RHO, h=LAYER_H):
    if path not in _cache:
        _cache[path] = _slices(trimesh.load(path), h)
    zs, sl = _cache[path]
    w = walls * LINE_W
    inner = [p.buffer(-w) for p in sl]
    m = mx = msolid = 0.0
    n = len(sl)
    for i, p in enumerate(sl):
        if p.is_empty: continue
        sparse = inner[i]
        for k in range(1, topbot + 1):
            for j in (i - k, i + k):
                sparse = sparse.intersection(inner[j]) if 0 <= j < n else Polygon()
        solid = p.difference(sparse)
        for g, d in ((solid, 1.0), (sparse, infill)):
            if g.is_empty: continue
            m += g.area * h * rho * d
            mx += g.area * g.centroid.x * h * rho * d
        msolid += p.area * h * rho
    return dict(mass=m, moment=mx, solid_mass=msolid)

def side_area(path, xcut=0.0):
    """Side (XZ) projected area of the part and its first moment about x = 0, split nose/tail."""
    mesh = trimesh.load(path)
    tri = mesh.vertices[mesh.faces][:, :, [0, 2]]
    polys = [Polygon(t) for t in tri if abs((t[1][0]-t[0][0])*(t[2][1]-t[0][1]) - (t[1][1]-t[0][1])*(t[2][0]-t[0][0])) > 1e-9]
    sil = unary_union(polys)
    box_n = Polygon([(xcut, -1e3), (1e3, -1e3), (1e3, 1e3), (xcut, 1e3)])
    nose, tail = sil.intersection(box_n), sil.difference(box_n)
    f = lambda g: (g.area, g.area * g.centroid.x if not g.is_empty else 0.0)
    return dict(total=sil.area, nose=f(nose), tail=f(tail))

if __name__ == "__main__":
    p = sys.argv[1]; inf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.35
    wl = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    r = fdm_mass(p, inf, wl)
    print(f"{p}: {r['mass']:.2f} g at {inf:.0%} infill/{wl} walls (solid {r['solid_mass']:.2f} g), moment {r['moment']:+.1f} g*mm")
