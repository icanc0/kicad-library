# sources/samsung.k4u6e3s4aa-mgcl — LPDDR4X x32 FBGA200 symbol generator + facts

Source of truth for `symbols/K4U6E3S4AA-MGCL.kicad_sym` (promoted from hydra, 2026-08-24
symbol campaign). ONE generator emits TWO symbols carried as internal symbols of that
file: the JEDEC generic `LPDDR4X_x32_FBGA200` (rank-1 balls LIVE) and the derived
`K4U6E3S4AA-MGCL` (Samsung 16 Gb x32 SDP single-rank, LCSC C2920249; ordering decode
6E = 16 Gb, 3S = x32 single-die -> H3 R3 J5 P5 A8 = CS1/CKE1/ZQ1 are no_connect) —
request either by internal name. hydra KEEPS authoring locally from these sources
(generator = declared-sides safety); other boards load the emitted symbols from central.

## Files

- `lpddr4x.py` — the generator (`symlib/lpddr4x.py` in hydra): 200 pins / 7 units at
  pitch 3.81 (CH A + CH B mirrors, PWR with vendor duplicate VDD1/VDD2/VDDQ names,
  three pure VSS GND columns, DNU/NC unit).
- `lpddr4x-truth.json` — per-ball facts with dual-datasheet citations
  (`facts/lpddr4x-truth.json` in hydra), asserted at import.

## Datasheet provenance

- Micron `MT53E256M32D2DS-046-IT-B-Octopart.pdf` (vendored in hydra `datasheets/`):
  Fig 5 p21 "200-Ball Dual-Channel, Single-Rank Discrete FBGA (x32 I/O)" + Table 3 p22
  ball descriptions (ODT_CA "shall be connected to a valid logic level", DNU "grounded or
  left floating", NC "not internally connected").
- Samsung `SEC_K4UBE3D4AA-MGCL_200F_10x15.pdf` (DDP sibling — K4U6E3S4AA's own DS is not
  published): sec 4.2 p10 ballout (rank-1 names), sec 4.3 p11 pad names (JEDEC spelling:
  DQS0_t_a, CK_c_b, ODT_CA_a, RESET_n), note 2 "ODT pin should connect to VDD2 or VSS".
- The two ballouts agree on all 200 balls except the rank-1/NC class. Adversarially
  re-derived by hydra `verify/symbols-0824/verify8/v-mem.md`: 0/200 diffs vs both.

## Regeneration

Requires the kicad-agent-guide engine (`engine.author_symbol` / `Unit` / `Group` API)
plus the hydra board tree's `symlib/common.py` import chain — run inside a board checkout
with `PYTHONPATH=<kicad-agent-guide>`. These files are a provenance vendoring, not a
standalone build.
