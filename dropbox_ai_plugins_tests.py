from __future__ import annotations

import re

from pathlib import Path
from typing import TypedDict

from dropbox import json, runfiles

PLUGIN_ROOT = Path(
    runfiles.data_path("//atlas/chatgpt_app/dropbox-ai-plugins/README.md")
).parent

PROVIDER_TOOLS = {
    "claude": {
        "search",
        "list_folder",
        "get_file_metadata",
        "fetch",
        "file_preview",
        "create_folder",
        "create_file",
        "create_shared_link",
    },
    "codex": {
        "search",
        "list_folder",
        "get_file_metadata",
        "who_am_i",
        "list_file_requests",
        "get_file_request",
        "create_file_request",
        "fetch",
        "download_link",
        "file_preview",
        "create_folder",
        "create_file",
        "create_shared_link",
        "list_shared_links",
        "get_shared_link_metadata",
        "move",
        "copy",
        "delete",
        "check_job_status",
    },
}

ALL_PROVIDER_TOOLS = {tool for tools in PROVIDER_TOOLS.values() for tool in tools}
FUTURE_TOOLS = {"restore"}
ALL_KNOWN_TOOLS = ALL_PROVIDER_TOOLS | FUTURE_TOOLS

MANIFEST_PATHS = {
    "claude": Path("claude/plugin.json"),
    "codex": Path("codex/.codex-plugin/plugin.json"),
}

GAP_DOC_PATHS = {
    "claude": Path("temp/claude/SKILL_TOOL_GAPS.md"),
    "codex": Path("temp/codex/SKILL_TOOL_GAPS.md"),
}


class CompatibilityRow(TypedDict):
    provider_tools: dict[str, set[str]]
    claude_status: str
    codex_status: str


def _read_json(path: Path) -> dict[str, object]:
    return json.loads((PLUGIN_ROOT / path).read_text())


def _manifest_skill_paths(provider: str) -> list[Path]:
    manifest = _read_json(MANIFEST_PATHS[provider])
    skills = manifest.get("skills", [])
    provider_root = PLUGIN_ROOT / provider

    if isinstance(skills, list):
        return [
            (provider_root / skill.removeprefix("./")).resolve() for skill in skills
        ]

    if isinstance(skills, str):
        skill_dir = provider_root / skills.removeprefix("./")
        return sorted(skill_dir.glob("*/SKILL.md"))

    raise AssertionError(
        f"{provider} manifest has unsupported skills value: {skills!r}"
    )


def _tools_from_skill(skill_path: Path) -> set[str]:
    tools: set[str] = set()
    in_tools_section = False

    for line in skill_path.read_text().splitlines():
        stripped = line.strip()
        if stripped == "## Tools":
            in_tools_section = True
            continue
        if in_tools_section and stripped.startswith("## "):
            break
        if in_tools_section:
            match = re.fullmatch(r"- `([^`]+)`", stripped)
            if match:
                tools.add(match.group(1))

    return tools


def _tool_like_backtick_names(path: Path) -> set[str]:
    return set(re.findall(r"`([a-z][a-z0-9_]+)`", path.read_text()))


def _provider_skill_paths(provider: str) -> list[Path]:
    return sorted((PLUGIN_ROOT / provider / "skills").glob("*/SKILL.md"))


def _skill_path_provider(skill_path: Path) -> str | None:
    resolved_path = skill_path.resolve()
    for provider in PROVIDER_TOOLS:
        provider_skill_root = (PLUGIN_ROOT / provider / "skills").resolve()
        if provider_skill_root in resolved_path.parents:
            return provider
    return None


def _temp_skill_paths() -> list[Path]:
    return sorted((PLUGIN_ROOT / "temp" / "skills").glob("*/SKILL.md"))


def _all_provider_skill_paths() -> list[Path]:
    return [
        skill_path
        for provider in PROVIDER_TOOLS
        for skill_path in _provider_skill_paths(provider)
    ]


def _all_skill_paths() -> list[Path]:
    return _all_provider_skill_paths() + _temp_skill_paths()


def _compatibility_matrix() -> dict[str, CompatibilityRow]:
    matrix_text = (PLUGIN_ROOT / "temp" / "SKILL_COMPATIBILITY.md").read_text()
    matrix: dict[str, CompatibilityRow] = {}

    for row in matrix_text.splitlines():
        if not row.startswith("| `"):
            continue
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        skill_name = cells[0].strip("`")
        matrix[skill_name] = {
            "provider_tools": {
                "claude": set(re.findall(r"`([^`]+)`", cells[1])),
                "codex": set(re.findall(r"`([^`]+)`", cells[2])),
            },
            "claude_status": cells[3],
            "codex_status": cells[4],
        }

    return matrix


def _matrix_tools(row: CompatibilityRow, provider: str) -> set[str]:
    return row["provider_tools"][provider]


def _matrix_status(row: CompatibilityRow, provider: str) -> str:
    if provider == "claude":
        return row["claude_status"]
    if provider == "codex":
        return row["codex_status"]
    raise AssertionError(f"Unknown provider: {provider}")


def _gap_doc_tools(provider: str) -> dict[str, set[str]]:
    gap_doc_text = (PLUGIN_ROOT / GAP_DOC_PATHS[provider]).read_text()
    gap_doc_tools: dict[str, set[str]] = {}

    for row in gap_doc_text.splitlines():
        if not row.startswith("| `"):
            continue
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        skill_name = cells[0].strip("`")
        missing_tools = set(re.findall(r"`([^`]+)`", cells[1]))
        gap_doc_tools[skill_name] = missing_tools

    return gap_doc_tools


