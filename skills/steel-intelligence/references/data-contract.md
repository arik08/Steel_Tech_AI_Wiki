# 데이터 계약

## 목차

1. 디렉터리
2. 출처
3. 주장
4. 검토
5. 엔터티와 이벤트
6. 실행 기록과 보고서

## 1. 디렉터리

```text
project/
├── WIKI-SETTINGS.md          # 사람이 편집하는 관심사·운영 설정
└── steel-wiki/
    ├── AGENTS.md
    ├── config/
    │   └── watchlist.json   # Markdown 설정의 기계용 JSON 캐시
    ├── index.md             # 사람이 보는 운영 시작 화면
    ├── REVIEW.md            # 사람이 보는 검토 대기열
    ├── companies/           # 회사 통합 문서
    ├── technologies/        # 기술 통합 문서
    ├── projects/            # 프로젝트 통합 문서
    ├── entities/            # 기타 주체 통합 문서
    ├── events/              # 사람이 보강하는 사건 노트
    ├── assets/
    │   └── media/           # 사용 권리가 확인된 Source 연결 이미지
    ├── sources/
    │   └── SRC-*.md         # 메타데이터·연결·원문 통합 페이지
    ├── .system/
    │   ├── raw/             # 등록 후 불변인 원문
    │   ├── source-records/  # source별 JSON 메타데이터
    │   ├── source-candidates/
    │   ├── claims/          # 상태 기준인 원자적 주장 JSON
    │   ├── reviews/
    │   │   ├── pending/
    │   │   └── resolved/
    │   └── runs/            # 검색 범위·쿼리·성공/실패
    ├── reports/
    │   ├── briefs/
    │   └── audits/
    └── log.md
```

`WIKI-SETTINGS.md`가 설정의 기준이다. `watchlist.json`을 직접 편집하지 않는다.
`steel_intel.py` 명령을 실행하면 Markdown 변경사항을 JSON에 자동 반영한다. 즉시
동기화하려면 `sync-settings`, 현재 적용값을 확인하려면 `show-settings`를 사용한다.

## 2. 출처

`.system/source-records/SRC-*.json`을 기준으로 한다.

```json
{
  "source_id": "SRC-20260725-A1B2C3D4",
  "title": "Project update",
  "url": "https://example.com/update",
  "canonical_url": "https://example.com/update",
  "publisher": "AIST",
  "published_at": "2026-07-21",
  "collected_at": "2026-07-25",
  "source_type": "academic",
  "language": "en",
  "reliability": "primary",
  "academic": {
    "kind": "conference_paper",
    "authors": ["A. Researcher", "B. Engineer"],
    "venue": "AISTech 2026 Proceedings",
    "doi": "10.1234/example.2026.001",
    "conference_name": "AISTech 2026",
    "conference_date": "2026-05-04",
    "conference_location": "Pittsburgh, USA",
    "peer_review_status": "peer_reviewed"
  },
  "content_sha256": "...",
  "raw_path": ".system/raw/SRC-20260725-A1B2C3D4.md",
  "previous_version": null,
  "supporting_sources": [],
  "images": [
    {
      "media_id": "MED-1234ABCDEF56",
      "kind": "facility_photo",
      "caption": "실증 설비 전경",
      "alt_text": "원통형 반응기와 배관이 설치된 실증 설비",
      "creator": "Example Steel",
      "image_url": "https://example.com/media/plant.jpg",
      "origin_url": "https://example.com/update",
      "rights_status": "permitted",
      "rights_note": "공식 미디어 자료 사용 조건 확인",
      "collected_at": "2026-07-25",
      "content_sha256": "...",
      "local_path": "assets/media/SRC-20260725-A1B2C3D4/MED-1234ABCDEF56.jpg",
      "subject_ids": ["COM-EXAMPLE-STEEL", "PRJ-HAMBURG-DRI"],
      "display_width": "detail",
      "hero_priority": -100
    }
  ]
}
```

필수 필드는 `source_id`, `title`, `collected_at`, `source_type`, `language`,
`reliability`, `content_sha256`, `raw_path`다. 게시일을 알 수 없으면
`published_at`을 `null`로 둔다. 수집일을 게시일처럼 쓰지 않는다.

`source_type=academic`은 `academic.kind`가 필요하다. 허용 값은
`journal_article`, `conference_paper`, `conference_presentation`, `preprint`,
`thesis`, `research_report`다. 저자·게재지 또는 프로시딩·DOI·학회명·학회 일자·
장소·동료심사 상태는 확인되는 값만 선택적으로 기록한다. 학회 프로그램의 발표
제목만 확인되고 본문이나 초록을 확인하지 못했다면, 프로그램 자체가 입증하는
발표 사실을 넘어 기술 성능 Claim을 만들지 않는다.

