"""CadQuery re-implementation of wind_vane.scad v2 (default parameters) -> wind_vane.step
Keep the parameters in sync with wind_vane.scad if you change them."""
import math, cadquery as cq
from shapely.geometry import Polygon

shaft_d, flat_depth, bore_clearance = 2.8, 0.5, 0.15
bore_depth, bore_chamfer = 11, 0.4
hub_d, hub_h, hub_top_chamfer = 11, 14, 1.2
screw_size, screw_angle, screw_z = "M2", 90, 5.5
arm_w, arm_h = 3.0, 5.0
nose_len, barb_len, barb_h = 72, 18, 7
tail_len_top, tail_len_bot, fin_top_chord, fin_h, fin_root_x, fin_t, fin_round, fin_curve = 100, 77, 33, 45, 11, 1.4, 2, 1.3
b_af, b_t, ballast_count, ballast_x = 10, 5, 2, 37.3
pod_wall, pod_floor, pocket_clear = 1.2, 1.0, 0.3

tap_d = 2.05 if screw_size == "M2.5" else 1.6
bore_r = (shaft_d + bore_clearance) / 2
flat_y = (shaft_d - flat_depth) - shaft_d / 2 + bore_clearance / 2
b_R = (b_af + pocket_clear) / math.sqrt(3)
pod_r = b_R + pod_wall
pocket_h = ballast_count * b_t + 0.4
pod_h = pod_floor + pocket_h

def plate_xz(pts, t):
    # Workplane("XZ"): local x->X, local y->Z, normal -Y; extrude t then centre on y=0
    return cq.Workplane("XZ").polyline(pts).close().extrude(t).translate((0, t / 2, 0))

hub = (cq.Workplane("XZ").polyline([(0, 0), (hub_d/2, 0), (hub_d/2, hub_h - hub_top_chamfer),
                                     (hub_d/2 - hub_top_chamfer, hub_h), (0, hub_h)]).close()
       .revolve(360, (0, 0, 0), (0, 1, 0)))
arm = (cq.Workplane("XY").box(tail_len_bot + nose_len - barb_len + 1, arm_w, arm_h, centered=False)
       .translate((-tail_len_bot, -arm_w/2, 0)))
x0 = nose_len - barb_len
barb = plate_xz([(x0, 0), (nose_len, 0), (nose_len, 0.8), (x0 + 1.0, arm_h + barb_h), (x0, arm_h + barb_h)], arm_w)
n = 24
lead = [(-(tail_len_top - fin_top_chord) + ((tail_len_top - fin_top_chord) - fin_root_x) * (i/n),
         arm_h + (fin_h - arm_h) * (1 - i/n) ** fin_curve) for i in range(n + 1)]
raw = Polygon([(-tail_len_top, fin_h)] + lead + [(-fin_root_x, arm_h - 1), (-tail_len_bot, arm_h - 1)])
rounded = raw.buffer(-fin_round, join_style=2).buffer(fin_round, join_style=1, quad_segs=8)
fin = plate_xz(list(rounded.exterior.coords)[:-1], fin_t)
fillet = plate_xz([(-tail_len_bot, arm_h - 0.5), (-fin_root_x, arm_h - 0.5),
                   (-fin_root_x - 6, arm_h + 1.5), (-tail_len_bot + 2, arm_h + 1.5)], arm_w)
pod = cq.Workplane("XY").circle(pod_r).extrude(pod_h).translate((ballast_x, 0, 0))
body = hub.union(arm).union(barb).union(fin).union(fillet).union(pod)

halfspace = cq.Workplane("XY").box(12, 6 + flat_y, 40, centered=False).translate((-6, -6, -2))
bore = cq.Workplane("XY").circle(bore_r).extrude(bore_depth + 1).translate((0, 0, -1))
bore = bore.union(cq.Workplane().add(cq.Solid.makeCone(bore_r, 0, bore_r, cq.Vector(0, 0, bore_depth - 0.01))))
bore = bore.intersect(halfspace)
chamf = cq.Workplane().add(cq.Solid.makeCone(bore_r + bore_chamfer, bore_r, bore_chamfer, cq.Vector(0, 0, -0.01)))
r = tap_d / 2
c45 = r * math.cos(math.radians(45))
td = (cq.Workplane("XZ").circle(r).extrude(-hub_d)
      .union(cq.Workplane("XZ").polyline([(c45, c45), (0, r*math.sqrt(2)), (-c45, c45), (0, 0)]).close().extrude(-hub_d))
      .translate((0, flat_y - 0.5, screw_z)))
cut = bore.union(chamf).union(td).rotate((0, 0, 0), (0, 0, 1), screw_angle - 90)
pocket = (cq.Workplane("XY").polygon(6, 2 * b_R).extrude(pocket_h + 1)
          .rotate((0, 0, 0), (0, 0, 1), 30).translate((ballast_x, 0, pod_floor)))
vane = body.cut(cut).cut(pocket)

cq.exporters.export(vane, "wind_vane.step")
s = vane.val()
bb = s.BoundingBox()
print("valid", s.isValid(), "solids", len(vane.solids().vals()), "volume", round(s.Volume(), 1),
      "bbox", [round(v, 2) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmax)], "COM", s.Center())
