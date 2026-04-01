"""UP5PanelBox V4 Final — Rev3 geometry + fillets + TechDraw SVG

Two-piece: Bezel (X=0-face-down) + Box (Z=0-brim-face-down)
"""
import FreeCAD, Part, os

for n in list(FreeCAD.listDocuments().keys()):
    FreeCAD.closeDocument(n)
doc = FreeCAD.newDocument("UP5_V4_Final")

def v(x, y, z): return FreeCAD.Vector(x, y, z)

# ── Parameters ────────────────────────────────────────────────────────────────
PANEL_W = 80.0; PANEL_H = 60.0
OUTER_X = 2.0;  OUTER_Y = 2.0
RING_W  = PANEL_W + OUTER_X        # = 82
RING_H  = PANEL_H + 2 * OUTER_Y   # = 64
BORDER  = 3.0; CX = CY = 8.0
PX0 = OUTER_X; PY0 = OUTER_Y

BOX_X   = PX0 + 7.5   # = 9.5
BOX_W   = 65.0
BOX_BOT = PY0 + 16.0  # = 18.0
BOX_TOP = PY0 + 42.0  # = 44.0
INT_X   = BOX_X + 3.5  # = 13.0
INT_W   = BOX_W - 7.0  # = 58.0
FLOOR_T = 1.0; CEIL_T = 3.5
INT_Y0  = BOX_BOT + FLOOR_T
INT_H   = (BOX_TOP - CEIL_T) - INT_Y0

FRONT_T = 2.0; CHAN_D = 1.5; FW_T = 2.0; BACK_T = 4.5
SLOT_Z0 = FRONT_T
SLOT_Z1 = SLOT_Z0 + CHAN_D
SLOT_Z2 = SLOT_Z1 + FW_T
BEZEL_D = SLOT_Z2 + BACK_T      # = 10.0
BOX_D   = 57.0
box_z   = FW_T + BOX_D          # = 59.0

BRIM_W  = 5.0
brim_x0 = BOX_X      - BRIM_W  # = 4.5
brim_x1 = BOX_X + BOX_W + BRIM_W  # = 79.5
brim_y0 = BOX_BOT    - BRIM_W  # = 13.0
brim_y1 = BOX_TOP    + BRIM_W  # = 49.0
brim_bx = brim_x1 - brim_x0    # = 75.0
brim_by = brim_y1 - brim_y0    # = 36.0

PANEL_TOL  = 0.3
Z_TOL      = 0.2
BRIM_Z_TOL = 0.1
BOW_D      = 2.0

TAB_H   = 10.0
TAB_Z0  = 11.0; TAB_Z1 = 17.0
TAB_EXT = 8.0
BORE_R  = 1.75; CSINK_R = 3.5; CSINK_D = 2.0

RJ12_Z_CTR = 27.5; RJ12_Y_CTR = PY0 + 28.0
RJ12_Z_H   = 9.0;  RJ12_Y_H   = 8.0
PWR_Z_CTR  = 40.5; PWR_Y_CTR  = PY0 + 27.0
PWR_Z_H    = 6.5;  PWR_Y_H    = 8.0

# ── Geometry helpers ──────────────────────────────────────────────────────────
def oct_face(x0, y0, w, h, cx, cy, z=0.0):
    pts = [v(x0+cx,y0,z), v(x0+w-cx,y0,z), v(x0+w,y0+cy,z), v(x0+w,y0+h-cy,z),
           v(x0+w-cx,y0+h,z), v(x0+cx,y0+h,z), v(x0,y0+h-cy,z), v(x0,y0+cy,z)]
    return Part.Face(Part.makePolygon(pts + [pts[0]]))

def arc_bow_solid(y_base, y_apex):
    arc_edge  = Part.Arc(v(0,y_base,0), v(RING_W/2,y_apex,0), v(RING_W,y_base,0)).toShape()
    line_edge = Part.makeLine(v(RING_W,y_base,0), v(0,y_base,0))
    return Part.Face(Part.Wire([arc_edge, line_edge])).extrude(v(0,0,BEZEL_D))

def tri_prism(xz_pts, y0, dy):
    pts3d = [v(p[0], y0, p[1]) for p in xz_pts]
    wire = Part.makePolygon(pts3d + [pts3d[0]])
    return Part.Face(wire).extrude(v(0, dy, 0))

