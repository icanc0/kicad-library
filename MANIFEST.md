# MANIFEST — provenance + fit notes, one line per part

Format (matches `engine.central promote` appends):
`- <paths> — mpn=<MPN> from=<source board|?> — fit: <note> [— <extra>]`

Fit-pass backfill audit 2026-07-19 (librarian): every pre-rule symbol rendered + reviewed
against the owner's laws (power-up/GND-down, body∝pins, internals-not-lazy-box, text
legibility, ERC-correct pin etypes). `fit: PASS` may carry notes; `fit: FLAG` needs a
re-author (see note). Mechanical fixes recorded per line.

- symbols/1N5819WS.kicad_sym — mpn=1N5819WS from=? — fit: PASS — diode glyph; etypes→passive, ref/value moved clear of glyph
- symbols/218-2LPSTR.kicad_sym — mpn=218-2LPSTR from=? — fit: FLAG — DIP switch drawn as plain box, no switch elements (KF1027B in this lib shows the standard); redraw wanted. etypes input→passive, refdes U→SW, value moved below
- symbols/2450AT18A100E.kicad_sym — mpn=2450AT18A100E from=? — fit: PASS — chip antenna, inline vertical glyph (feed pin 1 bottom); etypes→passive, ref/value moved off the pins
- symbols/245863050104829+.kicad_sym — mpn=245863050104829+ from=NS-display-mezzanine — fit: PASS — 56-pin FPC connector, MP1-6 mech pads exposed (full pad set). FINDING (high): second symbol `245863050104829+_missing_gnd` in this file is a stale bad copy pointing at the ATTICKED footprint `footprints:245863050104829_missing pads` (broken link) — never place it; owner should attic the symbol copy too
- symbols/A3901SEJTR-T.kicad_sym — mpn=A3901SEJTR-T from=? — fit: PASS — dual H-bridge, box OK; note GND sits mid-left not bottom. etypes set (GND/VBB power_in, IN input, OUT output, PAD passive), value moved below
- symbols/ABM8-272-T3_ABR.kicad_sym — mpn=ABM8-272-T3 from=? — fit: PASS — crystal glyph, cramped but legible; etypes→passive
- symbols/AMS1117-3.3.kicad_sym — mpn=AMS1117-3.3 from=? — fit: PASS — note GND/ADJ on right edge not bottom. VIN input→power_in, VOUT output→power_out (rail no longer needs PWR_FLAG — consumers re-check ERC on submodule bump)
- symbols/AXP2101.kicad_sym — mpn=AXP2101 from=? — fit: PASS — exemplary: VIN group top-left, LDO/DCDC outs right, GND+EP bottom. 41-pin etype backfill (supplies power_in, LDO outs power_out, LX/FB passive, IRQ/CHGLED open_collector)
- symbols/B5817WS_C7420329.kicad_sym — mpn=B5817WS (LCSC C7420329) from=? — fit: PASS — diode glyph; etypes→passive, ref/value moved
- symbols/BDHH002016101R0MDB.kicad_sym — mpn=BDHH002016101R0MDB (LCSC C2913752) from=? — fit: PASS — REPAIRED: JLC2KiCad import bug had the coil arcs +152.4 mm above the pins (glyph floated 6 in off-body); arcs translated onto the pins, etypes→passive, refdes U→FB
