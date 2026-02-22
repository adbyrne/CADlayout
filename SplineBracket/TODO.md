# SplineBracket TODO

## Project Status: v1.0.1 — Test Print #2 In Progress (2026-02-22)

### Completed
- [x] Holder geometry: outer block, trapezoid groove, bolt hole, V-tongue
- [x] Bracket geometry: L-shape, dual full-height gusset ribs, V-groove, bolt holes, 3mm inside fillets
- [x] Export STLs for both parts
- [x] Parametric generation script (`scripts/generate_splinebracket.py`)
- [x] PrusaSlicer successful, test print #1 started (v1.0, 220mm leg)
- [x] Corrected bracket leg height 220→120mm, lower bolt hole Y=-193→Y=-93
- [x] Re-sliced and sent to printer (v1.0.1, 120mm leg)

### Awaiting Test Print Results
- [ ] Evaluate holder groove fit with spline roadbed
- [ ] Evaluate V-tongue/groove mating — check for clean engagement and anti-rotation
- [ ] Check bolt hole alignment between holder and bracket
- [ ] Assess bracket strength under spline load (gusset ribs adequate?)
- [ ] Determine optimal print orientation for bracket

### Next Session Plan
1. **Review test print** — check dimensional accuracy, fit, and strength
2. **Test assembly** — bolt spline + holder + bracket, verify anti-rotation
3. **Test module mounting** — horizontal bolt through bracket leg to module edge
4. **Iterate if needed** — adjust tolerances, groove profile, or gusset dimensions based on test fit
5. **Update version** — bump to v1.1 if changes are made after test print

### Future Considerations
- [ ] Bracket print orientation guidance (may need supports depending on orientation)
- [ ] Consider adding a second horizontal bolt hole in the vertical leg for extra security
- [ ] Parametric variant for different spline widths (currently 40mm groove bottom)
