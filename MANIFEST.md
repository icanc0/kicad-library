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
- symbols/BM02B-SRSS-TB_(LF)(SN).kicad_sym — mpn=BM02B-SRSS-TB(LF)(SN) from=? — fit: PASS — JST SH 2-pos header, mech pads 3/4 exposed; etypes→passive, value moved below
- symbols/BQ298217RUGR.kicad_sym — mpn=BQ298217RUGR from=LED-driver-board — fit: PASS — note VSS bottom-right edge. etypes set (VDD/VSS power_in, CHG/DSG gate-drive output, sense pins passive), value moved below
- symbols/BZT52C3V6_C19077397.kicad_sym — mpn=BZT52C3V6 (LCSC C19077397) from=? — fit: PASS — zener glyph; etypes→passive, ref/value moved
- symbols/CH32X035G8U6.kicad_sym — mpn=CH32X035G8U6 from=? — fit: FLAG — sole ground is the QFN28 EP and it sits at the symbol TOP pointing down (GND-down law); needs pin relocation on re-author. Renamed pin 29→EP/VSS, VDD power_in, GPIO bidirectional
- symbols/CJ3139K.kicad_sym — mpn=CJ3139K from=? — fit: PASS — P-FET glyph with body diode + gate ESD internals shown; etypes→passive, value moved below
- symbols/CM4IO.kicad_sym — mpn=multi (RPi CM4IO reference pack: ComputeModule4-CM4, HDMI_A_1.4, MagJack, PCIe-x1, AP2553W6, AP64351, EMC2301, FSUSB42MX, RT9742SNGV, TPD4EUSB30, 74LVC1G07, USB_67298-4090, Barrel_Jack) from=cm4-carrier — fit: PASS — reference-design import; MagJack/HDMI/TPD4E draw full internals. Fixed: AP2553W6 GND power_out→power_in, TPD4EUSB30 GND(8)→power_in, RT9742 OUT→power_out. Notes: 8 sub-symbols carry no Footprint property (board-local mapping); AP64351 FB/SS/COMP typed input can false-ERC on divider/cap-only nets (left as ref-design)
- symbols/CUS10S40_H3F.kicad_sym — mpn=CUS10S40,H3F from=? — fit: PASS — diode glyph; etypes→passive, ref/value moved
- symbols/DRV8841PWPR.kicad_sym — mpn=DRV8841PWPR from=varifocal-motherboard — fit: PASS — note GND(28) top-right, GND(14) bottom-left is correct. Full etype rationalization (VMA/VMB/GND power_in, xOUT output, V3 power_out, nFLT open_collector, logic ins input, CP/ISEN/VREF passive, EP passive)
- symbols/ESP32-S3(FN8).kicad_sym — mpn=ESP32-S3FN8 from=? — fit: PASS — power top-left, SPI group bottom-right, EP bottom. 57-pin etype backfill (VDD3P3*/VDDA/VDD_SPI power_in, GPIO bidirectional, XTAL/straps/LNA passive, EP passive)
- symbols/FUSB302BUCX.kicad_sym — mpn=FUSB302BUCX from=varifocal-motherboard — fit: PASS — etypes set (VDD/GND power_in, CC/I2C bidirectional, INT_N open_collector, VBUS/VCONN passive), value moved below
