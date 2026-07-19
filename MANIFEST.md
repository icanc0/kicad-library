# MANIFEST — provenance + fit notes, one line per part

Format (matches `engine.central promote` appends):
`- <paths> — mpn=<MPN> from=<source board|?> — fit: <note> [— <extra>]`

Fit-pass backfill audit 2026-07-19 (librarian): every pre-rule symbol rendered + reviewed
against the owner's laws (power-up/GND-down, body∝pins, internals-not-lazy-box, text
legibility, ERC-correct pin etypes). `fit: PASS` may carry notes; `fit: FLAG` needs a
re-author (see note). Mechanical fixes recorded per line.

- symbols/1N5819WS.kicad_sym — mpn=1N5819WS from=? — fit: PASS — diode glyph; etypes→passive, ref/value moved clear of glyph
- symbols/218-2LPSTR.kicad_sym — mpn=218-2LPSTR from=? — fit: PASS — re-authored to the KF1027B house DIP standard: 2 vertical slider glyphs + ON label, pins restacked top/bottom (position columns 1↔4, 2↔3), pin names hidden. etypes input→passive, refdes U→SW (audit)
- symbols/2450AT18A100E.kicad_sym — mpn=2450AT18A100E from=? — fit: PASS — chip antenna, inline vertical glyph (feed pin 1 bottom); etypes→passive, ref/value moved off the pins
- symbols/245863050104829+.kicad_sym — mpn=245863050104829+ from=NS-display-mezzanine — fit: PASS — 56-pin FPC connector, MP1-6 mech pads exposed (full pad set). RESOLVED (librarian 2026-07-19): stale second symbol `245863050104829+_missing_gnd` (footprint link to the atticked `footprints:245863050104829_missing pads`) moved out to attic/245863050104829+_missing_gnd.kicad_sym; healthy symbol untouched — never place the attic copy
- symbols/A3901SEJTR-T.kicad_sym — mpn=A3901SEJTR-T from=? — fit: PASS — dual H-bridge, box OK; note GND sits mid-left not bottom. etypes set (GND/VBB power_in, IN input, OUT output, PAD passive), value moved below
- symbols/ABM8-272-T3_ABR.kicad_sym — mpn=ABM8-272-T3 from=? — fit: PASS — crystal glyph, cramped but legible; etypes→passive
- symbols/AMS1117-3.3.kicad_sym — mpn=AMS1117-3.3 from=? — fit: PASS — note GND/ADJ on right edge not bottom. VIN input→power_in, VOUT output→power_out (rail no longer needs PWR_FLAG — consumers re-check ERC on submodule bump)
- symbols/AXP2101.kicad_sym — mpn=AXP2101 from=? — fit: PASS — exemplary: VIN group top-left, LDO/DCDC outs right, GND+EP bottom. 41-pin etype backfill (supplies power_in, LDO outs power_out, LX/FB passive, IRQ/CHGLED open_collector)
- symbols/B5817WS_C7420329.kicad_sym — mpn=B5817WS (LCSC C7420329) from=? — fit: PASS — diode glyph; etypes→passive, ref/value moved
- symbols/BDHH002016101R0MDB.kicad_sym — mpn=BDHH002016101R0MDB (LCSC C2913752) from=? — fit: PASS — REPAIRED: JLC2KiCad import bug had the coil arcs +152.4 mm above the pins (glyph floated 6 in off-body); arcs translated onto the pins, etypes→passive, refdes U→FB
- symbols/BM02B-SRSS-TB_(LF)(SN).kicad_sym — mpn=BM02B-SRSS-TB(LF)(SN) from=? — fit: PASS — JST SH 2-pos header, mech pads 3/4 exposed; etypes→passive, value moved below
- symbols/BQ298217RUGR.kicad_sym — mpn=BQ298217RUGR from=LED-driver-board — fit: PASS — note VSS bottom-right edge. etypes set (VDD/VSS power_in, CHG/DSG gate-drive output, sense pins passive), value moved below
- symbols/BZT52C3V6_C19077397.kicad_sym — mpn=BZT52C3V6 (LCSC C19077397) from=? — fit: PASS — zener glyph; etypes→passive, ref/value moved
- symbols/CH32X035G8U6.kicad_sym — mpn=CH32X035G8U6 from=? — fit: PASS — re-authored EP/VSS(29) top→bottom edge (GND-down), sited clear of the long GPIO name rows; all 29 pins verified on 1.27 mm grid. Renamed pin 29→EP/VSS, VDD power_in, GPIO bidirectional (audit)
- symbols/CJ3139K.kicad_sym — mpn=CJ3139K from=? — fit: PASS — P-FET glyph with body diode + gate ESD internals shown; etypes→passive, value moved below
- symbols/CM4IO.kicad_sym — mpn=multi (RPi CM4IO reference pack: ComputeModule4-CM4, HDMI_A_1.4, MagJack, PCIe-x1, AP2553W6, AP64351, EMC2301, FSUSB42MX, RT9742SNGV, TPD4EUSB30, 74LVC1G07, USB_67298-4090, Barrel_Jack) from=cm4-carrier — fit: PASS — reference-design import; MagJack/HDMI/TPD4E draw full internals. Fixed: AP2553W6 GND power_out→power_in, TPD4EUSB30 GND(8)→power_in, RT9742 OUT→power_out. Notes: 8 sub-symbols carry no Footprint property (board-local mapping); AP64351 FB/SS/COMP typed input can false-ERC on divider/cap-only nets (left as ref-design)
- symbols/CUS10S40_H3F.kicad_sym — mpn=CUS10S40,H3F from=? — fit: PASS — diode glyph; etypes→passive, ref/value moved
- symbols/DRV8841PWPR.kicad_sym — mpn=DRV8841PWPR from=varifocal-motherboard — fit: PASS — note GND(28) top-right, GND(14) bottom-left is correct. Full etype rationalization (VMA/VMB/GND power_in, xOUT output, V3 power_out, nFLT open_collector, logic ins input, CP/ISEN/VREF passive, EP passive)
- symbols/ESP32-S3(FN8).kicad_sym — mpn=ESP32-S3FN8 from=? — fit: PASS — power top-left, SPI group bottom-right, EP bottom. 57-pin etype backfill (VDD3P3*/VDDA/VDD_SPI power_in, GPIO bidirectional, XTAL/straps/LNA passive, EP passive)
- symbols/FUSB302BUCX.kicad_sym — mpn=FUSB302BUCX from=varifocal-motherboard — fit: PASS — etypes set (VDD/GND power_in, CC/I2C bidirectional, INT_N open_collector, VBUS/VCONN passive), value moved below
- symbols/HT7533-1_C14289.kicad_sym — mpn=HT7533-1 (LCSC C14289) from=3v3-LDO-add — fit: PASS — note GND right-bottom edge not bottom. etypes (Vin power_in, Vout power_out, GND power_in), value moved below
- symbols/ICM-42670-P.kicad_sym — mpn=ICM-42670-P from=? — fit: PASS — note GND left-mid. etypes set (VDD/VDDIO/GND power_in, I2C/SPI bidirectional, INT1 output); RESV pins left passive (datasheet tie/float call not guessed)
- symbols/ICM-42688-P.kicad_sym — mpn=ICM-42688-P from=? — fit: PASS — re-authored compact 36x23 mm body, functional grouping: VDD/VDDIO top-left, SPI/I2C bus left (CS/SCLK/SDI/SDO order), INT1/INT2 top-right, RESV_1-5 banked bottom-right, sole GND bottom-center; proper _0_1 sub-symbol structure. VDD/VDDIO/GND→power_in (audit)
- symbols/isaac-anime-girl-oc.kicad_sym — non-part: keep (owner) — art, not graded
- symbols/KF1027B-04P-G00-DFT-01B.kicad_sym — mpn=KF1027B-04P-G00-DFT-01B from=? — fit: PASS — proper 4-slider glyphs + ON label; etypes input→passive, refdes U→SW, value moved below
- symbols/LP3320B6F.kicad_sym — mpn=LP3320B6F from=LED-driver-board — fit: PASS — note GND left row-2. etypes (VIN/GND power_in, NC no_connect, LX/FB/EN passive), value moved below
- symbols/MC33269DR2-3_3.kicad_sym — mpn=MC33269DR2-3.3 from=? — fit: PASS — GND/ADJ bottom. Deleted baked decorative text "comment"; OUT(2) power_out + stacked 3/6/7 passive (single-driver rule), NC→no_connect, value moved below
- symbols/MCP1603T_180I_OS.kicad_sym — mpn=MCP1603T-180I/OS from=1v8-buck — fit: PASS — GND bottom; etypes (VIN/GND power_in, LX/VFB/SHDN passive)
- symbols/MCU_RaspberryPi_RP2350.kicad_sym — mpn=RP2350A from=? — fit: PASS — official-style QFN-60: power rails top, GND(61) bottom, no changes
- symbols/NCP167BMX330TBG.kicad_sym — mpn=NCP167BMX330TBG from=LED-driver-board — fit: PASS — re-authored to inputs-left/outputs-right: IN(4)/EN(3) left, OUT(1) right, GND(2)+EPAD(5) bottom edge; stale pin-1 dot removed. etypes (IN/GND power_in, OUT power_out, EN/EPAD passive) (audit)
- symbols/NH-B1515RGBA-HF.kicad_sym — mpn=NH-B1515RGBA-HF from=? — fit: PASS — RGB LED glyphs shown; etypes→passive, refdes U→D, value moved below
- symbols/NTMFS5C410NLT1G.kicad_sym — mpn=NTMFS5C410NLT1G from=LED-driver-board — fit: PASS — re-authored as stock Transistor_FET NMOS glyph (gate left, drain up, source down, body diode); DFN-5 land mapped G=4 D=5, S=1-3 stacked on the source pin (2/3 hidden per stock convention). etypes→passive (audit)
- symbols/poka-yoke_rxtx.kicad_sym — mpn=n/a (owner utility) from=? — fit: PASS — RX/TX cross-over poka-yoke, in/out typed correctly
- symbols/PZ254-2-04-WS.kicad_sym — mpn=PZ254-2-04-WS from=LED-driver-board — fit: PASS — 2x4 header; etypes→passive, refdes U→J, value moved below
- symbols/PZ254-2-08-WS.kicad_sym — mpn=PZ254-2-08-WS from=? — fit: PASS — 2x8 header; etypes→passive, refdes U→J, value moved below
- symbols/RP2040.kicad_sym — mpn=RP2040 from=? — fit: PASS — official-style: stacked visible IOVDD/DVDD power_in pins (stock convention), GND(57) bottom, no changes
- symbols/SPH252012HR24MT.kicad_sym — mpn=SPH252012HR24MT (LCSC C370416) from=? — fit: PASS — REPAIRED: same JLC2KiCad +152.4 mm arc-offset bug as BDHH; coil translated onto pins, etypes→passive
- symbols/TC2050-IDC.kicad_sym — mpn=TC2050-IDC from=? — fit: PASS — Tag-Connect 2x5, clean, no changes
- symbols/TMAG5273A2QDBVR.kicad_sym — mpn=TMAG5273A2QDBVR from=LED-driver-board — fit: PASS — re-authored pin re-side: VCC(4) top-left, SCL/SDA pair left, INT#(5) right, GND(2)+GND(TEST)(3) bottom edge (power-up/GND-down); stale pin-1 dot removed. etypes (GND/VCC power_in, I2C bidirectional, INT open_collector, GND(TEST) passive) (audit)
- symbols/TP4065.kicad_sym — mpn=TP4065 from=? — fit: PASS — VCC top, PROG bottom; note GND left-mid. etypes (VCC/GND power_in, CHRG open_collector, BAT/PROG passive)
- symbols/TPS65132WRVCR_C2876379.kicad_sym — mpn=TPS65132WRVCR (LCSC C2876379) from=TPS65132-add — fit: PASS — VIN top-left, outs right, PGND/AGND/EP all bottom. 21-pin etypes (grounds power_in, OUTP/OUTN power_out with stacked twin passive, SW/CFLY/REG passive, I2C bidirectional)
- symbols/TS-1187A-B-A-B.kicad_sym — mpn=TS-1187A-B-A-B from=? — fit: PASS — tact switch glyph; refdes U→SW, value moved below
- symbols/TSSOP_0104PWR_TEX.kicad_sym — mpn=TXU0104PWR from=? — fit: PASS — NC pins properly no_connect; note VCCA/VCCB mid-left, GND left-bottom. GND power_out→power_in, OE→passive
- symbols/TZ1269D.kicad_sym — mpn=TZ1269D from=? — fit: PASS — zener array internals shown; note GND top-left. GND input→power_in (was ERC-poison), I/O→passive, value moved below
- symbols/USB-TYPE-C-018.kicad_sym — mpn=TYPE-C-018 (KH-TYPE-C-018) from=? — fit: PASS — 16P+4 shell receptacle, physical A/B column layout; all pins→passive (connector law), refdes U→J, value moved off the DP/DN rows
- symbols/W25Q128JVSIQTR.kicad_sym — mpn=W25Q128JVSIQ from=? — fit: PASS — etypes (VCC/GND power_in, CS/CLK input, IO bidirectional), value moved below
- symbols/Wago-2060-452-998-404.kicad_sym — mpn=2060-452/998-404 from=wago-add — fit: PASS — contact glyphs; etypes→passive (both body styles), value moved fully below box
- symbols/WPN252012H2R2MT.kicad_sym — mpn=WPN252012H2R2MT from=? — fit: PASS — coil glyph correct (healthy twin of the two repaired inductors); etypes→passive
- symbols/X322512MSB4SI.kicad_sym — mpn=X322512MSB4SI from=? — fit: PASS — 32.768k crystal, case GNDs; note GND(4) top-left. etypes→passive, value moved below
- symbols/XF2M-2215-1A.kicad_sym — mpn=XF2M-2215-1A from=iphone-x-shim — fit: PASS — 22-pin FPC + case pins 23/24 exposed (full pad set), clean single column, no changes
- symbols/XSON8_XH_2x3x0p4_WIN.kicad_sym — mpn=W25Q32RVXHJQ TR from=? — fit: PASS — VCC top / VSS bottom correct. REPAIRED: VSS pins were off the 1.27 grid (y=-24.765, silent-open trap) — snapped to -25.4 with length compensated; VSS power_out→power_in