# ── Fillet/chamfer helpers ────────────────────────────────────────────────────
def tf(shape, r, edges, lbl):
    if not edges: print(f"  fillet {lbl}: 0 edges"); return shape
    try:
        s = shape.makeFillet(r, edges)
        print(f"  fillet {lbl}: {len(edges)} edges R={r}"); return s
    except Exception as ex:
        print(f"  fillet {lbl}: FAIL ({ex})"); return shape

def tc(shape, d, edges, lbl):
    if not edges: print(f"  chamfer {lbl}: 0 edges"); return shape
    try:
        s = shape.makeChamfer(d, edges)
        print(f"  chamfer {lbl}: {len(edges)} edges C={d}"); return s
    except Exception as ex:
        print(f"  chamfer {lbl}: FAIL ({ex})"); return shape

def at_ax(shape, ax, val, tol=0.2):
    """Edges where all vertices lie at val on axis ax."""
    return [e for e in shape.Edges
            if all(abs(getattr(vx.Point, ax) - val) < tol for vx in e.Vertexes)]

def z_dir_edges(shape, x_val, y_val, xtol=0.2, ytol=0.2):
    """Vertical (Z-direction) straight edges near (x_val, y_val)."""
    return [e for e in shape.Edges
            if hasattr(e.Curve, 'Direction')
            and abs(abs(e.Curve.Direction.z) - 1.0) < 0.01
            and all(abs(vx.Point.x - x_val) < xtol for vx in e.Vertexes)
            and all(abs(vx.Point.y - y_val) < ytol for vx in e.Vertexes)]

# ── BEZEL ─────────────────────────────────────────────────────────────────────
bezel = Part.makeBox(RING_W, RING_H, BEZEL_D)

bezel = bezel.cut(
    oct_face(PX0+BORDER, PY0+BORDER, PANEL_W-2*BORDER, PANEL_H-2*BORDER, CX, CY)
    .extrude(v(0,0,FRONT_T))
)
bezel = bezel.cut(Part.makeBox(
    RING_W - PX0, PANEL_H + 2*PANEL_TOL, CHAN_D + Z_TOL,
    v(PX0, PY0 - PANEL_TOL, SLOT_Z0)
))
bezel = bezel.cut(Part.makeBox(
    RING_W - brim_x0, brim_by, FW_T + BRIM_Z_TOL,
    v(brim_x0, brim_y0, SLOT_Z1)
))
bezel = bezel.cut(Part.makeBox(RING_W - BOX_X, BOX_TOP - BOX_BOT, BACK_T,
    v(BOX_X, BOX_BOT, SLOT_Z2)))

tab_y0_bez = BOX_TOP - TAB_H
bezel = bezel.cut(Part.makeBox(BOX_X - brim_x0, TAB_H, BACK_T,
    v(brim_x0, tab_y0_bez, SLOT_Z2)))
bezel = bezel.cut(Part.makeBox(brim_x1 - (BOX_X + BOX_W), TAB_H, BACK_T,
    v(BOX_X + BOX_W, tab_y0_bez, SLOT_Z2)))

# ── BEZEL fillets/chamfers — applied BEFORE bow fuse (cleaner topology) ───────
print("Bezel fillets...")
# C0.5 on X=0 end-cap only — safe, 4 clean edges, no interaction with inner cuts
bezel = tc(bezel, 0.5, at_ax(bezel, 'x', 0), "X=0 end-cap pre-bow")

# Z=10 back face: outer perimeter edges only (skip inner opening edges)
z10_outer = [e for e in bezel.Edges
             if all(abs(vx.Z - BEZEL_D) < 0.2 for vx in e.Vertexes)
             and hasattr(e.Curve, 'Direction')
             and (all(abs(vx.Y) < 0.3          for vx in e.Vertexes) or
                  all(abs(vx.Y - RING_H) < 0.3 for vx in e.Vertexes) or
                  all(abs(vx.X) < 0.3          for vx in e.Vertexes))]
bezel = tf(bezel, 0.5, z10_outer, "Z=10 back face outer only")

# Now add bows (after fillets so topology is clean)
bezel = bezel.fuse(arc_bow_solid(0,      -BOW_D))
bezel = bezel.fuse(arc_bow_solid(RING_H, RING_H + BOW_D))

# ── BOX ───────────────────────────────────────────────────────────────────────
brim = Part.makeBox(brim_bx, brim_by, FW_T, v(brim_x0, brim_y0, 0))
body = Part.makeBox(BOX_W, BOX_TOP - BOX_BOT, box_z, v(BOX_X, BOX_BOT, 0))
box  = brim.fuse(body)

