"""LPDDR4X x32 200-ball FBGA (JEDEC JESD209-4 dual-channel ballout) — ONE generator, two symbols.

    lpddr4x()                     -> "K4U6E3S4AA-MGCL"      Samsung 16 Gb x32 SDP, SINGLE-rank (placed as U14)
    lpddr4x(variant="generic")    -> "LPDDR4X_x32_FBGA200"  JEDEC generic, rank-1 balls live (library part)

FACTS (D12): facts/lpddr4x-truth.json, cited per ball:
  * Micron MT53E256M32D2DS-046-IT-B-Octopart.pdf Fig 5 p21 "200-Ball Dual-Channel, Single-Rank
    Discrete FBGA (x32 I/O)" + Table 3 p22 ball descriptions (types: CK/CKE/CS/CA/RESET_n Input,
    DQ/DQS/DMI I/O, ZQ Reference, ODT_CA "shall be connected to a valid logic level", DNU
    "grounded or left floating", NC "not internally connected").
  * Samsung SEC_K4UBE3D4AA-MGCL_200F_10x15.pdf (datasheets/, DDP sibling — K4U6E3S4AA's own DS is
    not published) sec 4.2 p10 ballout (rank-1 names ZQ1 A8, CS1_a H3, CKE1_a J5, CKE1_b P5,
    CS1_b R3; DNU G11 K5 K8 N5 N8) + sec 4.3 p11 pad names (JEDEC spelling: DQS0_t_a, CK_c_b,
    ODT_CA_a, RESET_n) + note 2 "ODT pin should connect to VDD2 or VSS".
  The two ballouts agree on all 200 balls except the rank-1/NC class (Micron single-rank = NC).
  Rank: Samsung ordering key (sibling DS sec 3.0 p8) `3D = x32 DDP`; K4U6E3S4AA decodes 6E = 16 Gb,
  3S = x32 single-die -> one die per channel = single rank, so H3 R3 J5 P5 A8 are no_connect on it.

Units (7, pitch 3.81, review verify/symbols-0824/review/lpddr4x.md sec 5 winner):
  1 "LPDDR4X CH A"  DQ[7:0]_a + DQS0/DMI0, DQ[15:8]_a + DQS1/DMI1 left; CA[5:0]_a, CK, CS/CKE, ODT right
  2 "LPDDR4X CH B"  mirror, _b
  3 "LPDDR4X PWR"   VDD1 x8 / VDD2 x24 left; VDDQ x20 + ZQ0/ZQ1/RESET_n right (vendor duplicate names)
  4-6 "LPDDR4X GND n/3"  VSS single left columns 20/20/18 (D9)
  7 "LPDDR4X DNU / NC"   12 DNU + 5 NC, etype no_connect (D10)
Pin count == 200 == footprint pads (asserted). Names = vendor ink verbatim (D6); board roles are
net labels at the instance (boardlib/sheets/ddr.py).
"""
import contextlib as _ctx
import json as _json

from engine import symbols as _esym
from symlib.common import *  # noqa: F401,F403

_TRUTH = _json.load(open(_HERE / "facts/lpddr4x-truth.json"))
_SAM = _TRUTH["samsung_4_2"]          # ball -> vendor name, row-major (ballout reading order)
_MIC = _TRUTH["micron_fig5"]
_PADS = set(_json.load(open(_HERE / "facts/dram-200-ball-positions.json")))

# rank-1 balls: live on the JEDEC generic (Samsung 4.2 names), no_connect on the single-rank MPN
LPDDR4X_RANK1 = ("H3", "R3", "J5", "P5", "A8")          # CS1_a CS1_b CKE1_a CKE1_b ZQ1
LPDDR4X_NC_BALLS = tuple(b for b, n in _SAM.items() if n in ("DNU", "NC"))   # 12 DNU + 5 NC
_VSS = [b for b, n in _SAM.items() if n == "VSS"]                            # 58, row-major
LPDDR4X_VSS_UNITS = (_VSS[:20], _VSS[20:40], _VSS[40:])   # units 4/5/6 — the sheet partitions by THIS
DRAM_MPN = "K4U6E3S4AA-MGCL"
_DS_SAMSUNG = "datasheets/SEC_K4UBE3D4AA-MGCL_200F_10x15.pdf"
_DS_MICRON = "datasheets/MT53E256M32D2DS-046-IT-B-Octopart.pdf"


