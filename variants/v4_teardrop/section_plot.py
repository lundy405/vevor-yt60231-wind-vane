import trimesh, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as P
M = np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]], float)
def polys(f, x=0.0):
    m = trimesh.load(f); s = m.section(plane_origin=[x,0,0], plane_normal=[1,0,0])
    pl, _ = s.to_planar(to_2D=M, check=False); return pl.polygons_full
fig, ax = plt.subplots(figsize=(11, 11))
for f, col, lab in (("/tmp/v4_housing.stl", "#c8c8c8", "housing / boss / bearing / tab / shaft (stationary, shaft rotates)"),
                    ("/tmp/v4_cap.stl", "#2a8c8c", "printed cap"), ("/tmp/v4_blade.stl", "#155f5f", "printed blade (pad in slot)")):
    for i, p in enumerate(polys(f)):
        ax.add_patch(P(np.array(p.exterior.coords), closed=True, fc=col, ec="k", lw=0.6, label=lab if i == 0 else None))
        for h in p.interiors: ax.add_patch(P(np.array(h.coords), closed=True, fc="white", ec="k", lw=0.6))
def dim(x1, y1, x2, y2, t, dx=0, dy=0, c="crimson"):
    ax.annotate("", (x1, y1), (x2, y2), arrowprops=dict(arrowstyle="<->", color=c, lw=1.2))
    ax.text((x1+x2)/2 + dx, (y1+y2)/2 + dy, t, color=c, fontsize=10, ha="center", va="center",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
dim(-11.35, -1.0, -11.17, -1.0, "", dy=0)
ax.text(-16.8, -3.6, "skirt bottom ID 22.7 (r 11.35), 2.0 below\nhousing top: LINE-TO-LINE with housing\n(housing assumed Ø22.7 at that depth)", color="crimson", fontsize=9, ha="center")
dim(-7.64, 6.1, -8.35, 6.81, "≥1.0 tab corner→shoulder", dx=-9.5, dy=2.6)
dim(-7.64, 3.0, -11.35, 3.0, "3.7 radial (tab→skirt)", dx=0.0, dy=0.9)
dim(-3.64, 6.6, -2.64, 6.6, "1.0", dx=0.2, dy=0.9)
dim(1.9, 3.9, 1.9, 4.4, "0.5 stem→bearing (set by shaft tip)", dx=6.6, dy=-1.6)
ax.annotate("shaft tip seats on the bore end:\ncap self-locates 0.5 above bearing", (-0.3, 19.25), (-19, 21.5), color="crimson", fontsize=9, arrowprops=dict(arrowstyle="->", color="crimson"))
ax.annotate("M2 cup-point set screw on the 0.2 mm flat\n(z = 14.75), access hole through the neck", (5.5, 14.75), (8, 19.5), color="k", fontsize=10,
            arrowprops=dict(arrowstyle="->"))
ax.annotate("skirt overlaps housing side 2.0 mm;\nbottom edge + Ø27.1 lip = drip edge", (13.2, -1.6), (12.0, 7.5), fontsize=10, arrowprops=dict(arrowstyle="->"))
ax.annotate("M3 x 14 clamp bolt\n+ nut pocket", (-6, 24.7), (-19, 30), fontsize=10, arrowprops=dict(arrowstyle="->"))
ax.annotate("tab / post: outer edge r 7.64, 6.1 tall\n(4 mm OD assumed)", (-6.5, 4), (-21, 11.5), fontsize=10, arrowprops=dict(arrowstyle="->"))
ax.annotate("housing top Ø23.2 measured (taper assumed\n0.18 mm/mm, Ø22.34 at top in this dummy)", (8, 0), (4, -6.6), fontsize=9, arrowprops=dict(arrowstyle="->"))
ax.axvline(0, color="r", lw=0.6, ls="--")
ax.set_xlim(-24, 24); ax.set_ylim(-8, 38); ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax.set_xlabel("Y (mm)  — section on the plane through the shaft, perpendicular to the arm"); ax.set_ylabel("Z above housing top (mm)")
ax.set_title("v4 cap: skirt overlaps housing 2 mm — clearances (YT60231 caliper measurements)")
ax.legend(loc="upper right", fontsize=9)
plt.savefig("/workspace/wind-vane/preview_cap_section_clearances.png", dpi=110, bbox_inches="tight")
