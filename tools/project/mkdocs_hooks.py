"""MkDocs integration for the generated Obsidian-compatible wiki."""

from __future__ import annotations

import posixpath
import re
from pathlib import Path, PurePosixPath
from typing import Any


WIKILINK_RE = re.compile(r"\[\[([^\[\]|]+?)(?:\|([^\]]+))?\]\]")
HALF_YEAR_REPORT_TITLE_RE = re.compile(
    r"^(?P<period>\d{4}년 [상하]반기) 철강 신기술·프로젝트 동향$"
)


def convert_wikilinks(markdown: str, current_src_path: str) -> str:
    """Convert vault-root Obsidian links to page-relative Markdown links."""
    normalized_current = current_src_path.replace("\\", "/")
    current_dir = PurePosixPath(normalized_current).parent.as_posix()
    if current_dir == ".":
        current_dir = ""

    def replace(match: re.Match[str]) -> str:
        raw_target = match.group(1).strip().replace("\\", "/")
        label = (match.group(2) or "").strip()
        target_path, separator, anchor = raw_target.partition("#")
        if target_path and not PurePosixPath(target_path).suffix:
            target_path += ".md"
        if target_path:
            href = posixpath.relpath(target_path, current_dir or ".")
        else:
            href = ""
        if separator:
            href += f"#{anchor}"
        if not label:
            label = PurePosixPath(target_path).stem or anchor
        return f"[{label}]({href})"

    return WIKILINK_RE.sub(replace, markdown)


def on_page_markdown(
    markdown: str,
    page: Any,
    config: Any,
    files: Any,
) -> str:
    """Render Obsidian links without modifying the Markdown source."""
    return convert_wikilinks(markdown, page.file.src_path)


def on_page_content(
    html: str,
    page: Any,
    config: Any,
    files: Any,
) -> str:
    """Mark the change-history table for page-specific column sizing."""
    if page.file.src_path.replace("\\", "/") != "recent-updates.md":
        return html
    marker = "<table>"
    parts = html.split(marker, 2)
    if len(parts) != 3:
        return html
    return (
        f"{parts[0]}{marker}{parts[1]}"
        f"<table data-recent-updates-changes>{parts[2]}"
    )


def _page_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return (
                line[2:]
                .strip()
                .removesuffix(" 기술 현황")
                .removesuffix(" 기업 현황")
            )
    return path.stem


def _report_nav_title(path: Path) -> str:
    title = _page_title(path)
    match = HALF_YEAR_REPORT_TITLE_RE.fullmatch(title)
    if match:
        return f"{match.group('period')} 동향"
    return title


def _report_date(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            key, separator, value = line.partition(":")
            if separator and key.strip() == "date":
                return value.strip().strip("\"'")
    return ""


def _report_pages(root: Path) -> list[dict[str, str]]:
    paths = sorted(
        root.glob("reports/briefs/*.md"),
        key=lambda path: (
            _report_date(path),
            _page_title(path).casefold(),
        ),
        reverse=True,
    )
    return [
        {_report_nav_title(path): path.relative_to(root).as_posix()}
        for path in paths
        if path.is_file()
    ]


def _pages(root: Path, pattern: str) -> list[dict[str, str]]:
    paths = sorted(root.glob(pattern), key=lambda path: _page_title(path).casefold())
    if pattern == "companies/*.md":
        paths.sort(
            key=lambda path: (
                not path.stem.endswith("POSCO"),
                _page_title(path).casefold(),
            )
        )
    return [
        {_page_title(path): path.relative_to(root).as_posix()}
        for path in paths
        if path.is_file()
    ]


def on_config(config: Any) -> Any:
    """Build concise navigation from the generated knowledge pages."""
    root = Path(config["docs_dir"])
    nav: list[dict[str, Any]] = [{"홈": "index.md"}]

    recent_updates = root / "recent-updates.md"
    if recent_updates.is_file():
        nav.append({"업데이트": "recent-updates.md"})

    technologies = _pages(root, "technologies/*.md")
    if technologies:
        nav.append({"기술별 현황": technologies})

    companies = _pages(root, "companies/*.md")
    if companies:
        nav.append({"기업별 현황": companies})

    projects = _pages(root, "projects/*.md")
    if projects:
        nav.append({"프로젝트 진행": projects})

    trend_reports: list[dict[str, str]] = []
    report_index = root / "reports" / "index.md"
    if report_index.is_file():
        trend_reports.append({"동향 보고서 안내": "reports/index.md"})
    academic_landscape = root / "reports" / "academic-landscape-2026.md"
    if academic_landscape.is_file():
        trend_reports.append(
            {
                _report_nav_title(academic_landscape):
                academic_landscape.relative_to(root).as_posix()
            }
        )
    trend_reports.extend(_report_pages(root))
    if trend_reports:
        nav.append({"동향 보고서": trend_reports})

    nav.extend(
        [
            {"검토 대기": "REVIEW.md"},
        ]
    )
    config["nav"] = nav
    return config
