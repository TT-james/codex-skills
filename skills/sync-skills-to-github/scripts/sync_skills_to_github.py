#!/usr/bin/env python3
"""Sync local Codex skills to a GitHub repository without rewriting repo templates."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REPO_URL = "https://github.com/TT-james/codex-skills.git"
DEFAULT_BRANCH = "main"
DOC_FILES = ["README.md", "README.en.md", "README.zh-CN.md"]
GENERATED_FILES = DOC_FILES
START_MARKER = "<!-- sync-skills:skills:start -->"
END_MARKER = "<!-- sync-skills:skills:end -->"
SKILL_ORDER = [
    "project-knowledge-graph",
    "codegraph-project-knowledge",
    "understand-anything-project-knowledge",
    "skill-library-manager",
    "sync-skills-to-github",
    "install-github-skills",
    "ai-promotion-case-doc",
    "runqian-report-tooling",
]
PURPOSES = {
    "project-knowledge-graph": {
        "en": "Unified project knowledge graph orchestrator that chooses CodeGraph, Understand-Anything, hybrid mode, or fallback.",
        "zh": "统一的项目知识图谱编排器，可选择 CodeGraph、Understand-Anything、混合模式或回退。",
    },
    "codegraph-project-knowledge": {
        "en": "Builds, refreshes, and queries a CodeGraph-backed local project code graph.",
        "zh": "构建、刷新和查询基于 CodeGraph 的本地项目代码图。",
    },
    "understand-anything-project-knowledge": {
        "en": "Builds and reuses Understand-Anything project knowledge graph context.",
        "zh": "构建并复用 Understand-Anything 项目知识图谱上下文。",
    },
    "skill-library-manager": {
        "en": "Audits, curates, deduplicates, installs, validates, and publishes Codex skill libraries.",
        "zh": "审计、整理、去重、安装、验证和发布 Codex 技能库。",
    },
    "sync-skills-to-github": {
        "en": "Synchronizes local Codex skills to GitHub while preserving established repository templates.",
        "zh": "将本地 Codex 技能同步到 GitHub，同时保留既定仓库模板格式。",
    },
    "install-github-skills": {
        "en": "Installs, updates, lists, and removes Codex skills from a GitHub skills repository.",
        "zh": "从 GitHub 技能仓库安装、更新、列出或移除 Codex 技能。",
    },
    "ai-promotion-case-doc": {
        "en": "Generates reusable Chinese AI promotion case documents from Codex work evidence and history.",
        "zh": "基于 Codex 工作证据和历史记录生成可复用的中文 AI 推广案例文档。",
    },
    "runqian-report-tooling": {
        "en": "Inspects, extracts, edits, validates, and parameter-expands Runqian/Raqsoft RPX report dataset SQL.",
        "zh": "检查、抽取、修改、校验并按参数展开润乾 / Raqsoft RPX 报表数据集 SQL。",
    },
}
BEST_FOR = {
    "project-knowledge-graph": {
        "en": "New repository onboarding, multi-agent planning, impact analysis, reducing repeated scans.",
        "zh": "新仓库入职、多智能体规划、影响分析、减少重复扫描。",
    },
    "codegraph-project-knowledge": {
        "en": "Semantic code search, symbols, callers, candidate files, implementation entry points, impact analysis.",
        "zh": "语义代码搜索、符号、调用者、候选文件、实现入口点、影响分析。",
    },
    "understand-anything-project-knowledge": {
        "en": "Visual project maps, dashboard/chat/explain/diff workflows, shared project understanding.",
        "zh": "可视化项目地图、仪表板/聊天/解释/差异工作流、共享项目理解。",
    },
    "skill-library-manager": {
        "en": "Skill discovery, active-vs-backup decisions, safer global stacks, and team skill governance.",
        "zh": "技能发现、启用/备份决策、更安全的全局技能栈和团队技能治理。",
    },
    "sync-skills-to-github": {
        "en": "Publishing local skills to GitHub without disturbing README layout or hand-written docs.",
        "zh": "发布本地技能到 GitHub，且不破坏 README 排版或手写文档。",
    },
    "install-github-skills": {
        "en": "Keeping a local Codex skill set in sync with a shared GitHub skills repository.",
        "zh": "让本地 Codex 技能集与共享 GitHub 技能仓库保持同步。",
    },
    "ai-promotion-case-doc": {
        "en": "AI adoption stories, team enablement cases, delivery retrospectives, and management-facing Word reports.",
        "zh": "AI 应用案例、团队推广材料、交付复盘和面向管理层的 Word 汇报文档。",
    },
    "runqian-report-tooling": {
        "en": "Runqian report migration, dataset SQL comparison, datasource switching, mojibake repair, and RPX readback checks.",
        "zh": "润乾报表迁移、数据集 SQL 对比、数据源切换、中文乱码修复和 RPX 回读校验。",
    },
}


@dataclass
class SkillInfo:
    name: str
    description: str
    source: Path
    destination: str


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True, check=check)


def default_skills_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


def default_repo_dir() -> Path:
    return Path.home() / ".codex" / "synced-skill-repos" / "codex-skills"


def parse_frontmatter(skill_md: Path) -> tuple[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    name = skill_md.parent.name
    description = ""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            frontmatter = text[3:end].splitlines()
            for line in frontmatter:
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip("\"'")
                elif line.startswith("description:"):
                    description = line.split(":", 1)[1].strip().strip("\"'")
    if not description:
        description = "No description provided."
    return name, description


def discover_skills(skills_dir: Path, include_system: bool) -> list[SkillInfo]:
    if not skills_dir.exists():
        raise FileNotFoundError(f"Skills directory not found: {skills_dir}")

    skills: list[SkillInfo] = []
    for child in sorted(skills_dir.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir():
            continue
        if child.name == ".system" and not include_system:
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.exists():
            continue
        name, description = parse_frontmatter(skill_md)
        skills.append(SkillInfo(name=name, description=description, source=child, destination=f"skills/{child.name}"))
    return skills


def ensure_repo(repo_url: str, repo_dir: Path, branch: str) -> None:
    if (repo_dir / ".git").exists():
        run(["git", "fetch", "origin"], cwd=repo_dir)
        current = run(["git", "branch", "--show-current"], cwd=repo_dir).stdout.strip()
        if current != branch:
            run(["git", "checkout", branch], cwd=repo_dir)
        run(["git", "pull", "--ff-only", "origin", branch], cwd=repo_dir)
        return

    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--branch", branch, repo_url, str(repo_dir)])


def ensure_clean_or_generated(repo_dir: Path) -> None:
    status = run(["git", "status", "--porcelain"], cwd=repo_dir).stdout.splitlines()
    if not status:
        return

    unsafe = []
    for line in status:
        path = line[3:]
        if path.startswith("skills/"):
            continue
        unsafe.append(line)
    if unsafe:
        details = "\n".join(unsafe)
        raise RuntimeError(f"Target repository has unrelated uncommitted changes:\n{details}")


def ignore_patterns(_: str, names: list[str]) -> set[str]:
    ignored = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".DS_Store"}
    return {name for name in names if name in ignored or name.endswith(".pyc")}


def sync_skill_files(skills: list[SkillInfo], repo_dir: Path) -> None:
    dest_root = repo_dir / "skills"
    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    for skill in skills:
        destination = repo_dir / skill.destination
        shutil.copytree(skill.source, destination, ignore=ignore_patterns)


def ordered_skills(skills: list[SkillInfo]) -> list[SkillInfo]:
    priority = {name: index for index, name in enumerate(SKILL_ORDER)}
    return sorted(skills, key=lambda skill: (priority.get(skill.name, len(priority)), skill.name.lower()))


def short_description(skill: SkillInfo) -> str:
    first_sentence = skill.description.split(". ", 1)[0].strip()
    if first_sentence and not first_sentence.endswith("."):
        first_sentence += "."
    return first_sentence or skill.description


def table_value(skill: SkillInfo, values: dict[str, dict[str, str]], language: str, fallback: str) -> str:
    localized = values.get(skill.name, {})
    return localized.get(language) or localized.get("en") or fallback


def render_skill_table(skills: list[SkillInfo], language: str) -> str:
    if language == "zh":
        header = "| 技能 | 用途 | 最适合 |\n|---|---|---|"
    else:
        header = "| Skill | Purpose | Best For |\n|---|---|---|"
    rows = "\n".join(
        "| "
        + f"[`{skill.name}`]({skill.destination})"
        + " | "
        + table_value(skill, PURPOSES, language, short_description(skill))
        + " | "
        + table_value(skill, BEST_FOR, language, "Tasks that match this skill's trigger description.")
        + " |"
        for skill in ordered_skills(skills)
    )
    return f"{START_MARKER}\n{header}\n{rows}\n{END_MARKER}"


def render_docs(skills: list[SkillInfo], repo_url: str) -> dict[str, str]:
    """Return fallback docs used only when a target repository has no template files."""
    en_table = render_skill_table(skills, "en")
    zh_table = render_skill_table(skills, "zh")
    readme = f"""# Codex Skills

