---
title: 철강 신기술 논문·학회 근거 지형 2026
date: 2026-07-26
---

# 철강 신기술 논문·학회 근거 지형 2026

!!! abstract "한눈에 보기"

    현재 Wiki에는 **학술 출처 34건**이 등록되어 있습니다. 유형은 학술지 논문
    21건, 학회 논문 4건, 학회 발표 7건, 연구보고서 2건입니다. 감시 대상
    **11개 기술 모두 학술 출처가 1건 이상 연결**되어 있습니다.

    이 숫자는 문헌의 양을 보여줄 뿐 기술의 성숙도 순위가 아닙니다. 동료심사 논문,
    학회 논문, 개발사 발표, 연구보고서의 검증 수준을 구분해서 읽어야 합니다.

## 근거를 읽는 순서

```mermaid
flowchart LR
  J["학술지 논문<br/>원리·실험·검토"] --> C["학회 논문<br/>최신 방법·확장 검토"]
  C --> P["학회 발표<br/>개발사 로드맵·설계"]
  P --> O["운전·허가·발주 근거<br/>프로젝트 달성 상태"]
  J -. "상용 가동을 직접 증명하지 않음" .-> O
  P -. "발표 수치의 독립 검증 필요" .-> O
```

- **학술지 논문**은 반응 원리, 실험 조건, 물성 및 공정 제약을 확인하는 데
  우선 사용합니다.
- **학회 논문**은 최신 스케일업 방법과 설계 논리를 확인하되, 후속 출판 여부를
  함께 봅니다.
- **학회 발표**는 개발사의 현재 공정 구성과 로드맵을 빠르게 파악하는 자료입니다.
  비동료심사 발표의 목표 용량·일정은 가동 실적과 분리합니다.
- **프로젝트 상태**는 기업 공시, 정부 문서, 허가, 발주·가동 자료로 별도
  교차검증합니다.

## 기술별 커버리지

| 기술 | 연결된 학술 출처 | 포함 유형 | 이번 조사에서 보강한 핵심 |
| --- | ---: | --- | --- |
| [고로 CCUS](../technologies/TEC-blast-furnace-ccus.md) | 2 | 연구보고서, 학회 발표 | 전기화 상부가스 재순환 retrofit 제안과 독립 검증 경계[^bf] |
| [전기용융로](../technologies/TEC-electric-smelting-furnace.md) | 4 | 학술지, 학회 논문·발표 | 저품위 DRI–슬래그 flowsheet와 개념 설계치 경계[^esf] |
| [고급강 EAF·스크랩 불순물 제거](../technologies/TEC-high-grade-eaf-and-scrap-impurity-removal.md) | 6 | 학술지, 학회 발표 | 스크랩 인식·계측·MES 연계 및 제시된 탐지 성능[^scrap] |
| [무펠릿 미분광 수소환원](../technologies/TEC-hydrogen-based-fine-ore-reduction.md) | 2 | 학술지, 학회 발표 | 광종·맥석에 따른 다단 수소환원 거동[^h2ore] |
| [수소 직접환원철](../technologies/TEC-hydrogen-direct-reduced-iron.md) | 3 | 학술지, 학회 발표 | DRI–EAF 통합 설계와 광종별 환원도[^ternium] |
| [수소 플라즈마 용융환원](../technologies/TEC-hydrogen-plasma-smelting-reduction.md) | 5 | 학술지, 학회 논문 | 사전환원·스케일업 시나리오와 공개 실증 공백[^hpsr] |
| [저탄소 제철 종합 경로](../technologies/TEC-low-carbon-ironmaking.md) | 2 | 학술지 | 화학·전기화학 경로 비교와 지역별 제약[^routes] |
| [저온 수계 전해제철](../technologies/TEC-low-temperature-aqueous-iron-electrolysis.md) | 4 | 학술지, 학회 논문·발표 | 실험 조건, 혼합광 적용, SIDERWIN, Volteron 로드맵[^aqueous] |
| [마이크로웨이브·바이오매스 환원제철](../technologies/TEC-microwave-biomass-ironmaking.md) | 1 | 학회 발표 | BioIron 공정 구성과 최초 파일럿 계획[^bioiron] |
| [용융산화물 전기분해](../technologies/TEC-molten-oxide-electrolysis.md) | 4 | 학술지 | 양극·전해질·경제성·광석 환원 실험[^moe] |
| [스마트 제철소](../technologies/TEC-smart-steelworks.md) | 2 | 학회 논문·발표 | human-in-the-loop digital twin과 스크랩 cloud/edge 사례[^smart] |

## 비교해서 봐야 할 쟁점

| 쟁점 | 현재 근거가 말하는 범위 | 추가로 필요한 근거 |
| --- | --- | --- |
| 전기분해 스케일업 | 실험 셀, 혼합광, 개발사 step-up 로드맵 | 장기 연속운전, 전극 수명, 제품 품질, 실제 전력원단위 |
| 수소환원 원료 | sticking, 맥석·광종, 다단 환원 거동 | 산업 유동층·샤프트의 장기 조업 및 광석 포트폴리오 |
| ESF | 저품위 DRI 처리, 슬래그 물성, 개념 flowsheet | 내화물 수명, 열손실, 철수율 및 상업 설비 조업자료 |
| HPSR | 반응 관찰, 사전환원, 시나리오 기반 확장법 | 산업 규모 연속운전·전극/플라즈마 내구성·제품 품질 |
| BioIron | 개발사 학회 발표의 공정·파일럿 계획 | 동료심사 실험, 외부 검증, 연속운전 및 물질수지 |
| 스마트·스크랩 | 디지털트윈 구조와 공급사 탐지 사례 | 다현장 재현성, 데이터셋·오탐 비용, 품질·수율 영향 |

