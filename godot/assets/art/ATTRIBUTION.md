# Credits: `pc_sheet.png` (the courier sheet used by both Assignment 7 clips)

| Item | Value |
|---|---|
| File | `godot/assets/art/pc_sheet.png`, 320 × 32 px, SHA-256 `7e13d91efeba2d60a43a6212b51aa5a7ad12054fa1073bec4803ad61d89913c9`, unchanged since `5d1cc9b` (29 September 2026) |
| Import settings | `godot/assets/art/pc_sheet.png.import` (Godot-generated) |
| Source | Generated for this project in Assignment 2 (asset ART-PC-01), not a found or course sheet |
| Model | [black-forest-labs/FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell), revision `741f7c3`, run locally with mflux (`SOURCES.md`) |
| Licence | Apache-2.0, checked on the model page on 13 November 2026. It allows a public repository and a published film; no credit line is required, and this file credits the model anyway |
| Prompts and settings | every run in `gen/log/ART-PC-01/`; the chosen frames, palette and processing in `gen/mappings/ART-PC-01.json`, applied by `gen/art_process.py`; the review in `ASSET-LOG.md` (section ART-PC-01) |
| Editable source | the generation log and mapping above. The raw model outputs (`gen/raw/`) are not committed; `gen/reproduce.py` regenerates any logged run |
| Slicing used in Assignment 7 | 32 × 32 px cells, 10 columns × 1 row, no padding; frame order 0 turn_front, 1 idle, 2 walk_contact, 3 walk_passing, 4 cast, 5 hurt, 6 levelup, 7 sunflare, 8 defeat, 9 victory |
| Derivative use | none: the dash rig draws region rectangles of cell 2 at run time; no edited copy of the sheet exists |
| Named artists, brands, characters | none in the prompts (Assignment 2 rule; `gen/log/ART-PC-01/`) |
