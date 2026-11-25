"""CadQuery re-implementation of wind_vane.scad v5 (default parameters).
Writes wind_vane_cap.step, wind_vane_blade.step (installed coordinates) and
wind_vane_assembly.step.  Keep parameters in sync with wind_vane.scad."""
import math, cadquery as cq
from shapely.geometry import Polygon, Point

# --- housing estimates / shaft
boss_d, boss_h, shaft_protrusion, tab_outer_r, tab_h, tab_d = 8.92, 3.9, 15.35, 7.64, 6.1, 4
shaft_d, flat_depth, bore_clearance, flat_clear, hub_gap, bore_extra, bore_chamfer = 2.8, 0.2, 0.15, 0.05, 0.5, 0.0, 0.4
# --- cap
housing_top_d, skirt_overlap, skirt_rim_clear = 23.2, 2.0, 0.0
skirt_bottom_id = housing_top_d - 0.5
skirt_clear_r, tab_clear_z, wall, lip_w, lip_t = 1.5, 1.0, 1.4, 0.8, 1.0
stem_clear, stem_min_wall = 1.0, 1.1
neck_d, core_d, roof_t = 14, 8, 1.0
screw_size, screw_angle, screw_below_tip, access_d = "M2", 90, 4.5, 2.6
slot_d, slot_clear, pad_h, pad_l, joint_bolt_d, joint_nut_af = 6, 0.2, 8, 14, 3.3, 5.5
# --- blade
arm_w, arm_h, nose_len, barb_len, barb_h, barb_sweep, arrow_t = 3.0, 5.0, 72, 22, 8, 4, 5.0
tail_len_top, tail_len_bot, fin_top_chord, fin_h, fin_root_x, fin_curve, fin_t, fin_round = 97, 74, 33, 45, 11, 1.3, 1.4, 2

tap_d = 2.05 if screw_size == "M2.5" else 1.6
bore_r = (shaft_d + bore_clearance) / 2
flat_y = (shaft_d - flat_depth) + flat_clear - bore_r
z_hb = boss_h + hub_gap
z_tip = boss_h + shaft_protrusion
bore_depth = shaft_protrusion - hub_gap + bore_extra
z_bt = z_hb + bore_depth
z_slot = z_bt + bore_r + roof_t
z_top = z_slot + slot_d
screw_z = z_tip - screw_below_tip
rim_z = -skirt_overlap
skirt_ri = skirt_bottom_id / 2 + skirt_rim_clear; skirt_ro = skirt_ri + wall
assert skirt_ri >= tab_outer_r + skirt_clear_r
neck_ro = neck_d / 2; neck_ri = neck_ro - wall; core_r = core_d / 2
tab_in_r = min(boss_d / 2, tab_outer_r - tab_d)
stem_r = max(min(core_r, tab_in_r - stem_clear), bore_r + stem_min_wall)
z_step = max(tab_h + stem_clear, z_hb)
z_c = max(tab_h + tab_clear_z * math.sqrt(2) - (skirt_ri - tab_outer_r), 1.0)
z_in = lambda r: z_c + (skirt_ri - r)
z_out = lambda r: z_c + (skirt_ri - r) + wall * math.sqrt(2)
z_ann = z_slot - 1.5

def teardrop_y(d, length, y0, z, tip_up):
    """hole along +Y from y0, teardrop tip toward +Z or -Z"""
    r = d / 2; c = r * math.cos(math.radians(45)); s = 1 if tip_up else -1
    circ = cq.Workplane("XZ").circle(r).extrude(-length)
    tip = cq.Workplane("XZ").polyline([(c, s * c), (0, s * r * math.sqrt(2)), (-c, s * c), (0, 0)]).close().extrude(-length)
    return circ.union(tip).translate((0, y0, z))

# =============================== CAP =================================
prof = [(0, z_top), (neck_ro - 0.8, z_top), (neck_ro, z_top - 0.8), (neck_ro, z_out(neck_ro)),
        (skirt_ro, z_out(skirt_ro)), (skirt_ro, rim_z + lip_t + lip_w), (skirt_ro + lip_w, rim_z + lip_t),
        (skirt_ro + lip_w, rim_z), (skirt_ri, rim_z), (skirt_ri, z_c), (neck_ri, z_in(neck_ri)),
        (neck_ri, z_ann), (core_r, z_ann), (core_r, z_step), (stem_r, z_step), (stem_r, z_hb), (0, z_hb)]
cap = cq.Workplane("XZ").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))

