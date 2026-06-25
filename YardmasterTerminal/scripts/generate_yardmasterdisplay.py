#!/usr/bin/env python3
"""Generate YardmasterTerminal enclosure v3 — three-part design.

Three 3D-printed parts:
  1. Bezel      185×144mm face-down box lid; 166×100mm display opening (full
                LCD panel face); 4× M3 front-face screws clamp the sandwich.
                "YARDMASTER" recessed into the front face.
  2. Enclosure  185×144×12mm back-face-down box; 4× M3 boss cylinders for
                screw engagement; connector slot on port (+X) side.
  3. Wedge      80mm-wide 45° L-bracket (back leg + bottom leg + end caps);
                enclosure rests in the open V; one M3 screw at deep end locks.

Assembly (front → back):
  Bezel → LCD display + ELECROW board → Enclosure → (rests in) Wedge

Screw path:  4× M3×12 socket-head from bezel front face
  → counterbore in face plate
  → through hollow standoff (inside bezel box)
  → through board mounting tab (1.5 mm)
  → into M3 boss cylinder in enclosure (5 mm thread depth)

ELECROW 7" 1024×600 IPS board — confirmed measurements 2026-06-18:
  Body 165×107 mm; corner tabs extend ±8.5 mm top/bottom → 165×124 mm total
  Mounting holes: 157×115 mm c-t-c  →  ±78.5 / ±57.5 mm from board centre
  LCD panel face: 165×99 mm  (= viewable 155×88 + borders L3/R7/B4/T7 mm)
  Display face to board front face: 7 mm
  Board thickness: ~1.5 mm (placeholder — unconfirmed)
  Clearance beyond board back (HDMI, USB): 9 mm
  Connector zone (port / +X side): Y = 4–60 mm from board bottom edge

Design history:
  v0 2026-06-18  flat flange + standoff bosses — test-fit print
  v1 2026-06-22  hollow wedge + hypotenuse wall + screw bars
  v2 2026-06-23  open trough (no hyp. wall) + support bars — test-fit print
  v3 2026-06-24  three-piece redesign: bezel box lid / separate enclosure /
                 minimal L-bracket wedge (no hypotenuse face needed)
"""

import math


def _try_fillet(shape, radius, edges, label=""):
    if not edges:
        print(f"  fillet({label}): no edges, skip")
        return shape
    try:
        r = shape.makeFillet(radius, edges)
        print(f"  fillet({label}): R{radius} on {len(edges)} edges OK")
        return r
    except Exception as ex:
        print(f"  fillet({label}): FAILED ({ex}), skip")
        return shape


# ─────────────────────────────────────────────────────────────────────────────
# PARAMETERS  (mm)
# ─────────────────────────────────────────────────────────────────────────────

# Board (all confirmed 2026-06-18 except BOARD_T)
BOARD_W      = 165.0
BOARD_H      = 107.0
TAB_EXT      = 8.5          # tab protrudes beyond body top/bottom
HOLE_X       = 157.0 / 2   # ±78.5 mm from board centre
HOLE_Y       = 115.0 / 2   # ±57.5 mm from board centre
BOARD_T      = 1.6          # confirmed measurement 2026-06-25

# Display
LCD_W        = 165.0        # full panel face width  (= board body width)
LCD_H        = 99.0         # full panel face height (confirmed by border math)
DISP_DEPTH   = 7.0          # panel face → board front face

# Behind board
COMP_CLEAR   = 9.0          # board back → deepest component (HDMI)

# Connector zone — port side (+X), measured from board bottom edge
CONN_Y_LOW   = 4.0
CONN_Y_HIGH  = 60.0

# Shared outer footprint
MARGIN       = 10.0
FLANGE_W     = BOARD_W + 2 * MARGIN                        # 185.0
FLANGE_H     = (BOARD_H + 2 * TAB_EXT) + 2 * MARGIN       # 144.0

# Interior pocket — board body + tabs + 1 mm clearance per side
INT_W        = BOARD_W + 2.0                               # 167.0
INT_H        = (BOARD_H + 2 * TAB_EXT) + 2.0              # 126.0