def test_provider_manifests_are_valid_json() -> None:
    for manifest_path in MANIFEST_PATHS.values():
        assert isinstance(_read_json(manifest_path), dict)


def test_manifest_listed_skill_files_exist_and_are_provider_local() -> None:
    for provider in MANIFEST_PATHS:
        provider_root = (PLUGIN_ROOT / provider).resolve()
        shared_root = (PLUGIN_ROOT / "shared").resolve()

        for skill_path in _manifest_skill_paths(provider):
            assert skill_path.is_file(), (
                f"{provider} manifest lists missing skill: {skill_path}"
            )
            assert provider_root in skill_path.parents, (
                f"{provider} manifest must list provider-local skills only: {skill_path}"
            )
            assert shared_root not in skill_path.parents, (
                f"{provider} manifest must not load shared material directly: {skill_path}"
            )


def test_manifest_listed_skills_use_supported_provider_tools() -> None:
    for provider, supported_tools in PROVIDER_TOOLS.items():
        for skill_path in _manifest_skill_paths(provider):
            unknown_tools = _tools_from_skill(skill_path) - supported_tools
            assert not unknown_tools, (
                f"{provider} skill {skill_path.name} references unsupported tools: "
                f"{sorted(unknown_tools)}"
            )


def test_all_provider_skill_files_use_supported_provider_tools() -> None:
    for provider, supported_tools in PROVIDER_TOOLS.items():
        for skill_path in _provider_skill_paths(provider):
            unknown_tools = _tools_from_skill(skill_path) - supported_tools
            assert not unknown_tools, (
                f"{provider} skill {skill_path.parent.name} references "
                f"unsupported tools: {sorted(unknown_tools)}"
            )


def test_provider_skill_tool_references_use_supported_provider_tools() -> None:
    for provider, supported_tools in PROVIDER_TOOLS.items():
        for skill_path in _provider_skill_paths(provider):
            unknown_tools = _tool_like_backtick_names(skill_path) - supported_tools
            assert not unknown_tools, (
                f"{provider} skill {skill_path.parent.name} references "
                f"unsupported tool-like names: {sorted(unknown_tools)}"
            )


def test_provider_manifests_include_all_provider_skill_files() -> None:
    for provider in PROVIDER_TOOLS:
        manifest_skill_names = {
            skill_path.parent.name for skill_path in _manifest_skill_paths(provider)
        }
        provider_skill_names = {
            skill_path.parent.name for skill_path in _provider_skill_paths(provider)
        }

        assert manifest_skill_names == provider_skill_names


def test_compatibility_matrix_tools_are_known_tools() -> None:
    for skill_name, row in _compatibility_matrix().items():
        for provider in PROVIDER_TOOLS:
            unknown_tools = _matrix_tools(row, provider) - ALL_KNOWN_TOOLS
            assert not unknown_tools, (
                f"compatibility matrix row {skill_name} references unknown "
                f"{provider} tools: {sorted(unknown_tools)}"
            )


def test_compatibility_matrix_reflects_provider_skill_status() -> None:
    matrix = _compatibility_matrix()
    skill_names = {skill_path.parent.name for skill_path in _all_skill_paths()}

    assert set(matrix) == skill_names

    for skill_name, row in matrix.items():
        skill_paths = [
            skill_path
            for skill_path in _all_skill_paths()
            if skill_path.parent.name == skill_name
        ]
        assert skill_paths
        for skill_path in skill_paths:
            skill_provider = _skill_path_provider(skill_path)
            if skill_provider:
                assert _matrix_tools(row, skill_provider) == _tools_from_skill(
                    skill_path
                )
            else:
                all_provider_tools = set().union(
                    *[_matrix_tools(row, provider) for provider in PROVIDER_TOOLS]
                )
                assert all_provider_tools == _tools_from_skill(skill_path)

        for provider, supported_tools in PROVIDER_TOOLS.items():
            provider_manifest_names = {
                skill_path.parent.name for skill_path in _manifest_skill_paths(provider)
            }
            status = _matrix_status(row, provider)
            required_tools = _matrix_tools(row, provider)
            missing_tools = required_tools - supported_tools

            if skill_name in provider_manifest_names:
                assert not missing_tools
                assert f"registered in `{provider}/skills/`" in status
            else:
                assert missing_tools
                assert status.startswith("Blocked: missing ")
                assert set(re.findall(r"`([^`]+)`", status)) == missing_tools


def test_same_named_claude_and_codex_skills_are_identical_when_tools_match() -> None:
    claude_skill_paths = {
        skill_path.parent.name: skill_path
        for skill_path in _provider_skill_paths("claude")
    }
    codex_skill_paths = {
        skill_path.parent.name: skill_path
        for skill_path in _provider_skill_paths("codex")
    }

    for skill_name in set(claude_skill_paths) & set(codex_skill_paths):
        if _tools_from_skill(claude_skill_paths[skill_name]) != _tools_from_skill(
            codex_skill_paths[skill_name]
        ):
            continue
        assert (
            claude_skill_paths[skill_name].read_text()
            == codex_skill_paths[skill_name].read_text()
        )


def test_provider_gap_docs_match_compatibility_matrix_tool_gaps() -> None:
    matrix = _compatibility_matrix()

    for provider, supported_tools in PROVIDER_TOOLS.items():
        expected_gaps = {
            skill_name: _matrix_tools(row, provider) - supported_tools
            for skill_name, row in matrix.items()
            if _matrix_tools(row, provider) - supported_tools
        }

        assert _gap_doc_tools(provider) == expected_gaps