def _assert_pindata():
    """D12: every pindata.LPDDR4X_* ball exists on the footprint AND its role token matches the
    vendor name on that ball (Samsung 4.2; Micron Fig 5 for every non-rank-1 ball)."""
    def tok(vendor, strip_ch):
        t = vendor.upper()
        return t[:-2] if strip_ch and t.endswith(("_A", "_B")) else t
    seen = {}
    for role, d, ch in (("CHA", P.LPDDR4X_CHA, "a"), ("CHB", P.LPDDR4X_CHB, "b"),
                        ("CTL", P.LPDDR4X_CTL, None)):
        for name, ball in d.items():
            assert ball in _PADS, f"pindata.LPDDR4X_{role}[{name!r}] = {ball}: not a footprint pad"
            assert ball not in seen, f"pindata: ball {ball} listed twice ({seen[ball]} / {name})"
            v = _SAM[ball]
            assert tok(v, ch is not None) == name.upper(), \
                f"pindata.LPDDR4X_{role}[{name!r}] = {ball} but Samsung 4.2 names that ball {v!r}"
            assert ch is None or v.endswith("_" + ch), f"{ball} {v!r} is not channel {ch}"
            if ball not in LPDDR4X_RANK1:
                assert tok(_MIC[ball], ch is not None) == name.upper(), \
                    f"{ball}: Micron Fig 5 says {_MIC[ball]!r}, pindata says {name!r}"
            seen[ball] = name
    for rail, balls in P.LPDDR4X_PWR.items():
        for ball in balls:
            assert ball in _PADS and ball not in seen, f"pindata.LPDDR4X_PWR[{rail}] {ball} bad/dup"
            assert _SAM[ball] == rail == _MIC[ball], \
                f"{ball}: pindata rail {rail}, Samsung {_SAM[ball]!r}, Micron {_MIC[ball]!r}"
            seen[ball] = rail
    assert set(seen) | set(LPDDR4X_NC_BALLS) == _PADS == set(_SAM) == set(_MIC), \
        "pindata + DNU/NC balls do not tile the 200-pad footprint"
    assert len(_PADS) == 200 and len(LPDDR4X_NC_BALLS) == 17 and len(_VSS) == 58


_assert_pindata()


@_ctx.contextmanager
def _pin_len(mm):
    """One device, one stub length. The emitter sizes pin length PER SIDE from the longest pin
    number (4-char AA11 -> 7.62, 3-char -> 5.08), so units of one part get different stubs.
    Scoped override of the emitter floor until author_symbol(pin_len=) lands upstream."""
    se = _esym._se
    old = se.PIN_LEN
    se.PIN_LEN = mm
    try:
        yield
    finally:
        se.PIN_LEN = old


