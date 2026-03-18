# SwitchToggle v2 — Improvement Plan

*Prepared: 2026-03-16. Updated: 2026-03-18 to reflect v6 baseline.*
*Assumes v6 test print is mechanically acceptable.*
*Prioritized: High = functional improvement; Medium = quality/polish; Low = nice-to-have.*

## Completed in v5/v6 (not in scope for v2)

| Item | Resolved |
|------|---------|
| Lever width matches post gap | v5: 20mm wide, 1mm clearance each side of 22mm gap |
| Cylinder fulcrum | v5: Ø8mm cylinder runs X-axis through lever center (Y=17.5) |
| Single rod slot | v5: 5×14mm vertical slot replaces dual round holes |
| T-slot rod connection | v5: Pre-assembled stud+nut slides in from Y=0 edge; nut captive |
| Rod slot in FrontPlate | v5: Matches shell slot (5×14mm, X=22.5..27.5, Y=8..22) |
| Print orientation note | v5: Lever must flip 180° around X-axis in PrusaSlicer |
| LED diagonal placement | v6: Top LED left wall Y=38, bottom LED right wall Y=12 (7mm M3 clearance) |

---

---

## 1. JST-XH Connector Pocket  ★ High

**Problem:** v1 has a bare 6mm cable pass-through hole in the shell back wall. The
JST-XH socket floats inside the shell on the cable, can pull through the hole, and
is fiddly to reconnect without opening the assembly.

**Solution:** Recess a pocket in the shell back wall that captures the JST-XH 3-pin
receptacle body. Socket faces outward (flush or slightly proud of back face); plug
mates from the fascia side. Cable strain is carried by the housing, not the solder joints.

**Action:**
- Measure PEBA JST-XH 3-pin socket body dimensions (length × width × height)
- Replace the 6mm cable hole with a rectangular pocket + a slot for the cable exit
- Add a small friction ledge or tab to retain the socket body
- Route holes for the three LED wires from socket pocket to LED holes inside shell

---

## 2. LED Retention Features  ★ High

**Problem:** v1 LED holes are Ø5.2mm — LEDs drop in but have nothing to hold them.
Currently relies on glue after positioning, which makes removal impossible.

**Solution A — Snap rim:** Reduce LED hole to Ø4.8mm with a 0.4mm inward lip at the
outer surface. LEDs snap in with light press and are retained without glue.

**Solution B — Bezel recess:** Keep Ø5.2mm hole, add a 0.5mm-deep × 7mm-dia counterbore
on the outer face. LED flange seats in counterbore; thin bead of glue in counterbore
groove (not in hole) locks it flush.

*Recommendation: Solution B — easier to print cleanly, still allows replacement.*

---

## 3. Lever Stop Nubs  ★ Deferred

**Problem:** v1 lever has no mechanical travel limit.

**Status:** Deferred pending field testing. The BluePoint internal switch mechanism
provides a positive detent and holds position — no additional stop is needed until
real-world operation confirms otherwise. If added, nubs must be symmetric at ±θ° on
the FrontPlate face so the module works correctly in both normal and flipped orientation.

---

## 4. Thumb Pad Ergonomics  ★ Deferred

**Problem:** Lever upper arm has no grip texture.

**Status:** Deferred pending field testing. If added, ribs must be placed on BOTH the
upper arm AND the lower arm (above T-slot) at mirror positions from the pivot center —
the module can be installed flipped 180° on the fascia to reverse N/R sense, which
requires both arms to be equally ergonomic. The BluePoint detent provides sufficient
tactile feedback for now.

---

## 5. Shell-to-FrontPlate Snap Tabs  ★ Medium

**Problem:** v1 shell + FrontPlate are glued with CA after wiring. Glue is permanent —
if an LED fails or wiring needs rework, the assembly cannot be opened without destruction.

**Solution:** Replace (or supplement) CA glue with snap tabs: four flexible tabs on
the shell front rim that clip over the plate edge. Tab geometry: 1mm wide × 3mm tall
cantilevered beam with a 0.5mm inward hook.

