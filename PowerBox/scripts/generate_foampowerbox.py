"""
FoamPowerBox — foam-embedded power distribution tray
100 x 90 x 25mm outer, open top, no lid.

Components:
  - Barrel connector: two-tab U-channel (front-left), barrel points straight up
      · Z-stop lip on left inner wall (wire clearance)
      · X-retention lips at back of channel
      · 2 vertical press-fit ribs per tab face (Y grip) + 2 ribs on left wall (X grip)
  - DC-DC converter: flat floor, 2 round + 2 oval locating pegs (upper-left)
  - 2x 2-slot barrier terminal strips (Ideal 89-302 or similar): inline along Y-axis, right side
      · Shelves span full interior Y (42mm each, together = 84mm)
      · 4 retention pegs per strip at measured mounting hole positions
      · Peg height = half recess depth

Run via FreeCAD MCP bridge:
  proxy.execute(open('scripts/generate_foampowerbox.py').read())
"""

import FreeCAD as App
import Part

# ── Parameters ───────────────────────────────────────────────────────────────

BOX_X    = 100.0
BOX_Y    =  90.0
BOX_Z    =  25.0
WALL     =   3.0
CORNER_R =   3.0

# Terminal strips — 2-slot barrier strip (measured), rotated 90°
# Long axis (41.2mm, terminals) runs in Y; base width (22mm) runs in X from right wall
# Barrier body is 28mm wide but only 22mm base sits on shelf — barrier overhangs above
STRIP_W       = 41.2   # strip long span in Y (terminal axis, measured)
STRIP_D       = 22.0   # strip base width in X (minimum at mounting holes, measured)
STRIP_SHELF_D = 28.0   # shelf depth in X — STRIP_D + 4mm barrier tab + 2mm clearance to right wall
STRIP_DEPTH   = 12.75  # actual strip total depth (base body, measured)
STRIP_RECESS  =  6.35  # mounting flange height (from spec .25" = 6.35mm)
STRIP_SHELF_H = BOX_Z - WALL - STRIP_DEPTH    # 9.25mm solid shelf height

# Each shelf spans half the interior Y so the two shelves fill the full box Y
SHELF_Y = (BOX_Y - 2*WALL) / 2.0   # 42mm per shelf — fits 41.2mm strip with 0.4mm each end
STRIP_OFFSET = (SHELF_Y - STRIP_W) / 2.0   # 0.4mm — strip centred in shelf

# Strip retention pegs — 4 per strip, from direct measurement of physical strip
# Hole positions in strip-local coords (0-origin, long axis=X_strip, depth=Y_strip):
#   short edge to hole centre = 4mm (along long axis)
#   short edge hole-to-hole   = 10.5mm (along depth axis, i.e. 5.8mm and 16.3mm from long edge)
#   long edge to hole centre  = 5.8mm (along depth axis)
#   long edge hole-to-hole    = 32.4mm (along long axis → second hole at 36.4mm)
# After 90° rotation: box_X = STRIP_X_OUTER + Y_strip, box_Y = recess_start + X_strip
STRIP_HOLE_LONG  = [4.0, 36.4]    # X_strip positions (along long/Y axis in box)
STRIP_HOLE_DEPTH = [5.8, 16.3]    # Y_strip positions (along depth/X axis in box)
STRIP_PEG_R = 2.25   # peg radius → 4.5mm diameter (measured hole clearance)
STRIP_PEG_H = 8.0    # peg height — 8mm engagement depth

# DC-DC converter
DCDC_W       = 64.0    # total width in X (50mm body + 7mm flanges each side)
DCDC_L       = 53.0    # length in Y (placed at back/upper area)
# Round locating pegs (from PowerBox Sketch005)
DCDC_RND_PEG_R = 1.35
DCDC_RND_PEG_H = 2.0
DCDC_RND_PEGS  = [(7.0, 68.0), (63.4, 68.0)]
# Oval locating pegs (from PowerBox Sketch005 arc/line geometry)
# Stadium shape: 2.8mm wide (X), 6mm long (Y), centred at given coords
DCDC_OVL_PEG_R = 1.4    # arc radius = half of 2.8mm width
DCDC_OVL_PEG_H = 2.0
DCDC_OVL_PEGS  = [(14.0, 41.5), (56.0, 41.5)]
DCDC_OVL_SEG   = (6.0 - 2.0*DCDC_OVL_PEG_R) / 2.0   # 1.6mm half-segment (6mm total length)

