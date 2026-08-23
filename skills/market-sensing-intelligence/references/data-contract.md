# 데이터 계약

## Signal과 Insight

`.system/signals/SIG-*.json` schema v3는 변화 유형, 사업 시사점, 점수·평가시점과 양면 판단을,
`.system/insights/INS-*.json` schema v1은 관측 변화 제목, 문단 해석과 문서급 분석을 보존한다.
`insight_id`로 연결하며 Insight는 다시 `claim_ids`, `source_ids`, `document_path`를 통해
Claim·Source·Archive로 이어진다.

Signal의 `signal_type`은 다음 8개 값 중 정확히 하나다.

신규 발행 Signal은 `atomic_scope` schema v1을 필수로 가진다. `event_key`는 같은 사건의
후속 확인을 묶는 안정 키이며, `change_unit`, `observation`, `market_boundary`,
`time_boundary`, `excluded_context`, `single_event_rationale`를 함께 저장한다. 이 경계는
Claim의 원자성과 별개다. 여러 원자 Claim이 한 정책 조치 하나를 설명할 수는 있지만,
효력 주체·시장·시점·변화 변수가 다른 정책과 시장사건을 한 Signal로 합칠 수는 없다.
`add-signal --atomic-scope-file`과 run의 `atomic_signal_contract`가 신규 발행분에 이를
강제한다.

- `정책·규제`
- `수급·가격`
- `경쟁사`
- `투자·프로젝트`
- `공급망·물류`
- `고객·계약`
- `기술·운영`
- `재무·실적`

신규 발행 Signal은 `signal_role`과 `signal_origin`도 반드시 가진다.

- `signal_role`: `core_market_signal` 또는 `execution_context`
- `signal_origin`: `external_market`, `policy_regulator`,
  `competitor_counterparty`, `company_execution`
- `core_market_signal`에는 앞의 외부 발생원 세 개만 허용한다.
- `execution_context`에는 `company_execution`만 허용한다.
- 대상 회사·자회사의 `company_release`·`company_ir`만 연결된 실행 사실은
  `core_market_signal`로 저장하지 않는다.

신규 `core_market_signal`은 `assumption_challenge` schema v1도 필수다.

- `baseline_assumption`: 현재 계획이 암묵적으로 전제하는 수요·원료·접근·원가 조건
- `observed_break`: 그 전제를 약화시키는 검증된 외부 행동 또는 규칙
- `decision_change`: 관측이 지속될 때 실제로 바꿀 제품·계약·투자·운영 판단
- `pattern`: 허용된 8개 전제변경 패턴 중 하나
- `surprise_score`: 기존 정보와 결정의 거리를 나타내는 1~5점. 흥미 점수가 아님
- `falsification_check`: 이 해석을 약화시키거나 폐기할 구체적 확인 한 가지

`add-signal`이 외부 핵심 시그널을 발행하면 run의 `discovery_contract.version=1`과
적용 Signal ID를 기록한다. `audit`은 계약 대상 Signal에서 이 구조의 누락을 오류로 본다.

모든 active Signal의 `decision_lens`는 schema v1이며 다음 필드를 모두 가진다.

- `primary_direction`: 대표 방향인 `opportunity`, `risk`, `mixed` 중 하나
- `opportunity`: 기회가 열리는 `condition`, 사업 `business_effect`, 지금 할 `action`
- `risk`: 위험이 커지는 `condition`, 사업 `business_effect`, 방어 `action`
- `opportunity_cost`: 행동을 늦출 때 놓치는 고객·물량·가격 가산분·원가우위·선택권·시간
- `decision_trigger`: 기회 대응과 방어 대응 사이에서 결정을 바꿀 관찰 조건

대표 방향은 반대편 분석을 생략하는 허가가 아니다. 기회비용은 근거 없는 확정 손실액으로
만들지 않고 조건부 사업 효과로 쓰며, 정량 영향이 있으면 같은 Signal의 검증된
`impact_estimate` 범위와 해석을 일치시킨다. API와 LLM은
`decision-lens.schema.json`을 structured output 계약으로 사용한다.

```json
{
  "schema_version": 3,
  "signal_type": "정책·규제",
  "signal_role": "core_market_signal",
  "signal_origin": "policy_regulator",
  "sentence": "EU 조치로 고객별 계약 갱신일과 가격 전가 범위를 다시 확인해야 합니다.",
  "business_axis": "철강",
  "insight_id": "INS-..."
}
```