기존 레코드의 학술 메타데이터를 보강할 때는 `set-academic-metadata`를 사용하며,
보관 원문의 `raw_sha256`과 `raw_path`는 유지한다. 게시일 정정은 출판사·DOI·공식
학회 자료에서 날짜를 확인한 경우에만 수행한다.

허용 `source_type`:

- `company_release`
- `company_ir`
- `government`
- `permit`
- `patent`
- `academic`
- `equipment_supplier`
- `specialist_media`
- `general_media`
- `other`

허용 `reliability`:

- `primary`: 회사·정부·특허·논문 등 원자료
- `high`: 독립적이며 근거가 분명한 2차 자료
- `medium`: 전문매체 또는 근거가 일부 확인된 자료
- `low`: 단일 익명 보도, 블로그, 출처 불명 자료

`supporting_sources`에는 재인용 URL과 매체 정보를 넣을 수 있지만 이를 별도
지식으로 계산하지 않는다.

이미지는 Source의 선택 필드인 `images`에 둔다. 허용 `kind`는
`facility_photo`, `process_diagram`, `equipment_drawing`, `patent_figure`,
`academic_figure`, `ai_reconstruction`, `other`다. 허용 `rights_status`는
`permitted`, `link_only`, `ai_generated`다.

- `permitted`: 사용 조건을 확인한 이미지를 `assets/media/`에 보관하고 해시를 기록한다.
- `link_only`: 복제 권리가 불명확해 파일을 내려받지 않고 이미지 URL과 원문만 기록한다.
- `ai_generated`: AI 재구성 파일을 보관하되 `kind`는 반드시 `ai_reconstruction`이다.

모든 이미지에는 `caption`, `alt_text`, `origin_url`, `rights_note`가 필요하다.
이미지는 기술적 사실의 독립 근거가 아니며 연결된 Source와 Claim의 보조 시각 자료다.
`subject_ids`는 해당 이미지가 표시될 수 있는 회사·기술·프로젝트 주체의 명시적
허용 목록이다. 협력·투자·컨소시엄 관계만으로 파트너의 설비 이미지를 회사 페이지에
표시하지 않는다. 특히 회사 페이지는 회사 직접 Source 또는 `subject_ids`에 해당
`COM-` ID가 명시된 이미지로 제한한다.

`display_width`는 선택 필드이며 일반 사진은 `compact`, 세부 판독이 필요한 공정도·
장치도는 `detail`을 사용한다. `hero_priority`도 선택 필드이며 작은 값이 대표 이미지
선정에서 먼저 온다. 동일 기술 페이지의 생성형 공정도를 최상단에 고정할 때는
`-100`처럼 음수 우선순위를 사용하되, 실제 설비·학술 이미지는 본문 갤러리에 함께
남겨 기술 검증 자료로 활용한다.

## 3. 주장

`.system/claims/CLM-*.json`을 기준으로 한다. 한 파일은 한 가지 검증 가능한
명제만 표현한다.

```json
{
  "claim_id": "CLM-6F3E...",
  "subject_id": "PRJ-HAMBURG-DRI",
  "predicate": "target_start_date",
  "value": "2029 이후",
  "status": "active",
  "confidence": "medium",
  "first_seen": "2026-07-25",
  "last_verified": "2026-07-25",
  "source_ids": ["SRC-20260725-A1B2C3D4"],
  "supersedes": ["CLM-OLD..."],
  "coexists_with": [],
  "history": [
    {
      "date": "2026-07-25",
      "action": "created",
      "reason": "신규 회사 발표"
    }
  ]
}
```

허용 상태:

- `active`: 현재 유효
- `superseded`: 더 새로운 정보로 대체
- `disputed`: 출처끼리 충돌
- `cancelled`: 공식 취소
- `stale`: 재검증 기한 경과

허용 신뢰도는 `high`, `medium`, `low`다. 신뢰도는 출처 수만으로 올리지 않는다.
같은 보도자료를 인용한 여러 기사는 독립된 근거가 아니다.

`subject_id` 권장 접두사:

- `COM-`: 기업
- `TEC-`: 기술
- `PRJ-`: 프로젝트
- `FAC-`: 설비
- `POL-`: 정책