# Barrel connector
BC_HX   = 13.0   # housing X depth into box (from inner left wall) — +1mm clearance
BC_HY   = 15.0   # housing Y span / tab gap — +1mm clearance
BC_PD   =  9.2   # pocket engagement depth from top rim
TAB_T   =  3.0   # tab wall thickness in Y
TAB_X   = BC_HX + TAB_T    # 16mm tab length in X
TAB_H   = BOX_Z - WALL     # 22mm — tabs full internal height

LIP_Z      = 2.0   # Z-stop lip thickness
LIP_X      = 2.0   # Z-stop lip protrusion in X from inner left wall
LIP_RET    = 1.5   # X-retention lip protrusion in Y from each tab face
LIP_RET_ZH = 4.0   # Z height of retention lip from box rim downward

# Barrel press-fit ribs — vertical ribs to grip connector in Y (tab faces) and X (left wall)
RIB_W    = 4.0    # rib width along the wall surface
RIB_PROJ = 0.35   # rib protrusion into the channel
RIB_H    = BC_PD  # rib height = connector engagement zone (9.2mm, from housing bottom to rim)

# ── Derived ──────────────────────────────────────────────────────────────────

STRIP_X_OUTER  = BOX_X - WALL - STRIP_SHELF_D   # 71mm outer left edge of strip shelf
STRIP_SHELF_Z  = WALL + STRIP_SHELF_H            # 18.65mm — shelf top Z

# Barrel tab Y positions (outer coords)
TAB1_Y_START = WALL                              # front tab: Y=3mm
TAB2_Y_START = WALL + TAB_T + BC_HY             # back tab:  Y=21mm (3+3+15)
GAP_Y_START  = WALL + TAB_T                     # gap start: Y=6mm
GAP_Y_END    = WALL + TAB_T + BC_HY             # gap end:   Y=21mm

HOUSING_BOTTOM_Z = BOX_Z - BC_PD                # 15.8mm — housing bottom Z level
LIP_Z_START      = HOUSING_BOTTOM_Z - LIP_Z     # 13.8mm
LIP_Z_END        = HOUSING_BOTTOM_Z             # 15.8mm

RET_LIP_X_START = WALL + BC_HX - 1.0           # 15mm
RET_LIP_X_END   = WALL + TAB_X                  # 19mm
RET_LIP_Z_START = BOX_Z - LIP_RET_ZH            # 21mm
RET_LIP_Z_END   = BOX_Z                         # 25mm

DCDC_Y = BOX_Y - WALL - DCDC_L                  # 34mm outer front edge of DC-DC area

# ── Helpers ───────────────────────────────────────────────────────────────────

def _try_fillet(s, r, edges, label):
    try:
        return s.makeFillet(r, edges)
    except Exception as ex:
        print("Fillet %s skipped: %s" % (label, ex))
        return s

def make_oval_peg(cx, cy, floor_z, radius, seg_half, height):
    """Stadium/oval peg extruded upward in Z. Oval runs in Y direction."""
    if seg_half < 0.05:
        return Part.makeCylinder(radius, height, App.Vector(cx, cy, floor_z))
    cap1 = Part.makeCylinder(radius, height, App.Vector(cx, cy + seg_half, floor_z))
    cap2 = Part.makeCylinder(radius, height, App.Vector(cx, cy - seg_half, floor_z))
    mid  = Part.makeBox(radius * 2.0, seg_half * 2.0, height,
                        App.Vector(cx - radius, cy - seg_half, floor_z))
    return cap1.fuse(cap2).fuse(mid)

# ── Build ─────────────────────────────────────────────────────────────────────

