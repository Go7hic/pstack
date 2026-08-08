# Portability audit fixtures

`bad/` samples must trip at least one `PORTABILITY_PATTERNS` rule.
`good/` samples must trip none.

`scripts/audit_portability.py` fails if a pattern lacks bad coverage or a good fixture regresses.