Central-intake wave 2026-07-19 (librarian): cross-board dedupe + early-board candidates.
Every row below = rendered + LOOKed before promotion; pin numbers/names/etypes preserved
exactly unless the fix was geometry/text (noted per row).

- symbols/SY6280AAC.kicad_sym — mpn=SY6280AAC from=wristcam-v2 — fit: PASS — load switch, IN/OUT power corners, GND bottom, EN/ISET grouped left; byte-identical twin on foxjig; stardeck (input-typed ISET/EN) and headrig (pin 3 renamed ILIM) variants passed over
- symbols/TPD4E05U06.kicad_sym — mpn=TPD4E05U06DQAR from=cm5-carrier-v2 — fit: PASS — TVS-array internals drawn, flow-through D1/D2 left-right, GND 3+8 stacked bottom (8 hidden); NC etype 'free' preserved; symbol renamed TPD4E05U06DQA→TPD4E05U06; beats the plain-box foxjig/stardeck/headrig copies
- symbols/MT2492.kicad_sym — mpn=MT2492 from=iphone-x-shim — fit: PASS — buck: VIN/EN left power-up, FB passive (divider-safe), SW output + BS right, GND bottom; camera-fpc-adapters twin passed over (GND mid-left, input-typed FB)
- symbols/SDCW2012-2-900TF.kicad_sym — mpn=SDCW2012-2-900TF (LCSC C54888) from=wristcam-v2 — fit: PASS — USB CMC, vendor numbering 1/4 in-left, 2/3 out-right (windings 1-2, 4-3, verified against the LCSC DLW21SN land pattern convention); renamed CMC_USB→MPN, baked title updated, Value moved below body
- symbols/DLW21SN900SQ2L.kicad_sym — mpn=DLW21SN900SQ2L (LCSC C97856) from=skibidi-hub — fit: PASS — 2-line CMC, same 1-2/4-3 winding convention; renamed CMC_2LN→MPN, baked title updated, Value moved below body
- symbols/DLM0QSB120HY2D.kicad_sym — mpn=DLM0QSB120HY2D from=vitracker-v2 — fit: PASS — MIPI CMC as true coil glyph, windings 1-2 top / 4-3 bottom (Murata numbering). WARNING: headrig-jig's board-local CMC_2LN + CMC_0504 pair uses a DIFFERENT self-consistent corner numbering (1,2 left / 3,4 right) — never mix that board's symbol or footprint with this central part; migrate headrig as a pair or re-map both
- symbols/DLW21SN900HQ2L.kicad_sym — mpn=DLW21SN900HQ2L (LCSC C97855) from=vitracker-v2 — fit: PASS — coil glyph; un-hid pin numbers (winding orientation was invisible), Ref moved clear of coupling bars, Value cleaned of _C97855 suffix and moved below glyph
- symbols/EA3056.kicad_sym — mpn=EA3056QDR (LCSC C575411) from=wristcam-v2 — fit: PASS — 3-buck+LDO PMIC: VIN group top-left, EN/I2C left, LX/LDO/FB right, PGND/AGND/EP banked bottom; byte-identical twin on foxjig
- symbols/EA3036C.kicad_sym — mpn=EA3036CQBR (LCSC C570857) from=headrig-jig — fit: PASS — 3ch sync buck: VIN/EN/FB grouped left, LX right, all GNDs banked bottom
- symbols/RV1106G2.kicad_sym — mpn=RV1106G2 (LCSC C5272606) from=wristcam-v2 — fit: PASS — 5-unit SoC (A power, B system, C camera CSI-2, D FSPI NAND, E SPI/GPIO), domain-grouped; baked unit titles carried source refdes U10x — normalized to "unit X"; group "(NC)" tags reflect the source board's usage, re-judge per design
- symbols/RV1106G3.kicad_sym — mpn=RV1106G3 (LCSC C5328706) from=foxjig — fit: PASS — same 5-unit house style (A power, B system, C dual 2-lane CSI, D storage, E GPIO field); U10x titles normalized; NOT pin-interchangeable with G2 — distinct part, distinct file
- symbols/RV1106B.kicad_sym — mpn=RV1106BG3 from=headrig-jig — fit: PASS — QFN88 single-unit two-column with functional group headers, VSS/VSS_EP bottom; tall (~193mm) but organized and legible (note, not a re-author)
- symbols/MAX98357A.kicad_sym — mpn=MAX98357AETE+T from=cm5-carrier-v2 — fit: PASS — VDD top (dup pin 8 hidden-stacked), GND 3+11+15 stacked + EP_GND bottom, I2S left, OUTP/OUTN typed output right, NC hidden no_connect; added missing MPN prop (TQFN-16-EP 3x3 = ETE+T, matches stardeck twin); stardeck copy passed over (VDD mid-right, passive outs, all-visible NC column)