# ── Bezel ────────────────────────────────────────────────────────────────────
BEZEL_T      = 3.0          # face-plate thickness
STANDOFF_H   = DISP_DEPTH - BEZEL_T    # 4.0 mm (face-back → board front; display fits correctly)
STANDOFF_OD  = 7.0
CBORE_D      = 6.5          # M3 socket-head counterbore diameter
CBORE_H      = 2.0          # counterbore depth
BORE_D       = 3.2          # M3 clearance bore (confirmed 2026-06-25)
OPENING_W    = LCD_W + 1.0  # 166.0  (0.5 mm per side clearance)
OPENING_H    = LCD_H + 1.0  # 100.0
CORNER_R     = 5.0
TEXT_STR     = "YARDMASTER"
TEXT_SIZE    = 6.0
TEXT_RECESS  = 0.8          # depth of recessed lettering in front face
FONT         = "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf"

# ── Enclosure ────────────────────────────────────────────────────────────────
ENC_BACK_T   = 3.0          # back wall (wedge-contact face)
ENC_DEPTH    = ENC_BACK_T + COMP_CLEAR + BOARD_T   # 13.6 mm — extra BOARD_T lets rims close flush
BOSS_OD      = 7.0
BOSS_H       = COMP_CLEAR               # 9.0 mm (fills interior depth)
BOSS_BORE_D  = 2.5          # M3 tap drill (or use Ø3 mm for heat-set insert)
BOSS_BORE_H  = 5.0          # thread engagement depth

# ── Wedge ────────────────────────────────────────────────────────────────────
WEDGE_W      = 80.0
TILT_DEG     = 45.0
LEG          = FLANGE_H * math.sin(math.radians(TILT_DEG))  # ≈ 101.8 mm
WEDGE_WALL   = 3.0
CAP_T        = 4.0          # end-cap thickness
MNT_D        = 3.5          # framework wood-screw clearance (#6 / M3.5)
MNT_CBORE_D  = 7.0
MNT_CBORE_H  = 3.0
LOCK_D       = 3.2          # M3 lock-screw bore

# ── RPi3 mounting holes (bottom leg underside) ────────────────────────────
# Standard RPi3 hole pattern: 85×56mm board, holes at [3.5,61.5]×[3.5,52.5]
# Board centred on wedge width (56mm in X); centred along leg depth (85mm in Y)
RPI_BORE_D   = 3.0          # M2.5 standoff clearance bore
RPI_X0       = -56.0 / 2    # board left edge = −28.0 mm


# ─────────────────────────────────────────────────────────────────────────────
# BEZEL  — face-down print
# Z = 0  front face (on print plate)   Z increases rearward into the box
# Board centre at (0, 0) in XY
# ─────────────────────────────────────────────────────────────────────────────