`predicate`는 안정적인 영문 snake_case를 사용한다. 예:
`target_start_date`, `capex_eur`, `capacity_tpy`, `trl`, `project_status`,
`technology_route`, `funding_amount`.

## 4. 검토

`.system/reviews/pending/REV-*.json`에는 다음을 보존한다.

- 검토 유형
- 기존 claim 또는 source
- 신규 후보
- 충돌 원인
- 자동 판단을 보류한 이유
- 허용 결정

해결 후 파일을 `.system/reviews/resolved/`로 옮기고 다음을 추가한다.

```json
{
  "resolution": {
    "decided_at": "2026-07-25",
    "decision": "supersede",
    "rationale": "2026-07-21 회사 공식 발표가 기존 목표를 갱신함"
  }
}
```

결정과 근거가 없으면 해결된 것으로 처리하지 않는다.

## 5. 엔터티와 이벤트

기업·기술·프로젝트·기타 subject와 출처 페이지는 JSON에서 자동 생성되는
Markdown 투영본이다. 관련 subject와 source는 Obsidian `[[위키링크]]`로 양방향
연결한다. `<!-- AUTO-GENERATED BY steel-intelligence. DO NOT EDIT. -->`가 있는
페이지, `index.md`, `REVIEW.md`를 직접 수정하지 않는다. 페이지 본문
자체를 상태의 단일 기준으로 사용하지 않는다.

기업 페이지는 사람용 보고서 계층이다. 기술의 의미, 확인된 회사 현황, 출처 문구를
바탕으로 한 단계 판단, 추가 관찰 포인트와 사람이 읽을 수 있는 출처명을 표시한다.
Claim ID, subject ID, predicate와 원자적 레코드는 `.system/`에서 관리하고 기업
페이지 본문에는 표시하지 않는다. 위키링크의 대상 파일명에는 내부 Source ID가
남을 수 있지만 Obsidian 읽기 화면에는 출처명 별칭을 보여준다.

브라우저 사용자는 Material for MkDocs로 제공되는 `index.md`에서 시작한다. 첫
화면은 기술을 행, 기업을 열로 비교하는 매트릭스를 제공하며 각 확인 셀은 같은
Markdown 투영본인 기업별 상세 문서의 해당 기술 절로 연결된다. 생성 Markdown을
직접 편집하지 않고 `sync-obsidian`으로 재생성한다.

이벤트는 `events/YYYY-MM-DD-<slug>.md`로 작성한다. 이벤트 유형은
`announcement`, `pilot`, `investment`, `funding`, `permit`, `partnership`,
`delay`, `suspension`, `cancellation`, `commercial_operation` 중 하나를 우선 사용한다.

## 6. 실행 기록과 보고서

`.system/runs/YYYY-MM-DD-<run-id>.json`에 다음을 기록한다.

- 실행 시작·종료 시각
- 검색 기준일과 겹침 기간
- 기업·기술·국가·출처 범위
- 실제 쿼리
- 확인한 URL
- 접근 실패 URL
- 접근 제한 또는 재시도가 있었던 URL의 `access_attempts`
- 신규·중복·검토 후보 수

`access_attempts`는 접근 방식과 실패 원인을 재현할 수 있을 만큼만 기록한다.
성공한 일반 요청을 모두 기록할 필요는 없지만, 방식 승격·재시도·최종 실패가 발생한
URL은 다음 형태를 권장한다.

```json
{
  "url": "https://example.com/update",
  "attempted_at": "2026-07-25T15:10:00+09:00",
  "method": "browser",
  "outcome": "success",
  "http_status": 200,
  "failure_class": null,
  "retry_count": 1,
  "session_reused": true,
  "final": true,
  "note": "일반 HTTP에서 빈 렌더링 껍데기 확인 후 브라우저로 승격"
}
```

`method`는 `http`, `public_api`, `feed`, `document`, `browser` 중 하나를 우선
사용한다. `failure_class`는 `network`, `rate_limited`, `blocked`,
`javascript_required`, `auth_required`, `content_missing` 중 하나를 사용하고,
성공이면 `null`로 둔다. 민감한 쿠키·토큰·프록시 주소는 run에 저장하지 않는다.
기존 `failed_urls`는 최종 실패 URL의 요약 목록으로 유지한다.

보고서의 Markdown 원본과 HTML 파생본은 `reports/briefs/`에 함께 저장한다. 보고서의
사실 문장에는 source ID를 붙이고, AI의 경쟁적 시사점은 별도 절로 분리한다. HTML은
단일 파일로 생성하며 Markdown에 실제로 등장한 source ID만 출처 절에 포함한다.
