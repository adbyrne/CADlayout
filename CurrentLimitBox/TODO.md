# CurrentLimitBox TODO

## Post v1.1 Print Adjustments
- [ ] Verify tapered wedge clips grip bulb base adequately — adjust CLIP_WIDTH or taper if needed
- [ ] Check mounting post fit in terminal strip holes — adjust POST_RADIUS if needed
- [ ] Check switch cutout + chamfer tolerances — adjust if tight/loose
- [ ] Check bayonet pin notch clearance (3mm width) — adjust BULB_NOTCH_WIDTH if needed
- [ ] Verify M3 screw holes pass through cleanly

## Resolved in v1.1
- [x] Box too short in Y for comfortable wiring — increased 49→79mm
- [x] Bulb friction clips failed to print (rectangular extrusion dropped in Z) — redesigned as tapered wedges with constant-Z bottom
- [x] Switch cutout needs chamfer for actuator housing — added 2mm 45° chamfer

## Investigation
- [ ] Debug why `create_sketch` MCP tool crashes FreeCAD 1.0.2 in this project
  - Error: `AttributeError: 'Sketcher.SketchObject' object has no attribute 'Support'`
  - Works fine in `prusa-rack-conversion` project (Office/cad/) with same FreeCAD version
  - May be related to PartDesign::Body context vs standalone sketch
  - May be an MCP bridge version difference
  - Check if the Office project used `create_sketch` with or without `body_name` parameter
  - Workaround: Part primitives + boolean ops (current approach) or `execute_python` for sketch creation
