# Market Sensing Wiki Design

## Register

product

## Reading Scene

포스코그룹 임직원이 주간 회의 전 밝은 사무실 모니터에서 5~10분 동안 외부 변화,
사업 영향, 판단 근거와 원문을 순서대로 읽는 화면입니다.

## Editorial Direction

- 산업 주간지의 기사 리듬 70%, 리서치 레포트의 표·근거·출처 30%
- 제목, 두 문장 리드, 결론형 소제목, 본문, 근거 노트의 5단 정보 위계
- 저장 스키마의 필드명과 자동 번호를 사람용 목차로 노출하지 않음
- 3~5개의 소제목, 2~4문장의 짧은 문단, 판단을 줄이는 필요한 시각화를 기본 호흡으로 삼음
- 본문 폭 65~72ch, 본문 1rem 이상, 보조 텍스트 0.875rem 이상

## Typography

- 본문: 시스템 한국어 sans-serif, 1rem, line-height 1.7
- 기사 제목·핵심 판단: POSCO Blue, 700
- 결론형 소제목: 짙은 잉크 중립색, 650
- 검증용 kicker·메타데이터: 차분한 회색, 0.875rem, 600
- 숫자 표·점수: tabular numerals

## Visualization

- 시점 변화: timeline
- 3개 이상 비교·시나리오: Markdown table
- 3개 이상 인과 단계·분기: Mermaid
- 검증된 시계열·구성효과·민감도: quantitative chart
- 모든 시각화에 단위, 기준일, Source, 가정과 회사 실제값 아님을 인접 표시
- 문장보다 이해를 개선하지 못하거나 근거가 부족한 장식용 시각화 금지

## Color and Surfaces

- POSCO Blue `#05507D`: 기사 제목, 핵심 탐색, 선택 상태
- Ink `#20242C`: 본문·소제목
- Cool neutral `#F4F6F8`: 페이지 밖·보조 영역
- Green·amber·red: 기회·주의·위험의 실제 의미에만 사용
- 지나친 카드, 그라디언트, 글로우, 글래스모피즘 금지

## Responsive Rules

- 모바일에서 기회·위험 비교와 표는 한 열 또는 수평 스크롤로 안전하게 전환
- Signal 본문의 우측 목차는 최상위 절만 노출
- 시각화는 본문 폭을 넘지 않고, Mermaid 확대 보기와 출처 탐색을 유지
