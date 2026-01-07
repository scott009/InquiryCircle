#!/usr/bin/env python3
"""
Add Korean (한국어) translations to Chapter 9 of rdg_en_v3.json
"""

import json
from pathlib import Path

# Korean translations for Chapter 9
KOREAN_TITLE = "회복 다르마란 무엇인가?"

KOREAN_PARAGRAPHS = {
    "p9-1": "다르마(Dharma)는 '진리', '현상', 또는 '사물의 본질'을 의미하는 산스크리트어입니다. 대문자로 표기될 때, 다르마는 일반적으로 부처님의 가르침과 그러한 가르침에 기반한 수행을 의미합니다.",

    "p9-2": "부처님은 모든 인간이 어느 정도는 갈애와 씨름한다는 것을 알고 계셨습니다. 갈애란 우리의 생각, 감정, 또는 상황을 바꾸고자 하는 강력하고 때로는 맹목적인 욕망입니다. 중독을 경험하는 우리는 이러한 원하는 변화를 만들기 위해 습관적인 패턴으로 물질이나 해로운 행동을 사용하도록 몰려왔습니다. 부처님께서 중독에 대해 구체적으로 말씀하지 않으셨지만, 그분은 인간 마음의 집착적 본질을 이해하셨습니다. 그분은 쾌락에 대한 우리의 집착과 고통에 대한 혐오를 이해하셨습니다. 그분은 우리가 느끼고 싶은 것을 쫓고 두려워하는 감정에서 도망치기 위해 기꺼이 취하는 극단적인 조치들을 이해하셨습니다. 그리고 그분은 해결책을 찾으셨습니다.",

    "p9-3": "이 책은 불교 수행과 원칙을 사용하여 중독의 고통에서 우리 자신을 해방시키는 방법을 설명합니다. 이 프로그램은 알코올과 약물과 같은 물질 중독으로부터의 회복과 성, 도박, 포르노, 기술, 일, 공동의존, 쇼핑, 음식, 미디어, 자해, 거짓말, 절도, 강박적 걱정과 같은 과정 중독으로부터의 회복으로 이어집니다. 이것은 고통을 일으키는 반복적이고 습관적인 행동으로부터의 자유로 가는 길입니다.",

    "p9-4": "이 책을 읽는 우리 중 일부는 불교에 익숙하지 않거나 불교 수행을 회복의 길로 사용하지 않았을 수 있습니다. 이 책에는 익숙하지 않은 불교 용어와 개념도 있을 수 있습니다. 우리는 또한 이 책에서 제시하는 내용이 모든 불교 전통, 계보, 가르침 및 수행을 포함하지 않으며, 어느 정도 여러분 자신의 불교 수행과 다를 수 있다는 것을 이해합니다. 우리의 목표는 회복에 새로운 사람들, 불교에 새로운 사람들, 그리고 둘 다에 익숙한 사람들을 위해 회복 다르마에서 우리의 길과 수행을 명확하게 설명하는 것입니다. 이 책은 우리 프로그램이 유래한 원래의 불교 가르침, 불교의 근본적이고 초기 가르침의 본질인 사성제를 설명하여 팔정도 수행이 초기 및 장기 회복의 도전을 변화시킬 수 있는 실용적인 길임을 보여줍니다.",

    "p9-5": "이것은 포기에 기반한 프로그램입니다. 우리의 개별 중독이 무엇이든 간에, 우리 회원 모두는 그 물질이나 행동으로부터 기본적인 금욕을 약속합니다. 음식과 기술과 같은 과정 중독의 경우, 포기는 사려 깊은 경계와 의도를 확립하는 것을 의미할 수 있습니다. 우리 중 일부에게는 강박적인 성적 행동이나 사랑과 관계를 강박적으로 추구하는 것과 같은 것들로부터의 금욕이 우리가 의미 있는 경계를 이해하고 찾기 위해 노력할 때 필요할 수 있습니다. 우리 중 많은 사람들은 일정 기간 동안 주요 중독을 포기한 후, 다른 해로운 행동과 과정 중독이 우리 삶에서 명백해진다는 것을 발견했습니다. 낙담하기보다는, 우리는 자비, 지혜, 그리고 우리의 습관적 경향에 대한 인내심 있는 조사로 이러한 행동들을 만날 수 있다는 것을 발견했습니다. 우리는 회복이 우리 자신의 깨달음 잠재력을 찾기 위해 습관과 조건화된 행동의 층을 벗겨내는 평생의 전체적 과정이라고 믿습니다.",

    "p9-6": "우리의 프로그램은 동료 주도입니다: 우리는 특정한 스승이나 지도자를 따르지 않습니다. 우리는 함께 회복의 길을 걷는 동반자로서 서로를 지원합니다. 이것은 교리나 종교에 기반한 프로그램이 아니라, 우리 자신을 위해 진리를 찾는 것입니다. 이 통찰은 우리에게 효과가 있었지만, 유일한 길은 아닙니다. 그것은 다른 영적 길과 회복 프로그램과 완전히 양립할 수 있습니다. 우리는 자신의 경험으로부터 진정한 회복은 철저한 정직, 이해, 자각, 성실의 의도로만 가능하다는 것을 알고 있으며, 우리는 당신이 자신의 길을 발견할 것이라고 믿습니다.",

    "p9-7": "이것은 우리에게 결코 성장을 멈추지 말 것을 요구하는 프로그램입니다. 그것은 우리에게 우리의 선택을 소유하고 우리 자신의 치유에 책임을 질 것을 요구합니다. 그것은 마음챙김, 친절, 관대함, 용서, 그리고 깊은 자비에 기반합니다.",

    "p9-8": "우리는 동기부여로서 수치심과 두려움의 방법에 의존하지 않습니다. 이것들은 우리 자신의 과거에서 효과가 없었고, 종종 재발과 낙담을 통해 더 많은 투쟁과 고통을 만들어냈습니다. 중독으로부터 회복하는 데 필요한 용기는 궁극적으로 마음의 용기이며, 우리는 이 용감한 작업에 전념하면서 서로를 지원하는 것을 목표로 합니다.",

    "p9-9": "우리 중 많은 사람들은 우리 자신을 비판하는 데 많은 시간을 보냈습니다. 이 프로그램에서 우리는 우리 자신에게 하는 폭력과 해를 포함하여 폭력과 해를 끼치는 것을 포기합니다. 우리는 용서의 치유력을 믿습니다. 우리는 깨어나고 회복할 우리 자신의 잠재력, 부처님의 사성제, 그리고 모임에서 그리고 회복 여정 전반에 걸쳐 우리가 만나고 연결하는 사람들을 신뢰합니다.",

    "p9-10": "물론 우리는 인간 조건의 일부인 상황과 조건에서 벗어날 수 없습니다. 우리는 이미 시도했습니다 — 약물과 알코올을 통해, 성과 공동의존을 통해, 도박과 기술을 통해, 일과 쇼핑을 통해, 음식이나 음식 제한을 통해, 집착과 우리의 경험과 감정을 통제하려는 헛된 시도를 통해 — 그리고 그것이 효과가 없었기 때문에 우리는 여기에 있습니다. 이것은 어떤 고통과 실망이 항상 존재할 것임을 인식하고 받아들이도록 우리를 초대하고, 우리가 과거에 그 고통을 다룬 비숙련된 방법을 조사하며, 우리 자신의 고통, 다른 사람의 고통, 그리고 우리가 일으킨 고통에 대한 이해, 자비, 용서, 통찰의 습관을 개발하는 프로그램입니다. 통찰과 자비를 가진 수용은 우리의 고통을 견딜 수 없게 만드는 괴로움으로부터의 자유를 창조하는 것입니다.",

    "p9-11": "이 책은 중독의 순환으로부터 해방과 자유를 가져올 수 있는 길에 대한 소개일 뿐입니다. 우리 프로그램의 의도와 희망은 길 위의 모든 사람이 그것을 자신의 것으로 만들 수 있는 힘을 부여받는 것입니다.",

    "p9-12": "당신이 행복하기를 바랍니다.",

    "p9-13": "당신이 편안하기를 바랍니다.",

    "p9-14": "당신이 고통에서 벗어나기를 바랍니다.",

    "p9-15": "모든 존재가 고통에서 벗어나기를 바랍니다."
}

