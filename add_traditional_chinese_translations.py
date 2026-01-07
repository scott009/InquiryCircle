#!/usr/bin/env python3
"""
Add Traditional Chinese (繁體中文) translations to Chapter 9 of rdg_en_v3.json
"""

import json
from pathlib import Path

# Traditional Chinese translations for Chapter 9
TRADITIONAL_CHINESE_TITLE = "什麼是復原佛法？"

TRADITIONAL_CHINESE_PARAGRAPHS = {
    "p9-1": "佛法（Dharma）是一個梵文詞，意思是「真理」、「現象」或「事物的本質」。當首字母大寫時，佛法通常指佛陀的教義和基於這些教義的修行方法。",

    "p9-2": "佛陀知道所有人在某種程度上都與渴愛掙扎——那種強烈的、有時令人盲目的欲望，想要改變我們的思想、感受或境遇。我們這些經歷成癮的人被驅使使用物質和／或有害行為，以習慣性的模式試圖創造這種期望的改變。儘管佛陀沒有具體談論成癮，但他理解人類心智的執著本質。他理解我們對快樂的執著和對痛苦的厭惡。他理解我們願意採取的極端措施，追逐我們想要感受的東西，逃避我們害怕的感受。而他找到了解決方案。",

    "p9-3": "本書描述了一種利用佛教修行和原則從成癮的痛苦中解脫自己的方法。這個計劃引導從對酒精和毒品等物質的成癮中復原，以及從性、賭博、色情、科技、工作、共依存、購物、飲食、媒體、自我傷害、說謊、偷竊和強迫性擔憂等過程成癮中復原。這是一條通往自由的道路，遠離任何導致痛苦的重複和習慣性行為。",

    "p9-4": "我們中一些閱讀本書的人可能不熟悉佛教，或者沒有將佛教修行作為復原的途徑。本書中可能也有不熟悉的佛教詞彙和概念。我們也理解，我們在本書中呈現的內容並不包含所有佛教傳統、法脈、教義和修行，並且在某種程度上可能與您自己的佛教修行有所不同。我們的目標是清楚地描述我們在復原佛法中的道路和修行，為新接觸復原的人、新接觸佛教的人，以及熟悉兩者的人。本書描述了我們計劃所源自的原始佛教教義，佛教基本和早期教義的精髓——四聖諦——以展示如何修習八正道是一條實用的道路，可以轉化早期和長期復原的挑戰。",

    "p9-5": "這是一個基於放下的計劃。無論我們個人的成癮是什麼，我們所有的成員都承諾從該物質或行為中基本戒除。對於像食物和科技這樣的過程成癮，放下可能意味著建立深思熟慮的界限和意圖。對於我們中的一些人來說，戒除像強迫性性行為或強迫性尋求愛情和關係這樣的事情，可能是必要的，因為我們努力理解和找到有意義的界限。我們中的許多人發現，在放下我們的主要成癮一段時間後，其他有害行為和過程成癮在我們的生活中變得明顯。我們沒有氣餒，而是發現我們可以用慈悲、智慧和耐心調查我們的習慣傾向來面對這些行為。我們相信復原是一個終身的、整體的過程，剝離習慣和條件行為的層次，以找到我們自己覺醒的潛力。",

    "p9-6": "我們的計劃是同儕主導的：我們不追隨任何一位老師或領導者。我們作為夥伴互相支持，共同走在復原的道路上。這不是一個基於教條或宗教的計劃，而是為自己尋找真理。這種洞見對我們有效，但不是唯一的道路。它完全兼容其他靈性道路和復原計劃。我們從自己的經驗中知道，真正的復原只有在徹底誠實、理解、覺察和正直的意圖下才有可能，我們相信您會發現自己的道路。",

    "p9-7": "這是一個要求我們永不停止成長的計劃。它要求我們擁有自己的選擇，並對自己的療癒負責。它基於正念、仁慈、慷慨、寬恕和深深的慈悲。",

    "p9-8": "我們不依賴羞恥和恐懼的方法作為動力。這些在我們過去的經歷中沒有奏效，並且經常通過復發和沮喪造成更多的掙扎和痛苦。從成癮中復原所需的勇氣歸根結底是心靈的勇氣，我們的目標是在我們致力於這項勇敢的工作時互相支持。",

    "p9-9": "我們中的許多人花了很多時間批評自己。在這個計劃中，我們放棄暴力和造成傷害，包括我們對自己造成的暴力和傷害。我們相信寬恕的療癒力量。我們信任自己覺醒和復原的潛力，信任佛陀的四聖諦，以及我們在會議中遇到和聯繫的人，以及在我們整個復原旅程中。",

    "p9-10": "當然，我們無法逃避作為人類狀況一部分的環境和條件。我們已經嘗試過——通過毒品和酒精，通過性和共依存，通過賭博和科技，通過工作和購物，通過食物或限制食物，通過執著和徒勞的試圖控制我們的經驗和感受——而我們在這裡是因為它沒有奏效。這是一個邀請我們認識和接受某些痛苦和失望將永遠存在的計劃，調查我們過去處理那種痛苦的不善巧方式，並培養對我們自己的痛苦、他人的痛苦以及我們造成的痛苦的理解、慈悲、寬恕和洞見的習慣。接納伴隨洞見和慈悲是創造從使我們的痛苦看起來難以忍受的痛苦中解脫的自由的原因。",

    "p9-11": "本書只是介紹一條可以帶來從成癮循環中解脫和自由的道路。我們計劃的意圖和希望是，道路上的每個人都將被賦予力量，使其成為自己的。",

    "p9-12": "願你快樂。",

    "p9-13": "願你安詳。",

    "p9-14": "願你脫離痛苦。",

    "p9-15": "願一切眾生脫離痛苦。"
}

def main():
    """Update JSON with Traditional Chinese translations for Chapter 9."""
    input_file = Path("/mnt/c/Users/scott/Documents/AIProjects/Markdown/ThaiTranslation/rdg_en_v3.json")

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create backup
    backup_file = input_file.with_name('rdg_en_v3.json.backup_before_traditional_chinese')
    print(f"Creating backup at {backup_file}...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Adding Traditional Chinese translations to Chapter 9...")

    # Find and update Chapter 9
    updated_count = 0
    for section in data['content']:
        if 'chapters' in section:
            for chapter in section['chapters']:
                if chapter.get('title') == 'WHAT IS RECOVERY DHARMA?':
                    # Add Traditional Chinese title
                    chapter['Chinese_Tradition_title'] = TRADITIONAL_CHINESE_TITLE
                    print(f"✓ Updated chapter title")

                    # Update paragraphs
                    for sec in chapter.get('sections', []):
                        for content_item in sec.get('content', []):
                            if content_item.get('type') == 'paragraph':
                                para_id = content_item['id']
                                if para_id in TRADITIONAL_CHINESE_PARAGRAPHS:
                                    content_item['Chinese_Tradition_text'] = TRADITIONAL_CHINESE_PARAGRAPHS[para_id]
                                    updated_count += 1
                                    print(f"✓ Updated {para_id}")

    print(f"\nSaving updated JSON...")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Traditional Chinese translations added successfully!")
    print(f"   Updated: 1 title + {updated_count} paragraphs")
    print(f"   Backup saved at: {backup_file}")

if __name__ == "__main__":
    main()
