#!/usr/bin/env python3
"""Sync local Codex skills to a GitHub repository and generate bilingual docs."""

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
GENERATED_FILES = ["README.md", "README.en.md", "README.zh-CN.md"]


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

    allowed_paths = set(GENERATED_FILES)
    unsafe = []
    for line in status:
        path = line[3:]
        if path in allowed_paths or path.startswith("skills/"):
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


def render_docs(skills: list[SkillInfo], repo_url: str) -> dict[str, str]:
    skill_rows_en = "\n".join(
        f"| `{skill.name}` | {skill.description} | `{skill.destination}` |" for skill in skills
    )
    skill_rows_zh = "\n".join(
        f"| `{skill.name}` | {skill.description} | `{skill.destination}` |" for skill in skills
    )

    readme = """# Codex Skills

This repository stores reusable Codex skills synchronized from a local Codex environment.

- English: [README.en.md](README.en.md)
- 中文: [README.zh-CN.md](README.zh-CN.md)
"""

    en = f"""# Codex Skills

This repository is a backup and sharing space for reusable Codex skills.

Source repository: {repo_url}

## Skill Index

| Skill | What it does | Path |
| --- | --- | --- |
{skill_rows_en}

## How to Use in Codex

1. Copy the skill folder you need from `skills/<skill-name>` into your local `~/.codex/skills/<skill-name>` directory.
2. Restart or refresh Codex if your environment does not auto-discover new skills.
3. Invoke the skill explicitly with `$skill-name`, or ask for a task that matches the skill description.
4. Open the skill's `SKILL.md` to see its workflow, scripts, references, and usage constraints.

## How to Update This Repository

Run the local Codex skill `$sync-skills-to-github` and ask Codex to sync local skills to GitHub. The sync process copies local skill folders, regenerates these docs, commits the changes, and pushes them to the repository when authentication is available.

## Notes

Review generated changes before publishing if a skill may contain private project paths, internal business rules, credentials, or customer data.
"""

    zh = f"""# Codex Skills 技能库

这个仓库用于备份和共享本地 Codex 环境中生成的可复用技能。

源仓库：{repo_url}

## 技能索引

| 技能 | 用途 | 路径 |
| --- | --- | --- |
{skill_rows_zh}

## 如何应用到 Codex

1. 从 `skills/<skill-name>` 复制需要的技能目录到本地 `~/.codex/skills/<skill-name>`。
2. 如果当前 Codex 环境不会自动发现新技能，请重启或刷新 Codex。
3. 可以用 `$skill-name` 显式调用技能，也可以直接提出与技能描述匹配的任务。
4. 阅读技能目录里的 `SKILL.md`，了解工作流、脚本、参考资料和使用限制。

## 如何更新这个仓库

在本地 Codex 中使用 `$sync-skills-to-github`，让 Codex 将本地技能同步到 GitHub。同步过程会复制本地技能目录、重新生成中英文文档、提交变更，并在认证可用时推送到仓库。

## 注意事项

如果技能中可能包含项目内部路径、业务规则、密钥、客户数据或其他私密信息，发布前请先检查生成的变更。
"""

    readme = """# Codex Skills

This repository stores reusable Codex skills synchronized from a local Codex environment.

- English: [README.en.md](README.en.md)
- \u4e2d\u6587: [README.zh-CN.md](README.zh-CN.md)
"""

    zh = f"""# Codex Skills \u6280\u80fd\u5e93

\u8fd9\u4e2a\u4ed3\u5e93\u7528\u4e8e\u5907\u4efd\u548c\u5171\u4eab\u672c\u5730 Codex \u73af\u5883\u4e2d\u751f\u6210\u7684\u53ef\u590d\u7528\u6280\u80fd\u3002

\u6e90\u4ed3\u5e93\uff1a{repo_url}

## \u6280\u80fd\u7d22\u5f15

| \u6280\u80fd | \u7528\u9014 | \u8def\u5f84 |
| --- | --- | --- |
{skill_rows_zh}

## \u5982\u4f55\u5e94\u7528\u5230 Codex

1. \u4ece `skills/<skill-name>` \u590d\u5236\u9700\u8981\u7684\u6280\u80fd\u76ee\u5f55\u5230\u672c\u5730 `~/.codex/skills/<skill-name>`\u3002
2. \u5982\u679c\u5f53\u524d Codex \u73af\u5883\u4e0d\u4f1a\u81ea\u52a8\u53d1\u73b0\u65b0\u6280\u80fd\uff0c\u8bf7\u91cd\u542f\u6216\u5237\u65b0 Codex\u3002
3. \u53ef\u4ee5\u7528 `$skill-name` \u663e\u5f0f\u8c03\u7528\u6280\u80fd\uff0c\u4e5f\u53ef\u4ee5\u76f4\u63a5\u63d0\u51fa\u4e0e\u6280\u80fd\u63cf\u8ff0\u5339\u914d\u7684\u4efb\u52a1\u3002
4. \u9605\u8bfb\u6280\u80fd\u76ee\u5f55\u91cc\u7684 `SKILL.md`\uff0c\u4e86\u89e3\u5de5\u4f5c\u6d41\u3001\u811a\u672c\u3001\u53c2\u8003\u8d44\u6599\u548c\u4f7f\u7528\u9650\u5236\u3002

## \u5982\u4f55\u66f4\u65b0\u8fd9\u4e2a\u4ed3\u5e93

\u5728\u672c\u5730 Codex \u4e2d\u4f7f\u7528 `$sync-skills-to-github`\uff0c\u8ba9 Codex \u5c06\u672c\u5730\u6280\u80fd\u540c\u6b65\u5230 GitHub\u3002\u540c\u6b65\u8fc7\u7a0b\u4f1a\u590d\u5236\u672c\u5730\u6280\u80fd\u76ee\u5f55\u3001\u91cd\u65b0\u751f\u6210\u4e2d\u82f1\u6587\u6587\u6863\u3001\u63d0\u4ea4\u53d8\u66f4\uff0c\u5e76\u5728\u8ba4\u8bc1\u53ef\u7528\u65f6\u63a8\u9001\u5230\u4ed3\u5e93\u3002

## \u6ce8\u610f\u4e8b\u9879

\u5982\u679c\u6280\u80fd\u4e2d\u53ef\u80fd\u5305\u542b\u9879\u76ee\u5185\u90e8\u8def\u5f84\u3001\u4e1a\u52a1\u89c4\u5219\u3001\u5bc6\u94a5\u3001\u5ba2\u6237\u6570\u636e\u6216\u5176\u4ed6\u79c1\u5bc6\u4fe1\u606f\uff0c\u53d1\u5e03\u524d\u8bf7\u5148\u68c0\u67e5\u751f\u6210\u7684\u53d8\u66f4\u3002
"""

    return {"README.md": readme, "README.en.md": en, "README.zh-CN.md": zh}


def write_docs(repo_dir: Path, docs: dict[str, str]) -> None:
    for name, content in docs.items():
        (repo_dir / name).write_text(content, encoding="utf-8", newline="\n")


def commit_and_push(repo_dir: Path, message: str, branch: str, no_push: bool) -> tuple[bool, str]:
    run(["git", "add", "skills", *GENERATED_FILES], cwd=repo_dir)
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
        write_docs(repo_dir, render_docs(skills, args.repo_url))
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
