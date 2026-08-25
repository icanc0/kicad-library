"""RK3576 (Rockchip, FCCSP698L) — authored symbol, key "RK3576" (D13), 698 balls, 34 units.

Facts: facts/rk3576-balls.json = RK3576 Datasheet V1.6 §2.6 Table 2-1 (PDF pp.30-45), see
symlib/rk3576_facts.py for the parse provenance, the vendor-name rule (D6) and the etype rule
(D11). Unit map: symlib/rk3576_units.py (EVB1 U1000A..V domains, canon-split; review
verify/symbols-0824/review/rk3576.md §7 V2). GND: FOUR two-sided units (36 L + 36 R; owner 2026-08-25 guide #268) of the DS
returns (VSS_0..162, AVSS_0..76, AVSS1_0..24 = 163+77+25 = 265 balls; TVSS, PLL_AVSS and DDRPHY_PLL_AVSS
ride in units E/C with the domain they return) — 11 x 24 + 25, each 12 L + 12 R (owner 2026-08-25).
Package land: vendor `BGA698_16R1X17R2X1R08` (EVB p.11) — not in the repo, no Footprint prop.
Value/MPN = RK3576 (LCSC C42388007). Datasheet prop = the vendor PDF in datasheets/.

Assertions at import: 698 pins, every ball exactly once, every pindata.RK3576_* ball exists in
the facts with a matching DS token (D12 — provenance is the DS, not the DshanPi schematic).
"""
from symlib.common import *  # noqa: F401,F403
from symlib.rk3576_facts import BALLS, vendor_name, etype
from symlib.rk3576_units import UNITS, LETTERS

GND_PER_SIDE = 36                 # owner 2026-08-25 "fewer but bigger blocks": 4 x (36 L + 36 R)
GND_PER_UNIT = 2 * GND_PER_SIDE
_GND_ORDER = ([f"VSS_{i}" for i in range(163)] + [f"AVSS_{i}" for i in range(77)]
              + [f"AVSS1_{i}" for i in range(25)])


def _gnd_columns():
    """265 DS ground returns in vendor order as TWO-SIDED units (owner 2026-08-25: "left or
    right would be helpful to save space — why only one side of the symbol"): 24 balls per
    column-pair per unit -> 3 x (36 + 36) + (25 + 24): four page-band-tall blocks (owner 2026-08-25
    'fewer but bigger'; guide #268), one bus + one glyph per side. Each entry is
    (left_balls, right_balls); a column never exceeds GND_PER_UNIT (S1 24/row)."""
    from symlib.rk3576_facts import ball_of
    balls = [ball_of(n) for n in _GND_ORDER]
    assert len(balls) == 265
    out, i = [], 0
    while i < 265:
        chunk = balls[i:i + GND_PER_UNIT]
        half = (len(chunk) + 1) // 2
        out.append((chunk[:half], chunk[half:]))
        i += len(chunk)
    assert i == 265 and all(len(l) <= GND_PER_SIDE + 1 and len(r) <= GND_PER_SIDE for l, r in out)
    return out


GND_COLUMNS = _gnd_columns()

# letter/label -> unit number (author order); "GND1".."GND12" for the ground columns
UNIT = {L: i + 1 for i, L in enumerate(LETTERS)}
UNIT.update({f"GND{k + 1}": len(LETTERS) + k + 1 for k in range(len(GND_COLUMNS))})
N_UNITS = len(UNIT)

# unit number -> balls (all of them, in symbol order)
UNIT_BALLS = {UNIT[L]: [b for side in UNITS[L][1:] for _cap, bs in side for b in bs] for L in LETTERS}
UNIT_BALLS.update({UNIT[f"GND{k + 1}"]: list(l) + list(r) for k, (l, r) in enumerate(GND_COLUMNS)})
UNIT_TITLE = {UNIT[L]: UNITS[L][0] for L in LETTERS}
UNIT_TITLE.update({UNIT[f"GND{k + 1}"]: f"RK3576 GND {k + 1}/{len(GND_COLUMNS)}"
                   for k in range(len(GND_COLUMNS))})


def unit_balls(unit):
    """Every ball of `unit` (number or letter/label) — the sheet's nc= complement."""
    return list(UNIT_BALLS[UNIT[unit] if isinstance(unit, str) else unit])


def _check_map():
    seen = {}
    for u, balls in UNIT_BALLS.items():
        for b in balls:
            assert b in BALLS, f"unit {u}: {b!r} is not a DS ball"
            assert b not in seen, f"ball {b} in units {seen[b]} and {u}"
            seen[b] = u
    missing = sorted(set(BALLS) - set(seen))
    assert not missing, f"{len(missing)} DS balls in no unit: {missing[:12]}"
    assert len(seen) == 698, len(seen)
    for L in LETTERS:
        for side in UNITS[L][1:]:
            for cap, _bs in side:
                assert len(cap) <= 16, f"unit {L}: caption {cap!r} > 16 chars"


_check_map()


def _pin(ball):
    return (vendor_name(ball), ball, etype(ball))


def rk3576():
    units = []
    for L in LETTERS:
        title, left, right = UNITS[L]
        units.append(Unit(title,
                          left=[Group(cap, [_pin(b) for b in bs]) for cap, bs in left],
                          right=[Group(cap, [_pin(b) for b in bs]) for cap, bs in right]))
    for k, (lcol, rcol) in enumerate(GND_COLUMNS):
        # two caption-less columns (24 L + 24 R): half the height of the old single column;
        # width from ink (two ~8.4 mm names + margins), no 50.8 floor needed.
        units.append(Unit(UNIT_TITLE[UNIT[f"GND{k + 1}"]],
                          left=[Group("", [_pin(b) for b in lcol])],
                          right=[Group("", [_pin(b) for b in rcol])], width=38.1))
    assert len(units) == N_UNITS == 22 + len(GND_COLUMNS)
    npins = sum(len(g.pins) for u in units for s in (u.left, u.right) for g in s)
    assert npins == 698, npins
    return author_symbol(
        "RK3576", units,
        props=[("Reference", "U", False), ("Value", "RK3576", False), ("Footprint", "", True),
               ("MPN", "RK3576", True), ("LCSC", "C42388007", True),
               ("Datasheet", "datasheets/RK3576-Datasheet-V1.6.pdf", True)],
        pitch=3.81, library_override_reason=SRC_BOARD_REASON)


__all__ = ["rk3576", "UNIT", "UNIT_BALLS", "UNIT_TITLE", "unit_balls", "GND_COLUMNS", "N_UNITS"]
