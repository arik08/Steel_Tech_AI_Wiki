# 미래철강 AI 대표 이미지 독립 QC

- 점검일: 2026-07-27
- 점검 범위: 기존 기술 대표 AI 재구성 11장과 신규 ZESTY·HIsarna 2장
- 점검 방식: source-record JSON으로 Source/Media ID와 canonical 경로를 확인한 뒤
  각 PNG를 원본 해상도로 직접 확대 점검했다. 별도 OCR 도구는 사용하지 않았다.
- 판정 기준: 해상도, 공정 topology, 화살표 방향, 텍스트 잘림·오탈자, 라벨 과밀,
  실제 준공도·P&ID 오인 가능성, 기술 간 색·스타일 일관성
- 사용 목적: POSCO홀딩스 미래기술연구원 박사급 독자가 기술 구조와 검증 병목을
  빠르게 파악하는 기술 페이지 상단 대표 이미지

## 판정 정의

| 판정 | 의미 |
|---|---|
| `PASS` | 상단 대표 이미지로 사용 가능 |
| `PASS_WITH_CAPTION` | 그림은 사용 가능하나 바로 아래 AI 재구성·비준공도 캡션이 필수 |
| `REPLACED` | 원본은 비권고이며 아래 교정본으로 대체 |
| `REJECT` | 교정 없이 상단 대표 이미지로 사용하지 않음 |

## 한눈에 보는 최종 판정

| 기술 | Source / 원본 Media | 원본 해상도 | 원본 판정 | 핵심 문제 | 최종 권고 |
|---|---|---:|---|---|---|
| 저탄소 제철 경로 종합 | `SRC-20260725-38165ABC` / `MED-D0FBFEAE165E` | 1672×941 | `REPLACED` | 기존 범례는 blue를 전력으로 정의하면서 일부 주 물질선에도 blue를 사용해 색 의미가 충돌했다. | `MED-A73F859DA386` / `qc-fixed-low-carbon-ironmaking.png` `PASS` |
| 저온 수계 철 전해 | `SRC-20260725-133D1C12` / `MED-7B53D844AF8D` | 1672×941 | `REPLACED` | 하단 recycle 선이 잔사 배출부로 올라가 잔사를 재순환하는 듯 보였다. | `MED-042C9B48BD81` / `qc-fixed-aqueous-electrolysis-v2.png` `PASS` |
| 용융산화물 전해(MOE) | `SRC-20260725-26EA1CBD` / `MED-49390EFFBA04` | 1672×941 | `PASS_WITH_CAPTION` | 전극 극성, O²⁻ 이동, O₂ 발생, 액체철 음극 풀이 일관된다. 작은 글자 잘림이나 명백한 오탈자가 없다. | 원본 유지. `R&D SCHEMATIC`, 실제 Woburn cell 준공도가 아니라는 캡션 유지 |
| 고로 CCUS | `SRC-20260725-2EABD949` / `MED-23BDA82376B5` | 1920×1080 | `REPLACED` | 원본은 라벨 없는 장치·배관이 과밀하고 범례도 기호만 있어 공정 판독이 어렵고 실제 PFD처럼 보였다. | `MED-EFBC900681FA` / `qc-fixed-blast-furnace-ccus-v7.png` `PASS` |
| 고급강용 스크랩·EAF | `SRC-20260725-4366E5B1` / `MED-0899E249E8FA` | 1920×1080 | `REPLACED` | 라벨 없는 선별·대시보드·용해 아이콘이 과밀해 established route와 실험적 탈동 경로가 구분되지 않았다. | `MED-5B57D82A5381` / `qc-fixed-high-grade-scrap-eaf.png` `PASS` |
| 마이크로웨이브 바이오매스 제철 | `SRC-20260725-D965F782` / `MED-1D4B045DD76D` | 1920×1080 | `REPLACED` | 원본은 무라벨 feed silo·배관·계측이 과밀하고 독점 설비 흐름도처럼 보였다. | `MED-7220FCC31DD9` / `qc-fixed-microwave-biomass-ironmaking.png` `PASS` |
| 스마트 제철소 | `SRC-20260725-41586A75` / `MED-52C2D1320144` | 1920×1080 | `REPLACED` | 아이콘·점선이 과밀하고 데이터·승인·안전 override 방향이 읽히지 않았다. | `MED-9A1572EA2DFF` / `qc-fixed-smart-steelworks-v3.png` `PASS_WITH_CAPTION` |
| 수소 샤프트 DRI | `SRC-20260725-75A329BD` / `MED-EC43E3167DA9` | 1672×941 | `REPLACED` | fresh H₂ 보충 유입이 없고 `DRI → HOT DRI → HBI`가 직렬 변환처럼 보였다. | `MED-B7C2DC785571` / `qc-fixed-hydrogen-dri.png` `PASS_WITH_CAPTION` |
| 수소 미분광 유동층 환원 | `SRC-20260725-A23B5A64` / `MED-49CEB753F6E6` | 1672×941 | `REPLACED_AGAIN` | 1차 교정본 `MED-A3F73A83EE4F`도 4개 층을 한 압력용기에 수직 적층하고 단계간 개방 낙하를 그려 공개 HyREX·FINEX 캐스케이드와 압력 경계를 반영하지 못했다. | `SRC-20260725-013F0FA1` / `MED-1DFBEB84CEB5` / `hyrex-fluidized-bed-cascade-ai-reconstruction-2026-07-27.png` `PASS_WITH_CAPTION` |
| 전기용융로(ESF) | `SRC-20260725-6EC0DF4D` / `MED-667CEDEE9C8F` | 1672×941 | `REPLACED` | 노출 free arc가 강조돼 submerged/resistance ESF보다 EAF처럼 보였고, 1차 교정본은 slag와 hot metal을 같은 refining bracket에 묶었다. | `MED-7AC974D2873D` / `qc-fixed-electric-smelting-furnace-v2.png` `PASS` |
| 수소 플라즈마 용융환원(HPSR) | `SRC-20260725-A0AC41D7` / `MED-8C16D5A1B89E` | 1672×941 | `REPLACED` | 원본은 ore가 preheat 측과 hollow cathode 측에 중복 투입되는 것처럼 보였다. | `MED-DE2C759D0EE0` / `qc-fixed-hpsr.png` `PASS_WITH_CAPTION` |
| ZESTY 수소 플래시 환원 | `SRC-20260727-C43117BC` / 연구 원본 | 1536×1024 | `REPLACED` | cyclone 회수 미분을 상부 feed로 확정 재순환하는 화살표가 공개 근거보다 강했다. | `MED-6786347D8BBA` / `qc-fixed-zesty.png` `PASS` |
| HIsarna 사이클론 용융환원 | `SRC-20260727-FD3EBA92` / 연구 원본 | 1536×1024 | `REPLACED` | SRV inlet을 `Coal + O₂`로 묶고 reflux chamber 산소주입·air quench·off-gas cleaning을 생략했다. | `MED-4B9CC0789A73` / `qc-fixed-hisarna.png` `PASS` |

