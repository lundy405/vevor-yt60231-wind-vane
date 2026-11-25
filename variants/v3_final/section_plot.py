import trimesh, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as P
M = np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]], float)
def polys(f, x=0.0):
    m = trimesh.load(f); s = m.section(plane_origin=[x,0,0], plane_normal=[1,0,0])
    pl, _ = s.to_planar(to_2D=M, check=False); return pl.polygons_full
fig, ax = plt.subplots(figsize=(11, 11))
for f, col, lab in (("/tmp/v3_housing.stl", "#c8c8c8", "housing / boss / bearing / tab / shaft (stationary, shaft rotates)"),
                    ("/tmp/v3_cap.stl", "#2a8c8c", "printed cap"), ("/tmp/v3_blade.stl", "#155f5f", "printed blade (pad in slot)")):
    for i, p in enumerate(polys(f)):
        ax.add_patch(P(np.array(p.exterior.coords), closed=True, fc=col, ec="k", lw=0.6, label=lab if i == 0 else None))
        for h in p.interiors: ax.add_patch(P(np.array(h.coords), closed=True, fc="white", ec="k", lw=0.6))
def dim(x1, y1, x2, y2, t, dx=0, dy=0, c="crimson"):
    ax.annotate("", (x1, y1), (x2, y2), arrowprops=dict(arrowstyle="<->", color=c, lw=1.2))
    ax.text((x1+x2)/2 + dx, (y1+y2)/2 + dy, t, color=c, fontsize=10, ha="center", va="center",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
dim(-7.64, 3.0, -9.14, 3.0, "1.5 radial\n(tab→skirt)", dx=-4.5, dy=-1.6)
dim(-7.64, 6.1, -8.35, 6.81, "≥1.0 tab corner→shoulder", dx=-8.5, dy=2.2)
dim(-3.64, 6.6, -2.64, 6.6, "1.0", dx=0.2, dy=0.9)
ax.text(-12.5, 9.8, "stem r 2.64 clears tab inner side\n(r ≈ 3.64 if tab is 4 mm OD)", color="crimson", fontsize=9, ha="center")
dim(1.9, 3.9, 1.9, 4.4, "0.5 stem→bearing (shim)", dx=7.0, dy=-1.1)
dim(12.0, 0, 12.0, 1.5, "1.5 rim gap", dx=4.4)
dim(-0.8, 19.25, -0.8, 20.75, "1.5 shaft tip→bore end", dx=-6.5)
ax.annotate("M2 cup-point set screw on the 0.2 mm flat\n(z = 14.75), access hole through the neck", (5.5, 14.75), (8, 19.5), color="k", fontsize=10,
            arrowprops=dict(arrowstyle="->"))
ax.annotate("drip lip Ø25.1 overhangs the\nØ23.2 housing top edge", (12.2, 2.9), (12.5, 7.0), fontsize=10, arrowprops=dict(arrowstyle="->"))
ax.annotate("M3 x 14 clamp bolt\n+ nut pocket", (-6, 26.2), (-19, 31), fontsize=10, arrowprops=dict(arrowstyle="->"))
ax.annotate("tab / post: outer edge r 7.64, 6.1 tall\n(4 mm OD assumed)", (-6.5, 4), (-21, -4.5), fontsize=10, arrowprops=dict(arrowstyle="->"))
ax.axvline(0, color="r", lw=0.6, ls="--")
ax.set_xlim(-22, 22); ax.set_ylim(-6, 38); ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax.set_xlabel("Y (mm)  — section on the plane through the shaft, perpendicular to the arm"); ax.set_ylabel("Z above housing top (mm)")
ax.set_title("v3 cap over bearing boss + tab — clearances (YT60231 caliper measurements)")
ax.legend(loc="upper right", fontsize=9)
plt.savefig("/workspace/wind-vane/preview_cap_section_clearances.png", dpi=110, bbox_inches="tight")