사람 화면에서는 `business_axis`와 `signal_type`을 각각 하나의 pill로 표시한다. 회사명,
점수, 평가일은 pill 분류에 섞지 않는다. 이전 schema Signal은 기회·위험·미실행 기회비용을
사람이 검토한 뒤 전체 마이그레이션으로 v3로 전환하며, 필드를 추정해 조용히 통과시키지
않는다. `add-signal`은 분류와 양면 판단이 모두 없으면 신규 발행을 차단한다.

`Signal.urgency.response_deadline`은 선택 필드다. 법정 발효일·공모 마감·계약 종료·공식
의사결정일처럼 실제 날짜와 그 근거가 확인된 경우에만 ISO 날짜로 저장한다. 분석 편의를
위한 임의의 월말·분기말이나 근거 없는 내부 목표일은 저장하지 않는다. 날짜가 애매하면
필드를 생략하고, 긴급성의 이유와 재판단 조건만 기록한다. 사람 화면도 값이 있을 때만
`대응 시한`을 표시한다.

사람용 필드는 다음 편집 계약을 함께 만족해야 한다.

- `Insight.title`: 8~45자, 관측된 변화 중심의 짧고 평이한 사실형 제목, 서술형 존댓말
  종결과 헤드라인식 말줄임표 금지
- `Signal.sentence`: 20~180자, 제목과 분리해 회사의 사업영향과 달라지는 판단을 설명하는
  완전문장형 `사업 시사점`
- `Insight.summary`: 70~500자, 마침표로 구분된 2~4문장으로 무슨 일·회사 영향·지금
  판단을 평이한 한국어로 설명
- 제목에는 설명 없는 램프업·게이트·트리거·자본규율·공급곡선 같은 번역투나 내부
  메모 용어를 쓰지 않는다. 회사명·사업축·변화 유형·사업영향을 제목 하나에 반복해
  넣지 않는다. 구체 기준은 `editorial-style.md`를 따른다.

Insight의 `analysis_markdown`은 MkDocs Signal 상세 페이지에 인라인 투영되는 3단계
본문이다. 첫 도입 문단은 결론과 뜻을 평이한 한국어로 설명하고, 다음 의미 단위와
근거·수치·시나리오의 깊이는 그대로 유지해야 한다.
아래 항목은 **의미 커버리지 계약**이며 필드명·표시 순서·고정 소제목 계약이 아니다.
저장된 의미를 누락하지 않는 범위에서 3~5개의 결론형 소제목으로 통합하고, 사람
화면에는 자동 번호를 표시하지 않는다.

- 확인된 변화와 시점
- 회사에 전달되는 사업 영향 경로
- 조건부 사업 시나리오
- 지금 확인할 지표
- 의사결정에 필요한 다음 산출물
- 판단의 한계

`analysis_markdown`은 수치·시점·비교·인과 데이터가 충분할 때 판단을 실질적으로 줄이는
시각화를 포함한다. 시간 변화는 타임라인, 3개 이상 비교·시나리오는 표,
3개 이상 인과 단계·분기는 Mermaid, 검증된 시계열·구성효과·민감도는 차트를
우선한다. 모든 시각화는 단위, 기준일, Source, 확인값·역산·가정 구분을 보존한다.
사실 근거가 부족하거나 시각화가 짧은 문장보다 이해를 개선하지 못하면 생략한다.

Signal 페이지는 다른 보고서 링크를 상세 분석의 대체물로 사용하지 않는다. 내부 JSON의
Signal·Insight·Claim ID, 해시, raw 경로는 MkDocs 본문에 노출하지 않는다. Source 원문
링크와 보관 원문은 마지막 단계에서 사람이 읽을 수 있는 명칭으로 표시한다.
본문을 `공개 근거 확인`에서 다시 복제하지 않고, 핵심 사실은 각주, 추적용 수치·Claim은
접힌 근거 노트, 원문은 말미 출처 링크로 제공한다.

Insight의 선택 필드 `impact_estimate`는 MkDocs와 향후 웹 프로그램이 함께 사용하는
정량 영향 What-if 모델이다. `title`, `description`, `as_of`, `confidence`, `notice`,
`formula_display`, `variables`, `outputs`, `presets`를 가진다.

Insight의 `quantification`은 모든 active Signal에 필수인 schema v1 판정이다. API와 LLM은
`quantification-packet.schema.json`을 structured output 계약으로 사용한다. `decision`은
`modeled` 또는 `omitted`이며, `modeled`이면 같은 packet의 `impact_estimate`를 Insight의
`impact_estimate`에도 동일하게 저장한다. `omitted`이면 `reason_code`, 40자 이상의
`rationale`, `required_inputs`, `reconsider_when`을 저장하고 `impact_estimate`는 null이다.
비공개 입력은 omission의 충분조건이 아니며 assumption·넓은 범위·낮은 신뢰도를 먼저 쓴다.