## 파일별 상세 검수

### 1. 저탄소 제철 경로 종합

- 원본은 5개 경로의 topology 자체는 대체로 타당했다.
- 다만 범례에서 blue를 `ELECTRICITY`로 선언하면서 scrap, DRI, iron product 등
  일부 주 물질 흐름도 blue로 그려 색만 보고는 전력과 물질을 구분할 수 없었다.
- 교정본은 정확히 5개 swimlane만 남기고, grey=고체, green=H₂,
  blue=전력 연결, orange=용융금속, purple=CO₂로 제한했다.
- 1차 교정본은 EAF→refining, H₂-DRI EAF→casting, BF→hot metal 세 molten
  stream이 grey여서 조건부 판정했다. 최종본에서 이 세 선을 orange로 교정했다.
- 최종본은 텍스트 잘림·오탈자와 lane 간 선 교차가 없으며, 비준공도 footer가 보인다.

### 2. 저온 수계 철 전해

- 원본의 주 공정 `ore → acid leach → separation → purification → electrowinning`
  자체는 읽히지만 recycle 선이 residue 아래에서 위로 향해 잔사 재순환으로 오인된다.
- 교정본은 residue를 독립 폐기·부산물 stream으로 분리하고, acid/base regeneration을
  leach와 purification으로 되돌렸다.
- v2는 cathode(Fe), inert anode와 극성을 명시하고 O₂는 anode에서 분리했다.
- iron sheet arrow는 cell 출구에서 시작하지만 cathode label이 바로 붙어 있어 의미가
  충분히 해소된다. 실제 plate stripping geometry로 해석하지 않도록 캡션을 유지한다.

### 3. MOE

