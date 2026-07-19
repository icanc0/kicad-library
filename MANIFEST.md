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
- symbols/HT7533-1_C14289.kicad_sym — mpn=HT7533-1 (LCSC C14289) from=3v3-LDO-add — fit: PASS — note GND right-bottom edge not bottom. etypes (Vin power_in, Vout power_out, GND power_in), value moved below
- symbols/ICM-42670-P.kicad_sym — mpn=ICM-42670-P from=? — fit: PASS — note GND left-mid. etypes set (VDD/VDDIO/GND power_in, I2C/SPI bidirectional, INT1 output); RESV pins left passive (datasheet tie/float call not guessed)
- symbols/ICM-42688-P.kicad_sym — mpn=ICM-42688-P from=? — fit: FLAG — body ~66x69 mm for 14 pins (body∝pins law; package-style 4-side pin layout, legacy pins-at-top-level structure); needs compact re-author. VDD/VDDIO/GND→power_in applied
- symbols/isaac-anime-girl-oc.kicad_sym — non-part: keep (owner) — art, not graded
- symbols/KF1027B-04P-G00-DFT-01B.kicad_sym — mpn=KF1027B-04P-G00-DFT-01B from=? — fit: PASS — proper 4-slider glyphs + ON label; etypes input→passive, refdes U→SW, value moved below
- symbols/LP3320B6F.kicad_sym — mpn=LP3320B6F from=LED-driver-board — fit: PASS — note GND left row-2. etypes (VIN/GND power_in, NC no_connect, LX/FB/EN passive), value moved below
- symbols/MC33269DR2-3_3.kicad_sym — mpn=MC33269DR2-3.3 from=? — fit: PASS — GND/ADJ bottom. Deleted baked decorative text "comment"; OUT(2) power_out + stacked 3/6/7 passive (single-driver rule), NC→no_connect, value moved below
- symbols/MCP1603T_180I_OS.kicad_sym — mpn=MCP1603T-180I/OS from=1v8-buck — fit: PASS — GND bottom; etypes (VIN/GND power_in, LX/VFB/SHDN passive)
- symbols/MCU_RaspberryPi_RP2350.kicad_sym — mpn=RP2350A from=? — fit: PASS — official-style QFN-60: power rails top, GND(61) bottom, no changes
- symbols/NCP167BMX330TBG.kicad_sym — mpn=NCP167BMX330TBG from=LED-driver-board — fit: FLAG — sides mirrored: OUT on left, IN/EN on right (outputs-right law); needs re-side on re-author. etypes (IN/GND power_in, OUT power_out, EN/EPAD passive), value moved below
- symbols/NH-B1515RGBA-HF.kicad_sym — mpn=NH-B1515RGBA-HF from=? — fit: PASS — RGB LED glyphs shown; etypes→passive, refdes U→D, value moved below
- symbols/NTMFS5C410NLT1G.kicad_sym — mpn=NTMFS5C410NLT1G from=LED-driver-board — fit: FLAG — power NMOS drawn as plain box (charter rule 2: "mosfets don't look like mosfets"); re-author with FET glyph, S=1-3 G=4 D=5 on the DFN-5 land. etypes→passive, value moved below
- symbols/poka-yoke_rxtx.kicad_sym — mpn=n/a (owner utility) from=? — fit: PASS — RX/TX cross-over poka-yoke, in/out typed correctly
- symbols/PZ254-2-04-WS.kicad_sym — mpn=PZ254-2-04-WS from=LED-driver-board — fit: PASS — 2x4 header; etypes→passive, refdes U→J, value moved below
- symbols/PZ254-2-08-WS.kicad_sym — mpn=PZ254-2-08-WS from=? — fit: PASS — 2x8 header; etypes→passive, refdes U→J, value moved below
- symbols/RP2040.kicad_sym — mpn=RP2040 from=? — fit: PASS — official-style: stacked visible IOVDD/DVDD power_in pins (stock convention), GND(57) bottom, no changes
- symbols/SPH252012HR24MT.kicad_sym — mpn=SPH252012HR24MT (LCSC C370416) from=? — fit: PASS — REPAIRED: same JLC2KiCad +152.4 mm arc-offset bug as BDHH; coil translated onto pins, etypes→passive
- symbols/TC2050-IDC.kicad_sym — mpn=TC2050-IDC from=? — fit: PASS — Tag-Connect 2x5, clean, no changes
- symbols/TMAG5273A2QDBVR.kicad_sym — mpn=TMAG5273A2QDBVR from=LED-driver-board — fit: FLAG — GND(2) sits above VCC(4) across facing sides (power-up/GND-down); needs pin re-side on re-author. etypes (GND/VCC power_in, I2C bidirectional, INT open_collector, GND(TEST) passive), value moved below
- symbols/TP4065.kicad_sym — mpn=TP4065 from=? — fit: PASS — VCC top, PROG bottom; note GND left-mid. etypes (VCC/GND power_in, CHRG open_collector, BAT/PROG passive)
