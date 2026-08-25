"""RK806 — Rockchip 10-buck / 11-LDO PMIC, QFN68 7x7 0.35 (RK806-1/-2/-3 and RK806S-5 are OTP
programs of ONE die; the pinout is family-wide, so the library key is the family "RK806" and the
Value/MPN carries the variant — decision D13, review verify/symbols-0824/review/rk806s5.md §5).

FACTS  facts/rk806s5-pins.json = RK806 Datasheet V1.4 (datasheets/RK806-Datasheet-V1.4.pdf):
  §2.7 "Pinout Number Order" pp.15-16 (name / I-O / description per pad), §2.6 Fig 2-2 p14 (pin 1
  top of the left column, 18 bottom-left, 35 bottom-right, 52 top-right, ePAD = 69), §1.2 Feature
  p7 (BUCK1 6.5A, BUCK2/3/4 5A, BUCK5-10 3A, NLDO1/2/5 + PLDO2/3/5 + VCCIO 300mA, NLDO3/4 +
  PLDO1/4 500mA max), §1.3 block diagram p9 (VCCA -> PLDO6 -> VCCIO).
  pindata.RK806_PINS (the sheets' number->role dict) is ASSERTED against those facts at import
  (_assert_facts): all 69 pads present, every role token == the DS name token.

NAMES  DS §2.7 verbatim: mux pins keep both functions (MOSI/SDA, MISO/PWRCTRL3, CLK/SCL), the
  doubled pads keep the vendor name (VCC1 VCC1, SW1 SW1, VCC2 VCC2, SW2 SW2 — numbers stay
  unique), ePAD as printed. ONE deliberate deviation: the §2.7 table prints "PWRCRTLn"; the DS
  revision note 6 and every register/§4 mention spell PWRCTRLn, so the symbol does too.

UNITS  1..10 = BUCK1..BUCK10 (one tile per stage so a sheet draws SW -> L -> VOUT inline, owner
  08-20; L25 anatomy VOUT above SW above FB), 11 = LDO, 12 = CONTROL. Titles "RK806 <DS domain>"
  (D7); captions = DS section names + the §1.2 rating; pitch 7.62 (owner order 08-20 — room for
  the inline passives — kept; the dead ink was removed instead: no caption repeats a pin name).

ETYPES (docs/02 + D11)      power_in  VCC1..14, VCCA, ePAD
  power_out                 PLDO1..5, NLDO1..5, VCCIO (single-pin regulator outputs)
  passive                   SW1..10 (switch node; the two SW1 / SW2 pads are PARALLELED — two
                            power_out on one net is an ERC conflict), VOUTn / FBn (sense pins on a
                            PWR_FLAGged rail), CS (SPI/I2C strap), PWRON (key, internal 45K
                            pull-up), VDC (off-board detect), EXT_EN (Master/Slave strap; the ext
                            DCDC enable it also drives lands on passive EN pins)
  bidirectional             MOSI/SDA, MISO/PWRCTRL3, RESETB, PWRCTRL1/2, SYNC, SYNC_CLK (DS I/O)
  input                     CLK/SCL — DS I/O column "I": the RK806 is a pure slave in both bus
                            modes and never sources the clock; the host pin (any SoC/MCU) is
                            bidirectional, so ERC stays clean, and a clock-less bus becomes an
                            ERC error instead of silence. (bidirectional would also pass.)
  open_collector            INT — DS "O" with a 10K pull-up in every §1.4 typical application.
"""
import re as _re

from symlib.common import *  # noqa: F401,F403

_FACTS = _HERE / "facts" / "rk806s5-pins.json"


def _assert_facts():
    """pindata.RK806_PINS vs facts (DS §2.7): every pad 1..69 present, role token == DS token.
    Token rule: case-folded, the DS table's PWRCRTL typo normalised, a trailing _1/_2 duplicate
    suffix dropped (VCC1_1 -> VCC1), '_' == '/' (MOSI_SDA == MOSI/SDA)."""
    rows = _json.load(open(_FACTS))["pins"]
    by_num = {int(r["pin"]): r for r in rows}
    assert sorted(by_num) == list(range(1, 70)), "RK806 facts must list pads 1..69"
    assert sorted(P.RK806_PINS) == list(range(1, 70)), "pindata.RK806_PINS must cover pads 1..69"

    def tok(s):
        s = s.upper().replace("PWRCRTL", "PWRCTRL")
        return _re.sub(r"_[12]$", "", s).replace("_", "/")

    for num, role in P.RK806_PINS.items():
        ds = by_num[num]["ds_name"]
        assert tok(role) == tok(ds), f"RK806 pin {num}: pindata {role!r} != DS {ds!r}"
    return {num: r["ds_name"].replace("PWRCRTL", "PWRCTRL") for num, r in by_num.items()}


_NAME = _assert_facts()                       # pad number -> vendor pin name (DS §2.7)
_NUM = {role: num for num, role in P.RK806_PINS.items()}   # sheet role -> pad number


def _pin(role, etype):
    num = _NUM[role]
    return (_NAME[num], str(num), etype)


