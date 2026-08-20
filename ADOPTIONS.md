# ADOPTIONS — fleet block-symbol determinations (librarian wave 1, 2026-08-20)

The fleet audit that answered "why are the FETs just blocks": every authored
symbol flagged STOCK-COVERED / CENTRAL-DUP without an explicit
`library_override_reason`, each examined by its own focused agent (L24).
Verdicts below are instructions for the OWNING board sessions — boards are
never edited from the librarian lane.

| Part | Board | Verdict | Action for the board |
|---|---|---|---|
| 2N7002 | lever | **ADOPT-CLEAN (already adopted)** | `schematic/symbols.py:73` already loads `Transistor_FET:2N7002` (real glyph) through `_PassiveGateSymbol`. The authored block in `lever_authored.kicad_sym` is a REDUNDANT leftover — delete it from the lib file. Pin map 1=G/2=S/3=D verified both sides. |
| CH32X035G8U6 | lever | **KEEP-AUTHORED, declare it** | The authored symbol is a functional-role abstraction (UDP/SWDIO/EN_LOADSW… names, EP as pin 0, no_connect trims), production-tested; central's datasheet-name symbol would force ~15 net renames + EP renumber. Add `library_override_reason="functional-role symbol for the interposer: board-role pin names + EP pad 0; central CH32X035G8U6 is the datasheet-name reference"`. |
| LM74700 | capjack | **ADOPT-WITH-CARE** | `Power_Management:LM74700` is pin-identical (1=VCAP 2=GND 3=EN 4=CATHODE 5=GATE 6=ANODE, SOT-23-6) with MORE correct etypes (EN=input, ANODE=power_in). Swap `author_symbol` → `load_symbol("Power_Management", "LM74700")`, keep MPN=LM74700QDBVRQ1 / LCSC=C2941042 at the instance, re-run ERC (etype promotion may surface new pin-class checks). |
| LMV321 | capjack | **KEEP-AUTHORED, declare it** | Both symbols carry the TI DBV pinout (SLOS935 T5-2: 1=IN+ 2=V- 3=IN- 4=OUT 5=V+ — NOT the 1=OUT industry alt). Authored adds MPN LMV321IDBVR / LCSC C3014306 + role ink. Add `library_override_reason="TI-DBV pinout traceability for C3014306 + sourcing metadata; stock Amplifier_Operational:LMV321 is pin-identical"`. |
| AP64500 | skibidi-hub | **ADOPT-CENTRAL-CLEAN** | Byte-identical pin contract (9 pins incl. EP). `load_symbol("central", "AP64500")`, drop the authored copy. |
| CH211C | skibidi-hub | **ADOPT-WITH-CARE** | Identical except pin 11 ODH2 etype: central=bidirectional vs authored=open_collector — central is datasheet-correct (WCH Fig 8-2 gate path). Adopt central; verify ERC on the GATE_CH net. |
| CH217K | skibidi-hub | **ADOPT-CENTRAL-CLEAN** | Identical 6-pin contract. Adopt central, drop the copy. |
| CH634X | skibidi-hub | **ADOPT-CENTRAL-CLEAN** | Identical 69-pin contract; central is the POLISH upgrade (taller body, verbose port-role group labels matching this board's roles). Adopt central. |
| FSW3410 | skibidi-hub | **ADOPT-CENTRAL-CLEAN** | Byte-identical 19-pin mux contract. Adopt central. |

## Promotions owed (legacy → full part records)

- **CH32X035G8U6**: has `fit:PASS` but NO part.json. Needs
  `parts/wch.ch32x035g8u6.part.json`: MPN CH32X035G8U6, LCSC C7437027,
  footprint QFN-28_L4.0-W4.0-P0.40-BL-EP2.8, evidence link, fit note
  (librarian audit 2026-07-19; EP numbering: central uses pin 29 — boards
  using EP=0 must declare their divergence).
- AP64500, CH211C, CH217K, CH634X, FSW3410: all "legacy symbol" —
  promotion to part.json records queued as the next librarian wave
  (per-part focused agents, L24).

## Process (L24)

One part = one focused agent. This wave ran five agents (three per-part
stock checks, two per-board central diffs); every verdict above carries a
full pin-table comparison in its agent's report. Inline multi-part intake
is an unfinished intake.