def build_bezel(doc):
    import Part, FreeCAD as App

    total_z = BEZEL_T + STANDOFF_H     # 7.0 mm

    # ── outer block + corner fillets ─────────────────────────────────────────
    b = Part.makeBox(FLANGE_W, FLANGE_H, total_z,
                     App.Vector(-FLANGE_W/2, -FLANGE_H/2, 0))
    z_edges = [e for e in b.Edges
               if hasattr(e.Curve, 'Direction')
               and abs(e.Curve.Direction.z) > 0.99]
    b = _try_fillet(b, CORNER_R, z_edges, "outer corners")

    # ── interior pocket — open at rear, creates the box walls ─────────────────
    pocket = Part.makeBox(INT_W, INT_H, STANDOFF_H + 1,
                          App.Vector(-INT_W/2, -INT_H/2, BEZEL_T))
    b = b.cut(pocket)
    inner_z = [e for e in b.Edges
               if hasattr(e.Curve, 'Direction')
               and abs(e.Curve.Direction.z) > 0.99
               and abs(e.CenterOfMass.x) < FLANGE_W/2 - 0.5
               and abs(e.CenterOfMass.y) < FLANGE_H/2 - 0.5]
    b = _try_fillet(b, 1.0, inner_z, "pocket inner corners")

    # ── display opening through face plate ────────────────────────────────────
    opening = Part.makeBox(OPENING_W, OPENING_H, BEZEL_T + 2,
                           App.Vector(-OPENING_W/2, -OPENING_H/2, -1))
    b = b.cut(opening)
    front_open = [e for e in b.Edges
                  if hasattr(e.Curve, 'Direction')
                  and abs(e.Curve.Direction.z) < 0.1
                  and abs(e.CenterOfMass.z) < 0.1
                  and abs(e.CenterOfMass.x) < OPENING_W/2 + 1
                  and abs(e.CenterOfMass.y) < OPENING_H/2 + 1]
    b = _try_fillet(b, 1.0, front_open, "display opening edges")

    # ── standoffs (hollow cylinders inside the pocket at tab hole positions) ───
    for sx, sy in [(HOLE_X, HOLE_Y), (HOLE_X, -HOLE_Y),
                   (-HOLE_X, HOLE_Y), (-HOLE_X, -HOLE_Y)]:
        post = Part.makeCylinder(STANDOFF_OD/2, STANDOFF_H,
                                 App.Vector(sx, sy, BEZEL_T))
        b = b.fuse(post)

    b = b.removeSplitter()

    # ── counterbores + through-bores in face plate and standoffs ──────────────
    for sx, sy in [(HOLE_X, HOLE_Y), (HOLE_X, -HOLE_Y),
                   (-HOLE_X, HOLE_Y), (-HOLE_X, -HOLE_Y)]:
        cbore = Part.makeCylinder(CBORE_D/2, CBORE_H + 1,
                                  App.Vector(sx, sy, -1))
        bore  = Part.makeCylinder(BORE_D/2,  total_z + 2,
                                  App.Vector(sx, sy, -1))
        b = b.cut(cbore).cut(bore)

    b = b.removeSplitter()

    # ── "YARDMASTER" recessed into front face ─────────────────────────────────
    # Centred in X; positioned in top border above standoff counterbores
    y_text = (HOLE_Y + STANDOFF_OD/2 + FLANGE_H/2) / 2   # ≈ 66.5 mm
    try:
        wires = Part.makeWireString(TEXT_STR, "", FONT, TEXT_SIZE)
        faces = [Part.Face(w) for grp in wires for w in grp]
        txt = faces[0]
        for f in faces[1:]:
            txt = txt.fuse(f)
        txt = txt.extrude(App.Vector(0, 0, TEXT_RECESS))
        # Mirror X: makeWireString text reads correctly from +Z; front face is
        # viewed from -Z, so flip to avoid mirror-image text in the print.
        mat = App.Matrix()
        mat.scale(-1, 1, 1)
        txt = txt.transformGeometry(mat)
        bb  = txt.BoundBox
        txt.translate(App.Vector(
            -(bb.XMin + bb.XLength / 2),
            -(bb.YMin + bb.YLength / 2) + y_text,
            0.0))
        b = b.cut(txt)
        print(f"  text '{TEXT_STR}': recessed {TEXT_RECESS} mm OK")
    except Exception as ex:
        print(f"  text FAILED: {ex}")

    b = b.removeSplitter()
    rear_rim = [e for e in b.Edges
                if hasattr(e.Curve, 'Direction')
                and abs(e.Curve.Direction.z) < 0.1
                and abs(e.CenterOfMass.z - total_z) < 0.1
                and (abs(e.CenterOfMass.x) > INT_W/2 - 0.5
                     or abs(e.CenterOfMass.y) > INT_H/2 - 0.5)]
    b = _try_fillet(b, 0.5, rear_rim, "rear rim")
    obj = doc.addObject("Part::Feature", "Bezel")
    obj.Shape = b
    bb = b.BoundBox
    print(f"Bezel:     {b.Volume:.0f} mm³   "
          f"{bb.XLength:.1f} × {bb.YLength:.1f} × {bb.ZLength:.1f} mm")
    return b


# ─────────────────────────────────────────────────────────────────────────────
# ENCLOSURE  — back-face-down print
# Z = 0  back face / wedge-contact surface (on print plate)
# Z increases toward the board (front opening at Z = ENC_DEPTH)
# ─────────────────────────────────────────────────────────────────────────────

