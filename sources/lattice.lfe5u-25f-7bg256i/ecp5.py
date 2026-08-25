"""LFE5U-25F-7BG256I — Lattice ECP5 FPGA, caBGA-256, authored from the FULL ball set.

FACTS (D12): facts/ecp5-bg256-balls.json — 256 balls {name, bank, dqs, dual_function, class}
built from datasheets/BSDLLFE5U25FCABGA256.bsm (Lattice BSDL, `constant cabga256 :
PIN_MAP_STRING`, l.291-536: names, --secfnc dual functions) cross-checked 197/197 PIO against
datasheets/ecp5-25k-iodb.json (prjtrellis: bank, DQS group). Family DS FPGA-DS-02012 (ECP5 and
ECP5-5G Family Data Sheet) §"Pinout Information" is the vendor pin table these agree with;
sysCONFIG pin semantics from FPGA-TN-02039 §4.6-4.8; bank/VCCIO rules from FPGA-TN-02032 §4.

UNITS (review verify/symbols-0824/review/ecp5.md §6, V1): one unit per Lattice I/O BANK carrying
its own VCCIO (one unit = one I/O-voltage domain), then sysCONFIG/JTAG, core power, two GND
columns. Within a bank unit: VCCIO group top-left, then every PIC row as a captioned group
("<row> <dual function>", <= 16 chars, row dropped when the function alone needs the width);
A/B pairs on the left, C/D pairs on the right (top/bottom banks have A/B only: first half of the
rows left, second half right); pairs adjacent true-then-complement.
  1 BANK 7 (PL2-PL23, VCCIO7 H6 H7)     2 BANK 6 (PL26-PL47, VCCIO6 J6 J7)
  3 BANK 0 (PT4-PT29, VCCIO0 F6 F7)     4 BANK 1 (PT33-PT67, VCCIO1 F10 F11)
  5 BANK 2 (PR2-PR23, VCCIO2 H11 J11)   6 BANK 3 (PR26-PR47, VCCIO3 K11 L11)
  7 BANK 8 (PB4-PB18, VCCIO8 L6)        8 sysCONFIG/JTAG (11 balls)
  9 CORE POWER (VCC x6, VCCAUX x2)      10/11 GND (27 balls: 14 + 13, single left columns)
Pin NAMES = BSDL primary names (PL23A, VCCIO7, CCLK, GND ...); board roles are NET LABELS at the
instance. ETYPES (docs/02 + review §3): PIO bidirectional; CCLK bidirectional (input in slave
modes, TN-02039 §4.6.5); DONE/INITN bidirectional (open-drain, TN-02039 §4.6.4); PROGRAMN and
CFG_0-2 passive (pulled straps); TCK/TMS/TDI passive (JTAG inputs, pulled); TDO output;
VCC/VCCAUX/VCCIO/GND power_in.

FAMILY ALIASES (D13, for part.json): the caBGA-256 ballout is common to the whole LFE5U
BG256 family (FPGA-DS-02012 pinout table, one column per package): LFE5U-12F-6BG256C,
LFE5U-12F-6BG256I, LFE5U-12F-7BG256C, LFE5U-12F-7BG256I, LFE5U-12F-8BG256C, LFE5U-12F-8BG256I,
LFE5U-25F-6BG256C, LFE5U-25F-6BG256I, LFE5U-25F-7BG256C, LFE5U-25F-7BG256I (this symbol),
LFE5U-25F-8BG256C, LFE5U-25F-8BG256I, LFE5U-45F-6BG256C, LFE5U-45F-6BG256I, LFE5U-45F-7BG256C,
LFE5U-45F-7BG256I, LFE5U-45F-8BG256C, LFE5U-45F-8BG256I. Only the 25F BSDL is on disk (review
§1): diff the 12F/45F BSDL PIN_MAPs against facts/ecp5-bg256-balls.json before promoting an
alias to a placed part.
"""
import json as _json
import re as _re

from symlib.common import *  # noqa: F401,F403

