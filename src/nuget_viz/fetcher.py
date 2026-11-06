"""Fetches and parses NuGet package dependencies."""
import urllib.request
import xml.etree.ElementTree as ET
import json
import os

HTTP_TIMEOUT = 10


def fetch_nuspec(repo_url: str, package: str, version: str) -> str:
    """Downloads the .nuspec XML file for the package."""
    pkg_lower = package.lower()
    ver_lower = version.lower()
    url = f"{repo_url}/{pkg_lower}/{ver_lower}/{pkg_lower}.nuspec"
    try:
        with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT) as resp:
            return resp.read().decode("utf-8")
    except Exception as err:
        raise RuntimeError(f"Failed to fetch {url}: {err}")


def parse_nuspec(xml_content: str) -> list[str]:
    """Extracts direct dependencies from nuspec XML."""
    try:
        root = ET.fromstring(xml_content)
        ns_url = (
            "http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd"
        )
        namespaces = {'ns': ns_url}
        deps = []
        for dep in root.findall(".//ns:dependency", namespaces):
            dep_id = dep.get("id")
            if dep_id:
                deps.append(dep_id)
        return deps
    except ET.ParseError as err:
        raise RuntimeError(f"Invalid NUSPEC XML: {err}")


def load_test_graph(file_path: str) -> dict[str, list[str]]:
    """Loads mock graph from JSON for test mode."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test repo not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