# 1. Outer solid box — fillet vertical corners before cavity cut
#    (filleting after the cut loses the outer corner edges due to OCCT topology changes)
outer = Part.makeBox(BOX_X, BOX_Y, BOX_Z)
v_outer = [
    e for e in outer.Edges
    if hasattr(e.Curve, 'Direction')
    and abs(abs(e.Curve.Direction.z) - 1.0) < 0.01
    and (e.CenterOfMass.x < 1.0 or e.CenterOfMass.x > BOX_X - 1.0)
    and (e.CenterOfMass.y < 1.0 or e.CenterOfMass.y > BOX_Y - 1.0)
]
outer = _try_fillet(outer, CORNER_R, v_outer, "outer box corners")

# 2. Interior cavity
inner = Part.makeBox(BOX_X - 2*WALL, BOX_Y - 2*WALL, BOX_Z - WALL,
                     App.Vector(WALL, WALL, WALL))
shape = outer.cut(inner)

# 3. Terminal strip shelves — right side, two shelves spanning full interior Y
#    Each shelf: STRIP_SHELF_D (28mm) in X, SHELF_Y (42mm) in Y, STRIP_SHELF_H tall
#    Extra 6mm beyond strip base (4mm barrier tab + 2mm clearance to right wall).
#    Together the two shelves fill the full 84mm inner Y.
shelf1 = Part.makeBox(STRIP_SHELF_D, SHELF_Y, STRIP_SHELF_H,
                      App.Vector(STRIP_X_OUTER, WALL, WALL))
shelf2 = Part.makeBox(STRIP_SHELF_D, SHELF_Y, STRIP_SHELF_H,
                      App.Vector(STRIP_X_OUTER, WALL + SHELF_Y, WALL))
shape = shape.fuse(shelf1).fuse(shelf2)

# 4. Strip retention pegs — 4 per strip, at ElectricBox Sketch001 hole positions
#    Strip recess is centred within the 42mm shelf (STRIP_OFFSET on each end).
for shelf_idx, shelf_y_start in enumerate([WALL, WALL + SHELF_Y]):
    recess_y_start = shelf_y_start + STRIP_OFFSET  # centre strip in shelf
    for x_strip in STRIP_HOLE_LONG:
        for y_strip in STRIP_HOLE_DEPTH:
            peg_x = STRIP_X_OUTER + y_strip      # rotated: depth → X in box
            peg_y = recess_y_start + x_strip      # rotated: long → Y in box
            peg = Part.makeCylinder(STRIP_PEG_R, STRIP_PEG_H,
                                    App.Vector(peg_x, peg_y, STRIP_SHELF_Z))
            shape = shape.fuse(peg)

# 5. Barrel connector tabs — U-channel at front-left inner corner
tab1 = Part.makeBox(TAB_X, TAB_T, TAB_H,
                    App.Vector(WALL, TAB1_Y_START, WALL))
tab2 = Part.makeBox(TAB_X, TAB_T, TAB_H,
                    App.Vector(WALL, TAB2_Y_START, WALL))
shape = shape.fuse(tab1).fuse(tab2)

# 6. Barrel Z-stop lip (on inner left wall face, spans Y gap)
z_lip = Part.makeBox(LIP_X, BC_HY, LIP_Z,
                     App.Vector(WALL, GAP_Y_START, LIP_Z_START))
shape = shape.fuse(z_lip)

# 7. Barrel X-retention lips (from each tab inner face, at back-top of channel)
ret_lip1 = Part.makeBox(RET_LIP_X_END - RET_LIP_X_START, LIP_RET, LIP_RET_ZH,
                        App.Vector(RET_LIP_X_START, GAP_Y_START, RET_LIP_Z_START))
ret_lip2 = Part.makeBox(RET_LIP_X_END - RET_LIP_X_START, LIP_RET, LIP_RET_ZH,
                        App.Vector(RET_LIP_X_START, GAP_Y_END - LIP_RET, RET_LIP_Z_START))
shape = shape.fuse(ret_lip1).fuse(ret_lip2)

