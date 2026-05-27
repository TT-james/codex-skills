#!/usr/bin/env python3
"""Validate that sync-skills-to-github satisfies the requested requirements."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SYNC_SCRIPT = SKILL_DIR / "scripts" / "sync_skills_to_github.py"
DEFAULT_REPO = "https://github.com/TT-james/codex-skills.git"


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def load_sync_module():
    spec = importlib.util.spec_from_file_location("sync_skills_to_github", SYNC_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load sync_skills_to_github.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def record(checks: list[Check], name: str, condition: bool, detail: str) -> None:
    checks.append(Check(name=name, passed=condition, detail=detail))


def contains_all(text: str, needles: list[str]) -> bool:
    return all(needle in text for needle in needles)


def validate_static_files(checks: list[Check]) -> None:
    skill_md = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    openai_yaml = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    reference = (SKILL_DIR / "references" / "documentation-format.md").read_text(encoding="utf-8")

    record(
        checks,
        "skill metadata triggers GitHub sync use cases",
        contains_all(skill_md, ["sync local Codex skills to GitHub", "bilingual", "TT-james/codex-skills.git"]),
        "SKILL.md must describe upload/sync to GitHub, bilingual docs, and the default repository.",
    )
    record(
        checks,
        "skill has operational commands",
        contains_all(skill_md, ["--dry-run", "--no-push", "sync_skills_to_github.py"]),
        "SKILL.md must show dry-run, real sync, and no-push command paths.",
    )
    record(
        checks,
        "Codex UI metadata invokes the skill",
        "$sync-skills-to-github" in openai_yaml,
        "agents/openai.yaml default_prompt must mention $sync-skills-to-github.",
    )
    record(
        checks,
        "documentation reference protects repository templates",
        contains_all(reference, ["Do not rewrite established repository templates", "sync-skills:skills:start", "README.zh-CN.md"]),
        "references/documentation-format.md must define template preservation and marker-block updates.",
    )


def validate_sync_module(checks: list[Check]) -> None:
    module = load_sync_module()
    record(
        checks,
        "default GitHub repository is configured",
        getattr(module, "DEFAULT_REPO_URL", "") == DEFAULT_REPO,
        "sync script must default to TT-james/codex-skills.git.",
    )
    record(
        checks,
        "documentation file list is configured",
        set(getattr(module, "GENERATED_FILES", [])) == {"README.md", "README.en.md", "README.zh-CN.md"},
        "sync script must know README.md, README.en.md, and README.zh-CN.md.",
    )

    skill = module.SkillInfo(
        name="demo-skill",
        description="Demo skill for validation.",
        source=SKILL_DIR,
        destination="skills/demo-skill",
    )
    docs = module.render_docs([skill], DEFAULT_REPO)
    record(
        checks,
        "English README explains usage and update flow",
        contains_all(docs["README.en.md"], ["How to Use in Codex", "$sync-skills-to-github", "skills/demo-skill"]),
        "README.en.md must explain Codex usage, update flow, and skill paths.",
    )
    record(
        checks,
        "Chinese README explains usage and update flow",
        contains_all(docs["README.zh-CN.md"], ["如何应用到 Codex", "$sync-skills-to-github", "skills/demo-skill"]),
        "README.zh-CN.md must explain Codex usage, update flow, and skill paths in Chinese.",
    )
    record(
        checks,
        "root README links both languages",
        contains_all(docs["README.md"], ["README.en.md", "README.zh-CN.md", "中文"]),
        "README.md must link English and Chinese documentation.",
    )
    original = "# Custom README\n\nKeep this template.\n"
    updated, did_replace = module.replace_marked_block(original, module.render_skill_table([skill], "en"))
    record(
        checks,
        "unmarked README templates are preserved",
        not did_replace and updated == original,
        "Existing docs without sync marker blocks must remain unchanged.",
    )
    marked = f"# Custom README\n\n{module.START_MARKER}\nold\n{module.END_MARKER}\n"
    updated, did_replace = module.replace_marked_block(marked, module.render_skill_table([skill], "en"))
    record(
        checks,
        "marked README blocks are updated narrowly",
        did_replace and "old" not in updated and "Custom README" in updated and "skills/demo-skill" in updated,
        "Existing docs may only update the marked skill-index block.",
    )


def validate_dry_run_safety(checks: list[Check]) -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        skills_dir = root / "skills"
        skill_dir = skills_dir / "demo-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: demo-skill\ndescription: Demo skill.\n---\n\n# Demo\n",
            encoding="utf-8",
        )
        repo_dir = root / "repo"
        result = subprocess.run(
            [
                sys.executable,
                str(SYNC_SCRIPT),
                "--skills-dir",
                str(skills_dir),
                "--repo-dir",
                str(repo_dir),
                "--dry-run",
            ],
            text=True,
            capture_output=True,
        )
        record(
            checks,
            "dry run reports skills without changing repository",
            result.returncode == 0 and "demo-skill" in result.stdout and not repo_dir.exists(),
            "Dry run must discover skills and avoid cloning or writing the target repository.",
        )


def main() -> int:
    checks: list[Check] = []
    validate_static_files(checks)
    validate_sync_module(checks)
    validate_dry_run_safety(checks)

    failures = [check for check in checks if not check.passed]
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name} - {check.detail}")

    print(f"\nResult: {len(checks) - len(failures)}/{len(checks)} checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
