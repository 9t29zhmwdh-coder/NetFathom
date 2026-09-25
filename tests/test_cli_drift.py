"""baseline and changes must scan ports, and changes must scan before it reports."""

from unittest.mock import AsyncMock, patch

from click.testing import CliRunner

from netfathom.cli.baseline import baseline
from netfathom.cli.changes import changes
from netfathom.inventory.service import DEFAULT_DRIFT_PORTS


def _run(command, args, reference_target="10.0.0.0/24"):
    service = AsyncMock()
    service.run_and_persist.return_value = (AsyncMock(id=1), [])
    service.pin_baseline.return_value = AsyncMock(id=1, host_count=0, target="x")
    service.reference_target.return_value = reference_target
    service.get_changes.return_value = []
    service.list_assets.return_value = []
    module = command.callback.__module__
    with patch(f"{module}.InventoryService", return_value=service):
        result = CliRunner().invoke(command, args)
    assert result.exit_code == 0, result.output
    return service


def test_baseline_scans_the_default_ports():
    service = _run(baseline, ["--target", "10.0.0.0/24"])
    service.run_and_persist.assert_awaited_once_with(
        "10.0.0.0/24", discover_kwargs={"port_spec": DEFAULT_DRIFT_PORTS}
    )


def test_changes_rescans_the_baseline_target_first():
    service = _run(changes, [])
    service.run_and_persist.assert_awaited_once_with(
        "10.0.0.0/24", discover_kwargs={"port_spec": DEFAULT_DRIFT_PORTS}
    )
    service.get_changes.assert_awaited_once()


def test_changes_uses_given_target_and_ports():
    service = _run(changes, ["--target", "192.168.1.9", "-p", "22"])
    service.run_and_persist.assert_awaited_once_with(
        "192.168.1.9", discover_kwargs={"port_spec": "22"}
    )


def test_changes_no_scan_only_reports():
    service = _run(changes, ["--no-scan"])
    service.run_and_persist.assert_not_awaited()
    service.get_changes.assert_awaited_once()
