# AW35645 (Awinic) — 10-ch 2:1 MIPI D-PHY/C-PHY switch

Authored on hydra (boardlib/sheets/mux.py) 2026-08-28, promoted same day.
- MPN AW35645FBR, LCSC C5125896 (live, ¥1.43 @ 2026-08-23 sweep), FCBGA/DSBGA-36
  2.4x2.4x0.4 mm.
- Ball map verified TWICE: DS V1.1 pin table (AW35645-DS-V1.1.pdf, pp.2-3) AND the
  vendor EasyEDA symbol for C5125896 — full agreement.
- Truth table: OEB=H -> Hi-Z; OEB=L: SEL=L -> side A, SEL=H -> side B. SEL/OEB must
  never float (DS p6) — strap or pull them.
- Land: central-agent:AW35645_DSBGA36 = the vendor EasyEDA/JLC land (easyeda2kicad);
  3D: footprints/3dmodels/AW35645_DSBGA36.step.