- `variables`는 3~8개 지배변수만 두고 `id`, `label`, `unit`, `min`, `max`, `step`,
  `default`, `kind`, `basis`, `source_ids`를 보존한다.
- `kind`는 `verified`, `derived`, `assumption` 중 하나다. `verified`는 Source가 필수이며
  공개되지 않은 회사값은 사실처럼 만들지 않고 `assumption`으로 둔다.
- `outputs`는 매출·EBITDA·현금흐름·NPV와 가격·물량·원가·대응비용 구성효과를 정의한다.
  정확히 하나의 `primary=true` 결과가 있어야 한다.
- `expression`은 숫자, `{ "var": "variable_id" }`, 또는 `add`, `subtract`, `multiply`,
  `divide`, `negate`의 중첩 구조로 저장한다. 이는 임의 실행 코드를 막으면서 복합 회계·경제
  산식을 그대로 표현하기 위한 계약이다.
- `presets`는 최소 방어·기준·압박 3개이며 모든 변수값을 명시한다.
- 결과는 회사 실제 전망이 아니라 공개정보 기반 예비 추정임을 `notice`에 밝힌다.
- 동일한 시장가격·물량 충격을 공유하는 Signal은 독립 금액처럼 합산하지 않는다.

## 구조적 추세·전략가정·핵심 전략 이슈

반복되는 외부 Signal이 동일한 전략가정을 흔들 때 다음 세 레코드를 분리 저장한다.

- `.system/trends/TRD-*.json`: 사업축, 방향, 최초·최근 관찰일, Signal, 지지·반대 Source,
  수치 indicator
- `.system/theses/THS-*.json`: 위협받는 전략가정, 사업 영향 경로, 판단 기간, 반대 근거,
  반증 조건
- `.system/warnings/WRN-*.json`: 내부 호환 ID, 단계·상태·기회/위험 방향, 문서 제목과
  `issue_category`, 요약, 사건·시행·사업 판단 시간축, 자연어 보고서 절, LLM이 설계한 `causal_map`,
  판단 질문·조치·변경 이력

세 레코드는 schema version 7이며 `upsert-strategic-watch`로 함께 검증·저장한다. 활성
레코드는 명시적 review 없이 삭제하거나 종료하지 않으며 변경은 history에 append한다.
보고서 절은 `market_change`, `assumption_shift`, `business_impact`, `recommendation`,
`evidence`, `monitoring`, `limitations` 역할을 각각 한 번 갖는다. 화면 소제목은 역할명을
복사하지 않고 이슈에 맞는 명사구로 쓰며 본문 합계는 2,200자 이상이다. `timeline`은
최소 3개이고 사실 시점에는 Source ID를 연결한다.
Warning은 Signal과 같은 schema v1 `decision_lens`를 필수로 가지며, `issue_direction`은
대표 방향으로만 사용한다. 보고서 상단에는 포착할 기회, 방어할 위험, 미실행 기회비용,
결정 전환 조건을 함께 투영한다.
`issue_category`는 Signal의 8개 변화 유형 또는 `복합 이슈` 중 하나다. 사람 화면은
Thesis의 `company_ids`, Warning의 `business_axis`, `issue_category`를 제목보다 먼저
보여준다. 카테고리는 추론값으로 남기지 않고 모든 활성 Warning에 명시한다.

Warning의 `title`은 18~72자이며 그 제목만 읽어도 관측된 변화와 바뀌는 판단을 이해할 수
있어야 한다. 설명 없는 영문 대문자 약어, 법령 코드, 업계 은어를 제목에 둘 수 없으며
필요한 공식 명칭과 약어는 `executive_summary` 첫 사용에서 쉬운 한국어 뒤에 설명한다.
`upsert-strategic-watch`와 `audit`은 이 규칙을 위반한 활성 이슈를 차단한다.
활성 Warning 전체에서는 `~볼 때·~할 때·~나눌 때`를 하나의 `~할 때` 종결틀로 보고,
`~먼저다`, `~수 없다`와 함께 같은 틀이 2건을 넘으면 `strategic_watch` 감사 오류로
처리한다. 개별 제목의 유효성만으로 목록 문체의 다양성이 확보됐다고 보지 않는다.

모든 Warning은 다음 두 구조를 필수로 저장한다.