**Consideration:** PLA snap tabs are stiff; PETG preferred for this feature. If printing
in PLA, tabs may need to be designed as press-fit friction clips rather than snap hooks.

**Fallback:** Keep alignment pegs and add two M2 screws at mid-edges (top/bottom) to
allow screw-in assembly that can be opened.

---

## 6. Fascia-Mount Collet  ★ Medium

**Problem:** v1 uses 4×M3 corner screws — installer must drill 4 holes in fascia and
access all 4 screws from the front face. Crowded with lever in the way.

**Solution:** A printed collet that:
1. Inserts through a single round hole (≈30mm dia) in the fascia from behind
2. Has a flange that presses against the fascia back face
3. Shell mounts onto collet front face; printed thumb nut or quarter-turn tab
   on collet barrel threads/locks to clamp everything

**Variants to explore:**
- **Threaded collet + printed nut:** Most secure; needs thread profile in CAD
- **Quarter-turn bayonet:** Collet has 2 pins; shell has matching L-slots; push + rotate to lock
- **Push-clip tab:** Collet barrel has springy clip wings that splay behind fascia

*This is a significant design change — treat as a separate sub-project after v2 fit/function confirmed.*

---

## 7. Back Face Orientation Labels  ★ Medium

**Problem:** v1 back face has two identical 5mm rod holes at Y=15 and Y=35 with no
labeling. Installer must remember/document which hole to use for their layout's
normal-route orientation.

**Solution:** Emboss small text or arrows directly into the shell back face:
- "N" (or "↑") above the Y=35 hole
- Relief depth 0.4mm — visible without affecting function

**Action:** Add embossed text geometry to `build_shell()` using `Part.makeBox` letter
profiles, or investigate FreeCAD text-to-shape workflow.

*Alternative:* Laser-engrave or hand-label with paint pen after printing — simpler than CAD text.

---

## 8. Cable Slot Entry Chamfer  ★ Deferred

**Problem:** The 2-56 rod must be threaded into the T-slot during installation.

**Status:** Deferred pending field testing. Assembly experience will confirm whether
the current T-slot entry is awkward enough to warrant a chamfer.

---

## 9. Wire Management in Shell  ★ Low

**Problem:** The shell interior (46×46×10mm) has no features. LED wires will be loose
inside and may snag when the lever moves.

**Solution:** Add two small cable clips (1.5mm gap, 2mm tall snap tab) on the interior
side walls near each LED hole, to route the LED wires against the shell walls and away
from the lever path.

---

## Summary Table

| # | Item | Priority | Part(s) Affected | Complexity |
|---|------|----------|-----------------|------------|
| 1 | JST-XH connector pocket | High | Shell | Medium |
| 2 | LED retention (bezel) | High | Shell | Low |
| 3 | Lever stop nubs | Deferred | FrontPlate | Low |
| 4 | Thumb pad ribs | Deferred | Lever | Low |
| 5 | Snap tabs or M2 screws | Medium | Shell + FrontPlate | Medium |
| 6 | Fascia mount collet | Medium | New part | High |
| 7 | Back face orientation labels | Medium | Shell | Low |
| 8 | Cable slot chamfer | Deferred | Lever | Low |
| 9 | Wire management clips | Low | Shell | Low |

---

## Active v2 Scope

| Priority | Item | Status |
|----------|------|--------|
| High | 1 — JST-XH connector pocket | Blocked: measure PEBA 3-pin socket body first |
| High | 2 — LED retention bezel | Ready to implement |
| Medium | 5 — Snap tabs / M2 screws | Stretch goal |
| Low | 9 — Wire management clips | Optional filler |
| Separate | 6 — Fascia mount collet | Separate sub-project |
| Deferred | 3, 4, 8 | Pending field test of v7 print |
| Skipped | 7 — Orientation labels | Paint pen preferred over CAD text |

**Next action:** Implement item 2 (LED retention bezel). Then measure JST-XH socket
body to unblock item 1.

---

*This plan is a starting point — review after v5 test print results are confirmed.*
