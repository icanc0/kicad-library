"""RK3576 ball facts — the ONE source for the authored symbol (D6/D12, owner order 2026-08-24).

facts/rk3576-balls.json = Rockchip RK3576 Datasheet V1.6 (datasheets/RK3576-Datasheet-V1.6.pdf)
§2.6 Table 2-1 "Pin Number Order Information", PDF pp.30-45 (text mirror datasheets/rk3576-ds-
v16.txt line 2779+), re-parsed two-column by verify/symbols-0824/review/rk3576-parse_pins.py:
{ball: {name, kind, evb_unit, domain}}, 698 balls (FCCSP698L). `domain` (VCCIOn/PMUIOn) is the
EVB1 "IO Power Domain Map" (RK3576-EVB1-MV10-V1.0 sch p.6 + units U1000C..K) — the DS has no
per-ball domain column. `kind`: gnd 268 / power 90 / io 148 / ddr 81 / serdes 53 / mipi 44 /
analog 14. No ball on this package is NC (AK24/AL19 "NO_USE" is the C-PHY personality only).

Vendor pin NAME (D6): the DS token verbatim —
  io     -> the trailing `GPIOx_yz_[dpuz]` iomux token (the ball's identity across modes)
  ddr    -> the first token (`LP4_*`; the LP4X/LP5 aliases are the same ball)
  others -> the full DS string (`MIPI_DPHY_CSI3_RX_D2P/MIPI_DPHY_CSI4_RX_D0P`, `USB3_OTG0_SSRX1P/
            DP_TX_D0P`, `MIPI_DPHY_CSI1/2_RX_AVDD0V75` — the slash is part of the vendor name)
Electrical type (D11 / docs/02): supplies power_in; MIPI_DCPHY_VREG power_out (EVB p.15: a
regulator OUTPUT with a 1 uF cap only); GPIO bidirectional; RX lanes (DPHY/DCPHY CSI, USB3 SSRX,
PCIe/SATA RX, UFS RX, PCIe REFCLK) input; TX lanes (DSI, SSTX, PCIe TX, HDMI/eDP TX, UFS TX)
output; USB2 DP/DM, DP AUX, HDMI SBD bidirectional; DDR DQ/DMI/DQS bidirectional, CA/CLK/CSN/
CKE/WCK/RESET output; ZQ/REXT/ID/VBUSDET/SARADC/TSADC/OSC passive; NPOR input (PMIC RESETB
drives it); VSS/AVSS/AVSS1/TVSS/PLL_AVSS power_in.
"""
import json as _json
import pathlib as _pl
import re as _re

_HERE = _pl.Path(__file__).resolve().parent.parent
FACTS_PATH = _HERE / "facts" / "rk3576-balls.json"
BALLS = _json.load(open(FACTS_PATH))
assert len(BALLS) == 698, f"facts/rk3576-balls.json: {len(BALLS)} balls (DS Table 2-1: 698)"

_GPIO_TOK = _re.compile(r"^GPIO\d_[A-D]\d_[dpuz]$")


def vendor_name(ball):
    """The DS pin name for the symbol (rules in the module docstring)."""
    rec = BALLS[ball]
    toks = rec["name"].split("/")
    if rec["kind"] == "io":
        assert _GPIO_TOK.match(toks[-1]), f"{ball}: io ball without a GPIO token: {rec['name']}"
        return toks[-1]
    if rec["kind"] == "ddr":
        return toks[0]
    return rec["name"]


def etype(ball):
    """docs/02 electrical type from the vendor name + kind (see module docstring)."""
    rec = BALLS[ball]
    kind, name = rec["kind"], vendor_name(ball)
    first = name.split("/")[0]
    if kind == "gnd":
        return "power_in"
    if kind == "power":
        return "power_out" if name == "MIPI_DCPHY_VREG" else "power_in"
    if kind == "io":
        return "bidirectional"
    if kind == "ddr":
        if name.startswith("ZQ_"):
            return "passive"
        return "bidirectional" if _re.match(r"LP4_(DQ|DMI|DQS)", name) else "output"
    if kind == "mipi":
        return "input" if "_RX_" in first else "output"
    if kind == "serdes":
        if any(t in first for t in ("REXT", "VBUSDET")) or first.endswith("_ID"):
            return "passive"
        if "AUX" in name or "SBD" in first or _re.match(r"USB2_OTG\d_D[PM]$", first):
            return "bidirectional"
        return "input" if ("RX" in first or "REFCLK" in first) else "output"
    if kind == "analog":
        return "input" if name == "NPOR" else "passive"
    raise ValueError(f"{ball}: unknown kind {kind!r}")


