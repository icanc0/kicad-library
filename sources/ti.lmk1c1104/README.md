# LMK1C1104 (TI) — 1:4 LVCMOS clock buffer, 1.8-3.3 V

Authored on hydra (boardlib/sheets/mux.py) 2026-08-28, promoted same day.
- MPN LMK1C1104PWR, LCSC C1855734 (3.6k stock), TSSOP-8.
- Pinout verified: TI DS (LMK1C1104-DS.pdf) + the vendor EasyEDA symbol:
  1 CLKIN, 2 1G (enable, HIGH=run; outputs LOW when low), 3 Y0, 4 GND, 5 Y2,
  6 VDD, 7 Y3, 8 Y1.
- Chosen over CDCLVC1104 (same footprint family): the CDC part is 2.5/3.3 V only;
  camera MCLK domains need 1.8 V.
- Land: central-agent:LMK1C1104_TSSOP8 (vendor EasyEDA/JLC land);
  3D: footprints/3dmodels/LMK1C1104_TSSOP8.step.
