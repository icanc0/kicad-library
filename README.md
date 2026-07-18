# kicad-library — the centralized, PROVEN part library

One home for symbols, footprints, and 3D models that have earned trust on real boards.
Consumed by boards as a **git submodule** (`git submodule add
https://github.com/icanc0/kicad-library`) — a pinned commit per board = reproducible builds —
and resolved natively by the kicad-agent-guide engine:

```python
load_symbol("central", "RP2040")      # symbols/RP2040.kicad_sym (one file per part)
# footprints: "<pretty-name>:<fp>" (e.g. "CM4IO:...") or "footprints:<fp>" for the top-level dir
```

## Layout

- `symbols/` — one `.kicad_sym` per part, filename = part name.
- `footprints/` — `*.pretty/` libraries (each is a KiCad fp-lib-table entry) **plus** top-level
  `.kicad_mod` files served as the lib nick `footprints` (existing boards reference the bare dir;
  keep both working). Engine-promoted parts land in `central-agent.pretty/`.
- `3dmodels/` — STEP/WRL bodies; footprints reference them `${KIPRJMOD}/kicad-library/3dmodels/…`
  so they resolve inside any board that carries the submodule.
- `MANIFEST.md` — provenance, one line per promoted part (MPN, source board, proven-note).
- `attic/` — quarantined bad copies kept for history; never reference these.

## The contract (librarian charter, guide docs/10)

A part belongs here when it satisfies the charter: exact MPN identity, the footprint's FULL pad
set exposed, datasheet provenance, vendor-exact 3D committed here (never /tmp, never another
vendor's body), and ideally *soldered-proven* on a named board. The guide's
`python3 -m engine.central promote --sym … --fp … --model … --mpn … --from-board … --note …`
copies a part in and appends the MANIFEST line — review + commit by hand (render + LOOK first).

Boards' own `hardware/libs/` stay the scratch space for parts being authored; graduation to
central is deliberate, not automatic.
