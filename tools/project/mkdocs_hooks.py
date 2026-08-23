"""MkDocs integration for the generated Obsidian-compatible wiki."""

from __future__ import annotations

import html
import json
import posixpath
import re
from pathlib import Path, PurePosixPath
from typing import Any


WIKILINK_RE = re.compile(r"\[\[([^\[\]|]+?)(?:\|([^\]]+))?\]\]")
SIGNAL_WIKILINK_RE = re.compile(
    r"\[\[signals/(?P<signal_id>SIG-[A-Z0-9]+)(?:\|[^\]]+)?\]\]"
)
STRATEGIC_WARNING_WIKILINK_RE = re.compile(
    r"\[\[strategic-warnings/(?P<warning_id>WRN-[A-Z0-9-]+)(?:\|[^\]]+)?\]\]"
)
HALF_YEAR_REPORT_TITLE_RE = re.compile(
    r"^(?P<period>\d{4}년 [상하]반기) 철강 신기술·프로젝트 동향$"
)
COMPANY_DISPLAY_NAMES = {
    "COM-POSCO": "POSCO",
    "COM-POSCO-HOLDINGS": "POSCO Holdings",
    "COM-POSCO-INTERNATIONAL": "POSCO International",
}
SIGNAL_AXIS_ORDER = ("철강", "리튬", "전략광물", "에너지")
WARNING_LEVEL_NAV_PRIORITY = {
    "observe": 0,
    "watch": 1,
    "warning": 2,
    "critical": 3,
}


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


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _display_text(value: Any) -> str:
    if isinstance(value, list):
        return " · ".join(
            str(item).strip()
            for item in value
            if item is not None and str(item).strip()
        )
    return str(value or "").strip()


def _signal_ui_item(root: Path, signal_id: str) -> dict[str, Any] | None:
    signal_path = root / ".system" / "signals" / f"{signal_id}.json"
    if not signal_path.is_file():
        return None

    signal = _read_json(signal_path)
    insight_id = str(signal.get("insight_id") or "").strip()
    insight_path = root / ".system" / "insights" / f"{insight_id}.json"
    insight = _read_json(insight_path) if insight_id and insight_path.is_file() else {}
    company_names = [
        COMPANY_DISPLAY_NAMES.get(
            str(company_id),
            str(company_id).removeprefix("COM-").replace("-", " "),
        )
        for company_id in signal.get("company_ids", [])
        if str(company_id).strip()
    ]
    region = next(
        (
            _display_text(record.get(field))
            for record in (signal, insight)
            for field in ("country_region", "region", "regions", "countries")
            if _display_text(record.get(field))
        ),
        "",
    )
    decision_lens = signal.get("decision_lens") or {}
    opportunity = decision_lens.get("opportunity") or {}
    return {
        "title": _display_text(insight.get("title")),
        "sentence": _display_text(signal.get("sentence")),
        "company": " · ".join(company_names),
        "business_axis": _display_text(signal.get("business_axis")),
        "signal_type": _display_text(signal.get("signal_type")),
        "signal_role": _display_text(signal.get("signal_role")),
        "opportunity": _display_text(opportunity.get("business_effect")),
        "region": region,
        "business_impact": (signal.get("business_impact") or {}).get("score"),
        "urgency": (signal.get("urgency") or {}).get("score"),
        "assessed_at": _display_text(signal.get("assessed_at")),
    }


