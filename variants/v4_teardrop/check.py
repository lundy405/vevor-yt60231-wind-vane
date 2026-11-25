import sys, trimesh
m = trimesh.load(sys.argv[1])
print("watertight", m.is_watertight, "winding", m.is_winding_consistent, "volume_ok", m.is_volume, "bodies", len(m.split(only_watertight=False)))
print("bounds", m.bounds.round(2).tolist(), "extents", m.extents.round(2).tolist())
v = m.volume/1000
print("volume cm3 %.3f  solid PETG g %.2f" % (v, v*1.27))
print("COM mm", m.center_mass.round(3).tolist())
