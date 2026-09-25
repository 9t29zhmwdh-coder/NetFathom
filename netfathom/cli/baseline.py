"""netfathom baseline: pin the current scan as the drift-detection baseline."""

from __future__ import annotations

import asyncio

import click
from rich.console import Console

from netfathom.cli.discover import _auto_detect_network
from netfathom.inventory.service import DEFAULT_DRIFT_PORTS, InventoryService

console = Console(stderr=True)


@click.command()
@click.option("--target", default=None, help="Target network/host [default: auto-detect]")
@click.option(
    "-p", "--ports", default=DEFAULT_DRIFT_PORTS, show_default=True, help="Ports to check per host"
)
@click.option("--db-path", default=None, help="Override the SQLite database path")
def baseline(target: str | None, ports: str, db_path: str | None) -> None:
    """Run a fresh scan and pin it as the reference baseline for `netfathom changes`."""
    asyncio.run(_run(target or _auto_detect_network(), ports, db_path))


async def _run(target: str, ports: str, db_path: str | None) -> None:
    from pathlib import Path

    service = InventoryService(db_path=Path(db_path) if db_path else None)
    with console.status(f"[bold green]Scanning {target} for baseline…"):
        run, _changes = await service.run_and_persist(target, discover_kwargs={"port_spec": ports})
        pinned = await service.pin_baseline(run.id)

    console.print(
        f"[green]Baseline pinned:[/green] run #{pinned.id}, {pinned.host_count} hosts "
        f"({pinned.target})"
    )