!!! warning "해석 제한"

    학회 발표에서 제시된 용량, 정확도, 일정은 해당 발표의 시험·설계·사업 조건에
    한정됩니다. Wiki는 이를 `conference_presentation`과
    `not_peer_reviewed`로 표시하며, 프로젝트의 실제 가동·상용 단계 Claim으로
    자동 승격하지 않습니다.

## 대표 출처

[^bf]: [SRC-20260726-B392BD57](../sources/SRC-20260726-B392BD57.md), *Profitable Decarbonization of the Blast Furnace Through Electrified Top-Gas Recycling*, Association for Iron & Steel Technology, 2026-03-09, [원문](https://www.aist.org/getmedia/7b039809-54af-40f1-9c74-1a9df73d4c82/Profitable-Decarbonization-of-the-Blast-Furnace-updated.pdf), 보관 원문: `.system/raw/SRC-20260726-B392BD57.md`.
[^esf]: [SRC-20260726-6CC774DD](../sources/SRC-20260726-6CC774DD.md), *Electric Smelting Furnace-Based Flowsheets*, Association for Iron & Steel Technology, 2026-03-09, [원문](https://www.aist.org/getmedia/1f692aad-90e1-4d92-b591-6b97060144cf/Electric-Smelting-Furnace-based-Flowsheets.pdf), 보관 원문: `.system/raw/SRC-20260726-6CC774DD.md`.
[^scrap]: [SRC-20260726-DEF03677](../sources/SRC-20260726-DEF03677.md), *Evolving Scrapyard: Integrating New Solutions for Advanced Scrap Management*, Association for Iron & Steel Technology, 2026-03-09, [원문](https://www.aist.org/getmedia/e771fab2-8303-4f35-b945-bcac8028c804/Evolving-Scrapyard-Intergrating-New-Solutions-Advanced.pdf), 보관 원문: `.system/raw/SRC-20260726-DEF03677.md`.
[^h2ore]: [SRC-20260726-EADB3777](../sources/SRC-20260726-EADB3777.md), *Reduction Behaviour of Iron Ores by H2 at Multi-Stage Reduction*, Association for Iron & Steel Technology, 2026-03-11, [원문](https://www.aist.org/getmedia/36162fc5-d792-4bb2-bcb3-23c66d1e625e/Reduction-Behaviour-of-Iron-Ores-by-H2.pdf), 보관 원문: `.system/raw/SRC-20260726-EADB3777.md`.
[^ternium]: [SRC-20260726-CEDF7736](../sources/SRC-20260726-CEDF7736.md), *Tomorrow’s Steel Mill, Today: Ternium Pesquería Leads Sustainable Innovation*, Association for Iron & Steel Technology, 2026-03-09, [원문](https://www.aist.org/getmedia/e89e02e8-f108-4e65-b52a-939bec855f83/Tomorrows-Steel-Mill-Today-Ternium.pdf), 보관 원문: `.system/raw/SRC-20260726-CEDF7736.md`.
[^hpsr]: [SRC-20260726-443630DE](../sources/SRC-20260726-443630DE.md), *Conceptualizing Hydrogen Plasma Reduction for Industrial-Scale Prereduced Iron Ore Smelting*, Association for Iron & Steel Technology, 2025-05-05, [원문](https://imis.aist.org/AISTPapers/Abstracts_Only_PDF/PR-389-235.pdf), 보관 원문: `.system/raw/SRC-20260726-443630DE.md`.
[^routes]: [SRC-20260726-10602BC9](../sources/SRC-20260726-10602BC9.md), *Chemical and electrochemical pathways to low-carbon iron and steel*, Nature Portfolio, 2024-10-01, [원문](https://www.nature.com/articles/s44296-024-00036-6), 보관 원문: `.system/raw/SRC-20260726-10602BC9.md`.
[^aqueous]: [SRC-20260726-9F56DB69](../sources/SRC-20260726-9F56DB69.md), *Volteron — Scalable Electrochemical Ironmaking for Green Steel Production*, Association for Iron & Steel Technology, 2026-03-09, [원문](https://www.aist.org/getmedia/b2126be4-4ee8-47eb-a536-56cacf43d492/Scalable-Electrochemical-Ironmaking-or-Green-Steel-Production.pdf), 보관 원문: `.system/raw/SRC-20260726-9F56DB69.md`.
[^bioiron]: [SRC-20260726-7A19874F](../sources/SRC-20260726-7A19874F.md), *Rio Tinto Steel Decarbonisation and Biomass Ironmaking*, Association for Iron & Steel Technology, 2023-03-08, [원문](https://www.aist.org/AIST/aist/AIST/Conferences_Exhibitions/Training_Seminars/Scrap%20Files/18-Leigh-and-Buckley.pdf), 보관 원문: `.system/raw/SRC-20260726-7A19874F.md`.
[^moe]: [SRC-20260725-147875E9](../sources/SRC-20260725-147875E9.md), *A new anode material for oxygen evolution in molten oxide electrolysis*, Nature Portfolio, 2013-05-08, [원문](https://doi.org/10.1038/nature12134), 보관 원문: `.system/raw/SRC-20260725-147875E9.md`.
[^smart]: [SRC-20260725-8BA7A1B3](../sources/SRC-20260725-8BA7A1B3.md), *Conceptual Architecture of Digital Twins with Human-in-the-Loop Based Smart Manufacturing*, ASME, 2023-10-29, [원문](https://doi.org/10.1115/IMECE2023-112478), 보관 원문: `.system/raw/SRC-20260725-8BA7A1B3.md`.

