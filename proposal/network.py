"""Two-zone thermal model of an indoor ice rink.

(a) physical system  - building section: upper/lower air zones, ice, cooled slab
(b) thermal network  - conductances K = UA between the four temperature nodes

MATH3001 Group 8. Steady state, so no capacitances appear in the network.
"""
import os

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch

# ---------------- palette ----------------
SURF  = '#FBFAF7'   # paper
INK   = '#1F2328'   # primary ink, inter-zone flux
INK2  = '#5A6068'   # secondary text
MUTED = '#9AA1A9'   # prescribed quantities, envelope
HOT   = '#C2562B'   # heat input, warm upper zone
COLD  = '#2E6F9E'   # cold side: lower zone, ice, refrigeration
OPT   = '#7A5BA6'   # optional radiation term

fig = plt.figure(figsize=(14, 7.4), facecolor=SURF)
gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0],
                      left=0.035, right=0.975, top=0.80, bottom=0.04, wspace=0.10)

# physical system 
axL = fig.add_subplot(gs[0, 0]); axL.set_facecolor(SURF)
axL.set_xlim(0, 10); axL.set_ylim(0, 10); axL.axis('off')
axL.text(0, 9.7, '(a)  Physical system', fontsize=11, color=INK, fontweight='bold')

# building envelope
axL.add_patch(FancyBboxPatch((1.0, 1.25), 8.0, 7.15,
                             boxstyle='round,pad=0,rounding_size=0.18',
                             fc='none', ec=MUTED, lw=2.6, zorder=4))
axL.text(1.0, 8.62, '$T_{out}$   outside air', fontsize=9, color=MUTED)

# upper zone: warm, stratified
axL.add_patch(Rectangle((1.0, 3.08), 8.0, 5.32, fc=HOT, alpha=0.07, ec='none', zorder=1))
axL.text(1.3, 7.50, '$T_U$', fontsize=13, color=HOT, fontweight='bold')
axL.text(1.3, 7.10, 'upper zone, warm stratified air', fontsize=8, color=INK2)

# lower zone: thin cold layer sitting on the ice
axL.add_patch(Rectangle((1.0, 2.44), 8.0, 0.64, fc=COLD, alpha=0.09, ec='none', zorder=1))
axL.plot([1.0, 9.0], [3.08, 3.08], color=INK, lw=1.2, ls=(0, (5, 4)), zorder=3)
axL.text(8.45, 2.76, '$T_L$   lower zone', fontsize=8.5, color=COLD,
         ha='right', va='center')

# ice sheet on the refrigerated slab
axL.add_patch(Rectangle((1.4, 2.15), 7.2, 0.29, fc=COLD, alpha=0.30,
                        ec=COLD, lw=1.4, zorder=3))
axL.text(8.45, 2.29, '$T_{ice}$   ice sheet', fontsize=8.5, color=COLD,
         ha='right', va='center')
axL.add_patch(Rectangle((1.4, 1.25), 7.2, 0.90, fc=MUTED, alpha=0.20,
                        ec=MUTED, lw=1.4, zorder=2))
for i in range(11):                                    # brine pipes in the slab
    axL.add_patch(Circle((2.0 + 0.6 * i, 1.70), 0.09, fc=SURF, ec=COLD,
                         lw=1.1, zorder=3))

# envelope loss to outside
axL.annotate('', xy=(4.6, 9.15), xytext=(4.6, 8.25),
             arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.8, mutation_scale=13))
axL.text(4.82, 8.86, '$\\dot{Q}_{env}$', fontsize=10, color=MUTED)
axL.text(4.82, 8.46, 'sign set by season', fontsize=7.5, color=MUTED)

# heat into the upper zone: plant plus internal gains
axL.annotate('', xy=(6.4, 6.30), xytext=(6.4, 5.55),
             arrowprops=dict(arrowstyle='-|>', color=HOT, lw=1.8, mutation_scale=13))
axL.text(6.6, 5.80, '$\\dot{Q}_H$', fontsize=10, color=HOT,
         fontweight='bold')
axL.text(6.6, 5.40, 'heating plant', fontsize=7.5, color=INK2)

