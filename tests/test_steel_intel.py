import json
import re
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


SCRIPT_DIR = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "steel-intelligence"
    / "scripts"
)
sys.path.insert(0, str(SCRIPT_DIR))

import steel_intel  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
import mkdocs_hooks  # noqa: E402


class SteelIntelTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / "steel-wiki"
        steel_intel.scaffold(self.root)

    def tearDown(self):
        self.temp_dir.cleanup()

    def source_args(self, content_file, title, url, force=False):
        return Namespace(
            root=str(self.root),
            content_file=str(content_file),
            title=title,
            url=url,
            publisher="Example Steel",
            published_at="2026-07-21",
            collected_at="2026-07-25",
            source_type="company_release",
            language="en",
            reliability="primary",
            supporting_of=None,
            force=force,
        )

    def test_index_is_the_only_home_projection(self):
        self.assertTrue((self.root / "index.md").is_file())
        self.assertFalse((self.root / "HOME.md").exists())
        report_index = (
            self.root / "reports" / "index.md"
        ).read_text(encoding="utf-8")
        self.assertIn('!!! abstract "현재 발행 상태"', report_index)
        self.assertIn("아직 발행된 동향 보고서가 없습니다.", report_index)
        self.assertIn("## 보고서에서 바로 확인할 내용", report_index)
        self.assertIn("## 읽는 순서", report_index)

        legacy_home = self.root / "HOME.md"
        legacy_home.write_text("legacy duplicate\n", encoding="utf-8")
        steel_intel.sync_obsidian_store(self.root)

        self.assertFalse(legacy_home.exists())
        self.assertIn(
            "# 철강 기술 인텔리전스",
            (self.root / "index.md").read_text(encoding="utf-8"),
        )
        index = (self.root / "index.md").read_text(encoding="utf-8")
        self.assertIn(
            "classDef process fill:#EDF2FB,stroke:#3F66C9,color:#20242C",
            index,
        )
        self.assertIn(
            "classDef circular fill:#EDF7F2,stroke:#2F9765,color:#20242C",
            index,
        )
        self.assertIn("classDef enabler fill:#FFFFFF,stroke:#3F66C9", index)
        self.assertIn(
            "classDef outcome fill:#3F66C9,stroke:#3158B8,color:#FFFFFF",
            index,
        )
        self.assertIn("색상 범례 (AI 의미 그룹)", index)
        self.assertIn("옅은 코발트=전환 기술", index)

    def claim_args(self, source_id, value):
        return Namespace(
            root=str(self.root),
            subject_id="PRJ-EXAMPLE-DRI",
            predicate="target_start_date",
            value=value,
            source_id=[source_id],
            confidence="medium",
            as_of="2026-07-25",
            reason="Official project update",
        )

    def test_mkdocs_wikilinks_are_page_relative(self):
        markdown = (
            "[[index|홈]] "
            "[[sources/SRC-EXAMPLE|근거]] "
            "[[#한눈에-보기|이 문서의 요약]]"
        )
        rendered = mkdocs_hooks.convert_wikilinks(
            markdown,
            r"companies\COM-Example-Steel.md",
        )
        self.assertEqual(
            rendered,
            "[홈](../index.md) "
            "[근거](../sources/SRC-EXAMPLE.md) "
            "[이 문서의 요약](#한눈에-보기)",
        )

    def test_company_source_reference_uses_compact_link_label(self):
        reference = steel_intel.source_reference(
            "SRC-EXAMPLE",
            {
                "SRC-EXAMPLE": {
                    "publisher": "Example Steel",
                    "published_at": "2026-07-21",
                }
            },
        )
        self.assertEqual(
            reference,
            "[[sources/SRC-EXAMPLE|:material-link-variant:]]",
        )

    def test_technology_navigation_is_collapsed_and_marks_current_page(self):
        settings = {
            "technologies": [
                "hydrogen direct reduced iron",
                "electric smelting furnace",
                "molten oxide electrolysis",
            ]
        }
        markdown = "\n".join(
            steel_intel.technology_navigation_lines(
                "electric smelting furnace",
                settings,
            )
        )

        self.assertIn(
            '??? info "관련 기술 바로가기 · 현재 위치: 환원·용융 경로"',
            markdown,
        )
        self.assertNotIn("???+ info", markdown)
        self.assertIn(
            "**전기용융로 (Electric Smelting Furnace) · 현재**",
            markdown,
        )
        self.assertIn(
            "[[technologies/TEC-hydrogen-direct-reduced-iron"
            "|수소 직접환원철 (Hydrogen DRI)]]",
            markdown,
        )
        self.assertIn("**전해 기반 경로**", markdown)

    def test_technology_dossier_renders_generic_deep_profile(self):
        claims_by_subject = {
            "TEC-molten-oxide-electrolysis": [
                {
                    "predicate": "technical_definition",
                    "value": "용융 산화물에서 철과 산소를 직접 생산",
                    "status": "active",
                    "last_verified": "2026-07-25",
                    "source_ids": ["SRC-ACADEMIC"],
                },
                {
                    "predicate": "core_reaction",
                    "value": "Fe2O3 -> 2Fe + 1.5O2",
                    "status": "active",
                    "last_verified": "2026-07-25",
                    "source_ids": ["SRC-ACADEMIC"],
                },
                {
                    "predicate": "energy_intensity_estimate",
                    "value": "성숙 설비 가정 2.89-4.45 kWh/kg Fe",
                    "status": "active",
                    "last_verified": "2026-07-25",
                    "source_ids": ["SRC-ACADEMIC"],
                },
            ]
        }
        sources = {
            "SRC-ACADEMIC": {
                "source_id": "SRC-ACADEMIC",
                "title": "Academic MOE study",
                "publisher": "Example Journal",
                "published_at": "2026-07-07",
                "collected_at": "2026-07-25",
                "source_type": "academic",
                "url": "https://example.com/moe",
            }
        }

        markdown = "\n".join(
            steel_intel.technology_company_dossier_lines(
                "molten oxide electrolysis",
                {"companies": [], "technologies": ["molten oxide electrolysis"]},
                claims_by_subject,
                sources,
            )
        )

        self.assertIn("### 반응·셀·공정", markdown)
        self.assertIn("| **총괄 반응** | Fe2O3 -> 2Fe + 1.5O2", markdown)
        self.assertIn("### 에너지·환경·경제", markdown)
        self.assertIn("성숙 설비 가정 2.89-4.45 kWh/kg Fe", markdown)
        self.assertIn("| 학술 연구 |", markdown)
        self.assertNotIn("고온 용융염 전기분해가 아니라", markdown)

    def test_mkdocs_navigation_keeps_sources_out_of_sidebar(self):
        (self.root / "companies" / "COM-POSCO.md").write_text(
            "# POSCO 기술 현황\n",
            encoding="utf-8",
        )
        (self.root / "companies" / "COM-Zeta.md").write_text(
            "# Zeta Steel 기술 현황\n",
            encoding="utf-8",
        )
        (self.root / "technologies" / "TEC-hydrogen-dri.md").write_text(
            "# 수소 직접환원철 (Hydrogen DRI)\n",
            encoding="utf-8",
        )
        (self.root / "projects" / "PRJ-hydrogen-dri.md").write_text(
            "# 수소 직접환원철 프로젝트\n",
            encoding="utf-8",
        )
        config = {"docs_dir": str(self.root)}
        mkdocs_hooks.on_config(config)
        self.assertEqual(config["nav"][0], {"홈": "index.md"})
        self.assertEqual(
            config["nav"][1],
            {"업데이트": "recent-updates.md"},
        )
        self.assertNotIn("HOME.md", repr(config["nav"]))
        self.assertIn(
            {
                "수소 직접환원철 (Hydrogen DRI)":
                "technologies/TEC-hydrogen-dri.md"
            },
            config["nav"][2]["기술별 현황"],
        )
        self.assertEqual(
            config["nav"][3]["기업별 현황"][0],
            {"POSCO": "companies/COM-POSCO.md"},
        )
        self.assertEqual(
            config["nav"][4]["프로젝트 진행"][0],
            {
                "수소 직접환원철 프로젝트":
                "projects/PRJ-hydrogen-dri.md"
            },
        )
        self.assertNotIn("sources", str(config["nav"]))

    def test_mkdocs_navigation_exposes_trend_reports_but_not_audits(self):
        (self.root / "reports" / "index.md").write_text(
            "# 동향 보고서\n",
            encoding="utf-8",
        )
        (self.root / "reports" / "briefs" / "brief-2026-07-24.md").write_text(
            "# 일일 철강 기술 동향\n",
            encoding="utf-8",
        )
        (self.root / "reports" / "audits" / "audit-2026-07-25.md").write_text(
            "# Steel Intelligence Audit\n",
            encoding="utf-8",
        )

        config = {"docs_dir": str(self.root)}
        mkdocs_hooks.on_config(config)

        trend_nav = next(
            item["동향 보고서"]
            for item in config["nav"]
            if "동향 보고서" in item
        )
        self.assertEqual(
            trend_nav[0],
            {"동향 보고서 안내": "reports/index.md"},
        )
        self.assertIn(
            {"일일 철강 기술 동향": "reports/briefs/brief-2026-07-24.md"},
            trend_nav,
        )
        self.assertNotIn("audit-", repr(config["nav"]))

    def test_mermaid_contrast_fallback_is_loaded(self):
        config = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        theme = (
            PROJECT_ROOT
            / "steel-wiki"
            / "javascripts"
            / "mermaid-theme.js"
        ).read_text(encoding="utf-8")
        fallback = (
            PROJECT_ROOT
            / "steel-wiki"
            / "javascripts"
            / "mermaid-contrast.js"
        ).read_text(encoding="utf-8")

        self.assertIn("javascripts/mermaid-theme.js", config)
        self.assertIn("javascripts/mermaid-contrast.js", config)
        self.assertIn("pymdownx.superfences.fence_div_format", config)
        self.assertIn('primaryColor: "#edf2fb"', theme)
        self.assertIn('primaryBorderColor: "#3f66c9"', theme)
        self.assertIn('lineColor: "#6c737e"', theme)
        self.assertIn("MINIMUM_CONTRAST = 4.5", fallback)
        self.assertIn('style.setProperty("color"', fallback)
        self.assertIn('style.setProperty("fill"', fallback)

    def test_mermaid_fullscreen_viewer_is_loaded(self):
        config = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        viewer = (
            PROJECT_ROOT
            / "steel-wiki"
            / "javascripts"
            / "mermaid-viewer.js"
        ).read_text(encoding="utf-8")
        styles = (
            PROJECT_ROOT
            / "steel-wiki"
            / "stylesheets"
            / "extra.css"
        ).read_text(encoding="utf-8")

        self.assertIn("javascripts/mermaid-viewer.js", config)
        self.assertIn('button.setAttribute("title", "전체보기")', viewer)
        self.assertIn("mermaid-viewer-panel", viewer)
        self.assertIn('canvas.addEventListener("wheel"', viewer)
        self.assertIn('canvas.addEventListener("pointerdown"', viewer)
        self.assertIn('event.key === "Escape"', viewer)
        self.assertIn('data-action="zoom-out"', viewer)
        self.assertIn('data-action="zoom-in"', viewer)
        self.assertIn("const scaledWidth = size.width * scale", viewer)
        self.assertNotIn("scale(${scale})", viewer)
        self.assertIn("width: 27px", styles)
        self.assertIn("width: min(1480px, 80vw)", styles)
        self.assertIn("height: min(920px, 90vh)", styles)
        self.assertIn("border-color: #c9d5dc", styles)
        self.assertIn("backdrop-filter: blur(4px)", styles)

    def test_footnote_source_preview_is_loaded(self):
        config = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        tooltips = (
            PROJECT_ROOT
            / "steel-wiki"
            / "javascripts"
            / "footnote-tooltips.js"
        ).read_text(encoding="utf-8")
        styles = (
            PROJECT_ROOT
            / "steel-wiki"
            / "stylesheets"
            / "extra.css"
        ).read_text(encoding="utf-8")

        self.assertIn("javascripts/footnote-tooltips.js", config)
        self.assertIn('a.footnote-ref[href^=\'#fn\']', tooltips)
        self.assertIn('reference.setAttribute("aria-label"', tooltips)
        self.assertIn("data-footnote-tooltip", styles)
        self.assertIn(":focus-visible::after", styles)

    def test_mkdocs_headings_are_numbered_per_page(self):
        config = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        requirements = (
            PROJECT_ROOT / "requirements-docs.txt"
        ).read_text(encoding="utf-8")
        styles = (
            PROJECT_ROOT
            / "steel-wiki"
            / "stylesheets"
            / "extra.css"
        ).read_text(encoding="utf-8")

        self.assertIn("mkdocs-enumerate-headings-plugin==0.7.0", requirements)
        self.assertIn("- enumerate-headings:", config)
        self.assertIn("start_level: 2", config)
        self.assertIn("increment_across_pages: false", config)
        self.assertIn("toc_depth: 3", config)
        self.assertIn(".enumerate-headings-plugin", styles)
        self.assertIn(".md-typeset h2,", styles)
        self.assertIn(".md-typeset h3 {", styles)
        self.assertIn("color: var(--md-primary-fg-color)", styles)

    def test_recent_updates_table_balances_date_and_subject_columns(self):
        styles = (
            PROJECT_ROOT
            / "steel-wiki"
            / "stylesheets"
            / "extra.css"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "table[data-recent-updates-changes]",
            styles,
        )
        self.assertIn("width: 11%", styles)
        self.assertIn("width: 29%", styles)
        self.assertIn("width: 9%", styles)
        self.assertIn("white-space: nowrap", styles)

        page = type(
            "Page",
            (),
            {"file": type("File", (), {"src_path": "recent-updates.md"})()},
        )()
        html = "<h2>실행</h2><table></table><h2>변경</h2><table></table>"
        marked = mkdocs_hooks.on_page_content(html, page, None, None)
        self.assertEqual(marked.count("data-recent-updates-changes"), 1)
        self.assertIn(
            "<h2>변경</h2><table data-recent-updates-changes>",
            marked,
        )

    def test_home_matrix_gives_china_baowu_two_line_width(self):
        styles = (
            PROJECT_ROOT
            / "steel-wiki"
            / "stylesheets"
            / "extra.css"
        ).read_text(encoding="utf-8")

        self.assertIn(
            'table th a[href$="companies/COM-China-Baowu/"]',
            styles,
        )
        self.assertIn("display: inline-block", styles)
        self.assertIn("width: 6.25rem", styles)
        self.assertIn("word-break: keep-all", styles)

    def test_mkdocs_search_prioritizes_reader_pages(self):
        config = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        wiki_root = PROJECT_ROOT / "steel-wiki"

        source_meta = (wiki_root / "sources" / ".meta.yml").read_text(
            encoding="utf-8"
        )
        company_meta = (wiki_root / "companies" / ".meta.yml").read_text(
            encoding="utf-8"
        )
        technology_meta = (
            wiki_root / "technologies" / ".meta.yml"
        ).read_text(encoding="utf-8")
        project_meta = (wiki_root / "projects" / ".meta.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("- material/meta", config)
        self.assertIn("exclude: true", source_meta)
        self.assertIn("boost: 1.2", company_meta)
        self.assertIn("boost: 1.2", technology_meta)
        self.assertIn("boost: 1.1", project_meta)

    def test_duplicate_conflict_review_audit_and_brief_flow(self):
        incoming = Path(self.temp_dir.name) / "incoming"
        incoming.mkdir()
        first = incoming / "first.md"
        first.write_text(
            "Example Steel announced that the hydrogen DRI project targets "
            "commercial operation in 2027. Capacity is 1 million tonnes per year.",
            encoding="utf-8",
        )

        created = steel_intel.add_source(
            self.source_args(
                first,
                "Example Steel hydrogen DRI project update",
                "https://example.com/news/update?utm_source=newsletter",
            )
        )
        self.assertEqual(created["action"], "created")
        first_source_id = created["source_id"]

        duplicate = steel_intel.add_source(
            self.source_args(
                first,
                "Syndicated Example Steel hydrogen DRI update",
                "https://media.example.org/reprint",
            )
        )
        self.assertEqual(duplicate["action"], "exact_duplicate")
        self.assertEqual(duplicate["source_id"], first_source_id)

        similar = incoming / "similar.md"
        similar.write_text(
            "Example Steel announced that the hydrogen DRI project now targets "
            "commercial operation in 2029. Capacity is 1 million tonnes per year.",
            encoding="utf-8",
        )
        duplicate_review = steel_intel.add_source(
            self.source_args(
                similar,
                "Example Steel hydrogen DRI project revised update",
                "https://industry.example.net/revised-update",
            )
        )
        self.assertEqual(duplicate_review["action"], "review_required")
        self.assertEqual(duplicate_review["type"], "duplicate_candidate")

        duplicate_resolved = steel_intel.resolve_review(
            Namespace(
                root=str(self.root),
                review_id=duplicate_review["review_id"],
                decision="accept-new",
                rationale="The revised date is material independent content.",
                related_source=None,
            )
        )
        self.assertEqual(duplicate_resolved["action"], "resolved")
        second = duplicate_resolved["result"]
        self.assertEqual(second["action"], "created")

        first_claim = steel_intel.add_claim(
            self.claim_args(first_source_id, "2027")
        )
        self.assertEqual(first_claim["action"], "created")
        project_page = (
            self.root / "projects" / "PRJ-EXAMPLE-DRI.md"
        )
        source_page = (
            self.root / "sources" / f"{first_source_id}.md"
        )
        self.assertTrue(project_page.exists())
        self.assertTrue(source_page.exists())
        project_page_text = project_page.read_text(encoding="utf-8")
        self.assertIn("## 확인된 핵심 정보", project_page_text)
        self.assertIn("| **목표 가동 시점** | 2027", project_page_text)
        self.assertIn("## 전체 확인 이력", project_page_text)
        self.assertIn("| 2026-07-21 | 발표·검증 |", project_page_text)
        self.assertIn("| 2027 | 목표 일정 | **목표 가동 시점**", project_page_text)
        self.assertIn(
            f"[[sources/{first_source_id}|보관 원문·메타데이터]]",
            project_page_text,
        )
        self.assertNotIn("Subject ID", project_page_text)
        self.assertNotIn("Claim ID", project_page_text)
        self.assertNotIn("### `target_start_date`", project_page_text)
        self.assertIn(
            "[[projects/PRJ-EXAMPLE-DRI|PRJ-EXAMPLE-DRI]]",
            source_page.read_text(encoding="utf-8"),
        )
        self.assertIn(
            "## 보관 원문",
            source_page.read_text(encoding="utf-8"),
        )
        self.assertIn(
            "> Example Steel announced that the hydrogen DRI project targets",
            source_page.read_text(encoding="utf-8"),
        )
        steel_intel.add_claim(
            Namespace(
                root=str(self.root),
                subject_id="COM-Example-Steel",
                predicate="hydrogen_dri_status",
                value="공식 프로젝트 발표 확인",
                source_id=[first_source_id],
                confidence="medium",
                as_of="2026-07-25",
                reason="Company technology coverage test",
            )
        )
        company_page = (
            self.root / "companies" / "COM-Example-Steel.md"
        ).read_text(encoding="utf-8")
        self.assertIn("# Example Steel 기술 현황", company_page)
        self.assertIn('!!! abstract "한눈에 보기"', company_page)
        self.assertIn("## 기술 포트폴리오", company_page)
        self.assertIn("## 기술별 근거와 확인 과제", company_page)
        self.assertIn(
            '??? info "수소 직접환원철 (Hydrogen DRI) · 공식 현황 확인"',
            company_page,
        )
        self.assertIn(
            "**확인된 사실:** 공식 프로젝트 발표 확인",
            company_page,
        )
        self.assertIn(
            "**확인 날짜:** 발표 2026-07-21 · 검증 2026-07-25",
            company_page,
        )
        self.assertNotIn("공식 근거를 확인하지 못한 영역", company_page)
        self.assertNotIn(
            "용융산화물 전기분해 (Molten Oxide Electrolysis)",
            company_page,
        )
        self.assertIn("## AI 분석", company_page)
        self.assertIn("## 근거 자료", company_page)
        self.assertNotIn("Claim ID", company_page)
        self.assertNotIn(first_claim["claim_id"], company_page)
        index_page = (self.root / "index.md").read_text(encoding="utf-8")
        self.assertIn("# 철강 기술 인텔리전스", index_page)
        recent_updates = (self.root / "recent-updates.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("# 최근 업데이트", recent_updates)
        self.assertIn("## 최근 조사 실행", recent_updates)
        self.assertIn("## 변경된 지식", recent_updates)
        self.assertIn("신규 등록", recent_updates)
        self.assertIn(first_source_id, recent_updates)
        self.assertIn("|근거 보기]]", recent_updates)
        self.assertNotIn("현재 유효하지 않음 · 현재 유효", recent_updates)
        self.assertIn(
            "[[companies/COM-Example-Steel|Example Steel]]",
            index_page,
        )
        self.assertIn("## 기술별 기업 현황", index_page)
        self.assertIn("| 기술 |", index_page)
        self.assertIn(
            "[[companies/COM-Example-Steel|● 확인]]",
            index_page,
        )
        self.assertNotIn("○ 미확인", index_page)
        self.assertNotIn("기업 기술 현황 HTML 열기", index_page)
        technology_page = (
            self.root
            / steel_intel.technology_page_path("hydrogen direct reduced iron")
        ).read_text(encoding="utf-8")
        self.assertIn(
            "# 수소 직접환원철 (Hydrogen DRI)",
            technology_page,
        )
        self.assertNotIn("기업 현황", technology_page.splitlines()[2])
        self.assertIn("## 기업별 상세 현황", technology_page)
        self.assertIn(
            "[[companies/COM-Example-Steel|Example Steel]]",
            technology_page,
        )
        self.assertIn(
            "**확인된 현황.** 공식 프로젝트 발표 확인",
            technology_page,
        )
        self.assertIn(
            "**날짜:** 발표 2026-07-21 · 수집 2026-07-25 · 검증 2026-07-25",
            technology_page,
        )
        self.assertNotIn("공식 근거 미확인", technology_page)
        self.assertFalse((self.root / "reports" / "companies").exists())
        self.assertFalse((self.root / "기술별-기업현황.html").exists())
        self.assertFalse((self.root / "기업별-기술현황.html").exists())

        conflict = steel_intel.add_claim(
            self.claim_args(second["source_id"], "2029")
        )
        self.assertEqual(conflict["action"], "review_required")
        self.assertEqual(conflict["type"], "claim_conflict")

        resolved = steel_intel.resolve_review(
            Namespace(
                root=str(self.root),
                review_id=conflict["review_id"],
                decision="supersede",
                rationale="Newer official update replaces the earlier target.",
                related_source=None,
            )
        )
        self.assertEqual(resolved["action"], "resolved")
        self.assertIn(
            "- 검토 대기 항목이 없습니다.",
            (self.root / "REVIEW.md").read_text(encoding="utf-8"),
        )
        old_claim = json.loads(
            (
                self.root
                / ".system"
                / "claims"
                / f"{first_claim['claim_id']}.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(old_claim["status"], "superseded")

        log_before_search = (self.root / "log.md").read_text(encoding="utf-8")
        search_result = steel_intel.search_store(
            Namespace(root=str(self.root), query="hydrogen DRI 2029", limit=5)
        )
        self.assertEqual(search_result["action"], "search_results")
        self.assertTrue(search_result["verification_required"])
        self.assertEqual(search_result["claims"][0]["value"], "2029")
        self.assertEqual(search_result["claims"][0]["status"], "active")
        self.assertIn(
            second["source_id"],
            {item["source_id"] for item in search_result["sources"]},
        )
        self.assertIn(
            "projects/PRJ-EXAMPLE-DRI.md",
            {item["path"] for item in search_result["notes"]},
        )
        self.assertTrue(
            any(
                item["from"] == "projects/PRJ-EXAMPLE-DRI.md"
                and item["to"]
                == f"sources/{second['source_id']}.md"
                for item in search_result["followed_links"]
            )
        )
        self.assertEqual(
            (self.root / "log.md").read_text(encoding="utf-8"),
            log_before_search,
        )

        audit = steel_intel.audit_store(
            Namespace(root=str(self.root), stale_days=180)
        )
        self.assertEqual(audit["counts"]["source_integrity"], 0)
        self.assertEqual(audit["counts"]["claim_evidence"], 0)

        change_brief = steel_intel.brief(
            Namespace(root=str(self.root), since="2026-07-20", html=True)
        )
        self.assertGreaterEqual(change_brief["change_count"], 2)
        self.assertTrue((self.root / change_brief["report"]).exists())
        self.assertTrue((self.root / change_brief["html_report"]).exists())
        brief_markdown = (self.root / change_brief["report"]).read_text(
            encoding="utf-8"
        )
        self.assertIn("# 철강 기술 동향 브리프", brief_markdown)
        self.assertIn('!!! abstract "한눈에 보기"', brief_markdown)
        self.assertIn("## 확인된 변화", brief_markdown)
        self.assertNotIn("Claim ID", brief_markdown)
        self.assertNotIn("| Date | Claim |", brief_markdown)
        report_index = (self.root / "reports" / "index.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("**발행된 보고서 1건**", report_index)
        self.assertIn(
            "철강 기술 동향 브리프 · 2026-07-20–2026-07-25",
            report_index,
        )
        html_report = (self.root / change_brief["html_report"]).read_text(
            encoding="utf-8"
        )
        self.assertIn('<header class="report-header">', html_report)
        self.assertIn('id="source-1"', html_report)
        self.assertIn("https://example.com/news/update?utm_source=newsletter", html_report)
        self.assertTrue(html_report.endswith("</html>\n"))

        custom_markdown = self.root / "reports" / "briefs" / "custom-report.md"
        custom_markdown.write_text(
            "---\n"
            'title: "Custom sourced report"\n'
            "date: 2026-07-25\n"
            "---\n\n"
            "# Custom sourced report\n\n"
            f"Verified evidence: {first_source_id}\n\n"
            "<script>alert('unsafe')</script>\n\n"
            "[unsafe link](javascript:alert(1))\n",
            encoding="utf-8",
        )
        rendered = steel_intel.render_report(
            Namespace(
                root=str(self.root),
                input=str(custom_markdown),
                output=None,
            )
        )
        custom_html = (self.root / rendered["html_report"]).read_text(
            encoding="utf-8"
        )
        self.assertIn("&lt;script&gt;", custom_html)
        self.assertNotIn("<script>alert", custom_html)
        self.assertNotIn('href="javascript:', custom_html)
        self.assertEqual(rendered["source_count"], 1)

        for page in [
            self.root / "REVIEW.md",
            self.root / "index.md",
            *sorted((self.root / "companies").glob("**/*.md")),
            *sorted((self.root / "technologies").glob("**/*.md")),
            *sorted((self.root / "projects").glob("**/*.md")),
            *sorted((self.root / "entities").glob("**/*.md")),
            *sorted((self.root / "sources").glob("**/*.md")),
        ]:
            text = page.read_text(encoding="utf-8")
            for target in re.findall(r"\[\[([^]|]+)(?:\|[^]]+)?\]\]", text):
                self.assertTrue(
                    (self.root / f"{target}.md").exists(),
                    f"Broken wikilink in {page}: {target}",
                )

    def test_audit_detects_raw_source_mutation(self):
        incoming = Path(self.temp_dir.name) / "source.md"
        incoming.write_text("Original immutable source.", encoding="utf-8")
        created = steel_intel.add_source(
            self.source_args(
                incoming,
                "Immutable source",
                "https://example.com/immutable",
            )
        )
        raw_path = self.root / created["raw_path"]
        raw_path.write_text("Modified source.", encoding="utf-8")

        audit = steel_intel.audit_store(
            Namespace(root=str(self.root), stale_days=180)
        )
        self.assertEqual(audit["counts"]["source_integrity"], 1)

    def test_optional_source_images_are_projected_and_audited(self):
        incoming = Path(self.temp_dir.name) / "source.md"
        incoming.write_text(
            "Example Steel published a technical update with an equipment photo.",
            encoding="utf-8",
        )
        created = steel_intel.add_source(
            self.source_args(
                incoming,
                "Equipment photo source",
                "https://example.com/equipment-update",
            )
        )
        source_id = created["source_id"]
        steel_intel.add_claim(self.claim_args(source_id, "2028"))

        image_file = Path(self.temp_dir.name) / "facility.png"
        image_file.write_bytes(
            bytes.fromhex(
                "89504e470d0a1a0a"
                "0000000d49484452000000010000000108060000001f15c489"
                "0000000d4944415408d763f8ffff3f0005fe02fea73581a8"
                "0000000049454e44ae426082"
            )
        )
        added = steel_intel.add_image(
            Namespace(
                root=str(self.root),
                source_id=source_id,
                image_file=str(image_file),
                image_url=None,
                origin_url="https://example.com/equipment-update",
                caption="Example Steel 실증 설비 전경",
                alt_text="원통형 반응기와 배관이 설치된 실증 설비",
                creator="Example Steel",
                kind="facility_photo",
                rights_status="permitted",
                rights_note="공식 미디어 자료의 내부 기술검토 사용 조건 확인",
            )
        )
        self.assertEqual(added["action"], "image_added")
        local_image = self.root / added["local_path"]
        self.assertTrue(local_image.is_file())

        link_only = steel_intel.add_image(
            Namespace(
                root=str(self.root),
                source_id=source_id,
                image_file=None,
                image_url="https://example.com/media/restricted.jpg",
                origin_url="https://example.com/equipment-update",
                caption="상세 장치 배치도",
                alt_text=None,
                creator=None,
                kind="equipment_drawing",
                rights_status="link_only",
                rights_note="복제 권한이 불명확해 원문 링크만 보존",
            )
        )
        self.assertIsNone(link_only["local_path"])

        source_page = (
            self.root / "sources" / f"{source_id}.md"
        ).read_text(encoding="utf-8")
        project_page = (
            self.root / "projects" / "PRJ-EXAMPLE-DRI.md"
        ).read_text(encoding="utf-8")
        for page in (source_page, project_page):
            self.assertIn("## 설비·공정 이미지", page)
            self.assertIn("Example Steel 실증 설비 전경", page)
            self.assertIn("실제 설비 사진", page)
        self.assertIn(
            "![상세 장치 배치도]"
            "(<https://example.com/media/restricted.jpg>)"
            "{ .steel-media-image .steel-media-detail }",
            source_page,
        )
        self.assertIn(
            "![상세 장치 배치도]"
            "(<https://example.com/media/restricted.jpg>)"
            "{ .steel-media-image .steel-hero-image .steel-media-detail }",
            project_page,
        )
        self.assertIn(f"(../{added['local_path']})", source_page)

        record = json.loads(
            (
                self.root
                / ".system"
                / "source-records"
                / f"{source_id}.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(len(record["images"]), 2)
        self.assertEqual(record["images"][0]["content_sha256"], steel_intel.raw_sha256(
            local_image.read_bytes()
        ))
        clean_audit = steel_intel.audit_store(
            Namespace(root=str(self.root), stale_days=180)
        )
        self.assertEqual(clean_audit["counts"]["media_integrity"], 0)
        self.assertEqual(clean_audit["counts"]["media_schema"], 0)

        local_image.write_bytes(b"changed")
        changed_audit = steel_intel.audit_store(
            Namespace(root=str(self.root), stale_days=180)
        )
        self.assertEqual(changed_audit["counts"]["media_integrity"], 1)

    def test_link_only_image_can_be_rendered_as_remote_representative_image(self):
        source_id = "SRC-REMOTE-IMAGE"
        lines, excluded_media_ids = steel_intel.representative_image_lines(
            [source_id],
            {
                source_id: {
                    "images": [
                        {
                            "media_id": "MED-REMOTE",
                            "image_url": "https://example.com/media/cell-tap.jpg",
                            "origin_url": "https://example.com/official-release",
                            "caption": "공식 원문에 공개된 전해 셀 출선 장면",
                            "alt_text": "전해 셀에서 용융금속을 출선하는 장면",
                            "kind": "facility_photo",
                            "rights_status": "link_only",
                        }
                    ]
                }
            },
        )

        rendered = "\n".join(lines)
        self.assertIn(
            "![전해 셀에서 용융금속을 출선하는 장면]"
            "(<https://example.com/media/cell-tap.jpg>)"
            "{ .steel-media-image .steel-hero-image .steel-media-compact }",
            rendered,
        )
        self.assertIn("권리 `link_only`", rendered)
        self.assertIn("[원문 페이지](https://example.com/official-release)", rendered)
        self.assertEqual(excluded_media_ids, {"MED-REMOTE"})

    def test_link_only_gallery_embeds_remote_image_without_copying_it(self):
        source_id = "SRC-GALLERY-REMOTE"
        gallery = "\n".join(
            steel_intel.media_gallery_lines(
                [source_id],
                {
                    source_id: {
                        "images": [
                            {
                                "media_id": "MED-GALLERY-REMOTE",
                                "image_url": "https://example.com/media/process.png",
                                "origin_url": "https://example.com/official-release",
                                "caption": "공식 공정도",
                                "alt_text": "공식 공정 구성도",
                                "kind": "process_diagram",
                                "rights_status": "link_only",
                            }
                        ]
                    }
                },
            )
        )

        self.assertIn(
            "![공식 공정 구성도]"
            "(<https://example.com/media/process.png>)"
            "{ .steel-media-image .steel-media-detail }",
            gallery,
        )
        self.assertNotIn("이미지를 복제하지 않았습니다", gallery)

    def test_representative_image_prefers_process_diagram_for_technology_page(self):
        source_id = "SRC-ESF-IMAGES"
        lines, excluded_media_ids = steel_intel.representative_image_lines(
            [source_id],
            {
                source_id: {
                    "images": [
                        {
                            "media_id": "MED-FACILITY",
                            "image_url": "https://example.com/esf-facility.jpg",
                            "origin_url": "https://example.com/esf",
                            "caption": "ESF 실증 설비",
                            "alt_text": "전기용융로 실증 설비",
                            "kind": "facility_photo",
                            "rights_status": "link_only",
                        },
                        {
                            "media_id": "MED-PROCESS",
                            "image_url": "https://example.com/esf-process.png",
                            "origin_url": "https://example.com/esf",
                            "caption": "ESF 공정 구성도",
                            "alt_text": "전기용융로 공정 구성도",
                            "kind": "process_diagram",
                            "rights_status": "link_only",
                        },
                    ]
                }
            },
            preferred_kinds=("process_diagram", "facility_photo"),
        )

        rendered = "\n".join(lines)
        self.assertIn("https://example.com/esf-process.png", rendered)
        self.assertNotIn("https://example.com/esf-facility.jpg", rendered)
        self.assertEqual(excluded_media_ids, {"MED-PROCESS"})

    def test_technology_dossier_links_related_project_status_schedule_and_capacity(self):
        source_id = "SRC-NEOSMELT"
        claims_by_subject = {
            "TEC-electric-smelting-furnace": [
                {
                    "predicate": "technical_definition",
                    "value": "환원철을 용융·정련해 용선을 생산하는 전기 용융 공정",
                    "status": "active",
                    "last_verified": "2026-07-25",
                    "source_ids": [source_id],
                }
            ],
            "PRJ-NEOSMELT-KWINANA": [
                {
                    "predicate": "project_status",
                    "value": "최종 설계 및 투자결정 준비 중",
                    "status": "active",
                    "last_verified": "2026-07-25",
                    "source_ids": [source_id],
                },
                {
                    "predicate": "capacity_tpy",
                    "value": "연간 30,000~40,000톤 용선",
                    "status": "active",
                    "last_verified": "2026-07-25",
                    "source_ids": [source_id],
                },
                {
                    "predicate": "target_commissioning_date",
                    "value": "2028년 하반기",
                    "status": "active",
                    "last_verified": "2026-07-25",
                    "source_ids": [source_id],
                },
                {
                    "predicate": "capture_capacity_tpd",
                    "value": "5 t-CO2/day",
                    "status": "active",
                    "last_verified": "2026-07-25",
                    "source_ids": [source_id],
                },
            ],
        }
        sources = {
            source_id: {
                "source_id": source_id,
                "title": "NeoSmelt project update",
                "publisher": "BHP",
                "published_at": "2026-07-01",
                "collected_at": "2026-07-25",
                "source_type": "company_release",
                "url": "https://example.com/neosmelt",
            }
        }

        markdown = "\n".join(
            steel_intel.technology_company_dossier_lines(
                "electric smelting furnace",
                {"companies": [], "technologies": ["electric smelting furnace"]},
                claims_by_subject,
                sources,
            )
        )

        self.assertIn("## 관련 프로젝트", markdown)
        self.assertIn("PRJ-NEOSMELT-KWINANA", markdown)
        self.assertIn("최종 설계 및 투자결정 준비 중", markdown)
        self.assertIn("연간 30,000~40,000톤 용선", markdown)
        self.assertIn("2028년 하반기", markdown)
        self.assertIn("5 t-CO2/day", markdown)
        self.assertNotIn("<br>", markdown)

    def test_project_timeline_supports_month_dates_and_hides_bad_correction_values(self):
        source_id = "SRC-CORRECTION"
        claims = [
            {
                "predicate": "project_start_date",
                "value": "2024-02",
                "status": "active",
                "source_ids": [source_id],
            },
            {
                "predicate": "funding_amount",
                "value": "A million",
                "status": "superseded",
                "source_ids": [source_id],
                "history": [
                    {
                        "action": "status_changed",
                        "reason": "PowerShell 변수 확장으로 통화 기호와 금액이 누락된 입력 오류",
                    }
                ],
            },
        ]
        sources = {
            source_id: {
                "published_at": "2025-06-17",
                "collected_at": "2026-07-25",
            }
        }

        rows = steel_intel.project_timeline_rows(claims, sources)
        rendered = "\n".join(" | ".join(row) for row in rows)

        self.assertIn("2024-02", rendered)
        self.assertNotIn("A million", rendered)
        self.assertEqual(
            steel_intel.humanize_historical_claim_value(claims[1]),
            "입력 교정으로 대체됨 — 현재 유효 Claim과 원문 금액 참조",
        )

    def test_low_carbon_pathway_has_deep_structure_and_execution_timeline(self):
        detail = steel_intel.TECHNOLOGY_DETAILS["low-carbon ironmaking"]

        self.assertIn("다중 경로", detail["category"])
        self.assertIn("재생전력·전력망", detail["process_mermaid"])
        self.assertIn("PRJ-POSCO-GWANGYANG-EAF", detail["related_projects"])
        self.assertIn("PRJ-SSAB-LULEA-ELECTRIC-MILL", detail["related_projects"])
        self.assertIn("PRJ-TK-H2STEEL-DUISBURG", detail["related_projects"])
        self.assertGreaterEqual(len(detail["analysis_points"]), 6)
        self.assertGreaterEqual(len(detail["posco_implications"]), 3)
        self.assertEqual(
            steel_intel.PROJECT_TIMELINE_PREDICATES["tower_erection_date"],
            "실행 일정",
        )
        self.assertEqual(
            steel_intel.PREDICATE_LABELS["fid_conversion_rate_2026"],
            "FID 전환 비율",
        )

    def test_aqueous_electrolysis_has_deep_analysis_and_hides_event_photo(self):
        detail = steel_intel.TECHNOLOGY_DETAILS[
            "low-temperature aqueous iron electrolysis"
        ]

        self.assertIn("2단 전해채취 스택", detail["process_mermaid"])
        self.assertGreaterEqual(len(detail["analysis_points"]), 6)
        self.assertGreaterEqual(len(detail["posco_implications"]), 3)
        self.assertFalse(
            steel_intel.MEDIA_DISPLAY_OVERRIDES[
                "MED-098B84E432A7"
            ]["display_eligible"]
        )

    def test_markdown_settings_sync_and_drive_search_and_projection(self):
        settings_path = self.root.parent / "WIKI-SETTINGS.md"
        settings_path.write_text(
            "# LLM Wiki 관심사 설정\n\n"
            "## 분석 관점\n\n"
            "- 사업성 분석\n\n"
            "## 우선 기업\n\n"
            "- Example Steel\n\n"
            "## 중점 관찰 항목\n\n"
            "- capacity_tpy\n"
            "- target_start_date\n\n"
            "## 운영 값\n\n"
            "- 검색 겹침 일수: 7\n"
            "- Claim 재검증 일수: 45\n",
            encoding="utf-8",
        )
        synced = steel_intel.sync_settings(
            Namespace(root=str(self.root))
        )
        self.assertTrue(synced["changed"])
        watchlist = json.loads(
            (self.root / "config" / "watchlist.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(watchlist["companies"], ["Example Steel"])
        self.assertEqual(watchlist["focus"], ["사업성 분석"])
        self.assertEqual(watchlist["claim_stale_days"], 45)

        source_file = Path(self.temp_dir.name) / "settings-source.md"
        source_file.write_text(
            "Example Steel project capacity is 1 million tonnes and starts in 2029.",
            encoding="utf-8",
        )
        source = steel_intel.add_source(
            self.source_args(
                source_file,
                "Example Steel project facts",
                "https://example.com/settings-source",
            )
        )
        for predicate, value in (
            ("target_start_date", "2029"),
            ("capacity_tpy", "1000000"),
        ):
            steel_intel.add_claim(
                Namespace(
                    root=str(self.root),
                    subject_id="PRJ-EXAMPLE-DRI",
                    predicate=predicate,
                    value=value,
                    source_id=[source["source_id"]],
                    confidence="medium",
                    as_of="2026-07-25",
                    reason="Settings projection test",
                )
            )

        project_page = (
            self.root / "projects" / "PRJ-EXAMPLE-DRI.md"
        ).read_text(encoding="utf-8")
        self.assertLess(
            project_page.index("연간 생산능력"),
            project_page.index("목표 가동 시점"),
        )
        self.assertIn(
            "- 사업성 분석",
            (self.root / "index.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "- **기업:** Example Steel",
            (self.root / "index.md").read_text(encoding="utf-8"),
        )
        search = steel_intel.search_store(
            Namespace(
                root=str(self.root),
                query="PRJ-EXAMPLE-DRI",
                limit=5,
            )
        )
        self.assertEqual(search["claims"][0]["predicate"], "capacity_tpy")
        self.assertEqual(search["focus"], ["사업성 분석"])

        settings_path.write_text(
            settings_path.read_text(encoding="utf-8").replace(
                "- Example Steel", "- Updated Steel"
            ),
            encoding="utf-8",
        )
        steel_intel.search_store(
            Namespace(
                root=str(self.root),
                query="PRJ-EXAMPLE-DRI",
                limit=5,
            )
        )
        auto_synced = json.loads(
            (self.root / "config" / "watchlist.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(auto_synced["companies"], ["Updated Steel"])

if __name__ == "__main__":
    unittest.main()