- `structured_context`: `company_id`, `business_axis`, 실제 전달 경로가 있는
  `management_functions`, `change_category`, `regions`, `time_horizon`
- `company_lens`: `interest_level(core|conditional)`, 회사 공식 자료로 확인한
  `official_basis`, 직접 노출 `exposure`, 외부 변화의 `impact_path`, 바꿀 결정
  `decision_use`, 회사 IR·공식 발표의 `evidence_source_ids`

사람 화면은 제목을 읽기 전에 구조 지도를 보여주고, 바로 다음에 `왜 우리 회사
이슈인가`를 공식 사업 근거·직접 노출·전달 경로·바꿀 결정 순서로 설명한다. 전략광물처럼
신규 진입 후보는 기존 사업으로 확정하지 않고 `conditional`로 판정한다. 이 두 구조가
없거나 회사 공식 근거가 일반 시장자료뿐이면 발행과 audit을 통과하지 못한다.

신규·개편 핵심 전략 이슈는 `warning.synthesis_contract` schema v1을 가진다.
`decision_key`, `synthesis_statement`, Trend·Thesis와 동일한 `supporting_signal_ids`,
Signal별 `relationship`과 `contribution`을 저장한다. 연결 대상은 최소 2개의 활성
`core_market_signal`이며 각 Signal의 `atomic_scope.event_key`가 달라야 한다. 허용 관계는
`reinforces`, `limits`, `contradicts`, `contextualizes`다. 광역 결론은 이 계약과 이슈
보고서에만 두고 개별 Signal 본문에 역으로 복제하지 않는다.

### 독자용 편집 계획

신규 핵심 전략 이슈와 문서급 Signal을 발행하는 run은 근거 데이터와 별도로
`editorial_plans`를 기록한다. 이 계약은 분석자 근거철을 사람 화면에 그대로 노출하지
않고, 다른 세션·LLM도 같은 편집 판단을 이어받게 하기 위한 것이다.

각 편집 계획은 최소 다음 필드를 가진다.

- `target_id`: 대상 Signal 또는 Warning ID
- `reader_question`: 독자가 글을 읽고 답해야 할 판단 질문 1개
- `one_sentence_thesis`: 현재 근거의 한 문장 결론과 적용 조건
- `key_numbers`: 최대 3개의 값·단위·기준일·Source ID·역할
- `consensus_gap`: 익숙한 시장 해석과 확인된 사실 사이의 간극
- `decision_change`: 회사가 바꿀 결정 하나
- `next_catalyst`: 결론을 갱신할 공식 사건 또는 관찰값
- `visual_candidates`: 최소 3개의 질문·유형·필요 데이터·Source ID·채택 상태·기각 이유
- `first_viewport_check`: 변화·숫자·결정·촉매의 첫 화면 노출 여부
- `meta_moved_to_appendix`: 출처 수·근거 역할·검증 문구 등 본문에서 내린 항목
- `execution_sequence`: 세 단계 이상일 때 산출물·완료 기준·다음 결정·담당을 가진 실행 순서
- `monitoring_dashboard`: 세 개 이상 관찰값일 때 지표·판단 의미·전환 신호·담당을 가진 비교 구조

`key_numbers`는 출처로 확인된 값, 공개자료 역산, AI 가정을 구분한다. 시각화 후보는
`adopted`, `rejected_insufficient_data`, `rejected_redundant`, `deferred` 중 하나로
판정하고, 기각·보류 시 이유와 필요한 입력을 남긴다. 핵심 전략 이슈는 근거가 허용하면
서로 다른 질문에 답하는 `adopted` 시각화가 2개 이상이어야 한다. 이 수를 맞추기 위해
장식용 차트나 근거 없는 지도를 만들지 않는다.

Warning의 `editorial_plan.quantification`은 다음 계약을 따른다.

```json
{
  "status": "modeled",
  "decision_metric": "결정을 바꾸는 가격·물량·비율·영향액"
}
```

`modeled`는 `visuals`에 `type=quantitative_table|quantitative_chart`, `status=adopted`를
최소 1개 요구한다. `quantitative_table`은 `table_kind(scenario|comparison|trend)`,
3~5개 columns, 2~8개 rows, `unit`, `as_of`, `takeaway`, `method_note`,
`data_kind(verified|derived|scenario)`, Source ID를 저장한다. 2~3개 시점·비교값과
방어·기준·압박 민감도는 이 형식을 기본으로 한다.