axL.annotate('', xy=(5.0, 3.08), xytext=(5.0, 3.75),
             arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.6, mutation_scale=12))
axL.text(5.2, 3.30, '$\\dot{Q}_{UL}$', fontsize=10, color=INK)

axL.annotate('', xy=(2.45, 2.44), xytext=(2.45, 2.92),
             arrowprops=dict(arrowstyle='-|>', color=COLD, lw=1.6, mutation_scale=12))
axL.text(2.27, 2.56, '$\\dot{Q}_{LI}$', fontsize=10, color=COLD, ha='right')

axL.annotate('', xy=(6.0, 1.00), xytext=(6.0, 2.0),
             arrowprops=dict(arrowstyle='-|>', color=COLD, lw=2.4, mutation_scale=16))
axL.text(6.2, 1.02, '$\\dot{Q}_C$', fontsize=12, color=COLD, fontweight='bold')
axL.text(6.2, 0.62, 'refrigeration slab', fontsize=8, color=COLD)

axL.text(1.3, 0.95, 'Closed system: internal air circulation only,\nno outside-air exchange.',
         fontsize=8, color=INK2, style='italic', linespacing=1.4, va='top')

# thermal network
axR = fig.add_subplot(gs[0, 1]); axR.set_facecolor(SURF)
axR.set_xlim(0, 10); axR.set_ylim(0, 10); axR.axis('off')
axR.text(0, 9.7, '(b)  Thermal network', fontsize=11, color=INK, fontweight='bold')

XN, NR = 4.2, 0.20
YS = {'out': 8.70, 'U': 6.25, 'L': 3.80, 'ice': 1.95}

def dot(y, colour, filled=True):
    axR.add_patch(Circle((XN, y), NR, fc=(colour if filled else SURF),
                         ec=colour, lw=2.0, zorder=5))

def tlabel(y, sym, name, colour):
    axR.text(XN + NR + 0.28, y + 0.16, sym, fontsize=12.5, color=colour,
             ha='left', va='center')
    axR.text(XN + NR + 0.28, y - 0.30, name, fontsize=7.5, color=INK2,
             ha='left', va='center')

def resistor(y0, y1, label, expr, colour):
    ym = (y0 + y1) / 2
    axR.plot([XN, XN], [y0, ym - 0.42], color=colour, lw=1.7, zorder=2)
    axR.plot([XN, XN], [ym + 0.42, y1], color=colour, lw=1.7, zorder=2)
    axR.add_patch(Rectangle((XN - 0.24, ym - 0.42), 0.48, 0.84,
                            fc=SURF, ec=colour, lw=1.9, zorder=3))
    axR.text(XN + 0.44, ym + 0.14, label, fontsize=11.5, color=colour, va='center',
             fontweight='bold')
    axR.text(XN + 0.44, ym - 0.22, expr, fontsize=8.5, color=INK2, va='center',
             bbox=dict(fc=SURF, ec='none', pad=1.2), zorder=4)

def source(cx, cy, sym, note, colour):
    axR.add_patch(Circle((cx, cy), 0.30, fc=SURF, ec=colour, lw=1.9, zorder=4))
    axR.annotate('', xy=(cx, cy + 0.17), xytext=(cx, cy - 0.17),
                 arrowprops=dict(arrowstyle='-|>', color=colour, lw=1.5,
                                 mutation_scale=10), zorder=5)
    axR.text(cx - 0.44, cy + 0.16, sym, fontsize=11.5, color=colour, ha='right',
             va='center', fontweight='bold')
    axR.text(cx - 0.44, cy - 0.30, note, fontsize=7.5, color=colour, ha='right',
             va='center', linespacing=1.3)

dot(YS['out'], MUTED);  tlabel(YS['out'], '$T_{out}$', 'outside air', MUTED)
dot(YS['U'],   HOT);    tlabel(YS['U'],   '$T_U$',     'upper zone',  HOT)
dot(YS['L'],   COLD, filled=False); tlabel(YS['L'], '$T_L$', 'lower zone', COLD)
dot(YS['ice'], COLD);   tlabel(YS['ice'], '$T_{ice}$', 'ice surface', COLD)

