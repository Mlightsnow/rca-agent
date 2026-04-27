"""Allow `python -m rca_agent ...` to dispatch to the CLI."""
from rca_agent.cli import main

raise SystemExit(main())