- `Fe₂O₃ → 2Fe + 3/2 O₂`, inert anode(+), liquid Fe cathode(−), O²⁻ 이동과
  O₂ 발생 방향이 서로 맞는다.
- ore feed, liquid iron tapping, modular scale-up과 병목이 명확하다.
- `~1600°C`는 공정 설명 범위이며 실제 운전 보증값이 아니다.
- 이미지 자체에 `R&D SCHEMATIC`이 있어 오인 위험이 낮지만 source caption의
  `실제 Woburn cell 준공도가 아님` 문구는 유지한다.

### 4. 고로 CCUS

- 원본은 label-less 장치와 다수 색 배관 때문에 박사급 독자가 추론해야 하는 비중이
  지나치게 컸다.
- 여러 교정 iteration에서 rich solvent가 CO₂ compression으로 잘못 연결되거나
  geological storage가 utilization header 아래 놓이는 오류를 발견해 폐기했다.
- 최종 v7은 absorber→regenerator `RICH SOLVENT`, regenerator→absorber
  `LEAN SOLVENT`, regenerator→compression `CONCENTRATED CO₂`를 각각 독립 연결한다.
- compression→transport 뒤 storage/utilization으로 분기하며 green line은 compression에
  닿지 않는다. topology와 화살표 방향 모두 통과다.

### 5. 고급강용 스크랩·EAF

- 교정본은 established route를
  `dismantle/liberate → sensor sorting → grade bins → blend optimization → EAF
  → ladle refining → casting`으로 단순화했다.
- `EXPERIMENTAL Cu REMOVAL`은 purple dashed box로 분리해 상용 표준공정처럼 보이지 않는다.
- Cu/Sn residual은 일반 EAF 용해로 없어지지 않는다는 위험을 별도 orange callout으로 표시했다.
- 하단 bottleneck 문장은 다른 이미지보다 작지만 1672×941 원본 및 detail 폭에서 판독 가능하다.

### 6. 마이크로웨이브 바이오매스 제철

- 교정본은 `ore fines + biomass/binder → mix/briquette → pre-dry →
  microwave reduction → gas/char separation → DRI cooling → smelter`로 읽힌다.
- flame 대신 violet microwave field를 사용해 연소로 오인하지 않는다.
- off-gas recycle/heat recovery는 green conceptual loop이며 성능 수치를 만들지 않았다.
- 주요 scale-up 병목 네 개가 간결하고 비준공도 footer가 있다.

### 7. 스마트 제철소

- 원본은 dashboard·server·경고 아이콘과 점선이 과밀하고 화살표 의미가 불분명했다.
- 최종 v3는 `sensors → historian → physics+ML twin → optimization → operator review
  → interlocks/safety → approved setpoints → actuators → physical process`의 단일 경로를 쓴다.
- manual mode/rollback은 red dashed override로 분리해 무인 자율운전을 암시하지 않는다.
- 하단 `DATA QUALITY → MODEL DRIFT → CHANGE CONTROL → CYBERSECURITY`는 공정 인과가
  아니라 검증 checklist로 읽도록 본문 또는 캡션에서 한 번 더 명시하는 것이 안전하다.

### 8. 수소 샤프트 DRI

- 원본은 ore/shaft/recycle 기본 구조는 좋지만 fresh H₂가 없고 제품이 직렬처럼 보였다.
- 등록 교정본은 `dust removal → H₂O removal → compress/reheat → recycle`과
  `fresh/make-up H₂`를 추가했다.
- 등록본의 하단 `DRI → HDRI/HBI → EAF`는 실제로는 냉간 DRI, hot DRI direct use,
  HBI가 운전·물류 조건에 따라 갈리는 대안이라는 점을 캡션에서 명시해야 한다.
- 별도 후보 `qc-fixed-hydrogen-dri-v2.png`는 세 제품을 병렬로 표현했으나 fresh H₂
  mixing point가 reheat 후단에 있어 최종 등록본으로 권고하지 않았다.

### 9. 수소 미분광 유동층 환원

- 원본은 H₂O 제거가 cyclone보다 앞이고 fines graphic도 pellet처럼 보여 비권고다.
- 1차 등록 v2 역시 네 유동층을 하나의 수직 압력용기 안에 적층하고 고체가 단계 사이를
  개방 낙하하는 것처럼 보여 제외했다. 공개 HyREX·FINEX 설명은 별도 반응기가 계단식
  캐스케이드로 배치되는 구성이다.
