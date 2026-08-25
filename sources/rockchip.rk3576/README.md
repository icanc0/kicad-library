# sources/rockchip.rk3576 — RK3576 symbol generator + facts

Source of truth for `symbols/RK3576.kicad_sym` (promoted from hydra, 2026-08-24 symbol
campaign). SYMBOL-ONLY record: the vendor land `BGA698_16R1X17R2X1R08` (RK3576 EVB p.11)
is not in any repo and was never synthesized — the footprint pends the vendor land
drawing. hydra KEEPS authoring locally from these sources (generator = declared-sides
safety); other boards load the emitted symbol from central.

## Files

- `rk3576.py` — the generator (`symlib/rk3576.py` in hydra): 698 balls / 34 units at
  pitch 3.81 (EVB U1000A..V domain split; NC/DNU arrays in titled units; twelve pure
  single-column GND units, 10 x 24 + 13 + 12 = the 265 DS ground returns).
- `rk3576_facts.py` — facts loader: parse provenance, the D6 vendor-name rule, the D11
  etype rule, and the pindata assertion.
- `rk3576_units.py` — the V2 unit map (review rk3576.md §7).
- `rk3576-balls.json` — 698-ball truth (`facts/rk3576-balls.json` in hydra), asserted
  at import: every ball exactly once, names matched to the DS token.

## Datasheet provenance

Rockchip RK3576 Datasheet V1.6 (`datasheets/RK3576-Datasheet-V1.6.pdf`, vendored in
hydra): §2.6 Table 2-1 "Pin Description" (PDF pp.30-45) = the 698-ball FCCSP698L truth;
package land name from the RK3576 EVB doc p.11. LCSC C42388007. Adversarially re-derived
by hydra `verify/symbols-0824/verify8/v-rk3576.md` (CLEAN, 698/698 independent re-parse
of Table 2-1).

## Regeneration

Requires the kicad-agent-guide engine (`engine.author_symbol` / `Unit` / `Group` API)
plus the hydra board tree's `symlib/common.py` import chain — run inside a board checkout
with `PYTHONPATH=<kicad-agent-guide>`. These files are a provenance vendoring, not a
standalone build.