This repository stores reusable Codex skills synchronized from a local Codex environment.

- English: [README.en.md](README.en.md)
- 中文: [README.zh-CN.md](README.zh-CN.md)

## Skill Index

{en_table}
"""
    en = f"""# Codex Skills

This repository is a backup and sharing space for reusable Codex skills.

Source repository: {repo_url}

## Skill Index

{en_table}

## How to Use in Codex

Copy the skill folder you need from `skills/<skill-name>` into your local `~/.codex/skills/<skill-name>` directory, then restart Codex and invoke the skill with `$skill-name`.

## How to Update This Repository

Run `$sync-skills-to-github` from the local Codex environment. The sync copies local skill folders and updates only marked documentation blocks.
"""
    zh = f"""# Codex Skills 技能库

这个仓库用于备份和共享本地 Codex 环境中的可复用技能。

源仓库：{repo_url}

## 技能索引

{zh_table}

## 如何应用到 Codex

从 `skills/<skill-name>` 复制需要的技能目录到本地 `~/.codex/skills/<skill-name>`，然后重启 Codex，并用 `$skill-name` 调用。

## 如何更新这个仓库

在本地 Codex 中使用 `$sync-skills-to-github`。同步过程只复制本地技能目录，并且只更新文档中的固定标记区块。
"""
    return {"README.md": readme, "README.en.md": en, "README.zh-CN.md": zh}


def replace_marked_block(text: str, replacement: str) -> tuple[str, bool]:
    start = text.find(START_MARKER)
    end = text.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        return text, False
    end += len(END_MARKER)
    return text[:start] + replacement + text[end:], True


def update_template_docs(repo_dir: Path, skills: list[SkillInfo], repo_url: str) -> list[str]:
    """Preserve repository docs, updating only explicit sync marker blocks."""
    fallback_docs = render_docs(skills, repo_url)
    has_existing_template = any((repo_dir / name).exists() for name in DOC_FILES)
    changed: list[str] = []
    preserved: list[str] = []
    for name in DOC_FILES:
        path = repo_dir / name
        if not path.exists():
            if has_existing_template:
                preserved.append(f"{name} not present; not created because repository template already exists")
                continue
            path.write_text(fallback_docs[name], encoding="utf-8", newline="\n")
            changed.append(f"{name} created from fallback template")
            continue

        original = path.read_text(encoding="utf-8")
        language = "zh" if name.endswith("zh-CN.md") else "en"
        updated, did_replace = replace_marked_block(original, render_skill_table(skills, language))
        if not did_replace:
            preserved.append(f"{name} preserved; no sync marker block found")
            continue
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed.append(f"{name} marker block updated")
        else:
            preserved.append(f"{name} marker block already current")

    for line in preserved:
        print(line)
    return changed


def commit_and_push(repo_dir: Path, message: str, branch: str, no_push: bool) -> tuple[bool, str]:
    existing_docs = [name for name in DOC_FILES if (repo_dir / name).exists()]
    run(["git", "add", "skills", *existing_docs], cwd=repo_dir)
    status = run(["git", "status", "--porcelain"], cwd=repo_dir).stdout.strip()
    if not status:
        return False, "No changes to commit."

    run(["git", "commit", "-m", message], cwd=repo_dir)
    if no_push:
        return True, "Committed locally; push skipped by --no-push."

    run(["git", "push", "origin", branch], cwd=repo_dir)
    return True, "Committed and pushed."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=default_skills_dir())
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL)
    parser.add_argument("--repo-dir", type=Path, default=default_repo_dir())
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--message", default="Sync Codex skills")
    parser.add_argument("--include-system", action="store_true", help="Include ~/.codex/skills/.system")
    parser.add_argument("--dry-run", action="store_true", help="Show what would sync without changing the repository")
    parser.add_argument("--no-push", action="store_true", help="Commit locally but do not push")
    args = parser.parse_args()

    try:
        skills = discover_skills(args.skills_dir.expanduser(), args.include_system)
        if not skills:
            raise RuntimeError(f"No skills with SKILL.md found in {args.skills_dir}")

        print(f"Skills directory: {args.skills_dir.expanduser()}")
        print(f"Target repository: {args.repo_url}")
        print(f"Local checkout: {args.repo_dir.expanduser()}")
        print("Skills to sync:")
        for skill in skills:
            print(f" - {skill.name} -> {skill.destination}")

        if args.dry_run:
            print("Dry run complete. No files changed.")
            return 0

        repo_dir = args.repo_dir.expanduser()
        ensure_repo(args.repo_url, repo_dir, args.branch)
        ensure_clean_or_generated(repo_dir)
        sync_skill_files(skills, repo_dir)
        doc_changes = update_template_docs(repo_dir, skills, args.repo_url)
        if doc_changes:
            print("Documentation updates:")
            for doc_change in doc_changes:
                print(f" - {doc_change}")
        changed, message = commit_and_push(repo_dir, args.message, args.branch, args.no_push)
        print(message)
        if changed:
            print(f"Repository updated at: {repo_dir}")
        return 0
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(f"Command failed: {' '.join(exc.cmd)}\n")
        if exc.stdout:
            sys.stderr.write(exc.stdout)
        if exc.stderr:
            sys.stderr.write(exc.stderr)
        return exc.returncode or 1
    except Exception as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
