# Notice

This repository contains a behavioral reconstruction and static-analysis
artifact for a third-party Windows application. It is not affiliated with,
sponsored by, or endorsed by the original vendor.

## Rights

- Rights to the original application, binaries, trademarks, UI resources and
  third-party libraries remain with their respective owners.
- The recovered Python files are readable behavioral reconstructions. They are
  not a byte-for-byte copy of the original source and may contain inferred
  control flow.
- No license is granted for the original application or its bundled resources.
  Do not redistribute the original binary or bundled libraries without the
  rights holder's permission.

## Safety

- Do not execute the original `运营猫.exe`, `static_hybrid*.exe`, or any recovered
  entry point outside an isolated analysis environment.
- The target contains anti-debug and shutdown paths. Dynamic execution on a
  host machine is unsafe.
- The repository documents destructive behavior for defensive analysis only.
  It does not provide instructions or tooling for unauthorized access,
  license forgery, credential theft, or service disruption.
- Real server-side signatures, private keys and account data are not included.
  The offline lab uses synthetic fixtures only.

If you are a rights holder and want content removed, open an issue or contact
the repository owner.