resistor(YS['out'] - NR, YS['U'] + NR, '$K_{env}$', '$=U_{env}A_{env}$', MUTED)
resistor(YS['U']  - NR, YS['L'] + NR, '$K_{UL}$',  '$=U_{UL}A_{UL}$',   INK)
resistor(YS['L']  - NR, YS['ice'] + NR, '$K_{LI}$', '$=U_{LI}A_{ice}$', COLD)

# heat source into T_U: Q_H (unknown, solved for)
XS, XJ = 2.15, 3.10
source(XS, YS['U'], '$\\dot{Q}_H$', 'heating plant\n(unknown)', HOT)
axR.plot([XS + 0.30, XN - NR], [YS['U'], YS['U']], color=HOT, lw=1.7, zorder=2)


axR.annotate('', xy=(XN, 1.05), xytext=(XN, YS['ice'] - NR),
             arrowprops=dict(arrowstyle='-|>', color=COLD, lw=2.4, mutation_scale=16))
axR.text(XN - 0.26, 1.46, '$\\dot{Q}_C$', fontsize=12.5, color=COLD,
         fontweight='bold', ha='right', va='center')
axR.text(XN - 0.26, 1.02, 'refrigeration\nextraction (unknown)', fontsize=7.5,
         color=COLD, ha='right', va='center', linespacing=1.3)

from matplotlib.patches import FancyArrowPatch
axR.add_patch(FancyArrowPatch((XN + NR*0.7, YS['U'] - NR*0.7),
                              (XN + NR*0.7, YS['ice'] + NR*0.7),
                              connectionstyle='arc3,rad=-1.05', arrowstyle='-|>',
                              color=OPT, lw=1.5, ls=(0, (4, 3)), mutation_scale=13,
                              zorder=2, shrinkA=0, shrinkB=0))
axR.text(7.55, 4.15, '$\\dot{Q}_{rad}$', fontsize=10.5, color=OPT, va='center',
         fontweight='bold')
axR.text(7.55, 3.74, 'ceiling to ice,', fontsize=7.5, color=OPT, va='center')
axR.text(7.55, 3.44, 'transparent to air', fontsize=7.5, color=OPT, va='center')
axR.text(7.55, 3.02, 'OPTIONAL', fontsize=7.5, color=OPT, va='center', fontweight='bold')

# legend, single row along the bottom
axR.add_patch(Circle((0.30, 0.35), 0.15, fc=MUTED, ec=MUTED, lw=1.6))
axR.text(0.56, 0.35, 'prescribed', fontsize=8, color=INK2, va='center')
axR.add_patch(Circle((2.20, 0.35), 0.15, fc=SURF, ec=COLD, lw=1.8))
axR.text(2.46, 0.35, 'solved for', fontsize=8, color=INK2, va='center')
axR.add_patch(Rectangle((4.05, 0.22), 0.22, 0.26, fc=SURF, ec=INK, lw=1.6))
axR.text(4.42, 0.35, 'conductance  $K = UA$  [W K$^{-1}$]', fontsize=8,
         color=INK2, va='center')

fig.suptitle('Two-zone thermal model of an indoor ice rink',
             fontsize=14.5, color=INK, x=0.035, ha='left', y=0.955, fontweight='bold')
fig.text(0.035, 0.895,
         'MATH3001 Group 8   ·   steady state   ·   diagram inspired by '
'Harrikari (2020) and Frahm (2024)',
         fontsize=9, color=INK2, ha='left')
fig.text(0.035, 0.845,
         'No thermal capacitances are shown: the primary model is steady state, so '
         'accumulation terms vanish.',
         fontsize=8.5, color=MUTED, ha='left', style='italic')

OUTDIR = os.path.join(os.path.expanduser('~'), 'Documents', 'School',
                      'Applied Mathematical Modelling')
if not os.path.isdir(OUTDIR):
    OUTDIR = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(OUTDIR, 'Thermal_Network.png')
plt.savefig(out, dpi=200, facecolor=SURF, bbox_inches='tight', pad_inches=0.32)
print('saved ->', out)
plt.show()