Central-intake wave 2026-07-19 cont'd (librarian, batch 3): early-board candidates
(foxjig / skibidi-hub / stardeck / headrig-jig) + remaining shared + name-safety +
FN6252B geometry re-author. Same rule — render + LOOK before every row; pins/names/etypes
preserved exactly unless the fix was geometry (noted per row).

- symbols/FPC22_PI5.kicad_sym — mpn=AFC07-S22FCC-00 (LCSC C11056) from=foxjig — fit: PASS — 22p 0.5mm bottom-contact FPC, Pi-5 camera pinout; all 22 pads exposed (7 grounds GND1..19), pins passive (connector law); functional cols PWR/CTRL left, LANE0/1 + CLOCK + L2/L3 data + GND right; L2/L3 noted NC in 2-lane use. Application-flavored pin names preserved as authored
- symbols/GD5F1GQ5UEYIGY.kicad_sym — mpn=GD5F1GQ5UEYIGY (LCSC C2886520) from=foxjig — fit: PASS — 1Gb SPI NAND, WSON-8; VCC(8) top-left, SPI /CS/CLK/DI/DO left, /WP//HOLD right, GND(4)+EP(9) bottom. NAME-SAFETY: source symbol was mislabeled "W25N01GV" (a Winbond p/n) but its Value/MPN/LCSC + foxjig build.py + foxjig-bom.csv all identify GigaDevice GD5F1GQ5UEYIGY — promoted under the true build/BOM identity, symbol key renamed W25N01GV→GD5F1GQ5UEYIGY (pins/geometry untouched); foxjig migrates W25N01GV→GD5F1GQ5UEYIGY. Board's BOM-VERIFIED.md separately intends Winbond W25N01GVZEIG/C907680 — unresolved board discrepancy flagged to owner. Footprint prop board-local (not carried)
- symbols/CH217K.kicad_sym — mpn=CH217K (LCSC C7462749) from=skibidi-hub — fit: PASS — USB power-path / load switch; VIN(6)/EN#(4)/ISET(5) left power-up, VOUT(1)/FLAG#(3) right, GND(2) bottom edge; body ∝ 6 pins, grid-true
- symbols/AP64500.kicad_sym — mpn=AP64500SP-13 (LCSC C2070920) from=skibidi-hub — fit: PASS — sync buck; IN(VIN/EN/GND) + CTRL(RT_CLK/FB/COMP) grouped left, SW(8)/BST(1) right, EP(9) bottom; note GND(7) mid-left. Divider-facing FB/COMP left as authored
- symbols/CH211C.kicad_sym — mpn=CH211C (LCSC C49438114) from=skibidi-hub — fit: PASS — USB-C PD power IC; HV PWR/CC/OD + FET left power-up, I2C/LDO/LV-CC/LV-OD right, GND(3)+EP(17) bottom; clean functional headers, body ∝ 17 pins
- symbols/CH634X.kicad_sym — mpn=CH634X (LCSC C48985831) from=skibidi-hub — fit: PASS — USB3 4-port hub, QFN-68+EP; PWR 5V/3V3/1V2 top-left, upstream + P2/P3/P4 SS lanes left, P1 USB-C + CC/PD + CTRL + PORT-PWR + CLK right, EP(69) bottom; NC(38) no_connect. Tall but fully grouped (RV1106B-class). Name carries family "X" but LCSC C48985831 pins the concrete part
- symbols/FSW3410.kicad_sym — mpn=FSW3410YQFN18G/TR (LCSC C41370613) from=skibidi-hub — fit: PASS — USB3 2:1 mux; COM(hub) + CTRL(SEL/EN#) + VCC(17) left, PORT B (SEL=H) / PORT A (SEL=L) diff pairs right, NC1/NC2 no_connect, GND(18)+EP(19) bottom; body ∝ pins, grid-true
- symbols/GL3224.kicad_sym — mpn=GL3224-OIY04 (LCSC C157357) from=skibidi-hub — fit: PASS — USB3 card-reader controller; USB3-SS/USB2/CLK/REF + PWR left, SD BUS/CARD/REG-OUT/SPI-LED right, EP(33) bottom; note GND(27) mid-left under PWR. Multi-rail REG-OUT pins as authored
- symbols/SH-TF-01A.kicad_sym — mpn=SH-TF-01A (LCSC C22383473) from=skibidi-hub — fit: PASS — push microSD/TF socket; SD(DAT/CMD/CLK) + PWR(VDD/VSS) left, DET(CD1/CD2) + SHELL(SH1-3) right, pins passive (connector law), full pad+shell set. NAME-SAFETY: source symbol was generic "MICROSD" (shared-lib collision landmine) — promoted under MPN SH-TF-01A, symbol key renamed (pins untouched); skibidi migrates MICROSD→SH-TF-01A
- symbols/SL21A.kicad_sym — mpn=SL2.1A (LCSC C192893) from=skibidi-hub — fit: PASS — USB2 4-port hub; UPSTREAM(UDP/UDM) + PWR(VCC5/VDD33/VDD18/VSS) + CLK left, P1..P4 DP/DM pairs right; note VSS(12) mid-left, no EP. Symbol key SL21A kept (dot-free), true MPN SL2.1A recorded