ECP5_MPN = "LFE5U-25F-7BG256I"
ECP5_LCSC = "C1550762"          # LCSC live 2026-08-24: LFE5U-25F-7BG256I, Lattice, CABGA-256
ECP5_FACTS = _HERE / "facts/ecp5-bg256-balls.json"
ECP5_DATASHEET = "FPGA-DS-02012 + BSDLLFE5U25FCABGA256.bsm"
ECP5_FAMILY_ALIASES = tuple(f"LFE5U-{d}-{s}BG256{t}"
                            for d in ("12F", "25F", "45F") for s in (6, 7, 8) for t in "CI")

BALLS = _json.load(open(ECP5_FACTS))
assert len(BALLS) == 256, f"facts/ecp5-bg256-balls.json: {len(BALLS)} balls (expect 256)"

# unit numbers (1-based, KiCad) — the sheets key their ic_fanout(unit=) off this map
ECP5_UNIT = {"b7": 1, "b6": 2, "b0": 3, "b1": 4, "b2": 5, "b3": 6, "b8": 7,
             "cfg": 8, "pwr": 9, "gnd1": 10, "gnd2": 11}
_BANK_ORDER = (7, 6, 0, 1, 2, 3, 8)
_PIO_RE = _re.compile(r"^P([LRTB])(\d+)([ABCD])$")


def _natkey(ball):
    m = _re.match(r"^([A-Z]+)(\d+)$", ball)
    return (m.group(1), int(m.group(2)))


def bank_of(ball):
    return BALLS[ball].get("bank")


def _pio_rows(bank):
    """{row_label: {pos: ball}} for one bank's PIO, e.g. {'PL23': {'A': 'J1', 'B': 'J2', ...}}."""
    rows = {}
    for ball, v in BALLS.items():
        if v["class"] != "PIO" or v["bank"] != bank:
            continue
        side, num, pos = _PIO_RE.match(v["name"]).groups()
        rows.setdefault((int(num), f"P{side}{num}"), {})[pos] = ball
    return {lab: poss for (_n, lab), poss in sorted(rows.items())}


# --- captions: "<PIC row> <dual function>" -----------------------------------------------------
_DQ_GROUP = _re.compile(r"^[LR]DQ\d+$")
_DQS_STROBE = _re.compile(r"^[LR]DQSN?\d+$")


def _fn_short(f):
    """One BSDL/iodb dual-function token in caption form (vendor token, prefix-trimmed)."""
    f = _re.sub(r"^L[LR]C_", "", f)                 # LLC_/LRC_ = left/right PLL corner
    f = _re.sub(r"_S\d_(?:IN|OUT)$", "", f)          # PCLKT2_1_S2_OUT alt spelling of PCLKT2_1
    m = _re.match(r"^D(\d+)[/_]IO(\d+)$", f)
    if m:
        return f"IO{m.group(2)}"      # the D-number spelling collides with diode refdes (SYM-GENERIC)
    m = _re.match(r"^D\d+[/_](MISO2?|MOSI2?)[/_]IO\d+$", f)
    if m:
        return m.group(1)
    for pfx, short in (("HOLDN", "CSSPIN"), ("DOUT", "CSON"), ("SN", "SN/CSN"), ("WRITEN", "WRITEN")):
        if f.startswith(pfx):
            return short
    return f


def _pair_fn(a_dual, b_dual):
    """Merged dual-function text for a pin pair: named functions first, DQS strobes second, DQ
    group membership never (it is every pin of the bank)."""
    def pick(dual):
        named = [d for d in dual if not _DQ_GROUP.match(d) and not _DQS_STROBE.match(d)]
        strobe = [d for d in dual if _DQS_STROBE.match(d)]
        return (named, strobe)
    an, as_ = pick(a_dual)
    bn, bs = pick(b_dual)
    if an or bn:
        fa = _fn_short(an[0]) if an else ""
        fb = _fn_short(bn[0]) if bn else ""
    else:
        fa = as_[0] if as_ else ""
        fb = bs[0] if bs else ""
    if fa and fb:
        if fa == fb:
            return fa
        if fb == fa.replace("DQS", "DQSN"):           # LDQS8 / LDQSN8 strobe pair
            return fa
        m1, m2 = _re.match(r"^PCLKT(\d_\d)$", fa), _re.match(r"^PCLKC(\d_\d)$", fb)
        if m1 and m2 and m1.group(1) == m2.group(1):
            return f"PCLKT/PCLKC{m1.group(1)}"        # never a bare C{bank} token (refdes-shaped)
        diff = [i for i, (x, y) in enumerate(zip(fa, fb)) if x != y]
        if len(fa) == len(fb) and len(diff) == 1 and fa[diff[0]] == "T" and fb[diff[0]] == "C":
            i = diff[0]
            return fa[:i] + "T/C" + fa[i + 1:]        # GPLL0T_IN + GPLL0C_IN -> GPLL0T/C_IN
        m1, m2 = _re.match(r"^(GR_PCLK\d_)(\d)$", fa), _re.match(r"^(GR_PCLK\d_)(\d)$", fb)
        if m1 and m2 and m1.group(1) == m2.group(1):
            return f"{fa}/{m2.group(2)}"              # GR_PCLK0_1 + GR_PCLK0_0 -> GR_PCLK0_1/0
        return f"{fa}/{fb}"
    return fa or fb