box = box.cut(Part.makeBox(INT_W, INT_H, BOX_D, v(INT_X, INT_Y0, FW_T)))
box = box.cut(Part.makeBox(INT_W, INT_H, FW_T,  v(INT_X, INT_Y0, 0)))

tab_y0    = BOX_TOP - TAB_H
left_tab  = Part.makeBox(TAB_EXT, TAB_H, TAB_Z1 - TAB_Z0,
                          v(BOX_X - TAB_EXT, tab_y0, TAB_Z0))
right_tab = Part.makeBox(TAB_EXT, TAB_H, TAB_Z1 - TAB_Z0,
                          v(BOX_X + BOX_W,   tab_y0, TAB_Z0))
box = box.fuse(left_tab).fuse(right_tab)

box = box.fuse(tri_prism(
    [(BOX_X, TAB_Z0), (BOX_X - TAB_EXT, TAB_Z0), (BOX_X, TAB_Z0 - TAB_EXT)],
    tab_y0, TAB_H
))
box = box.fuse(tri_prism(
    [(BOX_X+BOX_W, TAB_Z0), (BOX_X+BOX_W, TAB_Z0-TAB_EXT), (BOX_X+BOX_W+TAB_EXT, TAB_Z0)],
    tab_y0, TAB_H
))

bore_xs = [BOX_X - TAB_EXT/2, BOX_X + BOX_W + TAB_EXT/2]
for bx in bore_xs:
    box = box.cut(Part.makeCylinder(BORE_R,  TAB_H+2, v(bx, tab_y0-1, 14), v(0,1,0)))
    box = box.cut(Part.makeCylinder(CSINK_R, CSINK_D, v(bx, tab_y0-1, 14), v(0,1,0)))

rj_y0 = RJ12_Y_CTR - RJ12_Y_H; rj_y1 = RJ12_Y_CTR + RJ12_Y_H
box = box.cut(Part.makeBox(3.5, rj_y1-rj_y0, RJ12_Z_H*2,
    v(BOX_X, rj_y0, RJ12_Z_CTR - RJ12_Z_H)))
pw_y0 = PWR_Y_CTR - PWR_Y_H; pw_y1 = PWR_Y_CTR + PWR_Y_H
box = box.cut(Part.makeBox(3.5, pw_y1-pw_y0, PWR_Z_H*2,
    v(BOX_X+BOX_W-3.5, pw_y0, PWR_Z_CTR - PWR_Z_H)))

# ── BOX fillets/chamfers ──────────────────────────────────────────────────────
print("Box fillets...")
# Z=0 brim bed face — outer perimeter only (skip interior clearance hole edges)
z0_outer = [e for e in box.Edges
            if all(abs(vx.Z) < 0.2 for vx in e.Vertexes)
            and hasattr(e.Curve, 'Direction')
            and (all(abs(vx.Y - brim_y0) < 0.3 for vx in e.Vertexes) or
                 all(abs(vx.Y - brim_y1) < 0.3 for vx in e.Vertexes) or
                 all(abs(vx.X - brim_x0) < 0.3 for vx in e.Vertexes) or
                 all(abs(vx.X - brim_x1) < 0.3 for vx in e.Vertexes))]
box = tc(box, 0.5, z0_outer, "Z=0 brim outer perimeter")

# Z=2 brim top: outer perimeter only (brim_y0/y1/x0/x1 edges — avoid body interior edges)
z2_outer = [e for e in box.Edges
            if all(abs(vx.Z - FW_T) < 0.2 for vx in e.Vertexes)
            and hasattr(e.Curve, 'Direction')
            and (all(abs(vx.Y - brim_y0) < 0.3 for vx in e.Vertexes) or
                 all(abs(vx.Y - brim_y1) < 0.3 for vx in e.Vertexes) or
                 all(abs(vx.X - brim_x0) < 0.3 for vx in e.Vertexes) or
                 all(abs(vx.X - brim_x1) < 0.3 for vx in e.Vertexes))]
box = tf(box, 0.5, z2_outer, "Z=2 brim top outer")

# Z=59 body top: outer perimeter edges only (skip interior cut edges)
z59_outer = [e for e in box.Edges
             if all(abs(vx.Z - box_z) < 0.2 for vx in e.Vertexes)
             and hasattr(e.Curve, 'Direction')
             and not all(vx.Point.x > INT_X - 0.3 and vx.Point.x < INT_X + INT_W + 0.3
                         and vx.Point.y > INT_Y0 - 0.3 and vx.Point.y < INT_Y0 + INT_H + 0.3
                         for vx in e.Vertexes)]