def _ch(ch, rank):
    d = P.LPDDR4X_CHA if ch == "A" else P.LPDDR4X_CHB
    s = ch.lower()

    def pins(keys, etype):
        return [(_SAM[d[k]], d[k], etype) for k in keys]

    def r1(key):
        return "no_connect" if (rank == 1 and d[key] in LPDDR4X_RANK1) else "input"
    odt = P.LPDDR4X_CTL[f"ODT_CA_{ch}"]
    return Unit(
        f"LPDDR4X CH {ch}",
        left=[Group(f"DQ[7:0]_{s}", pins([f"DQ{i}" for i in range(8)], "bidirectional")),
              Group("DQS0 / DMI0", pins(["DQS0_T", "DQS0_C", "DMI0"], "bidirectional")),
              Group(f"DQ[15:8]_{s}", pins([f"DQ{i}" for i in range(8, 16)], "bidirectional")),
              Group("DQS1 / DMI1", pins(["DQS1_T", "DQS1_C", "DMI1"], "bidirectional"))],
        right=[Group(f"CA[5:0]_{s}", pins([f"CA{i}" for i in range(6)], "input")),
               Group("CK", pins(["CK_T", "CK_C"], "input")),
               Group("CS / CKE", pins(["CS0", "CKE0"], "input")
                     + [(_SAM[d["CS1"]], d["CS1"], r1("CS1")),
                        (_SAM[d["CKE1"]], d["CKE1"], r1("CKE1"))]),
               # Micron T3 / Samsung note 2: strapped to VDD2 or VSS at the ball -> passive
               Group("ODT", [(_SAM[odt], odt, "passive")])],
        width=38.1)


def _pwr(rank):
    c = P.LPDDR4X_CTL

    def rail(name):     # vendor duplicate names (VDD1 x8 ...) — one rail = one Group (docs/02)
        return [(name, b, "power_in") for b, n in _SAM.items() if n == name]
    return Unit(
        "LPDDR4X PWR",
        left=[Group("VDD1", rail("VDD1")), Group("VDD2", rail("VDD2"))],
        right=[Group("VDDQ", rail("VDDQ")),
               Group("ZQ / RESET", [("ZQ0", c["ZQ0"], "passive"),
                                    ("ZQ1", c["ZQ1"], "no_connect" if rank == 1 else "passive"),
                                    ("RESET_n", c["RESET_N"], "input")])],
        width=25.4)


def _gnd(k):
    return Unit(f"LPDDR4X GND {k + 1}/3",
                left=[Group("", [("VSS", b, "power_in") for b in LPDDR4X_VSS_UNITS[k]])],
                width=20.32)


def _nc():
    # DNU x12 (both DS agree); NC x5 G11 K5 K8 N5 N8 = Micron Fig 5 "NC" on the single-rank
    # ballout (the Samsung DDP sibling marks the same five DNU) — both etype no_connect.
    return Unit("LPDDR4X DNU / NC",
                left=[Group("DNU", [("DNU", b, "no_connect") for b in LPDDR4X_NC_BALLS
                                    if _MIC[b] == "DNU"]),
                      Group("NC", [("NC", b, "no_connect") for b in LPDDR4X_NC_BALLS
                                   if _MIC[b] == "NC" and b not in LPDDR4X_RANK1])],
                width=20.32)


def lpddr4x(variant=DRAM_MPN):
    """variant="K4U6E3S4AA-MGCL" (default, single-rank) or "generic" (JEDEC, rank-1 live)."""
    generic = variant == "generic"
    rank = 2 if generic else 1
    units = [_ch("A", rank), _ch("B", rank), _pwr(rank), _gnd(0), _gnd(1), _gnd(2), _nc()]
    n = sum(len(g.pins) for u in units for side in (u.left, u.right, u.bottom) for g in side)
    assert n == len(_PADS) == 200, f"LPDDR4X symbol carries {n} pins, footprint has {len(_PADS)} pads"
    if generic:
        name, props = "LPDDR4X_x32_FBGA200", [
            ("Reference", "U", False), ("Value", "LPDDR4X_x32_FBGA200", False),
            ("Footprint", f"{_FPLIB}:LPDDR4X_WFBGA200", True), ("MPN", "", True),
            ("LCSC", "", True), ("Datasheet", _DS_MICRON, True)]
    else:
        name, props = DRAM_MPN, [
            ("Reference", "U", False), ("Value", DRAM_MPN, False),
            ("Footprint", f"{_FPLIB}:LPDDR4X_WFBGA200", True), ("MPN", DRAM_MPN, True),
            ("LCSC", "C2920249", True), ("Datasheet", _DS_SAMSUNG, True)]
    with _pin_len(7.62):
        return author_symbol(name, units, props=props, pitch=3.81)