- 2차 교정본은 4개 독립 FBR, 고체의 상단→하단 이동, H₂-rich gas의 하단→상단 향류를
  분리했다. 각 단계 cyclone은 배출가스의 비산 미분을 분리해 같은 반응기 하부로
  환류시키고, 정제된 가스만 앞 단계의 분산판 하부로 보낸다.
- 단계간 벌크 고체 이송에는 압력 경계를 유지하는 밀폐 이송 개념을 표시했다. 다만
  공개자료가 밝히지 않은 실제 HyREX seal leg·밸브·압력제어 형상을 확정하지 않도록
  `CONCEPTUAL — NOT AS-BUILT / NOT P&ID`를 이미지와 캡션에 유지한다.
- 고온 DRI는 마지막 FBR에서 별도 밀폐 배출되는 것으로 끝내고, 공개 POSCO 공정도에서
  후단 ESF 연계를 실제 참고 이미지로 함께 보여준다.

### 10. ESF

- 원본의 노출 blue arc는 EAF free arc처럼 보이는 기술 오류다.
- 교정본은 electrodes를 burden/slag 내부로 넣고 `RESISTANCE / SUBMERGED-ARC HEATING`으로
  명시했다.
- 1차 교정본의 slag/hot-metal 공통 refining bracket은 폐기했다.
- 최종 v2는 slag→`SLAG HANDLING`, hot metal→`TO BOF / EAF REFINING`을 독립 배출한다.

### 11. HPSR

- 원본은 preheat side feed와 hollow cathode 내부 feed가 동시에 보여 ore path가 중복됐다.
- 등록 교정본은 단일 side ore feed, H₂/Ar plasma gas, DC electrode(-), vessel/bath(+),
  dust removal, H₂O removal, H₂ recycle와 make-up H₂를 연결했다.
- 다만 해당 기술군에는 hollow electrode를 통한 ore injection 연구도 있으므로 이 그림은
  특정 SuS-F/H2PlasmaRed as-built가 아니라 일반화된 HPSR 개념이라는 캡션이 필수다.
- 이미지 안에는 비준공도 footer가 없고 3D cutaway가 강하므로 source caption을 대표 이미지
  바로 아래에서 숨기지 않아야 한다.

### 12. ZESTY

- 연구 원본은 recovered fines를 상부 ore feed로 자동 복귀시켜 아직 검증이 필요한
  취급 전략을 확정 설계처럼 보이게 했다.
- 교정본은 해당 선을 제거하고 `RECOVERED FINES — HANDLING TO VALIDATE`로 분리했다.
- gas loop는 `WATER REMOVAL → H₂ RECYCLE`만 표현해 미확정 purification/compression을
  만들지 않았다.
- downstream은 `DRI / HBI CONDITIONING + ESF / EAF TRIALS`로 표시해 통합운전 실적과
  제안 시험을 구분했다.

### 13. HIsarna

- 연구 원본은 SRV inlet을 `Coal + O₂`로 묶어 reflux chamber/상부공간 산소주입과
  구분하지 못했다.
- 교정본은 CCF=`FINE ORE + O₂`, SRV=`PULVERIZED COAL`로 분리하고 neck에
  `OXYGEN INJECTION`을 별도 표시했다.
- off-gas는 `AIR QUENCH → OFF-GAS CLEANING → OPTIONAL CCUS` 순서이고 optional CCUS만
  dashed 처리했다.
- slag와 hot metal tap은 독립이며 텍스트 잘림·오탈자가 없다.

## 최종 사용 권고

1. 대표 이미지는 가장 낮은 hero priority의 교정본을 사용한다.
2. 원본 오류 이미지와 실패 iteration은 hero 후보에서 제외하되 연구 이력으로만 보관한다.
3. 모든 AI 이미지 바로 아래에 `AI 재구성`, `실제 준공도/as-built/P&ID 아님`,
   근거 Source ID를 함께 표시한다.
4. MOE·smart steelworks·H₂ DRI·HPSR은 위 표의 캡션 조건을 지킨다.
5. 이미지 내 숫자는 검증된 운전 실적이 아니므로 임의 용량·효율·TRL을 추가하지 않는다.

## 최종 생성·교정 프롬프트 기록

아래는 이 QC에서 최종 채택 또는 비교 후보를 만들 때 사용한 핵심 프롬프트다.
공통 형식은 built-in image generation, scientific-educational 또는 precise-object-edit,
white/cool-gray background, large English labels, POSCO blue 중심, no logo/watermark였다.