def build_enclosure(doc):
    import Part, FreeCAD as App

    # ── outer shell ───────────────────────────────────────────────────────────
    e = Part.makeBox(FLANGE_W, FLANGE_H, ENC_DEPTH,
                     App.Vector(-FLANGE_W/2, -FLANGE_H/2, 0))

    outer_z = [ej for ej in e.Edges
               if hasattr(ej.Curve, 'Direction')
               and abs(ej.Curve.Direction.z) > 0.99]
    e = _try_fillet(e, CORNER_R, outer_z, "outer corners")

    # ── 45° wedge-engagement chamfers on back-face top/bottom corners ────────
    # The wedge's leg ends approach at 45°; chamfer matches that angle.
    # 84mm wide (WEDGE_W + 4mm clearance), centered on X=0.
    snap_c  = WEDGE_WALL + 1.0   # chamfer leg size: 4mm (>= leg thickness 3mm)
    snap_hw = WEDGE_W / 2 + 2    # half-width of chamfer cut = 42mm
    for y_sign in (+1, -1):
        y0 = y_sign * FLANGE_H / 2
        # Triangle in YZ: corner at (y0, 0), legs snap_c in -y_sign·Y and +Z
        p0 = App.Vector(0, y0,                    0)
        p1 = App.Vector(0, y0 - y_sign * snap_c,  0)
        p2 = App.Vector(0, y0,                    snap_c)
        tri = Part.Face(Part.makePolygon([p0, p1, p2, p0]))
        prism = tri.extrude(App.Vector(snap_hw * 2, 0, 0))
        prism.translate(App.Vector(-snap_hw, 0, 0))
        e = e.cut(prism)

    # ── interior pocket — open at front ───────────────────────────────────────
    inner = Part.makeBox(INT_W, INT_H, ENC_DEPTH - ENC_BACK_T + 1,
                         App.Vector(-INT_W/2, -INT_H/2, ENC_BACK_T))
    e = e.cut(inner)
    inner_z = [ej for ej in e.Edges
               if hasattr(ej.Curve, 'Direction')
               and abs(ej.Curve.Direction.z) > 0.99
               and abs(ej.CenterOfMass.x) < FLANGE_W/2 - 0.5
               and abs(ej.CenterOfMass.y) < FLANGE_H/2 - 0.5]
    e = _try_fillet(e, 1.0, inner_z, "pocket inner corners")

    # ── connector slot in right (+X) wall — full enclosure depth ──────────────
    wall_x = FLANGE_W/2 - INT_W/2
    y_bot  = -BOARD_H / 2
    conn   = Part.makeBox(
        wall_x + 2,
        CONN_Y_HIGH - CONN_Y_LOW,
        ENC_DEPTH + 2,
        App.Vector(-FLANGE_W/2 - 1, y_bot + CONN_Y_LOW, -1))
    e = e.cut(conn)

    # ── M3 boss cylinders (back-wall inner face → front opening) ─────────────
    for bx, by in [(HOLE_X, HOLE_Y), (HOLE_X, -HOLE_Y),
                   (-HOLE_X, HOLE_Y), (-HOLE_X, -HOLE_Y)]:
        boss = Part.makeCylinder(BOSS_OD/2, BOSS_H,
                                 App.Vector(bx, by, ENC_BACK_T))
        # Blind thread bore from the front opening end
        thread = Part.makeCylinder(BOSS_BORE_D/2, BOSS_BORE_H + 1,
                                   App.Vector(bx, by, ENC_BACK_T + BOSS_H - BOSS_BORE_H))
        boss = boss.cut(thread)
        e = e.fuse(boss)

    e = e.removeSplitter()
    front_rim = [ej for ej in e.Edges
                 if hasattr(ej.Curve, 'Direction')
                 and abs(ej.Curve.Direction.z) < 0.1
                 and abs(ej.CenterOfMass.z - ENC_DEPTH) < 0.1
                 and (abs(ej.CenterOfMass.x) > INT_W/2 - 0.5
                      or abs(ej.CenterOfMass.y) > INT_H/2 - 0.5)]
    e = _try_fillet(e, 0.5, front_rim, "front face rim")
    obj = doc.addObject("Part::Feature", "Enclosure")
    obj.Shape = e
    bb = e.BoundBox
    print(f"Enclosure: {e.Volume:.0f} mm³   "
          f"{bb.XLength:.1f} × {bb.YLength:.1f} × {bb.ZLength:.1f} mm")
    return e


# ─────────────────────────────────────────────────────────────────────────────
# WEDGE  — bottom-leg-down print
# Origin O at the right-angle corner.
# +Y = into layout depth (bottom leg direction)
# +Z = up along fascia  (back leg direction)
# T  = (0, 0, LEG)   top corner — flush with fascia
# Bs = (0, LEG, 0)   deep corner — extends into layout
# ─────────────────────────────────────────────────────────────────────────────

