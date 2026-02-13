# CurrentLimitBox TODO

## Project Status: Complete (v1.2)

All items resolved. Bulb secured by cable tie; no further clip adjustments needed.

## Resolved in v1.2
- [x] Bulb clips eliminated — cable tie used instead

## Resolved in v1.1
- [x] Box too short in Y for comfortable wiring — increased 49→79mm
- [x] Bulb friction clips failed to print (rectangular extrusion dropped in Z) — redesigned as tapered wedges with constant-Z bottom
- [x] Switch cutout needs chamfer for actuator housing — added 2mm 45° chamfer

## Investigation (deferred)
- [ ] Debug why `create_sketch` MCP tool crashes FreeCAD 1.0.2 in this project
  - Error: `AttributeError: 'Sketcher.SketchObject' object has no attribute 'Support'`
  - Workaround: Part primitives + boolean ops (current approach)