### 저탄소 경로 종합

```text
Create one 16:9 comparison infographic with exactly five horizontal swimlanes:
1 SCRAP ROUTE: SCRAP → SENSOR SORTING → EAF → REFINING → CASTING.
2 H₂ SHAFT DRI: PELLETS → SHAFT DRI → EAF → CASTING, with FRESH H₂ and
TOP GAS → H₂O REMOVAL → H₂ RECYCLE.
3 H₂ FINE ORE + ESF: ORE FINES → FLUIDIZED REDUCTION → ESF → BOF → CASTING,
with FRESH H₂ and TOP GAS → DUST + H₂O REMOVAL → H₂ RECYCLE.
4 IRON ELECTROLYSIS: IRON ORE → ELECTROLYSIS → IRON PRODUCT → REFINING → CASTING,
plus O₂ BY-PRODUCT.
5 BF + CCUS: BF → HOT METAL → BOF → CASTING, plus
TOP GAS → CO₂ CAPTURE → CO₂ COMPRESSION → GEOLOGICAL STORAGE.
Grey=solid, green=H₂, blue=electric power only, orange=molten metal,
purple=CO₂. No inter-lane crossing. Footer:
CONCEPTUAL ROUTE COMPARISON — NOT AS-BUILT / NOT P&ID.
```

최종 edit:

```text
Change only three molten-metal arrows to orange:
lane 1 EAF→REFINING, lane 2 EAF→CASTING, lane 5 BF→HOT METAL.
Preserve every other element and color.
```

### 저온 수계 철 전해

```text
Draw ORE → ACID LEACH → SOLID/LIQUID SEPARATION → IRON-ION PURIFICATION
→ ELECTROWINNING → IRON SHEET. Residue exits as WASTE/BY-PRODUCT and never
enters recycle. Electrolyte/water returns to ACID/BASE REGENERATION;
regenerated acid returns to leach. Show inert anode O₂ and bottlenecks
MEMBRANE FOULING, HYDROGEN EVOLUTION, CATHODE STRIPPING.
CONCEPTUAL R&D SCHEMATIC — NOT AS-BUILT / NOT P&ID.
```

최종 edit:

```text
Label left electrode bank CATHODE (Fe), negative; right electrode
ANODE (INERT), positive. Iron sheet originates from the cathode side;
O₂ originates from the inert anode. Preserve residue and recycle topology.
```

### 고로 CCUS

```text
Top row: BF/HOT STOVES → DUST REMOVAL → GAS CONDITIONING → CO₂ ABSORBER
→ TREATED GAS/RECYCLE. Put SOLVENT REGENERATION directly below absorber.
Green RICH SOLVENT arrow points down absorber→regenerator; green LEAN SOLVENT
returns up regenerator→absorber. Purple CONCENTRATED CO₂ leaves regenerator
to CO₂ COMPRESSION → TRANSPORT, then splits to GEOLOGICAL STORAGE and
CO₂ UTILIZATION. No green line touches compression.
CONCEPTUAL R&D SCHEMATIC — NOT AS-BUILT / NOT P&ID.
```

최종 edit:

```text
Connect the purple CONCENTRATED CO₂ arrow continuously from the right/bottom
edge of SOLVENT REGENERATION into CO₂ COMPRESSION. Preserve the correct
rich/lean solvent arrows and every other element.
```

### 고급강용 스크랩·EAF

```text
END-OF-LIFE SCRAP → DISMANTLE/LIBERATE → SENSOR SORTING
(MAGNETIC + VISION + XRF/LIBS) → GRADE BINS → BLEND OPTIMIZATION
→ EAF → LADLE REFINING → CAST STEEL.
Put EXPERIMENTAL Cu REMOVAL in a dashed purple side branch returning cleaned
scrap to grade bins; keep Cu-rich reject separate. Show Cu/Sn residual risk
and bottlenecks COATINGS + MIXED MATERIALS, YIELD/DUST, Cu/Sn TRAMP.
NOT AS-BUILT / NOT P&ID.
```
### 마이크로웨이브 바이오매스 제철

