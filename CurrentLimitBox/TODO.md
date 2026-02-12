# CurrentLimitBox TODO

## Post-Print Adjustments
- [ ] Check bulb clip friction fit - adjust CLIP_GAP and CLIP_THICKNESS if needed
- [ ] Check mounting post fit in terminal strip holes - adjust POST_RADIUS if needed
- [ ] Check switch cutout tolerances (11.8x6.3mm) - adjust if tight/loose
- [ ] Check bayonet pin notch clearance (3mm width) - adjust BULB_NOTCH_WIDTH if needed
- [ ] Verify M3 screw holes pass through cleanly

## Investigation
- [ ] Debug why `create_sketch` MCP tool crashes FreeCAD 1.0.2 in this project
  - Error: `AttributeError: 'Sketcher.SketchObject' object has no attribute 'Support'`
  - Works fine in `prusa-rack-conversion` project (Office/cad/) with same FreeCAD version
  - May be related to PartDesign::Body context vs standalone sketch
  - May be an MCP bridge version difference
  - Check if the Office project used `create_sketch` with or without `body_name` parameter
  - Workaround: Part primitives + boolean ops (current approach) or `execute_python` for sketch creation
