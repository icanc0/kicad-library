# sources/rockchip.rk806s-5 — RK806 symbol generator + facts

Source of truth for `symbols/RK806.kicad_sym` (promoted from hydra, 2026-08-24 symbol
campaign). The board that authored it (hydra) KEEPS authoring locally from these sources
(generator = declared-sides safety); other boards load the emitted symbol from central.

## Files

- `rk806.py` — the generator (`symlib/rk806.py` in hydra). Emits the 69-pin / 12-unit
  family symbol `RK806` (BUCK1..10 one tile per stage, LDO, CONTROL; pitch 7.62,
  owner order 2026-08-20). Value/MPN carry the OTP variant (hydra: RK806S-5, LCSC
  C49174044); RK806-1/-2/-3/S-5 are OTP programs of ONE die (DS §2.1), pinout family-wide.
- `rk806s5-pins.json` — ball->name/type facts (`facts/rk806s5-pins.json` in hydra),
  asserted at import by the generator.

## Datasheet provenance

RK806 Datasheet V1.4 (`RK806-Datasheet-V1.4.pdf`, vendored in hydra `datasheets/`):
§2.7 "Pinout Number Order" pp.15-16 (name / I-O / description per pad), §2.6 Fig 2-2 p14
(pin order around the QFN68), §1.2 Feature p7 (per-buck/LDO current ratings used as unit
captions), §1.3 block diagram p9 (VCCA -> PLDO6 -> VCCIO). One deliberate deviation:
the §2.7 table prints "PWRCRTLn"; DS revision note 6 and every register/§4 mention spell
PWRCTRLn, so the symbol does too. Adversarially re-derived by hydra
`verify/symbols-0824/verify8/v-pmic.md` (CLEAN, 69/69 vs DS §2.7).

## Regeneration

Requires the kicad-agent-guide engine (`engine.author_symbol` / `Unit` / `Group` API) plus
the hydra board tree's `symlib/common.py` import chain — run inside a board checkout with
`PYTHONPATH=<kicad-agent-guide>`. These files are a provenance vendoring, not a standalone
build.