def _caption(row, balls):
    fn = _pair_fn(*(BALLS[b]["dual_function"] for b in balls)) if len(balls) == 2 else \
        _pair_fn(BALLS[balls[0]]["dual_function"], [])
    cap = f"{row} {fn}".strip()
    if len(cap) > 16:
        cap = fn                                      # pin names PL44A/B already carry the row
    assert len(cap) <= 16, f"caption {cap!r} for {row} exceeds 16 chars"
    return cap


def _pair_group(row, poss, pair):
    balls = [poss[p] for p in pair if p in poss]
    return Group(_caption(row, balls), [(BALLS[b]["name"], b, "bidirectional") for b in balls])


def _bank_unit(bank):
    rows = _pio_rows(bank)
    vccio = sorted((b for b, v in BALLS.items() if v["class"] == "VCCIO" and v["bank"] == bank),
                   key=_natkey)
    left = [Group(f"BANK {bank} VCCIO", [(BALLS[b]["name"], b, "power_in") for b in vccio])]
    right = []
    if all(set(p) <= {"A", "B"} for p in rows.values()):      # top/bottom banks: A/B only
        labs = list(rows)
        half = (len(labs) + 1) // 2
        left += [_pair_group(r, rows[r], "AB") for r in labs[:half]]
        right += [_pair_group(r, rows[r], "AB") for r in labs[half:]]
    else:                                                     # left/right banks: A/B | C/D
        left += [_pair_group(r, p, "AB") for r, p in rows.items()]
        right += [_pair_group(r, p, "CD") for r, p in rows.items()]
    # width: two 16-char captions (1.0 face) share a gap row across the body; 45.72 keeps
    # >= 5 mm between a left caption's end and a right caption's start.
    return Unit(f"LFE5U-25F BANK {bank}", left=left, right=right, width=45.72)


def _cfg_unit():
    n = {v["name"]: b for b, v in BALLS.items() if v["class"] == "CFG"}
    return Unit(
        "LFE5U-25F sysCONFIG",
        left=[Group("JTAG", [("TCK", n["TCK"], "passive"), ("TMS", n["TMS"], "passive"),
                             ("TDI", n["TDI"], "passive"), ("TDO", n["TDO"], "output")]),
              Group("CONFIG MODE", [("CFG_0", n["CFG_0"], "passive"), ("CFG_1", n["CFG_1"], "passive"),
                                    ("CFG_2", n["CFG_2"], "passive")])],
        right=[Group("sysCONFIG", [("PROGRAMN", n["PROGRAMN"], "passive"),
                                   ("INITN", n["INITN"], "bidirectional"),
                                   ("DONE", n["DONE"], "bidirectional"),
                                   ("CCLK", n["CCLK"], "bidirectional")])])


def _pwr_unit():
    vcc = sorted((b for b, v in BALLS.items() if v["class"] == "VCC"), key=_natkey)
    aux = sorted((b for b, v in BALLS.items() if v["class"] == "VCCAUX"), key=_natkey)
    return Unit("LFE5U-25F CORE POWER",
                left=[Group("VCC (CORE)", [("VCC", b, "power_in") for b in vcc]),
                      Group("VCCAUX", [("VCCAUX", b, "power_in") for b in aux])])