```text
ORE FINES + BIOMASS/BINDER → MIX + BRIQUETTE → PRE-DRY
→ MICROWAVE REDUCTION → GAS/CHAR SEPARATION → DRI COOLING → TO SMELTER.
Use violet microwave field without combustion flame. Add conceptual
OFF-GAS RECYCLE/HEAT RECOVERY and bottlenecks MICROWAVE PENETRATION,
BRIQUETTE STRENGTH, GAS RECYCLE, SCALE-UP.
NOT AS-BUILT / NOT P&ID.
```

### 스마트 제철소

```text
Draw exactly one blue path:
SENSORS + EDGE → HISTORIAN/DATA PLATFORM → PHYSICS + ML DIGITAL TWIN
→ OPTIMIZATION → OPERATOR REVIEW → INTERLOCKS + SAFETY.
Then one green path:
INTERLOCKS + SAFETY → APPROVED SETPOINTS → ACTUATORS/FINAL ELEMENTS
→ PHYSICAL PROCESS.
Manual mode/rollback is a separate red dashed override to actuators.
No direct twin/optimization bypass to setpoints or actuators.
CONCEPTUAL ARCHITECTURE — NOT AS-BUILT / NOT P&ID.
```

### ESF

```text
DRI + FLUX + CARBON enter a SEALED ESF. Show three SUBMERGED ELECTRODES
inside burden/slag with RESISTANCE / SUBMERGED-ARC HEATING and no exposed
free-burning arc. Separate SLAG and HOT METAL layers and tap holes.
Off-gas goes to cleaning. Show FeO IN SLAG, REFRACTORY WEAR,
ELECTRODE CONTROL. NOT AS-BUILT / NOT P&ID.
```

최종 edit:

```text
Remove the common product bracket. Route SLAG only to SLAG HANDLING.
Route HOT METAL only to TO BOF / EAF REFINING. Never merge the two arrows.
```

### ZESTY

```text
Preserve the vertical electrically heated reduction cutaway and
Fe₂O₃→Fe₃O₄→FeO→Fe sequence. Remove every recovered-fines return to the
top feed. Route cyclone solids to RECOVERED FINES — HANDLING TO VALIDATE.
Keep only WATER REMOVAL → H₂ RECYCLE in the gas loop. Label downstream
DRI / HBI CONDITIONING + ESF / EAF TRIALS.
CONCEPTUAL R&D SCHEMATIC — NOT AS-BUILT / NOT P&ID.
```

### HIsarna

```text
Keep upper CCF inlet FINE ORE + O₂. Change lower SRV inlet to
PULVERIZED COAL only. Add separate OXYGEN INJECTION into the reflux chamber.
Top gas route: AIR QUENCH → OFF-GAS CLEANING → OPTIONAL CCUS, with only
optional CCUS dashed. Keep separate SLAG and HOT METAL taps.
CONCEPTUAL R&D SCHEMATIC — NOT AS-BUILT / NOT P&ID.
```

### 추가 비교 후보: H₂ DRI

```text
Pellets descend and H₂-rich gas rises in a shaft. Top gas goes through
DUST REMOVAL → WATER REMOVAL → COMPRESSOR → HEATER → H₂ RECYCLE;
add FRESH H₂ MAKE-UP. Show COLD DRI, HOT DRI TO EAF, HBI as parallel
alternatives, not serial conversion. Mark METALLIZATION,
STICKING/CLUSTERING, GAS DISTRIBUTION.
NOT AS-BUILT / NOT P&ID.
```

### 추가 비교 후보: 미분광 유동층

```text
ORE FINES → PREHEAT → FBR-1 → FBR-2 → FBR-3 with solids flow and
countercurrent H₂ upflow. Top gas must go first to CYCLONE/DUST RECOVERY,
then WATER REMOVAL → COMPRESSOR → HEATER → H₂ RECYCLE; add FRESH H₂.
Cyclone solids go to dust/recovery handling, not automatic feed return.
Fine DRI branches to HBI conditioning or ESF/smelter.
NOT AS-BUILT / NOT P&ID.
```

### 추가 비교 후보: HPSR

```text
Use one ore route only: ORE FINES → PREHEAT → PREHEATED ORE TO HOLLOW CATHODE,
joining H₂ + Ar. Hollow cathode is negative, conductive bath positive.
Show DC plasma arc, separate slag and crude iron/steel taps, and
OFF-GAS → CYCLONE/DUST RECOVERY → WATER REMOVAL → H₂ RECYCLE.
Make BATCH / NO CONTINUOUS TAP PROOF visible.
NOT AS-BUILT / NOT P&ID.
```