NAME_TO_BALL = {}
for _b in BALLS:
    _n = vendor_name(_b)
    assert _n not in NAME_TO_BALL, f"vendor name {_n!r} on two balls: {NAME_TO_BALL[_n]}, {_b}"
    NAME_TO_BALL[_n] = _b


def ball_of(name):
    """Ball by exact vendor name (raises on a typo — never a silent miss)."""
    return NAME_TO_BALL[name]


def gpio(bank, letter, idx):
    """Ball of GPIO<bank>_<letter><idx> (the DS suffix _d/_u/_z/_p varies per ball)."""
    hits = [b for n, b in NAME_TO_BALL.items() if n.startswith(f"GPIO{bank}_{letter}{idx}_")]
    assert len(hits) == 1, f"GPIO{bank}_{letter}{idx}: {hits}"
    return hits[0]


# ---------------------------------------------------------------------------------------------
# D12: pindata.py role dicts are the sheets' netmap keys; they must AGREE with the DS facts —
# every ball exists and the hydra role name maps to a token of the DS iomux string.
# ---------------------------------------------------------------------------------------------
_ALIAS = [   # (regex on the pindata key, DS token template) — first match wins
    (r"^([AB])_DQ(\d+)$", r"LP4_DQ\2_\1"), (r"^([AB])_DM(\d)$", r"LP4_DMI\2_\1"),
    (r"^([AB])_DQS(\d)([PN])$", r"LP4_DQS\2\3_\1"), (r"^([AB])_CA(\d)$", r"LP4_A\2_\1"),
    (r"^([AB])_CK([PN])$", r"LP4_CLK\2_\1"), (r"^([AB])_CS(\d)$", r"LP4_CSN\2_\1"),
    (r"^([AB])_CKE(\d)$", r"LP4_CKE\2_\1"), (r"^DDR_RESET$", "LP4_RESET"),
    (r"^CSI(\d)_D(\d)([PN])$", r"MIPI_DPHY_CSI\1_RX_D\2\3"),
    (r"^CSI(\d)_CK([PN])$", r"MIPI_DPHY_CSI\1_RX_CLK\2"),
    (r"^CSI(\d)(\d)_(AVDD\w+)$", r"MIPI_DPHY_CSI\1/\2_RX_\3"), (r"^DCPHY_(\w+)$", r"MIPI_DCPHY_\1"),
    (r"^SS(TX|RX)(\d)([PN])$", r"USB3_OTG0_SS\1\2\3"), (r"^OTG0_(\w+)$", r"USB2_OTG0_\1"),
    (r"^USB3_REXT$", "USB3_OTG0_REXT"), (r"^USB3_(\w+)$", r"USB3_OTG0_DP_TX_\1"),
    (r"^USB2_(\w+)$", r"USB2_OTG_\1"),
    (r"^SD_(\w+)$", r"SDMMC0_\1"), (r"^FSPI_CSN$", "FSPI1_CSN0"), (r"^FSPI_(\w+)$", r"FSPI1_\1"),
    (r"^A_PROGRAMN$", "GPIO1_C0"), (r"^B_PROGRAMN$", "GPIO1_C1"), (r"^A_INITN$", "GPIO1_D2"),
    (r"^B_INITN$", "GPIO1_D3"), (r"^A_DONE$", "GPIO1_D0"), (r"^B_DONE$", "GPIO1_D1"),
    (r"^ETH_RESET$", "GPIO0_C2"), (r"^ETH_INT$", "GPIO0_C6"),
    (r"^(TXD\d|RXD\d|TXCLK|TXCTL|RXCLK|RXCTL|MDC|MDIO)$", r"ETH0_\1"),
    (r"^CAM_CLK(\d)$", r"CAM_CLK\1_OUT"), (r"^CAM_RST0$", "GPIO3_A4"), (r"^CAM_RST1$", "GPIO3_C5"),
    (r"^PMUIO0_VCC$", "PMUIO0_VCC1V8"), (r"^PMU_DVDD_(\d)$", r"PMU_LOGIC_DVDD0V75_\1"),
    (r"^SARADC_VIN(\d)$", r"SARADC_IN\1"), (r"^TSADC_TS$", "TSADC_TEST_OUT_TS"),
    (r"^OTP_VDD0V75$", "OTP_DVDD0V75"),
    (r"^PLL_(DVDD|AVDD1V8|AVSS)$", r"DDRPHY_PLL_\1"), (r"^(CKE|CK)_VDDQ$", r"DDRPHY_\1_VDDQ"),
    (r"^HDMI_(\w+)$", r"HDMI_TX_EDP_TX_\1"), (r"^PCIE1_(\w+)$", r"PCIE1_SATA1_USB3_OTG1_\1"),
    (r"^PCIE0_(\w+)$", r"PCIE0_SATA0_\1"),
    (r"^VCCIO0$", "VCCIO0_VCC1V8"), (r"^VCCIO5_(\d)$", r"VCCIO5_VCC_\1"), (r"^VCCIO(\d)$", r"VCCIO\1_VCC"),
]
_LIST_PREFIX = {"CPU_BIG": "CPU_BIG_DVDD_", "CPU_LIT": "CPU_LIT_DVDD_", "LOGIC": "LOGIC_DVDD_",
                "LOGIC_MEM": "LOGIC_MEM_DVDD_", "GPU": "GPU_DVDD_", "NPU": "NPU_DVDD_",
                "DVDD": "DDRPHY_DVDD_", "VDDQ": "DDRPHY_VDDQ_"}


