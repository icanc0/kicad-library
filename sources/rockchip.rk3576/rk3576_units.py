"""RK3576 unit map — V2 of verify/symbols-0824/review/rk3576.md §7 (owner order 2026-08-24).

Rockchip's own EVB1 unit split (U1000A..V: one unit per power domain / VCCIO domain / PHY),
refined to canon: DDR split per channel + power, PMU split PMUIO0/OSC vs PMUIO1 vs SARADC, GND as
pure 24-ball columns (rk3576.py), every supply group FIRST on its side, GND returns LAST. Titles
are `RK3576 <DS domain>` (D7); captions are DS interface names (<= 16 chars). Sides are balanced
so no half-body is empty; groups of one rail stay contiguous so the sheet's rail buses never
cross (docs/02 "own rail -> own Group"). Balls are looked up by VENDOR NAME (rk3576_facts) so a
typo raises at import — never a silent mis-ball.

Unit numbers (author order): 1..21 = A,B,D..V below (C merged into D), 22..24 = GND 1/3..3/3
(two-sided, 48 + 48 + 48 + 48 + 37 + 36).
"""
from symlib.rk3576_facts import ball_of as B, gpio as G


def _g(bank, letter, lo, hi):
    return [G(bank, letter, i) for i in range(lo, hi + 1)]


def _ddr(ch):
    """One DDRPHY channel: DQ bytes left, CA/CLK/CS/CKE/WCK/ZQ right (LP4 names; LP5 WCK/A6)."""
    dq = lambda lo, hi: [B(f"LP4_DQ{i}_{ch}") for i in range(lo, hi + 1)]   # noqa: E731
    left = [("DQ0-7 DMI0 DQS0", dq(0, 7) + [B(f"LP4_DMI0_{ch}"), B(f"LP4_DQS0P_{ch}"), B(f"LP4_DQS0N_{ch}")]),
            ("DQ8-15 DMI1 DQS1", dq(8, 15) + [B(f"LP4_DMI1_{ch}"), B(f"LP4_DQS1P_{ch}"), B(f"LP4_DQS1N_{ch}")])]
    right = [("CA", [B(f"LP4_A{i}_{ch}") for i in range(6)] + [B(f"LP5_A6_{ch}")]),
             ("CLK", [B(f"LP4_CLKP_{ch}"), B(f"LP4_CLKN_{ch}")]),
             ("CS / CKE", [B(f"LP4_CSN0_{ch}"), B(f"LP4_CSN1_{ch}"), B(f"LP4_CKE0_{ch}"), B(f"LP4_CKE1_{ch}")]),
             ("LP5 WCK", [B(f"LP5_WCK0P_{ch}"), B(f"LP5_WCK0N_{ch}"), B(f"LP5_WCK1P_{ch}"), B(f"LP5_WCK1N_{ch}")]),
             ("ZQ", [B(f"ZQ_{ch}")])]
    return left, right


_A = _ddr("A")
_B = _ddr("B")