def _strategic_issue_ui_item(root: Path, warning_id: str) -> dict[str, Any] | None:
    warning_path = root / ".system" / "warnings" / f"{warning_id}.json"
    if not warning_path.is_file():
        return None
    warning = _read_json(warning_path)
    structured_context = warning.get("structured_context") or {}
    company_lens = warning.get("company_lens") or {}
    thesis_id = str(warning.get("thesis_id") or "").strip()
    thesis_path = root / ".system" / "theses" / f"{thesis_id}.json"
    thesis = _read_json(thesis_path) if thesis_id and thesis_path.is_file() else {}
    company_names = [
        COMPANY_DISPLAY_NAMES.get(
            str(company_id),
            str(company_id).removeprefix("COM-").replace("-", " "),
        )
        for company_id in (
            [structured_context.get("company_id")]
            if structured_context.get("company_id")
            else thesis.get("company_ids", [])
        )
        if str(company_id).strip()
    ]
    signal_types = set()
    for signal_id in thesis.get("supporting_signal_ids", []):
        signal_path = root / ".system" / "signals" / f"{signal_id}.json"
        if not signal_path.is_file():
            continue
        signal = _read_json(signal_path)
        if signal.get("status", "active") != "active":
            continue
        signal_type = _display_text(signal.get("signal_type"))
        if signal_type:
            signal_types.add(signal_type)
    category = _display_text(warning.get("issue_category"))
    if not category:
        category = next(iter(signal_types)) if len(signal_types) == 1 else "복합 이슈"
    return {
        "title": _display_text(warning.get("title")),
        "company": " · ".join(company_names),
        "business_axis": _display_text(warning.get("business_axis")),
        "signal_type": category,
        "management_function": _display_text(
            structured_context.get("management_functions")
        ),
        "region": _display_text(structured_context.get("regions")),
        "interest_level": {
            "core": "핵심 관심",
            "conditional": "조건부 관심",
        }.get(str(company_lens.get("interest_level") or ""), ""),
    }


def _signal_ui_payload(
    root: Path, src_path: str, source_markdown: str
) -> dict[str, Any] | None:
    normalized_path = src_path.replace("\\", "/")
    if normalized_path == "signals/index.md":
        signal_ids = dict.fromkeys(
            match.group("signal_id")
            for match in SIGNAL_WIKILINK_RE.finditer(source_markdown)
        )
        items = [
            item
            for signal_id in signal_ids
            if (item := _signal_ui_item(root, signal_id)) is not None
        ]
        return {"kind": "index", "items": items}

    match = re.fullmatch(r"signals/(?P<signal_id>SIG-[A-Z0-9]+)\.md", normalized_path)
    if not match:
        return None
    item = _signal_ui_item(root, match.group("signal_id"))
    return {"kind": "detail", "item": item} if item else None


def _strategic_issue_ui_payload(
    root: Path, src_path: str, source_markdown: str
) -> dict[str, Any] | None:
    normalized_path = src_path.replace("\\", "/")
    if normalized_path == "strategic-warnings/index.md":
        warning_ids = dict.fromkeys(
            match.group("warning_id")
            for match in STRATEGIC_WARNING_WIKILINK_RE.finditer(source_markdown)
        )
        items = [
            item
            for warning_id in warning_ids
            if (item := _strategic_issue_ui_item(root, warning_id)) is not None
        ]
        return {"kind": "strategic-index", "items": items}

    match = re.fullmatch(
        r"strategic-warnings/(?P<warning_id>WRN-[A-Z0-9-]+)\.md",
        normalized_path,
    )
    if not match:
        return None
    item = _strategic_issue_ui_item(root, match.group("warning_id"))
    return {"kind": "strategic-detail", "item": item} if item else None


def _strategic_issue_context_html(item: dict[str, Any]) -> str:
    pills = []
    for value, class_name, aria_prefix in (
        (item.get("company"), "signal-pill-company signal-company-name", "회사"),
        (item.get("business_axis"), "signal-pill-axis", "사업축"),
        (item.get("signal_type"), "signal-pill-type", "변화 유형"),
    ):
        text = _display_text(value)
        if not text:
            continue
        pills.append(
            '<span class="signal-pill '
            f'{class_name}" aria-label="{html.escape(f"{aria_prefix} {text}", quote=True)}">'
            f"{html.escape(text)}</span>"
        )
    return (
        '<div class="signal-detail-context strategic-issue-context">'
        '<div class="signal-pills" aria-label="회사, 사업축과 변화 유형">'
        f"{''.join(pills)}</div></div>"
    )