def _token_ok(expect, ball):
    toks = [_re.sub(r"_M\d$", "", t) for t in BALLS[ball]["name"].split("/")]
    return any(t == expect or t.startswith(expect + "_") or (expect.endswith("_") and t.startswith(expect))
               for t in toks) or (expect == BALLS[ball]["name"])


def _expect(key):
    for pat, rep in _ALIAS:
        if _re.match(pat, key):
            return _re.sub(pat, rep, key)
    return key


def assert_pindata(P):
    """Every pindata.RK3576_* ball exists in facts and its role name matches a DS token."""
    bad = []
    for dname in sorted(n for n in dir(P) if n.startswith("RK3576_")):
        d = getattr(P, dname)
        items = enumerate(d) if isinstance(d, list) else d.items()
        for key, val in items:
            balls = [x[0] if isinstance(x, tuple) else x for x in (val if isinstance(val, list) else [val])]
            for ball in balls:
                if ball not in BALLS:
                    bad.append(f"{dname}[{key!r}]: ball {ball!r} not in DS Table 2-1")
                    continue
                if dname == "RK3576_VSS_EXT" or key == "VSS":
                    ok = BALLS[ball]["kind"] == "gnd"
                elif isinstance(key, str) and key in _LIST_PREFIX and isinstance(val, list):
                    ok = _token_ok(_LIST_PREFIX[key], ball)
                else:   # verbatim first (PLL_AVSS in SYS), then the alias (PLL_AVSS in DDR_PWR)
                    ok = _token_ok(str(key), ball) or _token_ok(_expect(str(key)), ball)
                if not ok:
                    bad.append(f"{dname}[{key!r}] -> {ball}: {BALLS[ball]['name']!r} has no token {_expect(str(key))!r}")
    assert not bad, "pindata.py disagrees with facts/rk3576-balls.json:\n  " + "\n  ".join(bad)


__all__ = ["BALLS", "FACTS_PATH", "NAME_TO_BALL", "vendor_name", "etype", "ball_of", "gpio",
           "assert_pindata"]
