# sources/lattice.lfe5u-25f-7bg256i — ECP5 caBGA-256 symbol generator + facts

Source of truth for `symbols/LFE5U-25F-7BG256I.kicad_sym` (promoted from hydra, 2026-08-24
symbol campaign). hydra KEEPS authoring locally from these sources (generator =
declared-sides safety); other boards load the emitted symbol from central.

## Files

- `ecp5.py` — the generator (`symlib/ecp5.py` in hydra): 256 pins / 11 units at pitch
  3.81 — one unit per Lattice I/O BANK carrying its own VCCIO (banks 7/6/0/1/2/3/8;
  captioned PIC rows with dual functions, A/B pairs left, C/D pairs right,
  true-then-complement), sysCONFIG/JTAG, CORE POWER, two pure GND columns.
- `ecp5-bg256-balls.json` — 256 balls {name, bank, dqs, dual_function, class}
  (`facts/ecp5-bg256-balls.json` in hydra), asserted at import.

## Datasheet provenance

- `BSDLLFE5U25FCABGA256.bsm` (Lattice BSDL, vendored in hydra `datasheets/`):
  `constant cabga256 : PIN_MAP_STRING` l.291-536 — primary names + `--secfnc` dual
  functions; cross-checked 197/197 PIO against `ecp5-25k-iodb.json` (prjtrellis: bank,
  DQS group).
- Family DS FPGA-DS-02012 (ECP5 and ECP5-5G Family Data Sheet) §"Pinout Information";
  sysCONFIG pin semantics FPGA-TN-02039 §4.6-4.8 (CCLK bidirectional in slave modes,
  DONE/INITN open-drain); bank/VCCIO rules FPGA-TN-02032 §4.
- Adversarially re-derived by hydra `verify/symbols-0824/verify8/v-ecp5.md` (CLEAN,
  256/256 BSDL-verbatim).

## Family aliases (D13)

The caBGA-256 ballout is common to the whole LFE5U BG256 family per the FPGA-DS-02012
pinout table (one column per package): LFE5U-{12F,25F,45F} x -{6,7,8} x BG256{C,I} —
recorded as aliases on the part record. CAVEAT: only the 25F BSDL is on disk; diff the
12F/45F BSDL PIN_MAPs before promoting an alias to a placed part.

## Regeneration

Requires the kicad-agent-guide engine (`engine.author_symbol` / `Unit` / `Group` API)
plus the hydra board tree's `symlib/common.py` import chain — run inside a board checkout
with `PYTHONPATH=<kicad-agent-guide>`. These files are a provenance vendoring, not a
standalone build.