def _signal_ui_data_script(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    serialized = (
        serialized.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )
    kind = payload["kind"]
    return (
        # Material instant navigation executes inserted script nodes even when their
        # type is application/json. A template preserves inert JSON across both full
        # loads and instant navigation without producing a console SyntaxError.
        f'<template data-signal-ui="{kind}">'
        f"{serialized}</template>"
    )


def on_page_markdown(
    markdown: str,
    page: Any,
    config: Any,
    files: Any,
) -> str:
    """Render links and attach Signal UI data without changing source Markdown."""
    rendered = convert_wikilinks(markdown, page.file.src_path)
    root = Path(config["docs_dir"])
    payload = _signal_ui_payload(root, page.file.src_path, markdown)
    if payload is None:
        payload = _strategic_issue_ui_payload(root, page.file.src_path, markdown)
    if payload is None:
        return rendered
    if payload["kind"] == "strategic-detail":
        if "strategic-issue-context" in rendered:
            return rendered
        return f"{_strategic_issue_context_html(payload['item'])}\n\n{rendered}"
    return f"{_signal_ui_data_script(payload)}\n\n{rendered}"


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


def _signal_nav_groups(root: Path) -> list[dict[str, list[dict[str, str]]]]:
    grouped: dict[str, list[tuple[str, str, str]]] = {}
    for path in root.glob("signals/SIG-*.md"):
        if not path.is_file():
            continue
        record_path = root / ".system" / "signals" / f"{path.stem}.json"
        record = _read_json(record_path) if record_path.is_file() else {}
        axis = _display_text(record.get("business_axis")) or "기타"
        grouped.setdefault(axis, []).append(
            (
                _display_text(record.get("assessed_at")),
                _page_title(path),
                path.relative_to(root).as_posix(),
            )
        )

    axes = [*SIGNAL_AXIS_ORDER, *sorted(set(grouped) - set(SIGNAL_AXIS_ORDER))]
    return [
        {
            axis: [
                {title: relative_path}
                for _, title, relative_path in sorted(
                    sorted(
                        grouped.get(axis, []),
                        key=lambda item: item[1].casefold(),
                    ),
                    key=lambda item: item[0],
                    reverse=True,
                )
            ]
        }
        for axis in axes
        if grouped.get(axis)
    ]


def _strategic_warning_nav_groups(
    root: Path,
) -> list[dict[str, list[dict[str, str]]]]:
    grouped: dict[str, list[tuple[int, str, str, str]]] = {}
    for path in root.glob("strategic-warnings/WRN-*.md"):
        if not path.is_file():
            continue
        record_path = root / ".system" / "warnings" / f"{path.stem}.json"
        record = _read_json(record_path) if record_path.is_file() else {}
        if record.get("status", "active") != "active":
            continue
        axis = _display_text(record.get("business_axis")) or "기타"
        grouped.setdefault(axis, []).append(
            (
                WARNING_LEVEL_NAV_PRIORITY.get(_display_text(record.get("level")), -1),
                _display_text(record.get("last_reviewed_at")),
                _page_title(path),
                path.relative_to(root).as_posix(),
            )
        )

    axes = [*SIGNAL_AXIS_ORDER, *sorted(set(grouped) - set(SIGNAL_AXIS_ORDER))]
    groups = []
    for axis in axes:
        items = sorted(grouped.get(axis, []), key=lambda item: item[2].casefold())
        items.sort(key=lambda item: (item[0], item[1]), reverse=True)
        if items:
            groups.append(
                {axis: [{title: relative_path} for _, _, title, relative_path in items]}
            )
    return groups


def on_config(config: Any) -> Any:
    """Build concise navigation from the generated knowledge pages."""
    root = Path(config["docs_dir"])
    nav: list[dict[str, Any]] = [{"홈": "index.md"}]

    warning_groups = _strategic_warning_nav_groups(root)
    warning_index = root / "strategic-warnings" / "index.md"
    if warning_index.is_file():
        nav.append(
            {
                "핵심 전략 이슈": [
                    {"전체 이슈": "strategic-warnings/index.md"},
                    *warning_groups,
                ]
            }
        )

    signal_groups = _signal_nav_groups(root)
    signal_index = root / "signals" / "index.md"
    if signal_index.is_file():
        nav.append(
            {
                "마켓 시그널": [
                    {"전체 시그널": "signals/index.md"},
                    *signal_groups,
                ]
            }
        )

    recent_updates = root / "recent-updates.md"
    if recent_updates.is_file():
        nav.append({"최근 변화": "recent-updates.md"})

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
