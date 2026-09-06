#!/usr/bin/env python3
"""Validate every repository patch with hardware disabled."""

from __future__ import annotations

import io
import json
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RACK = Path("/Applications/VCV Rack 2 Pro.app/Contents/MacOS/Rack")
PLUGINS = Path.home() / "Library/Application Support/Rack2/plugins-mac-arm64"
ZSTD_CANDIDATES = [
    shutil.which("zstd"),
    str(
        Path.home()
        / ".cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin/zstd"
    ),
]
ZSTD = next((Path(path) for path in ZSTD_CANDIDATES if path and Path(path).exists()), None)


def read_archive(path: Path) -> dict:
    raw = subprocess.run([str(ZSTD), "-d", "-q", "-c", str(path)], check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        member = next(item for item in archive.getmembers() if item.name == "patch.json")
        return json.load(archive.extractfile(member))


def write_archive(patch: dict, path: Path) -> None:
    payload = json.dumps(patch, indent=2).encode()
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        member = tarfile.TarInfo("patch.json")
        member.size = len(payload)
        archive.addfile(member, io.BytesIO(payload))
    subprocess.run([str(ZSTD), "-q", "-f", "-o", str(path)], input=buffer.getvalue(), check=True)


def silence_hardware(patch: dict) -> dict:
    mcp_ids = {
        item["id"]
        for item in patch.get("modules", [])
        if item.get("plugin") == "VCVRackMcpServer"
    }
    patch["modules"] = [item for item in patch.get("modules", []) if item["id"] not in mcp_ids]
    patch["cables"] = [
        cable
        for cable in patch.get("cables", [])
        if cable.get("outputModuleId") not in mcp_ids and cable.get("inputModuleId") not in mcp_ids
    ]
    for item in patch["modules"]:
        if item.get("plugin") != "Core":
            continue
        data = item.setdefault("data", {})
        if item.get("model", "").startswith("Audio"):
            data.setdefault("audio", {}).update({"driver": -1, "deviceName": ""})
        if item.get("model", "").startswith("MIDI"):
            data.setdefault("midi", {}).update({"driver": -1, "deviceName": "", "channel": -1})
    return patch


def main() -> None:
    if not RACK.exists():
        raise SystemExit(f"Rack executable not found: {RACK}")
    if ZSTD is None:
        raise SystemExit("zstd executable not found")

    temp_root = Path(tempfile.mkdtemp(prefix="vcv-patch-validation-"))
    try:
        user_dir = temp_root / "user"
        user_dir.mkdir()
        (user_dir / "plugins-mac-arm64").symlink_to(PLUGINS, target_is_directory=True)
        (user_dir / "settings.json").write_text(
            json.dumps({"token": "", "autoCheckUpdates": False, "skipLoadOnLaunch": True}) + "\n"
        )
        reports = []
        for source in sorted((ROOT / "patches").rglob("*.vcv")):
            patch = silence_hardware(read_archive(source))
            test_patch = temp_root / source.name
            write_archive(patch, test_patch)
            result = subprocess.run(
                [str(RACK), "--headless", "--user", str(user_dir), str(test_patch)],
                input="\n",
                text=True,
                capture_output=True,
                timeout=45,
            )
            log_path = user_dir / "log.txt"
            log = log_path.read_text(errors="replace") if log_path.exists() else ""
            bad_markers = (
                "could not load module",
                "could not find module",
                "could not find plugin",
                "cannot load plugin",
                "failed to load patch",
                "exception",
                "assertion failed",
                "segmentation fault",
            )
            errors = [
                line
                for line in (log + result.stdout + result.stderr).splitlines()
                if any(marker in line.lower() for marker in bad_markers)
            ]
            reports.append(
                {
                    "file": str(source.relative_to(ROOT)),
                    "rack_loaded": result.returncode == 0,
                    "exit_code": result.returncode,
                    "load_errors": errors,
                }
            )
        summary = {
            "patches": len(reports),
            "passed": sum(item["rack_loaded"] and not item["load_errors"] for item in reports),
            "failed": sum(not item["rack_loaded"] or bool(item["load_errors"]) for item in reports),
            "hardware_disabled_during_test": True,
            "results": reports,
        }
        (ROOT / "metadata/load-validation.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps({key: summary[key] for key in ("patches", "passed", "failed")}, indent=2))
        if summary["failed"]:
            raise SystemExit(1)
    finally:
        shutil.rmtree(temp_root)


if __name__ == "__main__":
    main()
