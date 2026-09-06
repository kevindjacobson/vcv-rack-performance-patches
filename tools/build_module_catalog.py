#!/usr/bin/env python3
"""Build docs/MODULES.md from the module inventory and current VCV Library."""

from __future__ import annotations

import html
import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "metadata/module-inventory.json"
CATALOG = ROOT / "metadata/module-catalog.json"
DOCUMENT = ROOT / "docs/MODULES.md"
PLUGIN_ROOT = Path.home() / "Library/Application Support/Rack2/plugins-mac-arm64"
RACK_SOURCE = ROOT.parent / "downloads/Rack-src"

LOCAL_MODULES = {
    ("VCVRackMcpServer", "RackMcpServer"): {
        "url": "https://github.com/Neural-Harmonics/vcv-rack-plugin-mcp-server",
        "access": "Free / local helper",
        "license": "MIT",
        "note": "Patch-control helper; it is not in the VCV Library and is not in the audio path.",
    }
}


def load_manifests() -> dict[tuple[str, str], dict]:
    manifests = []
    core = RACK_SOURCE / "Core.json"
    if core.exists():
        manifests.append(json.loads(core.read_text()))
    if PLUGIN_ROOT.exists():
        for path in PLUGIN_ROOT.glob("*/plugin.json"):
            try:
                manifests.append(json.loads(path.read_text()))
            except (OSError, json.JSONDecodeError):
                pass
    result = {}
    for plugin in manifests:
        for module in plugin.get("modules", []):
            result[(plugin.get("slug", ""), module.get("slug", ""))] = {
                "plugin_name": plugin.get("name") or plugin.get("slug", ""),
                "module_name": module.get("name") or module.get("slug", ""),
                "license": plugin.get("license") or "See module page",
                "source_url": plugin.get("sourceUrl") or plugin.get("pluginUrl") or "",
            }
    return result


def inspect_library(item: dict, names: dict[tuple[str, str], dict]) -> dict:
    key = (item["plugin"], item["module"])
    metadata = names.get(
        key,
        {
            "plugin_name": item["plugin"],
            "module_name": item["module"],
            "license": "See module page",
            "source_url": "",
        },
    )
    if key in LOCAL_MODULES:
        special = LOCAL_MODULES[key]
        return {**item, **metadata, **special, "library_http_status": 404}

    url = f"https://library.vcvrack.com/{item['plugin']}/{item['module']}"
    status = 0
    body = ""
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "VCV patch catalog/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        status = error.code
    except urllib.error.URLError:
        status = 0

    if status == 200:
        price = re.search(r'class="library-price"[^>]*>\s*([^<]+)', body)
        if price:
            access = f"Paid ({html.unescape(price.group(1)).strip()})"
        else:
            access = "Free"
        license_link = re.search(r"License:\s*<a[^>]*>([^<]+)</a>", body)
        license_text = re.search(r"License:\s*([^<\n]+)", body)
        if license_link:
            license_name = html.unescape(license_link.group(1)).strip()
        elif license_text:
            license_name = html.unescape(license_text.group(1)).strip()
        else:
            license_name = metadata["license"]
        if license_name == "https://vcvrack.com/eula":
            license_name = "VCV EULA"
        note = "Official VCV Library module page."
    else:
        url = metadata["source_url"] or f"https://library.vcvrack.com/{item['plugin']}"
        access = "Free / source installation"
        license_name = metadata["license"]
        note = "Not currently listed at the expected VCV Library module URL; source link provided."

    return {
        **item,
        **metadata,
        "url": url,
        "access": access,
        "license": license_name,
        "note": note,
        "library_http_status": status,
    }


def main() -> None:
    inventory = json.loads(INVENTORY.read_text())
    names = load_manifests()
    with ThreadPoolExecutor(max_workers=12) as pool:
        catalog = list(pool.map(lambda item: inspect_library(item, names), inventory))
    catalog.sort(key=lambda item: (item["plugin_name"].casefold(), item["module_name"].casefold()))
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n")

    paid = [item for item in catalog if item["access"].startswith("Paid")]
    unavailable = [item for item in catalog if item["library_http_status"] != 200]
    lines = [
        "# Module and Plugin Catalog",
        "",
        "This is the dependency catalog for every patch in this repository. Each module name links directly to its official VCV Library page; source links are used for local modules that are not listed there.",
        "",
        f"**Access summary:** {len(catalog) - len(paid) - len(unavailable)} free Library modules, {len(paid)} paid Library module, and {len(unavailable)} local/source-installed module.",
        "",
        "Prices and availability were checked against the VCV Library when this catalog was generated. A price applies to the plugin bundle shown on the linked module page, not necessarily to one module by itself.",
        "",
    ]
    grouped = {}
    for item in catalog:
        grouped.setdefault((item["plugin"], item["plugin_name"]), []).append(item)
    for (plugin_slug, plugin_name), items in grouped.items():
        plugin_statuses = sorted({item["access"] for item in items})
        lines.extend(
            [
                f"## {plugin_name}",
                "",
                f"Plugin slug: `{plugin_slug}` · Access: {', '.join(plugin_statuses)}",
                "",
                "| Module | Access | License | Used by |",
                "| --- | --- | --- | ---: |",
            ]
        )
        for item in items:
            label = item["module_name"].replace("|", "\\|")
            license_name = item["license"].replace("|", "\\|")
            count = len(item["patches"])
            usage = f"{count} patch" if count == 1 else f"{count} patches"
            lines.append(f"| [{label}]({item['url']}) | {item['access']} | {license_name} | {usage} |")
        lines.append("")
    DOCUMENT.write_text("\n".join(lines))
    print(
        json.dumps(
            {
                "modules": len(catalog),
                "free_library": len(catalog) - len(paid) - len(unavailable),
                "paid_library": len(paid),
                "local_or_source": len(unavailable),
                "unavailable": [f"{item['plugin']}/{item['module']}" for item in unavailable],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
