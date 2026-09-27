#!/usr/bin/env bash
# Local development, Linux / macOS
set -e

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  # Same hashed lock as CI, so a fresh venv gets exactly the tested versions.
  .venv/bin/python -m pip install --require-hashes -r requirements/ci.txt
  .venv/bin/python -m pip install --no-deps --no-build-isolation -e .
fi

echo "NetFathom venv ready."
echo "Activate: source .venv/bin/activate"
echo "Run:      netfathom --help"
echo ""
echo "Note: ARP sweep and SYN scan require root:"
echo "  sudo .venv/bin/netfathom discover --arp"