half = cq.Workplane("XY").box(12, 6 + flat_y, bore_depth + 10, centered=False).translate((-6, -6, z_hb - 2))
bore = cq.Workplane("XY").circle(bore_r).extrude(bore_depth + 1).translate((0, 0, z_hb - 1))
bore = bore.union(cq.Workplane().add(cq.Solid.makeCone(bore_r, 0, bore_r, cq.Vector(0, 0, z_bt - 0.01)))).intersect(half)
bore = bore.union(cq.Workplane().add(cq.Solid.makeCone(bore_r + bore_chamfer, bore_r, bore_chamfer, cq.Vector(0, 0, z_hb - 0.01))))
screw = teardrop_y(tap_d, core_r + 1 - flat_y, flat_y - 0.5, screw_z, False) \
    .union(teardrop_y(access_d, neck_ro + 2, core_r - 0.2, screw_z, False))
cap = cap.cut(bore.union(screw).rotate((0, 0, 0), (0, 0, 1), screw_angle - 90))
zb = z_slot + slot_d / 2
slot = cq.Workplane("XY").box(neck_d + 2, arm_w + slot_clear, slot_d + 1, centered=False) \
    .translate((-neck_ro - 1, -(arm_w + slot_clear) / 2, z_slot))
bolt = teardrop_y(joint_bolt_d, neck_d + 2, -neck_ro - 1, zb, False)
nut = (cq.Workplane("XZ").polygon(6, 2 * (joint_nut_af + 0.3) / math.sqrt(3)).extrude(5)
       .rotate((0, 0, 0), (0, 1, 0), 30).translate((0, -neck_ro + 2.6, zb)))
spot = cq.Workplane("XZ").circle(3.25).extrude(-5).translate((0, neck_ro - 0.8, zb))
cap = cap.cut(slot).cut(bolt).cut(nut).cut(spot)

# ============================== BLADE ================================
def plate_xz(pts, t):
    return cq.Workplane("XZ").polyline(pts).close().extrude(t).translate((0, t / 2, 0))
arm = cq.Workplane("XY").box(tail_len_bot + nose_len - barb_len + barb_sweep + 1, arm_w, arm_h, centered=False).translate((-tail_len_bot, -arm_w / 2, 0))
x0 = nose_len - barb_len
barb = plate_xz([(x0 + barb_sweep, 0), (nose_len, 0), (nose_len, 1.0), (x0 + 1.5, arm_h + barb_h), (x0, arm_h + barb_h), (x0 + barb_sweep, arm_h)], arrow_t)
n = 24
lead = [(-(tail_len_top - fin_top_chord) + ((tail_len_top - fin_top_chord) - fin_root_x) * (i / n),
         arm_h + (fin_h - arm_h) * (1 - i / n) ** fin_curve) for i in range(n + 1)]
raw = Polygon([(-tail_len_top, fin_h)] + lead + [(-fin_root_x, arm_h - 1), (-tail_len_bot, arm_h - 1)])
rounded = raw.buffer(-fin_round, join_style=2).buffer(fin_round, join_style=1, quad_segs=8)
fin = plate_xz(list(rounded.exterior.coords)[:-1], fin_t)
fillet = plate_xz([(-tail_len_bot, arm_h - 0.5), (-fin_root_x, arm_h - 0.5), (-fin_root_x - 6, arm_h + 1.5), (-tail_len_bot + 2, arm_h + 1.5)], arm_w)
pad = plate_xz([(-pad_l / 2, 0), (pad_l / 2, 0), (pad_l / 2, pad_h - 1.5), (pad_l / 2 - 1.5, pad_h), (-pad_l / 2 + 1.5, pad_h), (-pad_l / 2, pad_h - 1.5)], arm_w)
blade = arm.union(barb).union(fin).union(fillet).union(pad)
blade = blade.cut(teardrop_y(joint_bolt_d, 10, -5, slot_d / 2, True))
blade_inst = blade.translate((0, 0, z_slot))

cq.exporters.export(cap, "wind_vane_cap.step")
cq.exporters.export(blade_inst, "wind_vane_blade.step")
asm = cq.Assembly().add(cap, name="cap", color=cq.Color(0.1, 0.5, 0.5)).add(blade_inst, name="blade", color=cq.Color(0.0, 0.4, 0.4))
asm.save("wind_vane_assembly.step")
for name, w in (("cap", cap), ("blade", blade)):
    s = w.val(); print(name, "valid", s.isValid(), "solids", len(w.solids().vals()), "volume", round(s.Volume(), 1), "COM", s.Center())
