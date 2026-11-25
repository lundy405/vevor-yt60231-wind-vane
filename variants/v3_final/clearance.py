"""Minimum clearance between the rotating cap and the stationary housing envelope
(boss + bearing + tab swept through 360 deg + housing top). Usage: python clearance.py [cap.stl envelope.stl]"""
import sys, numpy as np, trimesh
cap = trimesh.load(sys.argv[1] if len(sys.argv) > 1 else "/tmp/v3_cap.stl")
env = trimesh.load(sys.argv[2] if len(sys.argv) > 2 else "/tmp/v3_envelope.stl")
pts = np.vstack([cap.vertices, trimesh.sample.sample_surface_even(cap, 60000)[0]])
pts = pts[pts[:, 2] < 12]                       # only the lower part can approach the housing
inside = env.contains(pts)
_, dist, _ = trimesh.proximity.closest_point(env, pts)
print("cap points inside stationary envelope:", int(inside.sum()))
i = np.argmin(dist); p = pts[i]
print("min clearance %.2f mm at r=%.2f z=%.2f" % (dist[i], np.hypot(p[0], p[1]), p[2]))
r = np.hypot(pts[:,0], pts[:,1]); z = pts[:,2]
groups = (("rim / drip lip to housing top", z < 3.0),
          ("skirt wall to tab outer edge (r>8)", (r > 8.0) & (z >= 3.0)),
          ("shoulder over the tab (3.5<r<9.5, z>5)", (r > 3.5) & (r < 9.5) & (z > 5.0)),
          ("stem/core to tab inner side (r<3.5, z>4.9)", (r < 3.5) & (z > 4.9)),
          ("stem bottom to bearing (z<4.9)", (r < 3.5) & (z <= 4.9)))
for name, sel in groups:
    if sel.any(): print("  %-44s min %.2f mm" % (name, dist[sel].min()))
