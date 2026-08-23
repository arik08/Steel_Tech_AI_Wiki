"""Rewrite every active strategic issue around decision-grade quantitative exhibits."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = (
    PROJECT_ROOT
    / "skills"
    / "market-sensing-intelligence"
    / "scripts"
    / "market_sensing.py"
)
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("market_sensing", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load {MODULE_PATH}")
market_sensing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(market_sensing)


REWRITE: dict[str, dict[str, Any]] = {
    "WRN-AU-GAS-RESERVATION-WINTER": {
        "title": "호주 가스는 연간 남아도 겨울에는 부족하다, 판매계획을 계절별로 나눌 때",
        "lead": "호주 동부 가스시장은 2026년 4분기에 13페타줄(PJ)이 남을 것으로 예상되지만, 2027년 2·3분기에는 다시 부족할 수 있습니다. 평균 수급만 보면 가격 하방이지만 겨울과 호주 남부 인도 물량을 따로 보면 희소성이 남습니다. 현지 가스 자회사 세넥스(Senex)의 2027년 판매계획은 연간 물량보다 분기·인도지점·저장권별 순마진으로 다시 짜는 편이 타당합니다.",
        "conclusion": "내수공급 의무의 평균가격 하방과 겨울 남부 부족의 계절 프리미엄을 분리해 판매배분을 결정해야 합니다.",
        "market_note": "핵심은 연간 잉여와 겨울 부족이 동시에 성립한다는 점입니다. ACCC가 제시한 2026년 4분기 잉여 13PJ는 연평균 가격을 누를 수 있지만, 2027년 2·3분기 부족 위험은 저장·운송·남부 인도권의 가격을 따로 만듭니다.",
        "model_signal": "SIG-87E7FDAE469F",
        "driver_ids": ["sales_pj", "price_delta"],
        "chart_title": "계절 수급이 Senex 지분 상각 전 영업이익을 얼마나 흔드는가",
        "chart_takeaway": "공개 수급 전망과 넓은 가정으로 계산한 범위이며, 연간 잉여만으로 겨울 선택권의 가치를 0으로 둘 수 없습니다.",
    },
    "WRN-ENERGY-EU-METHANE-COMPLIANCE": {
        "title": "유럽은 2027년부터 수입 가스의 메탄 검증을 요구한다, 가격만으로 계약할 수 없다",
        "lead": "2027년 1월부터 새 계약과 갱신계약으로 유럽에 액화천연가스(LNG)를 팔려면 생산지의 메탄 측정·보고·검증 자료가 필요합니다. 2028년 강도 보고, 2030년 상한 적용까지 규제가 단계적으로 강화되므로 한 번의 인증으로 끝나지 않습니다. 포스코인터내셔널은 계약별 데이터권과 제3자 검증비용을 목적지 자유 조항과 같은 수준으로 가격에 반영해야 합니다.",
        "conclusion": "계약 갱신 전에 생산지별 메탄 자료와 감사권을 확보하지 못하면 유럽 판매선택권의 가치가 먼저 줄어듭니다.",
        "market_note": "규제는 2027년 MRV 동등성, 2028년 메탄 강도 보고, 2030년 강도 상한의 세 단계로 올라갑니다. 첫 기준까지 남은 시간이 짧다는 사실보다 더 중요한 것은 이후에도 같은 계약 데이터가 반복 검증된다는 점입니다.",
        "model_signal": "SIG-1BC42A78C68E",
        "driver_ids": ["restricted", "unmitigated"],
        "chart_title": "메탄 자료 공백이 만드는 연간 LNG 마진 노출",
        "chart_takeaway": "유럽 연계물량·단위마진·판매제한·완화율을 바꾸면 노출이 크게 달라지므로 계약별 생산지 데이터가 첫 내부 확인값입니다.",
    },
    "WRN-LITHIUM-45X-ELIGIBILITY": {
        "title": "미국 리튬 세액공제, 공급자와 원재료까지 검증해야 받을 수 있다",
        "rationale": "미국 세액공제 제한의 적용 기준일은 이미 지났고 공급자 인증과 비용추적이 사후 세무작업이 아니라 실증·계약의 선행조건이 됐습니다.",
        "company_lens": {
            "official_basis": "포스코홀딩스는 미국 직접리튬추출 실증과 북미 비중국 리튬 공급망 옵션을 추진해 생산세액공제 적격성과 공급자 구조가 투자안에 직접 연결됩니다.",
            "exposure": "미국 리튬 실증비, 원료·공정 공급자, 생산세액공제 적격 비용과 향후 상업투자 현금흐름이 직접 노출됩니다.",
            "decision_use": "공급망 적격성이 확인될 때까지 미국 생산세액공제를 0%로 두고 투자안을 평가할지 결정해야 합니다.",
        },
        "decision_question": "미국 리튬 실증을 계속하되 생산세액공제를 전액 가정할 것인가, 공급망 적격성이 확인될 때까지 공제 0%를 기준으로 둘 것인가?",
        "opportunity_effect": "미국 생산세액공제를 현금흐름에 반영해 현지 생산의 세후 경제성을 개선",
        "lead": "미국의 첨단제조 생산세액공제(세법 45X)는 미국 공장에서 생산했다는 사실만으로 받을 수 없습니다. 공급자의 중국 연계 지분, 원재료 원산지, 직접재료비 장부와 계약상 통제권까지 검증합니다. 미국 리튬 실증·양산 투자는 세액공제를 확정값으로 넣기 전에 공급자별 적격성과 대체조달비를 확인해야 합니다.",
        "conclusion": "공제액을 사업성에 넣기 전에 공급자별 비적격 비용비중과 계약상 통제권을 계산해야 합니다.",
        "market_note": "법은 지분 25%, 합산 지분 40%, 특정 채무 15% 같은 정량 문턱과 계약상 실질통제를 함께 봅니다. 지분율만 통과해도 공급처 지정·운영 지시·장기 로열티 같은 권리가 남으면 적격성은 다시 흔들릴 수 있습니다.",
        "model_signal": "SIG-616AB52ADDF4",
        "driver_ids": ["ineligible_share", "compliance_cost"],
        "chart_title": "비적격 비용비중이 45X 순가치를 얼마나 지우는가",
        "chart_takeaway": "적격 생산비가 같아도 비적격 비용과 준수비가 늘면 공제 순가치가 빠르게 줄어 공급자 장부가 기술실증의 선행조건이 됩니다.",
    },
    "WRN-LITHIUM-BLACK-MASS-FEEDSTOCK": {
        "title": "중국이 폐배터리 원료 수입을 다시 연다, 재활용 공장보다 원료계약이 먼저다",
        "lead": "중국은 2025년 8월부터 기준을 충족한 폐배터리 분쇄 원료(블랙매스)를 자유수입 대상으로 바꿨습니다. 수입문이 열렸다는 사실보다 니켈·코발트 합계 25% 이상, 리튬 3.5% 이상 등 품질 문턱을 통과하는 원료가 중국 설비와 다시 경쟁하게 된 점이 중요합니다. 포스코의 재활용 증설은 처리능력이 아니라 규격별 장기 원료확보율과 도착원가를 기준으로 판단해야 합니다.",
        "conclusion": "고품위 원료가 중국으로 이동할 가능성을 반영해 증설 게이트를 계약 원료확보율과 품질별 순회수마진으로 바꿔야 합니다.",
        "market_note": "중국의 새 문턱은 모든 폐배터리에 동일하지 않습니다. 니켈·코발트계는 니켈·코발트 합계 25% 이상과 리튬 3.5% 이상, LFP계는 철 18%·인 10%·리튬 2% 이상을 요구해 고품위 원료부터 국제 경쟁에 노출됩니다.",
        "model_signal": "SIG-F6C60D414787",
        "driver_ids": ["premium", "china_exposure"],
        "chart_title": "중국 수입 재개가 만드는 블랙매스 원료비 노출",
        "chart_takeaway": "수입 전환율·가격 프리미엄·회수율 가정에 따라 원료비 노출이 달라지므로 품질별 장기계약이 증설보다 먼저입니다.",
    },
    "WRN-LITHIUM-HYDROXIDE-MIX": {
        "title": "인산철 배터리가 세계 절반을 넘었다, 수산화리튬 성장계획을 다시 볼 때",
        "rationale": "인산철 배터리가 세계 전기차 배터리의 절반을 넘었고 가격 격차, 원료 선호, 북미 완성차의 양산 전환까지 같은 제품구성 변화가 확인됐습니다.",
        "lead": "세계 전기차 배터리에서 리튬인산철 배터리(LFP)의 비중은 2023년 약 40%에서 2024년 거의 50%, 2025년 55% 초과로 높아졌습니다. 같은 기간 인산철 배터리 팩은 니켈계 배터리(NMC)보다 평균 40% 이상 저렴해져 총 리튬 수요와 수산화리튬 수요가 같은 속도로 늘어난다는 전제가 약해졌습니다. 2027~2030 사업계획은 지역·차종·고객별 배터리 종류와 설비 전환능력으로 다시 계산해야 합니다.",
        "conclusion": "총 리튬 성장률이 아니라 고객별 배터리 화학계와 탄산·수산화 전환능력을 증설 기준으로 써야 합니다.",
        "market_note": "연속된 시장 비중은 방향을 분명히 보여줍니다. LFP는 2023년 40%에서 2025년 55%를 넘어섰고, 가격 격차도 2024년 약 30%에서 2025년 40% 초과로 벌어져 제품 믹스 전환을 동시에 밀고 있습니다.",
        "chart": {
            "chart_kind": "line",
            "title": "LFP는 3년 만에 세계 전기차 배터리의 과반을 넘었다",
            "unit": "%",
            "as_of": "2026-05-20",
            "takeaway": "LFP 비중이 2023년 40%에서 2025년 55% 초과로 상승해 총 리튬 수요와 수산화리튬 수요의 분리가 구조적일 가능성을 높였습니다.",
            "method_note": "IEA의 2023년 40%, 2024년 거의 50%, 2025년 55% 초과를 보수적으로 40·49·55로 표시했습니다.",
            "data_kind": "verified",
            "series": [{"name": "세계 EV 배터리 LFP 비중", "points": [{"label": "2023", "value": 40}, {"label": "2024", "value": 49}, {"label": "2025", "value": 55}]}],
            "source_ids": ["SRC-20260819-3F479FFE", "SRC-20260819-C39C1B19"],
        },
    },
    "WRN-LITHIUM-SODIUM-ESS-SUBSTITUTION": {
        "title": "대규모 나트륨 배터리 주문이 나왔다, 저장장치용 리튬 수요를 따로 볼 때",
        "rationale": "60기가와트시 규모의 주문과 40기가와트시 증설, 2026년 납품일이 확인돼 저장장치용 리튬 수요를 즉시 분리해 볼 필요가 있습니다.",
        "lead": "중국 배터리기업 CATL과 하이퍼스트롱은 3년간 60기가와트시(GWh) 규모의 나트륨이온 에너지저장장치(ESS)를 공급하는 주문을 체결했습니다. CATL은 2026년 1GWh 출하, 40GWh 증설과 160GWh 계획을 함께 제시했지만 주문·출하·생산능력은 서로 다른 단계입니다. 포스코홀딩스는 저장장치용 리튬 수요를 단일 성장률에서 떼어내 실제 납품과 후속 수주에 따라 전환율을 갱신해야 합니다.",
        "conclusion": "ESS 리튬 수요는 실제 나트륨 출하량과 후속 계약을 독립 변수로 두고 다시 계산해야 합니다.",
        "market_note": "상용화 증거는 크기가 아니라 단계로 읽어야 합니다. 60GWh 계약과 160GWh 계획은 크지만, 2026년 실제 출하 목표는 1GWh이므로 주문→생산능력→인도의 전환율이 결론을 가릅니다.",
        "model_signal": "SIG-C09FE799E568",
        "driver_ids": ["displacement", "lithium_price"],
        "chart_title": "ESS 나트륨 전환율이 리튬 매출 노출을 얼마나 바꾸는가",
        "chart_takeaway": "60GWh 계약을 시장점유율로 곧바로 환산하지 않고 전환율을 방어·기준·압박으로 나눠 리튬 매출 민감도를 봅니다.",
    },
    "WRN-RARE-EARTH-CONTROL-OPTION": {
        "title": "중국 희토류 추가 통제의 유예가 11월 끝난다, 광산보다 구매권이 먼저다",
        "lead": "중국의 2025년 4월 희토류 통제는 유지되는 반면 10월 추가조치는 2026년 11월 10일까지 한시 중단됐습니다. 미국은 그 사이 MP Materials에 4억 달러 우선주와 1억5천만 달러 대출, 10년 가격하한·구매계약을 묶었습니다. 포스코홀딩스는 통제 재개를 단정해 광산을 사기보다 고객 최소구매와 정책 하방이 붙은 조건부 구매권을 먼저 확보해야 합니다.",
        "conclusion": "11월 후속결정 전에는 확정 자산보다 철회 가능한 구매권·소수지분·단계투자의 가치를 비교해야 합니다.",
        "market_note": "미국 지원은 보조금 한 줄이 아니라 4억 달러 자본, 1억5천만 달러 대출, kg당 110달러 가격하한과 10년 구매계약을 묶은 구조입니다. 대체공급의 경제성은 광물가격보다 이 하방분담 패키지를 받을 수 있는지에 달렸습니다.",
        "chart": {
            "chart_kind": "bar", "title": "미국은 희토류 공급망에 자본 4억 달러와 대출 1.5억 달러를 묶었다", "unit": "USD million", "as_of": "2025-08-10", "takeaway": "자본과 대출만 5.5억 달러이며 가격하한·구매계약까지 붙어 비중국 공급의 하방을 여러 층으로 나눴습니다.", "method_note": "MP Materials 공시와 미국 국방부 발표의 확정 금액만 비교했으며 가격하한과 구매계약 가치는 합산하지 않았습니다.", "data_kind": "verified", "series": [{"name": "확정 지원", "points": [{"label": "우선주 투자", "value": 400}, {"label": "분리설비 대출", "value": 150}]}], "source_ids": ["SRC-20260819-0692EE56", "SRC-20260819-F04174E5"]
        },
    },
    "WRN-STEEL-DEMAND-CAPACITY-GAP": {
        "title": "세계 철강 과잉설비가 2028년 7.45억 톤으로 늘어난다, 판매량보다 가격방어가 먼저다",
        "lead": "세계 철강 과잉설비는 2025년 6.4억 톤에서 2028년 7.45억 톤으로 늘어날 전망입니다. 같은 기간 수요 증가는 3,400만 톤인데 설비 증가는 최대 1억3,900만 톤이어서 가동률을 높이면 이익이 따라온다는 범용재 계획이 맞지 않습니다. 포스코는 총톤 목표를 제품·시장별 도착마진과 자동 감산 기준으로 바꿔야 합니다.",
        "conclusion": "2027~2028 생산·판매 예산은 총톤이 아니라 제품별 가격방어력과 시장접근비용으로 재배분해야 합니다.",
        "market_note": "OECD 전망에서 2026~2028 수요 증가는 3,400만 톤, 신규 설비는 최대 1억3,900만 톤입니다. 차이는 1억500만 톤으로 과잉설비가 6.4억 톤에서 7.45억 톤으로 커지는 계산과 정확히 맞물립니다.",
        "chart": {
            "chart_kind": "line", "title": "수요보다 설비가 1억500만 톤 더 늘어난다", "unit": "Mt", "as_of": "2026-06-04", "takeaway": "2025~2028 과잉설비가 640Mt에서 745Mt로 16% 늘어 범용재 가동률 경쟁의 가격 하방이 강화됩니다.", "method_note": "OECD가 제시한 2025년 추정치와 2028년 전망치를 연결했습니다. 중간 연도는 보간하지 않았습니다.", "data_kind": "verified", "series": [{"name": "세계 과잉설비", "points": [{"label": "2025", "value": 640}, {"label": "2028", "value": 745}]}], "source_ids": ["SRC-20260818-2778E1E7"]
        },
    },
    "WRN-STEEL-DRI-PELLET-BOTTLENECK": {
        "title": "수소환원제철용 고품위 철광석은 전체의 3~4%뿐이다, 원료 확보가 기술 경쟁을 가른다",
        "rationale": "외부 원료 병목은 명확하지만 포스코 수소환원제철 기술의 상업 규모 성능과 총원가는 아직 실증이 필요합니다.",
        "lead": "기존 수소환원제철 경로가 요구하는 철 함량 67% 초과 고품위 원료는 해상 철광석의 3~4%에 불과합니다. 수소 가격이 내려가도 이 좁은 원료층에 수요가 몰리면 가공 프리미엄과 공급제약이 상업성을 다시 깎습니다. 포스코의 수소환원제철 기술(HyREX) 실증은 환원성능뿐 아니라 광종별 총현금원가와 공급가능량으로 원료 유연성의 가치를 증명해야 합니다.",
        "conclusion": "HyREX의 투자·기술제휴 기준에 광종별 원료비와 공급가능량을 넣어 원료 유연성을 숫자로 검증해야 합니다.",
        "market_note": "현재 직접환원급 원료는 해상물량 100 가운데 약 3.5에 불과합니다. 전통 DRI가 요구하는 67% 초과 철 함량과 희소한 공급 비중이 함께 작동하므로 원료 프리미엄은 수소비와 별도 변수입니다.",
        "model_signal": "SIG-73C13A4E0FC9",
        "driver_ids": ["pellet_premium", "unsubstituted"],
        "chart_title": "직접환원급 원료 프리미엄이 제조원가를 얼마나 늘리는가",
        "chart_takeaway": "직접환원급 원료비와 사용량에 따라 제조원가 노출이 커져, 광종별 실증원가가 기술 성공의 핵심 숫자가 됩니다.",
    },
    "WRN-STEEL-EU-VOLUME-CARBON-MIX": {
        "title": "유럽의 무관세 철강 수입량이 47% 줄어든다, 한정된 물량을 고객별로 다시 배분할 때",
        "lead": "유럽연합(EU)의 연간 무관세 철강 수입한도는 2024년 기준보다 47% 줄어든 1,830만 톤이고 초과 물량에는 50% 관세가 붙습니다. 저탄소 조달기준은 아직 제안 단계이므로 수입한도와 탄소 프리미엄을 확정된 하나의 제도로 합치면 안 됩니다. 포스코는 고객별 순마진·관세 귀속·검증 배출량을 묶어 희소한 무관세 물량을 다시 배분해야 합니다.",
        "conclusion": "EU 쿼터는 물량 소진율이 아니라 고객별 순마진과 저탄소 계약 가능성으로 배분해야 합니다.",
        "market_note": "47% 축소를 역산하면 이전 기준 물량은 약 3,450만 톤입니다. 1,830만 톤으로 줄어든 뒤 초과분에 50% 관세가 붙으므로 쿼터 안 1톤과 밖 1톤의 경제성이 크게 갈립니다.",
        "chart": {
            "chart_kind": "bar", "title": "EU 무관세 수입공간이 약 3,450만 톤에서 1,830만 톤으로 줄었다", "unit": "Mt/year", "as_of": "2026-06-30", "takeaway": "무관세 공간이 47% 줄어 같은 판매량보다 어떤 고객에게 쿼터를 배분하는지가 더 중요해졌습니다.", "method_note": "새 한도 18.3Mt와 공식 축소율 47%로 이전 기준을 18.3÷0.53=34.5Mt로 역산했습니다.", "data_kind": "derived", "series": [{"name": "무관세 수입한도", "points": [{"label": "2024 기준", "value": 34.5}, {"label": "2026 조치", "value": 18.3}]}], "source_ids": ["SRC-20260818-5C2CEB19"]
        },
    },
    "WRN-STEEL-MARKET-REGIONALISATION": {
        "title": "주요 철강시장의 진입조건이 관세에서 생산지·원산지 자격으로 바뀐다",
        "lead": "미국·유럽연합(EU)·영국의 철강 장벽은 모두 50% 수준이지만, 실제 병목은 관세율보다 생산경로·원산지·무관세 수입한도·저탄소 자격으로 갈라집니다. 동시에 2028년 세계 과잉설비 7.45억 톤이 보호시장 밖 가격을 누를 가능성이 큽니다. 포스코는 수출 총량이 아니라 주문별 시장 진입 가능성과 3년 순노출을 기준으로 현지화 선택권을 설계해야 합니다.",
        "conclusion": "현지화 투자는 관세율 하나가 아니라 고객별 시장 진입 가능성·순노출·최소구매를 같은 3년 순현재가치로 비교한 뒤 결정해야 합니다.",
        "market_note": "같은 50% 장벽이라도 미국은 생산자격, EU와 영국은 쿼터가 병목입니다. 보호시장에 못 들어간 물량은 2028년 7.45억 톤 과잉설비와 합쳐져 제3시장 가격까지 누르므로 직접 관세와 간접 가격압력을 함께 봐야 합니다.",
        "chart": {
            "chart_kind": "bar", "title": "같은 10만 톤도 전가율에 따라 순관세 노출이 100배 달라진다", "unit": "USD million/year", "as_of": "2026-08-20", "takeaway": "물량보다 관세율·고객 전가율·시장접근자격이 현지화 경제성을 지배합니다.", "method_note": "순관세 노출=물량×가격×관세율×(1-고객 전가율). 방어 0.9, 기준 20, 압박 87.5는 공개 규정과 조절 가능한 가정이며 POSCO 전망이 아닙니다.", "data_kind": "scenario", "series": [{"name": "순관세 노출", "points": [{"label": "방어", "value": 0.9}, {"label": "기준", "value": 20}, {"label": "압박", "value": 87.5}]}], "source_ids": ["SRC-20260818-5C2CEB19", "SRC-20260820-422EE636"]
        },
    },
    "WRN-STRATEGIC-MINERALS-MARKET-DESIGN": {
        "title": "정부가 전략광물의 가격·구매·세제를 함께 보장하기 시작했다, 광산보다 계약을 먼저 설계할 때",
        "lead": "미국은 희토류에 가격하한·구매계약·자본·대출을 묶고, 호주는 적격 가공비의 10%를 최대 10년 상계하며, 유럽연합(EU)은 공동수요 매칭을 시작했습니다. 정책은 광산 보조금 한 번이 아니라 가격·물량·자본비를 장기간 나누는 시장설계로 이동하고 있습니다. 포스코홀딩스는 광종 선정 전에 고객 최소구매·정책 하방·철회조건을 한 계약 패키지로 비교해야 합니다.",
        "conclusion": "신규 광종은 자산 매입보다 고객 수요와 정부 하방분담을 동시에 잠그는 조건부 계약부터 설계해야 합니다.",
        "market_note": "확정된 미국 사례만 봐도 4억 달러 자본, 1억5천만 달러 대출, kg당 110달러 가격하한과 10년 구매계약이 함께 움직입니다. 호주의 10% 세액상계와 EU 공동매칭은 다른 방식이므로 지원 건수를 세기보다 어떤 하방을 누가 부담하는지 비교해야 합니다.",
        "chart": {
            "chart_kind": "bar", "title": "미국 희토류 패키지는 자본과 대출만 5.5억 달러다", "unit": "USD million", "as_of": "2025-08-10", "takeaway": "가격하한·구매계약 가치를 빼고도 확정 금융이 5.5억 달러여서 단일 보조금보다 계약 패키지의 하방분담이 큽니다.", "method_note": "MP Materials 공시와 미국 국방부 발표의 자본·대출만 비교했습니다. 서로 다른 통화·세제인 호주 10% 상계는 같은 축에 합치지 않았습니다.", "data_kind": "verified", "series": [{"name": "확정 금융", "points": [{"label": "우선주 투자", "value": 400}, {"label": "분리설비 대출", "value": 150}]}], "source_ids": ["SRC-20260819-0692EE56", "SRC-20260819-F04174E5"]
        },
    },
    "WRN-TUNGSTEN-LICENSE-PRICE": {
        "title": "텅스텐 가격이 1년 새 두 배가 됐다, 고객이 살 규격부터 확인할 때",
        "lead": "2025년 로테르담 텅스텐 정광 가격은 266에서 551로, 중간재 가격은 331에서 675로 올라 두 지표가 모두 약 두 배가 됐습니다. 중국이 세계 광산생산의 79%를 차지한 상태에서 수출허가가 추가돼 가격보다 납기와 고객의 규격 승인 위험이 먼저 커졌습니다. 포스코홀딩스는 광산 매입보다 고객 규격·최소구매·비중국 가공경로가 결합된 사업안을 우선해야 합니다.",
        "conclusion": "고객 승인과 최소구매가 확인되기 전에는 가격 상승을 자산 수익으로 환산하지 말고 계약형 옵션으로 접근해야 합니다.",
        "market_note": "같은 해 정광은 266에서 551로 107%, APT는 331에서 675로 104% 상승했습니다. 두 제품이 비슷한 폭으로 움직였다는 점은 단일 품목 이상이 아니라 공급망 전반의 충격이었음을 보여주지만 영구 가격수준을 보장하지는 않습니다.",
        "chart": {
            "chart_kind": "line", "title": "정광과 APT 가격이 같은 해 모두 두 배가 됐다", "unit": "2025 start=100 index", "as_of": "2026-02-06", "takeaway": "정광은 207, APT는 204로 올라 수출통제 충격이 원료와 중간재에 함께 전달됐습니다.", "method_note": "USGS가 인용한 2025년 시작·종료 가격을 각각 100으로 지수화했습니다. POSCO 조달가격이나 장기 전망이 아닙니다.", "data_kind": "derived", "series": [{"name": "65% 정광", "points": [{"label": "2025 시작", "value": 100}, {"label": "2025 종료", "value": 207}]}, {"name": "APT", "points": [{"label": "2025 시작", "value": 100}, {"label": "2025 종료", "value": 204}]}], "source_ids": ["SRC-20260819-1D416335"]
        },
    },
}


def evaluate(expression: Any, values: dict[str, float]) -> float:
    if isinstance(expression, (int, float)):
        return float(expression)
    if not isinstance(expression, dict):
        raise ValueError(f"Unsupported expression: {expression!r}")
    if "var" in expression:
        return float(values[str(expression["var"])])
    op = str(expression.get("op"))
    args = [evaluate(item, values) for item in expression.get("args") or []]
    if op == "add":
        return sum(args)
    if op == "subtract" and len(args) == 2:
        return args[0] - args[1]
    if op == "multiply":
        result = 1.0
        for item in args:
            result *= item
        return result
    if op == "divide" and len(args) == 2:
        return args[0] / args[1]
    if op == "min":
        return min(args)
    if op == "max":
        return max(args)
    raise ValueError(f"Unsupported operation: {op!r}")


def display_number(value: float, unit: str = "") -> str:
    if unit in {"fraction", "share"}:
        return f"{value * 100:.0f}%"
    if abs(value) >= 100:
        number = f"{value:,.0f}"
    elif abs(value) >= 10:
        number = f"{value:.1f}".rstrip("0").rstrip(".")
    else:
        number = f"{value:.2f}".rstrip("0").rstrip(".")
    return f"{number} {unit}".strip()


def model_table(store: Path, config: dict[str, Any]) -> dict[str, Any]:
    signal = market_sensing.read_json(
        store / ".system" / "signals" / f"{config['model_signal']}.json"
    )
    insight = market_sensing.read_json(
        store / ".system" / "insights" / f"{signal['insight_id']}.json"
    )
    estimate = market_sensing.validate_impact_estimate(insight["impact_estimate"])
    output = next(item for item in estimate["outputs"] if item.get("primary"))
    variables_by_id = {item["id"]: item for item in estimate["variables"]}
    driver_ids = list(config.get("driver_ids") or list(variables_by_id)[:2])
    drivers = [variables_by_id[item] for item in driver_ids]
    rows = []
    for preset in estimate["presets"]:
        values = {key: float(value) for key, value in preset["values"].items()}
        rows.append(
            [
                str(preset["label"]).replace(" 시나리오", ""),
                display_number(evaluate(output["expression"], values), output["unit"]),
                *[
                    display_number(values[item["id"]], item["unit"])
                    for item in drivers
                ],
            ]
        )
    source_ids = list(
        dict.fromkeys(
            list(signal.get("source_ids") or [])
            + [
                source_id
                for variable in estimate.get("variables") or []
                for source_id in variable.get("source_ids") or []
            ]
        )
    )
    return {
        "type": "quantitative_table",
        "status": "adopted",
        "table_kind": "scenario",
        "title": config["chart_title"],
        "unit": "표 안에 표시",
        "as_of": estimate["as_of"],
        "takeaway": config["chart_takeaway"],
        "method_note": f"{estimate.get('formula_display') or estimate['description']} {estimate['notice']}",
        "data_kind": "scenario",
        "columns": [
            "시나리오",
            output["label"],
            *[item["label"] for item in drivers],
        ],
        "rows": rows,
        "source_ids": source_ids,
    }


def explicit_table(config: dict[str, Any]) -> dict[str, Any]:
    chart = config["chart"]
    series = chart["series"]
    labels = [str(point["label"]) for point in series[0]["points"]]
    if chart["data_kind"] == "scenario":
        values = [float(point["value"]) for point in series[0]["points"]]
        base_index = labels.index("기준") if "기준" in labels else 0
        base = values[base_index]
        rows = []
        for label, value in zip(labels, values):
            relative = "기준" if value == base else (
                f"기준 대비 {value / base:.1f}배" if base else "비율 계산 불가"
            )
            rows.append([label, display_number(value, chart["unit"]), relative])
        columns = ["시나리오", "정량 결과", "기준 대비"]
        table_kind = "scenario"
    elif len(series) == 1:
        first = float(series[0]["points"][0]["value"])
        rows = []
        for point in series[0]["points"]:
            value = float(point["value"])
            if value == first:
                change = "기준"
            elif first:
                change = f"{(value / first - 1) * 100:+.0f}%"
            else:
                change = "비율 계산 불가"
            rows.append(
                [str(point["label"]), display_number(value, chart["unit"]), change]
            )
        columns = ["시점·항목", "확인값", "첫 값 대비"]
        table_kind = "trend" if all(label[:2] == "20" for label in labels) else "comparison"
    else:
        first_values = [float(item["points"][0]["value"]) for item in series]
        rows = []
        for point_index, label in enumerate(labels):
            values = [float(item["points"][point_index]["value"]) for item in series]
            changes = []
            for value, first in zip(values, first_values):
                changes.append("기준" if value == first else f"{(value / first - 1) * 100:+.0f}%")
            rows.append(
                [
                    label,
                    *[display_number(value, chart["unit"]) for value in values],
                    " / ".join(changes),
                ]
            )
        columns = ["시점·항목", *[item["name"] for item in series], "첫 시점 대비"]
        table_kind = "trend"
    return {
        "type": "quantitative_table",
        "status": "adopted",
        "table_kind": table_kind,
        "title": chart["title"],
        "unit": "표 안에 표시",
        "as_of": chart["as_of"],
        "takeaway": chart["takeaway"],
        "method_note": chart["method_note"],
        "data_kind": chart["data_kind"],
        "columns": columns,
        "rows": rows,
        "source_ids": chart["source_ids"],
    }


def rewrite(store: Path, apply: bool) -> list[str]:
    changed: list[str] = []
    for warning_path in sorted((store / ".system" / "warnings").glob("WRN-*.json")):
        warning = market_sensing.read_json(warning_path)
        warning_id = str(warning["warning_id"])
        config = REWRITE.get(warning_id)
        if config is None:
            raise ValueError(f"Missing rewrite configuration for {warning_id}")
        thesis = market_sensing.read_json(
            store / ".system" / "theses" / f"{warning['thesis_id']}.json"
        )
        trend_ids = list(thesis.get("trend_ids") or [])
        if len(trend_ids) != 1:
            raise ValueError(f"{warning_id}: expected exactly one trend")
        trend = market_sensing.read_json(
            store / ".system" / "trends" / f"{trend_ids[0]}.json"
        )

        warning["title"] = config["title"]
        warning["executive_summary"] = config["lead"]
        if config.get("rationale"):
            warning["rationale"] = config["rationale"]
        if config.get("company_lens"):
            warning["company_lens"].update(config["company_lens"])
        if config.get("decision_question"):
            warning["decision_question"] = config["decision_question"]
        if config.get("opportunity_effect"):
            warning["decision_lens"]["opportunity"]["business_effect"] = config[
                "opportunity_effect"
            ]
        plan = warning["editorial_plan"]
        if config.get("decision_question"):
            plan["reader_question"] = config["decision_question"]
        plan["provisional_conclusion"] = config["conclusion"]
        plan["quantification"] = {
            "status": "modeled",
            "decision_metric": str(config.get("chart_title") or config["chart"]["title"]),
        }
        chart = model_table(store, config) if config.get("model_signal") else explicit_table(config)
        plan["visuals"] = [
            chart,
            *[
                item
                for item in plan.get("visuals") or []
                if item.get("type")
                not in {"quantitative_chart", "quantitative_table", "scenario_bars"}
            ],
        ]

        for section in warning.get("report_sections") or []:
            if section.get("role") == "market_change":
                body = str(section["body"])
                if not body.startswith(config["market_note"]):
                    section["body"] = config["market_note"] + "\n\n" + body
            elif section.get("role") == "business_impact":
                body = str(section["body"])
                if body.startswith(("상단 차트는 ", "상단 정량표는 ")) and "\n\n" in body:
                    body = body.split("\n\n", 1)[1]
                section["body"] = (
                    f"상단 정량표는 {chart['takeaway']} "
                    f"단위와 기준일을 확인하고, "
                    f"{'회사 실제 실적 전망이 아닌 민감도 결과로' if chart['data_kind'] == 'scenario' else '공식 확인값과 공개자료 역산값으로'} 읽어야 합니다.\n\n"
                    + body
                )
        history = list(warning.get("history") or [])
        if not any(
            event.get("date") == "2026-08-20" and event.get("action") == "sparse_visual_rewrite"
            for event in history
        ):
            history.append(
                {
                    "date": "2026-08-20",
                    "action": "sparse_visual_rewrite",
                    "rationale": "2~3개 값과 시나리오를 강제 차트에서 가정·결과가 함께 보이는 정량표로 교체",
                }
            )
        if not any(
            event.get("date") == "2026-08-20" and event.get("action") == "executive_title_rewrite"
            for event in history
        ):
            history.append(
                {
                    "date": "2026-08-20",
                    "action": "executive_title_rewrite",
                    "rationale": "법령 코드·영문 약어·단위·업계 은어를 제목에서 제거하고 임원이 사전 설명 없이 이해할 수 있는 시장 변화와 판단으로 재작성",
                }
            )
        warning["history"] = history
        manifest = {
            "schema_version": market_sensing.STRATEGIC_WATCH_SCHEMA_VERSION,
            "trend": trend,
            "thesis": thesis,
            "warning": warning,
        }
        market_sensing.validate_strategic_watch_manifest(store, manifest)
        changed.append(warning_id)
        if apply:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / f"{warning_id}.json"
                market_sensing.write_json(path, manifest)
                market_sensing.upsert_strategic_watch(
                    argparse.Namespace(root=str(store), watch_file=str(path))
                )
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    changed = rewrite(args.root.resolve(), args.apply)
    print(
        json.dumps(
            {"mode": "apply" if args.apply else "dry-run", "rewritten": changed},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