`quantitative_chart`는 `chart_kind(line|bar)`와 같은 메타데이터를 저장하되 선 차트는
series별 4개 이상 동일 시계열, 막대 차트는 series별 5개 이상 동일 비교항목을 요구한다.
최대·최소값이 20배 이상 차이 나는 선형 막대그래프는 만들지 않는다. 같은 series의
point는 같은 정의·단위를 사용하고, 시장 확인값과 회사 민감도는 같은 series에 섞지
않는다. 차트 계열색은 POSCO Blue `#05507D` 기반 청색 팔레트를 기본으로 하며 의미 없는
녹색을 사용하지 않는다. `omitted`는 `reason`, `attempted_data_paths`, `required_inputs`,
`recheck_trigger`를 모두 요구하고 정량 전시를 채택하지 않는다.

`causal_map`은 원문 Mermaid가 아니라 LLM이 분석 후 선택한 구조 데이터다. `title`,
`direction`, `design_rationale`, 3~9개의 의미형 노드와 2~12개의 연결을 저장한다. 노드는
변화·동인·전제·조건·기회·위험·영향·판단·행동·트리거 중 실제 인과에 필요한 것만
선택한다. 모든 이슈를 같은 4단계로 맞추지 않으며, 분기가 판단을 바꾸면 조건 노드와
두 경로를 명시한다. `LR`은 넓은 화면에서 시간·인과가 이어질 때, `TB`는 병렬 분기가
겹쳐 좌우 흐름보다 읽기 어려울 때만 선택하고 그 이유를 `design_rationale`에 적는다.

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
└── market-sensing-wiki/
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
    │   ├── raw/             # 일반 운영 중 불변인 원문(명시 승인된 전체 초기화 제외)
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
`market_sensing.py` 명령을 실행하면 Markdown 변경사항을 JSON에 자동 반영한다. 즉시
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
연결한다. `<!-- AUTO-GENERATED BY market-sensing-intelligence. DO NOT EDIT. -->`가 있는
페이지, `index.md`, `REVIEW.md`를 직접 수정하지 않는다. 페이지 본문
자체를 상태의 단일 기준으로 사용하지 않는다.

기업 페이지는 사람용 보고서 계층이다. 기술의 의미, 확인된 회사 현황, 출처 문구를
바탕으로 한 단계 판단, 추가 관찰 포인트와 사람이 읽을 수 있는 출처명을 표시한다.
Claim ID, subject ID, predicate와 원자적 레코드는 `.system/`에서 관리하고 기업
페이지 본문에는 표시하지 않는다. 위키링크의 대상 파일명에는 내부 Source ID가
남을 수 있지만 Obsidian 읽기 화면에는 출처명 별칭을 보여준다.

브라우저 사용자는 Material for MkDocs로 제공되는 `index.md`에서 시작한다. 첫 화면은
사업영향도·긴급도 순 Signal과 철강·리튬·전략광물·에너지 사업축을 보여주며 각 Signal은 같은 페이지 안에서
Insight·문서급 분석·원문으로 이어진다. 회사·정책·프로젝트 문서는 근거 탐색용 보조
투영본이다. 생성 Markdown을 직접 편집하지 않고 `sync-obsidian`으로 재생성한다.

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
- 신규 Claim 수, 발행한 Signal 수와 Signal ID 목록
- 신규 발행 run의 `signal_contract`: 계약 버전, 이 계약이 적용되는 `signal_ids`, 사업축별
  외부 핵심 시그널 최소 비율 0.7, 단일 프로젝트·설비 편중 기준 0.5, 편중 검사를
  시작하는 Signal 수 3
- 최근 3년 또는 전사 범위 발굴 run의 `candidate_funnel`: 발견 후보, 중복 통합 사건,
  심층 검증 후보, 승격 이슈의 전체·사업축별 건수와 표준화된 탈락 사유
- 승격한 핵심 전략 이슈별 `evidence_packets`: 원문 Source ID, 독립 채널, 근거 역할,
  반증 Source, 빠진 역할, 예외 사유, 평가 신뢰도

`results.new_claims`가 1 이상인 저장 작업은 `results.new_signals`와 `signal_ids`를 함께
기록한다. 읽기 전용 조사나 사용자가 발행을 금지한 작업이 아니라면 Claim을 만들고
Signal이 0건인 run은 미완료로 감사된다.

`signal_contract.version=1`인 run은 사업축별 active Signal 가운데
`core_market_signal`이 70% 이상이어야 한다. Signal이 3건 이상이면 Claim의 `PRJ-`와
`FAC-` subject를 기준으로 한 프로젝트·설비가 과반을 차지하는지도 감사한다. 이 편중
검사는 일반 시장·정책 subject를 억지로 자산으로 취급하지 않는다.

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
