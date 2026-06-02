from __future__ import annotations

import json
import re

from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent

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

MANIFEST_PATHS = {
    "claude": Path("claude/plugin.json"),
    "codex": Path("codex/.codex-plugin/plugin.json"),
}


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