def build_wedge(doc):
    import Part, FreeCAD as App

    W, t = WEDGE_W, WEDGE_WALL

    # ── back leg — vertical, flush against fascia / framework ─────────────────
    back = Part.makeBox(W, t, LEG, App.Vector(-W/2, 0, 0))

    # ── bottom leg — horizontal, extends into layout depth ────────────────────
    bot  = Part.makeBox(W, LEG, t, App.Vector(-W/2, 0, 0))

    w = back.fuse(bot)
    # R3mm inner V corner — MUST apply before end caps (OCCT loses this edge after cap fuse)
    v_corner = [e for e in w.Edges
                if hasattr(e.Curve, 'Direction')
                and abs(e.Curve.Direction.x) > 0.99
                and abs(e.CenterOfMass.y - t) < 0.5
                and abs(e.CenterOfMass.z - t) < 0.5]
    w = _try_fillet(w, 3.0, v_corner, "inner V corner")

    # ── triangular end caps ───────────────────────────────────────────────────
    O  = App.Vector(0, 0, 0)
    T  = App.Vector(0, 0, LEG)
    Bs = App.Vector(0, LEG, 0)
    tri = Part.Face(Part.makePolygon([O, T, Bs, O]))

    cap_neg = tri.extrude(App.Vector( CAP_T, 0, 0))
    cap_neg.translate(App.Vector(-W/2, 0, 0))
    cap_pos = tri.extrude(App.Vector(-CAP_T, 0, 0))
    cap_pos.translate(App.Vector( W/2, 0, 0))
    w = w.fuse(cap_neg).fuse(cap_pos)

    # ── framework mounting holes in back leg (counterbored) ───────────────────
    for z_frac in (0.25, 0.5, 0.75):
        z_pos = LEG * z_frac
        cb   = Part.makeCylinder(MNT_CBORE_D/2, MNT_CBORE_H + 1,
                                 App.Vector(0, -1, z_pos),
                                 App.Vector(0, 1, 0))
        bore = Part.makeCylinder(MNT_D/2, t + 2,
                                 App.Vector(0, -1, z_pos),
                                 App.Vector(0, 1, 0))
        w = w.cut(cb).cut(bore)

    # ── lock-screw bore through bottom leg near Bs end ────────────────────────
    # Enclosure edge aligns with this when fully seated; M3 screw locks slide
    lock_y = LEG - 20.0
    lock   = Part.makeCylinder(LOCK_D/2, t + 2,
                               App.Vector(0, lock_y, -1))
    w = w.cut(lock)

    # ── RPi3 mounting holes — bottom leg underside ────────────────────────────
    # 4× M2.5 clearance bores through the 3mm bottom leg
    rpi_y0 = (LEG - 85.0) / 2.0    # centres the 85mm board on the leg depth
    for hx in (3.5, 61.5):
        for hy in (3.5, 52.5):
            h = Part.makeCylinder(RPI_BORE_D / 2, t + 2,
                                  App.Vector(RPI_X0 + hx, rpi_y0 + hy, -1))
            w = w.cut(h)
    print(f"  RPi3 holes: X={[round(RPI_X0+hx,1) for hx in (3.5,61.5)]}  "
          f"Y={[round(rpi_y0+hy,1) for hy in (3.5,52.5)]}")

    w = w.removeSplitter()
    top_edge = [e for e in w.Edges
                if hasattr(e.Curve, 'Direction')
                and abs(e.Curve.Direction.x) > 0.99
                and abs(e.CenterOfMass.z - LEG) < 0.5
                and e.CenterOfMass.y < t / 2]
    w = _try_fillet(w, 1.0, top_edge, "back leg top edge")
    far_edge = [e for e in w.Edges
                if hasattr(e.Curve, 'Direction')
                and abs(e.Curve.Direction.x) > 0.99
                and abs(e.CenterOfMass.y - LEG) < 0.5
                and e.CenterOfMass.z < t / 2]
    w = _try_fillet(w, 1.0, far_edge, "bottom leg far edge")
    obj = doc.addObject("Part::Feature", "Wedge")
    obj.Shape = w
    bb = w.BoundBox
    print(f"Wedge:     {w.Volume:.0f} mm³   "
          f"{bb.XLength:.1f} × {bb.YLength:.1f} × {bb.ZLength:.1f} mm")
    return w


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def build():
    import FreeCAD as App

    doc = App.newDocument("YardmasterTerminal_v3")

    build_bezel(doc)
    build_enclosure(doc)
    build_wedge(doc)

    # Side-by-side layout for visual comparison
    gap = 30
    doc.getObject("Enclosure").Placement.Base.x = FLANGE_W + gap
    doc.getObject("Wedge").Placement.Base.x     = 2 * (FLANGE_W + gap)

    doc.recompute()
    print("v3 complete — Bezel  /  Enclosure  /  Wedge")
    return doc


if __name__ == "__main__":
    build()