def main():
    """Update JSON with Korean translations for Chapter 9."""
    input_file = Path("/mnt/c/Users/scott/Documents/AIProjects/Markdown/ThaiTranslation/rdg_en_v3.json")

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create backup
    backup_file = input_file.with_name('rdg_en_v3.json.backup_before_korean')
    print(f"Creating backup at {backup_file}...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Adding Korean translations to Chapter 9...")

    # Find and update Chapter 9
    updated_count = 0
    for section in data['content']:
        if 'chapters' in section:
            for chapter in section['chapters']:
                if chapter.get('title') == 'WHAT IS RECOVERY DHARMA?':
                    # Add Korean title
                    chapter['korean_title'] = KOREAN_TITLE
                    print(f"✓ Updated chapter title")

                    # Update paragraphs
                    for sec in chapter.get('sections', []):
                        for content_item in sec.get('content', []):
                            if content_item.get('type') == 'paragraph':
                                para_id = content_item['id']
                                if para_id in KOREAN_PARAGRAPHS:
                                    content_item['korean_text'] = KOREAN_PARAGRAPHS[para_id]
                                    updated_count += 1
                                    print(f"✓ Updated {para_id}")

    print(f"\nSaving updated JSON...")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Korean translations added successfully!")
    print(f"   Updated: 1 title + {updated_count} paragraphs")
    print(f"   Backup saved at: {backup_file}")

if __name__ == "__main__":
    main()