ECP5_GND = sorted((b for b, v in BALLS.items() if v["class"] == "GND"), key=_natkey)
ECP5_GND_SPLIT = (ECP5_GND[:(len(ECP5_GND) + 1) // 2], ECP5_GND[(len(ECP5_GND) + 1) // 2:])
ECP5_VCC = sorted((b for b, v in BALLS.items() if v["class"] == "VCC"), key=_natkey)
ECP5_VCCAUX = sorted((b for b, v in BALLS.items() if v["class"] == "VCCAUX"), key=_natkey)
# bank -> every ball of its unit (PIO + VCCIO), for the sheets' nc= complement
ECP5_BANK_BALLS = {bk: sorted((b for b, v in BALLS.items() if v.get("bank") == bk), key=_natkey)
                   for bk in _BANK_ORDER}
ECP5_CFG_BALLS = {v["name"]: b for b, v in BALLS.items() if v["class"] == "CFG"}


def _assert_pindata():
    """D12: pindata.ECP5_* role dicts (the sheets' netmap keys) are ASSERTED against facts."""
    def pio(ball, banks=None):
        v = BALLS[ball]
        assert v["class"] == "PIO", f"pindata: {ball} is {v['name']} ({v['class']}), not a PIO"
        assert banks is None or v["bank"] in banks, f"pindata: {ball} {v['name']} bank {v['bank']} not in {banks}"
        return v["name"]

    def pair(pb, nb):
        a, b = pio(pb), pio(nb)
        assert a[:-1] == b[:-1] and (a[-1], b[-1]) in (("A", "B"), ("C", "D")), \
            f"pindata: {pb}/{nb} = {a}/{b} is not a true PIC pair (T on A/C, C on B/D)"
    for cam in P.ECP5_RX_HS:
        for lane, (pb, nb) in P.ECP5_RX_HS[cam].items():
            pair(pb, nb)
            for lp in P.ECP5_RX_LP[cam][lane]:
                pio(lp, (0, 1))
    for lane, (pb, nb) in P.ECP5_TX_HS.items():
        pair(pb, nb)
        for lp in P.ECP5_TX_LP[lane]:
            pio(lp, (0, 1))
    for role, ball in P.ECP5_CTRL.items():
        pio(ball, (3,))
    for role, ball in P.ECP5_CFG.items():
        v = BALLS[ball]
        if role.startswith("SPI_"):
            tok = {"SPI_CSN": "CSSPIN", "SPI_MOSI": "MOSI", "SPI_MISO": "MISO"}[role]
            assert v["bank"] == 8 and any(tok in d for d in v["dual_function"]), \
                f"pindata: {role}={ball} ({v['name']}) lacks the {tok} sysCONFIG function"
        else:
            assert v["name"] == role, f"pindata: {role}={ball} but the ball is {v['name']}"
    for name, balls in P.ECP5_PWR.items():
        for ball in balls:
            assert BALLS[ball]["name"] == name, f"pindata: {name}={ball} but the ball is {BALLS[ball]['name']}"
    assert sorted(P.ECP5_PWR["GND"], key=_natkey) == ECP5_GND


_assert_pindata()


def ecp5():
    units = [_bank_unit(bk) for bk in _BANK_ORDER]
    units += [_cfg_unit(), _pwr_unit()]
    units += [Unit("LFE5U-25F GND", left=[Group("", [("GND", b, "power_in") for b in half])])
              for half in ECP5_GND_SPLIT]
    assert len(units) == len(ECP5_UNIT) == 11
    pins = [pnum for u in units for side in (u.left, u.right, u.bottom) for g in side for _n, pnum, _e in g.pins]
    pads = {f"{r}{c}" for r in "ABCDEFGHJKLMNPRT" for c in range(1, 17)}   # ECP5_CABGA256 = grid(16,16)
    assert len(pins) == 256 and set(pins) == pads == set(BALLS), \
        f"ECP5 symbol pins {len(pins)} vs 256 footprint pads (missing {sorted(pads - set(pins))[:8]})"
    props = [("Reference", "U", False), ("Value", ECP5_MPN, False),
             ("Footprint", f"{_FPLIB}:ECP5_CABGA256", True), ("MPN", ECP5_MPN, True),
             ("LCSC", ECP5_LCSC, True), ("Datasheet", ECP5_DATASHEET, True)]
    return author_symbol(ECP5_MPN, units, props=props, pitch=3.81)


__all__ = [_n for _n in dict(globals()) if not _n.startswith("__")]