# letter -> (title, left groups, right groups); group = (caption, [balls])
UNITS = {
    "A": ("RK3576 DDRPHY CH A", _A[0], _A[1]),
    "B": ("RK3576 DDRPHY CH B", _B[0], _B[1] + [("RESET", [B("LP4_RESET")])]),
    # D = CORE + DDRPHY supplies in ONE unit (guide SYM-ANATOMY-SUPPLY-SPLIT, 2026-08-26: at
    # most 4 supply/GND-only units per symbol — 3 GND blocks + this; the former C unit's DDRPHY
    # rails ride here, PLL AVSS return LAST on the right). Letter C is retired.
    "D": ("RK3576 CORE + DDRPHY PWR",
          [("CPU_BIG DVDD", [B(f"CPU_BIG_DVDD_{i}") for i in range(8)]),
           ("CPU_LIT DVDD", [B(f"CPU_LIT_DVDD_{i}") for i in range(5)]),
           ("NPU DVDD", [B(f"NPU_DVDD_{i}") for i in range(5)]),
           ("DDRPHY DVDD", [B(f"DDRPHY_DVDD_{i}") for i in range(5)]),
           ("PLL DVDD", [B("DDRPHY_PLL_DVDD")]), ("PLL AVDD", [B("DDRPHY_PLL_AVDD1V8")])],
          [("LOGIC DVDD", [B(f"LOGIC_DVDD_{i}") for i in range(7)]),
           ("LOGIC_MEM DVDD", [B(f"LOGIC_MEM_DVDD_{i}") for i in range(2)]),
           ("GPU DVDD", [B(f"GPU_DVDD_{i}") for i in range(5)]),
           ("DDRPHY VDDQ", [B(f"DDRPHY_VDDQ_{i}") for i in range(6)]),
           ("CK VDDQ", [B("DDRPHY_CK_VDDQ")]), ("CKE VDDQ", [B("DDRPHY_CKE_VDDQ")]),
           ("PLL AVSS", [B("DDRPHY_PLL_AVSS")])]),
    "E": ("RK3576 PMUIO0/OSC",
          [("PMUIO0", [B("PMUIO0_VCC1V8")]),
           ("PMU LOGIC", [B("PMU_LOGIC_DVDD0V75_0"), B("PMU_LOGIC_DVDD0V75_1")]),
           ("PLL DVDD", [B("PLL_DVDD0V75")]), ("OTP", [B("OTP_DVDD0V75")]),
           ("PLL AVDD", [B("PLL_AVDD1V8")]), ("OSC AVDD", [B("OSC_AVDD1V8")]),
           ("PLL AVSS / TVSS", [B("PLL_AVSS"), B("TVSS")])],
          [("OSC 24M", [B("OSC_XIN"), B("OSC_XOUT")]), ("RESET", [B("NPOR")]),
           ("GPIO0_A", _g(0, "A", 0, 7))]),
    "F": ("RK3576 PMUIO1",
          [("PMUIO1", [B("PMUIO1_VCC")]), ("GPIO0_B", _g(0, "B", 0, 7))],
          [("GPIO0_C", _g(0, "C", 0, 7)), ("GPIO0_D", _g(0, "D", 0, 5))]),
    "G": ("RK3576 SARADC/TSADC",
          [("SARADC AVDD", [B("SARADC_AVDD1V8")]),
           ("SARADC IN0-3", [B("SARADC_IN0_BOOT"), B("SARADC_IN1"), B("SARADC_IN2"), B("SARADC_IN3")])],
          [("SARADC IN4-7", [B(f"SARADC_IN{i}") for i in range(4, 8)]),
           ("TSADC", [B("TSADC_TEST_OUT_TS")])]),
    "H": ("RK3576 VCCIO0 EMMC",
          [("VCCIO0", [B("VCCIO0_VCC1V8")]), ("EMMC CTL / FSPI0", _g(1, "B", 0, 3))],
          [("EMMC D0-7/FSPI0", _g(1, "A", 0, 7))]),
    "I": ("RK3576 VCCIO1 SDMMC0",
          [("VCCIO1", [B("VCCIO1_VCC")]), ("SDMMC0 D0-3", _g(2, "A", 0, 3))],
          [("SDMMC0 CMD / CLK", _g(2, "A", 4, 5))]),
    "J": ("RK3576 VCCIO2",
          [("VCCIO2", [B("VCCIO2_VCC")]), ("GPIO4_A SAI1/4", _g(4, "A", 2, 7))],
          [("GPIO4_B SAI1", _g(4, "B", 0, 5))]),
    "K": ("RK3576 VCCIO3",
          [("VCCIO3", [B("VCCIO3_VCC")]), ("GPIO1_B4-7 ETH1", _g(1, "B", 4, 7)),
           ("GPIO1_D ETH1", _g(1, "D", 0, 5))],
          [("GPIO1_C FSPI1", _g(1, "C", 0, 7))]),
    "L": ("RK3576 VCCIO4",
          [("VCCIO4", [B("VCCIO4_VCC")]),
           ("GPIO2_A/B VI_CIF", _g(2, "A", 6, 7) + _g(2, "B", 0, 7)),
           ("GPIO3_A VI_CIF", _g(3, "A", 0, 3))],
          [("GPIO2_C VI_CIF", _g(2, "C", 0, 7)), ("GPIO2_D ETH1", _g(2, "D", 0, 7))]),
    "M": ("RK3576 VCCIO5",
          [("VCCIO5", [B("VCCIO5_VCC_0"), B("VCCIO5_VCC_1")]),
           ("GPIO3_A/B LCDC", _g(3, "A", 4, 7) + _g(3, "B", 0, 7)),
           ("GPIO4_A CAM_CLK", _g(4, "A", 0, 1))],
          [("GPIO3_C VO_LCDC", _g(3, "C", 0, 7)), ("GPIO3_D VO_LCDC", _g(3, "D", 0, 7))]),
    "N": ("RK3576 VCCIO6",
          [("VCCIO6", [B("VCCIO6_VCC")]), ("GPIO4_C HDMI CEC", _g(4, "C", 0, 3))],
          [("GPIO4_C SAI4/VP", _g(4, "C", 4, 7))]),
    "O": ("RK3576 VCCIO7 OSC_UFS",
          [("VCCIO7", [B("VCCIO7_VCC")]),
           ("OSC_UFS", [B("OSC_UFS_AVDD"), B("OSC_UFS_XIN"), B("OSC_UFS_XOUT")])],
          [("GPIO4_D UFS", _g(4, "D", 0, 1))]),
    "P": ("RK3576 MIPI DPHY CSI",
          [("CSI1/2 AVDD1V8", [B("MIPI_DPHY_CSI1/2_RX_AVDD1V8")]),
           ("CSI1/2 AVDD0V75", [B("MIPI_DPHY_CSI1/2_RX_AVDD0V75")]),
           ("CSI1 RX", [B(f"MIPI_DPHY_CSI1_RX_{p}") for p in ("D0P", "D0N", "D1P", "D1N", "CLKP", "CLKN")]),
           ("CSI1/CSI2 SHARED", [B("MIPI_DPHY_CSI1_RX_D2P/MIPI_DPHY_CSI2_RX_D0P"),
                                 B("MIPI_DPHY_CSI1_RX_D2N/MIPI_DPHY_CSI2_RX_D0N"),
                                 B("MIPI_DPHY_CSI1_RX_D3P/MIPI_DPHY_CSI2_RX_D1P"),
                                 B("MIPI_DPHY_CSI1_RX_D3N/MIPI_DPHY_CSI2_RX_D1N")]),
           ("CSI2 CLK", [B("MIPI_DPHY_CSI2_RX_CLKP"), B("MIPI_DPHY_CSI2_RX_CLKN")])],
          [("CSI3/4 AVDD1V8", [B("MIPI_DPHY_CSI3/4_RX_AVDD1V8")]),
           ("CSI3/4 AVDD0V75", [B("MIPI_DPHY_CSI3/4_RX_AVDD0V75")]),
           ("CSI3 RX", [B(f"MIPI_DPHY_CSI3_RX_{p}") for p in ("D0P", "D0N", "D1P", "D1N", "CLKP", "CLKN")]),
           ("CSI3/CSI4 SHARED", [B("MIPI_DPHY_CSI3_RX_D2P/MIPI_DPHY_CSI4_RX_D0P"),
                                 B("MIPI_DPHY_CSI3_RX_D2N/MIPI_DPHY_CSI4_RX_D0N"),
                                 B("MIPI_DPHY_CSI3_RX_D3P/MIPI_DPHY_CSI4_RX_D1P"),
                                 B("MIPI_DPHY_CSI3_RX_D3N/MIPI_DPHY_CSI4_RX_D1N")]),
           ("CSI4 CLK", [B("MIPI_DPHY_CSI4_RX_CLKP"), B("MIPI_DPHY_CSI4_RX_CLKN")])]),
    "Q": ("RK3576 MIPI DCPHY",
          [("DCPHY AVDD1V8", [B("MIPI_DCPHY_AVDD1V8")]), ("DCPHY AVDD1V2", [B("MIPI_DCPHY_AVDD1V2")]),
           ("DCPHY AVDD", [B("MIPI_DCPHY_AVDD")]),
           ("CSI0 RX D/C-PHY", [B("MIPI_DPHY_CSI0_RX_D0P/MIPI_CPHY_CSI_RX_TRIO0_B"),
                                B("MIPI_DPHY_CSI0_RX_D0N/MIPI_CPHY_CSI_RX_TRIO0_A"),
                                B("MIPI_DPHY_CSI0_RX_D1P/MIPI_CPHY_CSI_RX_TRIO1_A"),
                                B("MIPI_DPHY_CSI0_RX_D1N/MIPI_CPHY_CSI_RX_TRIO0_C"),
                                B("MIPI_DPHY_CSI0_RX_CLKP/MIPI_CPHY_CSI_RX_TRIO1_C"),
                                B("MIPI_DPHY_CSI0_RX_CLKN/MIPI_CPHY_CSI_RX_TRIO1_B"),
                                B("MIPI_DPHY_CSI0_RX_D2P/MIPI_CPHY_CSI_RX_TRIO2_B"),
                                B("MIPI_DPHY_CSI0_RX_D2N/MIPI_CPHY_CSI_RX_TRIO2_A"),
                                B("MIPI_DPHY_CSI0_RX_D3P/NO_USE"),
                                B("MIPI_DPHY_CSI0_RX_D3N/MIPI_CPHY_CSI_RX_TRIO2_C")])],
          [("DCPHY VREG", [B("MIPI_DCPHY_VREG")]),
           ("DSI TX D/C-PHY", [B("MIPI_DPHY_DSI_TX_D0P/MIPI_CPHY_DSI_TX_TRIO0_B"),
                               B("MIPI_DPHY_DSI_TX_D0N/MIPI_CPHY_DSI_TX_TRIO0_A"),
                               B("MIPI_DPHY_DSI_TX_D1P/MIPI_CPHY_DSI_TX_TRIO1_A"),
                               B("MIPI_DPHY_DSI_TX_D1N/MIPI_CPHY_DSI_TX_TRIO0_C"),
                               B("MIPI_DPHY_DSI_TX_CLKP/MIPI_CPHY_DSI_TX_TRIO1_C"),
                               B("MIPI_DPHY_DSI_TX_CLKN/MIPI_CPHY_DSI_TX_TRIO1_B"),
                               B("MIPI_DPHY_DSI_TX_D2P/MIPI_CPHY_DSI_TX_TRIO2_B"),
                               B("MIPI_DPHY_DSI_TX_D2N/MIPI_CPHY_DSI_TX_TRIO2_A"),
                               B("MIPI_DPHY_DSI_TX_D3P/NO_USE"),
                               B("MIPI_DPHY_DSI_TX_D3N/MIPI_CPHY_DSI_TX_TRIO2_C")])]),
    "R": ("RK3576 USB3 OTG0 DP",
          [("PHY AVDD1V8", [B("USB3_OTG0_DP_TX_AVDD1V8")]),
           ("PHY A/DVDD0V85", [B("USB3_OTG0_DP_TX_AVDD0V85"), B("USB3_OTG0_DP_TX_DVDD0V85")]),
           ("SSRX1", [B("USB3_OTG0_SSRX1P/DP_TX_D0P"), B("USB3_OTG0_SSRX1N/DP_TX_D0N")]),
           ("SSRX2", [B("USB3_OTG0_SSRX2P/DP_TX_D2P"), B("USB3_OTG0_SSRX2N/DP_TX_D2N")])],
          [("SSTX1", [B("USB3_OTG0_SSTX1P/DP_TX_D1P"), B("USB3_OTG0_SSTX1N/DP_TX_D1N")]),
           ("SSTX2", [B("USB3_OTG0_SSTX2P/DP_TX_D3P"), B("USB3_OTG0_SSTX2N/DP_TX_D3N")]),
           ("DP AUX", [B("DP_TX_AUXP"), B("DP_TX_AUXN")]),
           ("REXT", [B("USB3_OTG0_REXT/DP_TX_REXT")])]),
    "S": ("RK3576 USB2 OTG",
          [("PHY AVDD3V3", [B("USB2_OTG_AVDD3V3")]), ("PHY AVDD1V8", [B("USB2_OTG_AVDD1V8")]),
           ("PHY DVDD0V75", [B("USB2_OTG_DVDD0V75")]),
           ("OTG0", [B("USB2_OTG0_DP"), B("USB2_OTG0_DM"), B("USB2_OTG0_ID"),
                     B("USB2_OTG0_VBUSDET"), B("USB2_OTG0_REXT")])],
          [("OTG1", [B("USB2_OTG1_DP"), B("USB2_OTG1_DM"), B("USB2_OTG1_ID"),
                     B("USB2_OTG1_VBUSDET"), B("USB2_OTG1_REXT")])]),
    "T": ("RK3576 PCIE/SATA/OTG1",
          [("PCIE AVDD1V8", [B("PCIE0_SATA0_AVDD1V8"), B("PCIE1_SATA1_USB3_OTG1_AVDD1V8")]),
           ("PCIE AVDD0V85", [B("PCIE0_SATA0_AVDD0V85"), B("PCIE1_SATA1_USB3_OTG1_AVDD0V85")]),
           ("PCIE0/SATA0 RX", [B("PCIE0_RXP/SATA0_RXP"), B("PCIE0_RXN/SATA0_RXN")]),
           ("PCIE1/SATA1 RX", [B("PCIE1_RXP/SATA1_RXP/USB3_OTG1_SSRXP"),
                               B("PCIE1_RXN/SATA1_RXN/USB3_OTG1_SSRXN")])],
          [("PCIE0/SATA0 TX", [B("PCIE0_TXP/SATA0_TXP"), B("PCIE0_TXN/SATA0_TXN")]),
           ("PCIE0 REFCLK", [B("PCIE0_REFCLKP"), B("PCIE0_REFCLKN")]),
           ("PCIE1/SATA1 TX", [B("PCIE1_TXP/SATA1_TXP/USB3_OTG1_SSTXP"),
                               B("PCIE1_TXN/SATA1_TXN/USB3_OTG1_SSTXN")]),
           ("PCIE1 REFCLK", [B("PCIE1_REFCLKP"), B("PCIE1_REFCLKN")])]),
    "U": ("RK3576 HDMI/EDP TX",
          [("PHY AVDD 1V8", [B("HDMI_TX_EDP_TX_AVDDIO1V8"), B("HDMI_TX_EDP_TX_AVDDCMN1V8")]),
           ("PHY AVDD 0V75", [B("HDMI_TX_EDP_TX_AVDDD0V75"), B("HDMI_TX_EDP_TX_AVDDC0V75")]),
           ("SBD / AUX", [B("HDMI_TX_SBDP/EDP_TX_AUXP"), B("HDMI_TX_SBDN/EDP_TX_AUXN")]),
           ("REXT", [B("HDMI_TX_REXT/EDP_TX_REXT")])],
          [("TX D0-3", [B(f"HDMI_TX_D{i}{p}/EDP_TX_D{i}{p}") for i in range(4) for p in "PN"])]),
    "V": ("RK3576 UFS",
          [("PHY AVDD1V8", [B("UFS_AVDD1V8")]), ("PHY AVDD0V85", [B("UFS_AVDD0V85")]),
           ("RX", [B("UFS_RX_D0P"), B("UFS_RX_D0N"), B("UFS_RX_D1P"), B("UFS_RX_D1N")]),
           ("REXT", [B("UFS_TX_REXT")])],
          [("TX", [B("UFS_TX_D0P"), B("UFS_TX_D0N"), B("UFS_TX_D1P"), B("UFS_TX_D1N")])]),
}

LETTERS = "ABDEFGHIJKLMNOPQRSTUV"   # C retired 2026-08-26 (merged into D)
assert list(UNITS) == list(LETTERS)

__all__ = ["UNITS", "LETTERS"]
