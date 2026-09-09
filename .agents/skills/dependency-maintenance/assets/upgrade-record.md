# Dependency upgrade record

Copy for a material upgrade; fill from actual evidence.

| Field | Record |
| --- | --- |
| Package/action/hook and consumers | Manifest path, call sites and current version/ref |
| Selected version and source | Official release, verified ref, checked date |
| Reason | Required capability, resolved defect or advisory |
| Compatibility | Runtime/API/configuration changes and migration steps |
| Resolution | Package manager, lockfile, relevant transitive/build changes |
| Evidence | Baseline and candidate commands, results, CI revision |
| Recovery | Previous version/ref and compatible rollback procedure |
| Decision | Adopt, reject or blocked, with remaining uncertainty |