# 8. Barrel press-fit ribs
#    Y-direction: 2 ribs on each tab inner face (tab1 at y=GAP_Y_START, tab2 at y=GAP_Y_END)
#    X-direction: 2 ribs on inner left wall face (at x=WALL), spanning connector gap in Y
rib_z   = HOUSING_BOTTOM_Z           # start at housing bottom (15.8mm)
rib_x1  = WALL + TAB_X * 0.25 - RIB_W / 2.0   # first rib X position (~5mm)
rib_x2  = WALL + TAB_X * 0.75 - RIB_W / 2.0   # second rib X position (~13mm)
rib_y1  = GAP_Y_START + BC_HY * 0.25 - RIB_W / 2.0  # first Y-wall rib Y position
rib_y2  = GAP_Y_START + BC_HY * 0.75 - RIB_W / 2.0  # second Y-wall rib Y position
# Tab1 inner face ribs (protrude toward +Y into gap)
for rx in [rib_x1, rib_x2]:
    rib = Part.makeBox(RIB_W, RIB_PROJ, RIB_H, App.Vector(rx, GAP_Y_START, rib_z))
    shape = shape.fuse(rib)
# Tab2 inner face ribs (protrude toward -Y into gap)
for rx in [rib_x1, rib_x2]:
    rib = Part.makeBox(RIB_W, RIB_PROJ, RIB_H, App.Vector(rx, GAP_Y_END - RIB_PROJ, rib_z))
    shape = shape.fuse(rib)
# Left wall ribs (protrude toward +X into channel)
for ry in [rib_y1, rib_y2]:
    rib = Part.makeBox(RIB_PROJ, RIB_W, RIB_H, App.Vector(WALL, ry, rib_z))
    shape = shape.fuse(rib)

# 9. DC-DC round locating pegs
for px, py in DCDC_RND_PEGS:
    peg = Part.makeCylinder(DCDC_RND_PEG_R, DCDC_RND_PEG_H,
                            App.Vector(px, py, WALL))
    shape = shape.fuse(peg)

# 10. DC-DC oval locating pegs (stadium shape, 2.8mm wide × 6mm long in Y)
for px, py in DCDC_OVL_PEGS:
    peg = make_oval_peg(px, py, WALL, DCDC_OVL_PEG_R, DCDC_OVL_SEG, DCDC_OVL_PEG_H)
    shape = shape.fuse(peg)

# 11. Internal fillets
# Shelf leading edge: top horizontal edge of shelf face at x=STRIP_X_OUTER, z=STRIP_SHELF_Z
shelf_top_edges = [
    e for e in shape.Edges
    if hasattr(e.Curve, 'Direction')
    and abs(e.Curve.Direction.y) > 0.99
    and abs(e.CenterOfMass.x - STRIP_X_OUTER) < 0.5
    and abs(e.CenterOfMass.z - STRIP_SHELF_Z) < 0.5
]
shape = _try_fillet(shape, 1.5, shelf_top_edges, "shelf leading top edge")

# Shelf inner vertical corners at x=STRIP_X_OUTER (below shelf top)
shelf_vert_edges = [
    e for e in shape.Edges
    if hasattr(e.Curve, 'Direction')
    and abs(abs(e.Curve.Direction.z) - 1.0) < 0.01
    and abs(e.CenterOfMass.x - STRIP_X_OUTER) < 0.5
    and e.CenterOfMass.z < STRIP_SHELF_Z - 0.5
]
shape = _try_fillet(shape, 1.0, shelf_vert_edges, "shelf inner vertical corners")

# ── Document ──────────────────────────────────────────────────────────────────

doc = App.newDocument("FoamPowerBox")
feat = doc.addObject("Part::Feature", "FoamPowerBox")
feat.Shape = shape
doc.recompute()

if App.GuiUp:
    import FreeCADGui
    FreeCADGui.activeDocument().activeView().viewIsometric()
    FreeCADGui.SendMsgToActiveView("ViewFit")

out_path = "/home/abyrne/Projects/Trains/CADlayout/PowerBox/freecad/FoamPowerBox.FCStd"
doc.saveAs(out_path)
_result_ = "OK — FoamPowerBox v9 (production) saved to %s" % out_path
