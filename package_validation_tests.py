from __future__ import annotations

import json
import re

from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent

EXPECTED_MCP_ENDPOINTS = {
    "claude/.mcp.json": {
        "name": "claude_app_mcp",
        "url": "https://mcp.dropbox.com/claude_app_mcp",
    },
    "codex/.mcp.json": {
        "name": "chatgpt_app_mcp",
        "url": "https://mcp.dropbox.com/chatgpt_app_mcp",
    },
}

MANIFEST_PATHS = [
    Path("claude/plugin.json"),
    Path("codex/.codex-plugin/plugin.json"),
]

PUBLIC_PACKAGE_PATHS = [
    Path("README.md"),
    Path("LICENSE"),
    Path("claude"),
    Path("codex"),
    Path("shared"),
]

REPO_ONLY_FILE_PATTERNS = [
    re.compile(r"(^|/)BUILD(?:\.in)?$"),
    re.compile(r"(^|/)mcp_host_skills_tests\.py$"),
    re.compile(r"(^|/)package_validation_tests\.py$"),
    re.compile(r"^temp/"),
    re.compile(r"(^|/)__pycache__/"),
    re.compile(r"(^|/)\.DS_Store$"),
]


DISALLOWED_PUBLIC_PATTERNS = [
    re.compile(r"/Users/[^/\s]+/\.codex"),
    re.compile(r"/Users/[^/\s]+/Developer"),
    re.compile(r"/Users/[^/\s]+/src/server"),
    re.compile(r"/home/[^/\s]+/src/server"),
    re.compile(r"\b[A-Za-z0-9_-]+-internal\b", re.IGNORECASE),
    re.compile(
        r"\.(?:corp|dev|pp)\.[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        re.IGNORECASE,
    ),
    re.compile(r"\blocalhost\b", re.IGNORECASE),
    re.compile(r"\b127\.0\.0\.1\b"),
    re.compile(r"\bngrok\b", re.IGNORECASE),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{20,}\b"),
    re.compile(
        r"\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|"
        r"refresh[_-]?token)\b\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{8,}",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bauthorization\s*:\s*bearer\s+[A-Za-z0-9._~+/-]+=*",
        re.IGNORECASE,
    ),
]


def _package_root() -> Path:
    return REPO_ROOT


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object."
    return value


def _mcp_host_root_for_manifest(package_root: Path, manifest_path: Path) -> Path:
    if manifest_path.parts[:2] == ("codex", ".codex-plugin"):
        return package_root / "codex"
    return package_root / manifest_path.parts[0]


def _resolve_relative_path(root: Path, raw_path: str) -> Path:
    assert raw_path.startswith("./"), (
        f"Manifest path must be ./-relative: {raw_path!r}"
    )
    resolved = (root / raw_path.removeprefix("./")).resolve()
    root_resolved = root.resolve()
    assert root_resolved == resolved or root_resolved in resolved.parents, (
        f"Manifest path escapes MCP Host root: {raw_path!r}"
    )
    return resolved


def _iter_manifest_path_references(manifest: dict[str, Any]) -> Iterable[str]:
    for key in ("skills", "mcpServers", "apps", "hooks"):
        value = manifest.get(key)
        if isinstance(value, str):
            yield value

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        return

    for key in ("composerIcon", "logo"):
        value = interface.get(key)
        if isinstance(value, str):
            yield value

    screenshots = interface.get("screenshots")
    if isinstance(screenshots, list):
        for value in screenshots:
            if isinstance(value, str):
                yield value


def _iter_public_package_files(package_root: Path) -> Iterable[Path]:
    for relative_package_path in PUBLIC_PACKAGE_PATHS:
        package_path = package_root / relative_package_path
        if package_path.is_file():
            yield package_path
            continue
        for path in sorted(package_path.rglob("*")):
            if path.is_file():
                yield path


def test_mcp_host_json_files_are_valid() -> None:
    package_root = _package_root()
    for relative_path in [
        *MANIFEST_PATHS,
        *(Path(path) for path in EXPECTED_MCP_ENDPOINTS),
    ]:
        path = package_root / relative_path
        assert path.is_file(), f"Missing required JSON file: {relative_path}"
        _load_json(path)


def test_mcp_host_manifest_path_references_are_valid() -> None:
    package_root = _package_root()
    for manifest_path in MANIFEST_PATHS:
        manifest = _load_json(package_root / manifest_path)
        mcp_host_root = _mcp_host_root_for_manifest(package_root, manifest_path)
        for raw_path in _iter_manifest_path_references(manifest):
            resolved_path = _resolve_relative_path(mcp_host_root, raw_path)
            assert resolved_path.exists(), (
                f"{manifest_path} references a missing path: {raw_path}"
            )


def test_mcp_configs_use_only_production_dropbox_endpoints() -> None:
    package_root = _package_root()
    for relative_path, expected in EXPECTED_MCP_ENDPOINTS.items():
        config = _load_json(package_root / relative_path)
        mcp_servers = config.get("mcpServers")
        assert isinstance(mcp_servers, dict), (
            f"{relative_path} must define mcpServers."
        )
        assert set(mcp_servers) == {expected["name"]}, (
            f"{relative_path} must define only {expected['name']}."
        )

        server = mcp_servers[expected["name"]]
        assert isinstance(server, dict), (
            f"{relative_path} server config must be an object."
        )
        assert server.get("type") == "http", (
            f"{relative_path} must use an HTTP MCP server."
        )
        assert server.get("url") == expected["url"], (
            f"{relative_path} must point at the production endpoint."
        )


def test_public_package_paths_exclude_repo_only_files() -> None:
    package_root = _package_root()
    repo_only_files = []
    for path in _iter_public_package_files(package_root):
        relative_path = path.relative_to(package_root).as_posix()
        if any(
            pattern.search(relative_path)
            for pattern in REPO_ONLY_FILE_PATTERNS
        ):
            repo_only_files.append(relative_path)

    assert not repo_only_files, (
        "Public plugin package paths must not include repo-only files:\n"
        + "\n".join(repo_only_files)
    )


def test_public_package_files_do_not_contain_private_or_secret_material() -> None:
    package_root = _package_root()
    failures: list[str] = []
    for path in _iter_public_package_files(package_root):
        if path.suffix not in {".json", ".md", ".yaml", ".yml"}:
            continue
        contents = path.read_text(encoding="utf-8")
        relative_path = path.relative_to(package_root).as_posix()
        for pattern in DISALLOWED_PUBLIC_PATTERNS:
            if pattern.search(contents):
                failures.append(f"{relative_path} matches {pattern.pattern}")

    assert not failures, (
        "Public plugin package files must not contain private URLs, local paths, "
        "or secret-looking values:\n" + "\n".join(failures)
    )


def _run_tests() -> None:
    tests = [
        (name, test)
        for name, test in sorted(globals().items())
        if name.startswith("test_") and callable(test)
    ]
    for _, test in tests:
        test()
    print(f"{Path(__file__).name}: {len(tests)} tests passed")


if __name__ == "__main__":
    _run_tests()