# k: (supply roles, VOUT, SW roles, FB role or None, §1.2 rating)
_BUCK = {
    1: (["VCC1_1", "VCC1_2"], "VOUT1", ["SW1_1", "SW1_2"], "FB1", "6.5A"),
    2: (["VCC2_1", "VCC2_2"], "VOUT2", ["SW2_1", "SW2_2"], "FB2", "5A"),
    3: (["VCC3"], "VOUT3", ["SW3"], None, "5A"),
    4: (["VCC4"], "VOUT4", ["SW4"], None, "5A"),
    5: (["VCC5"], "VOUT5", ["SW5"], "FB5", "3A"),
    6: (["VCC6"], "VOUT6", ["SW6"], "FB6", "3A"),
    7: (["VCC7"], "VOUT7", ["SW7"], None, "3A"),
    8: (["VCC8"], "VOUT8", ["SW8"], None, "3A"),
    9: (["VCC9"], "VOUT9", ["SW9"], "FB9", "3A"),
    10: (["VCC10"], "VOUT10", ["SW10"], None, "3A"),
}


def _buck_unit(k):
    vccs, vout, sws, fb, rating = _BUCK[k]
    # right column top-to-bottom VOUT -> SW -> FB (owner 08-20 / L25: the divider drops straight
    # down under the output run, the inductor returns up from SW to VOUT). Left: the supply pad(s)
    # uncaptioned — "VCCn" over a VCCn pin is dead ink; the title carries the domain.
    outs = [_pin(vout, "passive")] + [_pin(s, "passive") for s in sws]
    if fb:
        outs.append(_pin(fb, "passive"))
    return Unit(f"RK806 BUCK{k}",
                left=[Group("", [_pin(v, "power_in") for v in vccs])],
                right=[Group(f"{rating} MAX", outs)])


def _ldo_unit():
    # One supply rail = one Group (docs/02), captioned by WHAT IT FEEDS (DS §2.7 "Power supply of
    # PLDO1/2/3"); spacer rows put each VCC pin directly opposite the first output it feeds and
    # every caption row level with its block's caption. Right captions = §1.2 ratings in pin order.
    sp = Group("", [])
    return Unit("RK806 LDO",
                left=[Group("PLDO1/2/3", [_pin("VCC11", "power_in")]), sp, sp,
                      Group("PLDO4/5", [_pin("VCC12", "power_in")]), sp,
                      Group("NLDO1/2/3", [_pin("VCC13", "power_in")]), sp, sp,
                      Group("NLDO4/5", [_pin("VCC14", "power_in")])],
                right=[Group("500/300/300mA", [_pin("PLDO1", "power_out"), _pin("PLDO2", "power_out"),
                                               _pin("PLDO3", "power_out")]),
                       Group("500/300mA", [_pin("PLDO4", "power_out"), _pin("PLDO5", "power_out")]),
                       Group("300/300/500mA", [_pin("NLDO1", "power_out"), _pin("NLDO2", "power_out"),
                                               _pin("NLDO3", "power_out")]),
                       Group("500/300mA", [_pin("NLDO4", "power_out"), _pin("NLDO5", "power_out")])])


def _control_unit():
    # A9: supply top-left (VCCA, captioned by what it feeds — DS "Power supply of
    # PLDO6/RESETB/INT"), inputs/buses left, outputs right with VCCIO (= PLDO6, fed from VCCA per
    # the §1.3 block diagram) directly opposite VCCA; the single ePAD ground centred on the bottom.
    return Unit("RK806 CONTROL",
                left=[Group("PLDO6/RESETB/INT", [_pin("VCCA", "power_in")]),
                      Group("SPI/I2C", [_pin("MOSI_SDA", "bidirectional"),
                                        _pin("MISO_PWRCTRL3", "bidirectional"),
                                        _pin("CLK_SCL", "input"), _pin("CS", "passive")]),
                      Group("POWER CONTROL", [_pin("PWRON", "passive"), _pin("VDC", "passive"),
                                              _pin("PWRCTRL1", "bidirectional"),
                                              _pin("PWRCTRL2", "bidirectional")]),
                      Group("DUAL PMIC", [_pin("SYNC", "bidirectional"),
                                          _pin("SYNC_CLK", "bidirectional")])],
                right=[Group("PLDO6 300mA", [_pin("VCCIO", "power_out")]),
                       Group("TO AP / EXT DCDC", [_pin("INT", "open_collector"),
                                                 _pin("RESETB", "bidirectional"),
                                                 _pin("EXT_EN", "passive")])],
                bottom=[Group("", [_pin("EPAD", "power_in")])])


def rk806():
    """Symbol "RK806": units 1..10 BUCK1..10, 11 LDO, 12 CONTROL; Value/MPN RK806S-5 (hydra's
    variant), LCSC C49174044, footprint hydra_authored:RK806_QFN68 (69 pads incl. ePAD 69)."""
    units = [_buck_unit(k) for k in range(1, 11)] + [_ldo_unit(), _control_unit()]
    assert sum(len(g.pins) for u in units for s in (u.left, u.right, u.bottom) for g in s) == 69
    props = [("Reference", "U", False), ("Value", "RK806S-5", False),
             ("Footprint", f"{_FPLIB}:RK806_QFN68", True), ("MPN", "RK806S-5", True),
             ("LCSC", "C49174044", True), ("Datasheet", "RK806-Datasheet-V1.4.pdf", True)]
    return author_symbol("RK806", units, props=props,
                         pitch=7.62)   # owner 08-20 "make the symbols bigger": room for the
                                       # inline SW->L->VOUT passives without collision gymnastics


rk806s5 = rk806      # legacy name (symbols_hydra / env.py callers)

__all__ = [_n for _n in dict(globals()) if not _n.startswith("__")]
