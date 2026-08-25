# sources/samsung.klmbg2jetd-b041 — eMMC BGA153 symbol generator + facts

Source of truth for `symbols/KLMBG2JETD-B041.kicad_sym` (promoted from hydra, 2026-08-24
symbol campaign). ONE generator emits TWO symbols carried as internal symbols of that file:
the JEDEC generic `eMMC_BGA153` and the derived `KLMBG2JETD-B041` (Samsung 32 GB, LCSC
C2803245) — request either by internal name. hydra KEEPS authoring locally from these
sources (generator = declared-sides safety); other boards load the emitted symbols from
central.

## Files

- `emmc.py` — the generator (`symlib/emmc.py` in hydra). 153 pins / 5 units at pitch 3.81:
  eMMC I/F (DAT/CMD/CLK/STROBE/RESET left; Vcc x4, Vccq x5, Vddi right — vendor duplicate
  rail names, never invented indices), one pure Vss/Vssq GND column, three NC/RFU/VSF
  units with every ball pinned.
- `emmc-truth-153.json` — ball -> vendor-name facts (`facts/emmc-truth-153.json` in
  hydra), asserted at import against the footprint pad set.

## Datasheet provenance

- Kingston eMMC TB29 (PZ90) v1.1 (`Kingston-EMMC-TB29-PZ90-v1.1.pdf`, vendored in hydra
  `datasheets/`): "Table 8 - Ball Assignment, Top View (HS400)" doc p13 = the JEDEC
  153-ball truth; pin descriptions + types doc pp.9-10 (Vddi "not a power supply input ...
  external Creg capacitor"; NC balls "may be routed through").
- Cross-check: Samsung KLMAG1JETD-B041 s3.1 Table 2 (`KLMAG1JETD-B041-UUGear.pdf`, same
  B041-family ballout; Samsung merges Vssq into VSS, names RST_n "RSTN").
- Adversarially re-derived by hydra `verify/symbols-0824/verify8/v-mem.md` (153/153,
  accurate as landed).

## Regeneration

Requires the kicad-agent-guide engine (`engine.author_symbol` / `Unit` / `Group` API) plus
the hydra board tree's `symlib/common.py` import chain — run inside a board checkout with
`PYTHONPATH=<kicad-agent-guide>`. These files are a provenance vendoring, not a standalone
build.