box = tf(box, 0.5, z59_outer, "Z=59 body top outer")

# ── Panel ghost ───────────────────────────────────────────────────────────────
panel = Part.makeBox(PANEL_W, PANEL_H, 1.5, v(PX0, PY0, 0))

# ── Document objects ──────────────────────────────────────────────────────────
X_OFF = RING_W + 15  # = 97

ob  = doc.addObject("Part::Feature", "Bezel");       ob.Shape  = bezel
obx = doc.addObject("Part::Feature", "Box");         obx.Shape = box
op  = doc.addObject("Part::Feature", "Panel_ghost"); op.Shape  = panel

obx.Placement.Base.x = X_OFF
doc.recompute()

if FreeCAD.GuiUp:
    import FreeCADGui
    ob.ViewObject.ShapeColor   = (0.75, 0.55, 0.2, 0.0)
    obx.ViewObject.ShapeColor  = (0.2,  0.5,  1.0, 0.0)
    op.ViewObject.ShapeColor   = (0.9,  0.9,  0.9, 0.0)
    op.ViewObject.Transparency = 70
    FreeCADGui.ActiveDocument.ActiveView.fitAll()
    FreeCADGui.ActiveDocument.ActiveView.viewIsometric()

# ── TechDraw page ─────────────────────────────────────────────────────────────
if FreeCAD.GuiUp:
    td_dir = os.path.join(FreeCAD.getResourceDir(), 'Mod', 'TechDraw', 'Templates')
    tmpl_path = os.path.join(td_dir, 'A3_Landscape_ISO5457_minimal.svg')

    page = doc.addObject('TechDraw::DrawPage',        'Page')
    tmpl = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
    tmpl.Template = tmpl_path
    page.Template = tmpl

    def add_view(name, src, direc, xdir, px, py, scale=1.0):
        vw = doc.addObject('TechDraw::DrawViewPart', name)
        vw.Source    = [src]
        vw.Direction = direc
        vw.XDirection = xdir
        vw.Scale     = scale
        vw.X = px; vw.Y = py
        page.addView(vw)
        return vw

    # ── Bezel: left half of A3, scale 1:1
    # Front (view from -Z → looking at front face XY plane)
    add_view('Bezel_Front', ob, v(0,0,-1), v(1,0,0),  75, 190, 1.0)
    # Side profile (view from +Y → looking down at XZ plane, shows depth)
    add_view('Bezel_Side',  ob, v(0,1,0),  v(1,0,0),  75,  95, 1.0)
    # Right end (view from -X → end cap face YZ plane)
    add_view('Bezel_End',   ob, v(-1,0,0), v(0,0,-1), 180, 190, 1.0)

    # ── Box: right half of A3, scale 1:1
    # Front (view from -Z → brim face XY plane)
    add_view('Box_Front', obx, v(0,0,-1), v(1,0,0),  295, 190, 1.0)
    # Right (view from +X → YZ plane, shows height + depth)
    add_view('Box_Right', obx, v(1,0,0),  v(0,0,-1), 390, 190, 1.0)
    # Top (view from -Y → XZ plane, shows width + depth)
    add_view('Box_Top',   obx, v(0,-1,0), v(1,0,0),  295,  95, 1.0)

    doc.recompute()

    out_dir = '/home/abyrne/Projects/Trains/CADlayout/UP5PanelBox/drawings/'
    os.makedirs(out_dir, exist_ok=True)
    print(f"TechDraw page ready — export SVG via FreeCAD: File > Export > SVG")

# ── STL export ────────────────────────────────────────────────────────────────
import MeshPart
stl_dir = '/home/abyrne/Projects/Trains/CADlayout/UP5PanelBox/printed_files/'
for name, shape, fname in [
    ('Bezel', bezel, 'UP5_V4_Final-Bezel.stl'),
    ('Box',   box,   'UP5_V4_Final-Box.stl'),
]:
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05,
                                   AngularDeflection=0.1, Relative=False)
    mesh.write(stl_dir + fname)
    print(f"STL {fname}: {mesh.CountFacets} facets")

print(f"\nBezel volume: {bezel.Volume:.0f} mm³")
print(f"Box volume:   {box.Volume:.0f} mm³")
