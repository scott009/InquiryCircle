#!/usr/bin/env python3
"""
Add Simplified Chinese (简体中文) translations to Chapter 9 of rdg_en_v3.json
"""

import json
from pathlib import Path

# Simplified Chinese translations for Chapter 9
SIMPLIFIED_CHINESE_TITLE = "什么是复原佛法？"

SIMPLIFIED_CHINESE_PARAGRAPHS = {
    "p9-1": "佛法（Dharma）是一个梵文词，意思是\"真理\"、\"现象\"或\"事物的本质\"。当首字母大写时，佛法通常指佛陀的教义和基于这些教义的修行方法。",

    "p9-2": "佛陀知道所有人在某种程度上都与渴爱挣扎——那种强烈的、有时令人盲目的欲望，想要改变我们的思想、感受或境遇。我们这些经历成瘾的人被驱使使用物质和/或有害行为，以习惯性的模式试图创造这种期望的改变。尽管佛陀没有具体谈论成瘾，但他理解人类心智的执着本质。他理解我们对快乐的执着和对痛苦的厌恶。他理解我们愿意采取的极端措施，追逐我们想要感受的东西，逃避我们害怕的感受。而他找到了解决方案。",

    "p9-3": "本书描述了一种利用佛教修行和原则从成瘾的痛苦中解脱自己的方法。这个计划引导从对酒精和毒品等物质的成瘾中复原，以及从性、赌博、色情、科技、工作、共依存、购物、饮食、媒体、自我伤害、说谎、偷窃和强迫性担忧等过程成瘾中复原。这是一条通往自由的道路，远离任何导致痛苦的重复和习惯性行为。",

    "p9-4": "我们中一些阅读本书的人可能不熟悉佛教，或者没有将佛教修行作为复原的途径。本书中可能也有不熟悉的佛教词汇和概念。我们也理解，我们在本书中呈现的内容并不包含所有佛教传统、法脉、教义和修行，并且在某种程度上可能与您自己的佛教修行有所不同。我们的目标是清楚地描述我们在复原佛法中的道路和修行，为新接触复原的人、新接触佛教的人，以及熟悉两者的人。本书描述了我们计划所源自的原始佛教教义，佛教基本和早期教义的精髓——四圣谛——以展示如何修习八正道是一条实用的道路，可以转化早期和长期复原的挑战。",

    "p9-5": "这是一个基于放下的计划。无论我们个人的成瘾是什么，我们所有的成员都承诺从该物质或行为中基本戒除。对于像食物和科技这样的过程成瘾，放下可能意味着建立深思熟虑的界限和意图。对于我们中的一些人来说，戒除像强迫性性行为或强迫性寻求爱情和关系这样的事情，可能是必要的，因为我们努力理解和找到有意义的界限。我们中的许多人发现，在放下我们的主要成瘾一段时间后，其他有害行为和过程成瘾在我们的生活中变得明显。我们没有气馁，而是发现我们可以用慈悲、智慧和耐心调查我们的习惯倾向来面对这些行为。我们相信复原是一个终身的、整体的过程，剥离习惯和条件行为的层次，以找到我们自己觉醒的潜力。",

    "p9-6": "我们的计划是同伴主导的：我们不追随任何一位老师或领导者。我们作为伙伴互相支持，共同走在复原的道路上。这不是一个基于教条或宗教的计划，而是为自己寻找真理。这种洞见对我们有效，但不是唯一的道路。它完全兼容其他灵性道路和复原计划。我们从自己的经验中知道，真正的复原只有在彻底诚实、理解、觉察和正直的意图下才有可能，我们相信您会发现自己的道路。",

    "p9-7": "这是一个要求我们永不停止成长的计划。它要求我们拥有自己的选择，并对自己的疗愈负责。它基于正念、仁慈、慷慨、宽恕和深深的慈悲。",

    "p9-8": "我们不依赖羞耻和恐惧的方法作为动力。这些在我们过去的经历中没有奏效，并且经常通过复发和沮丧造成更多的挣扎和痛苦。从成瘾中复原所需的勇气归根结底是心灵的勇气，我们的目标是在我们致力于这项勇敢的工作时互相支持。",

    "p9-9": "我们中的许多人花了很多时间批评自己。在这个计划中，我们放弃暴力和造成伤害，包括我们对自己造成的暴力和伤害。我们相信宽恕的疗愈力量。我们信任自己觉醒和复原的潜力，信任佛陀的四圣谛，以及我们在会议中遇到和联系的人，以及在我们整个复原旅程中。",

    "p9-10": "当然，我们无法逃避作为人类状况一部分的环境和条件。我们已经尝试过——通过毒品和酒精，通过性和共依存，通过赌博和科技，通过工作和购物，通过食物或限制食物，通过执着和徒劳的试图控制我们的经验和感受——而我们在这里是因为它没有奏效。这是一个邀请我们认识和接受某些痛苦和失望将永远存在的计划，调查我们过去处理那种痛苦的不善巧方式，并培养对我们自己的痛苦、他人的痛苦以及我们造成的痛苦的理解、慈悲、宽恕和洞见的习惯。接纳伴随洞见和慈悲是创造从使我们的痛苦看起来难以忍受的痛苦中解脱的自由的原因。",

    "p9-11": "本书只是介绍一条可以带来从成瘾循环中解脱和自由的道路。我们计划的意图和希望是，道路上的每个人都将被赋予力量，使其成为自己的。",

    "p9-12": "愿你快乐。",

    "p9-13": "愿你安详。",

    "p9-14": "愿你脱离痛苦。",

    "p9-15": "愿一切众生脱离痛苦。"
}

def main():
    """Update JSON with Simplified Chinese translations for Chapter 9."""
    input_file = Path("/mnt/c/Users/scott/Documents/AIProjects/Markdown/ThaiTranslation/rdg_en_v3.json")

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create backup
    backup_file = input_file.with_name('rdg_en_v3.json.backup_before_simplified_chinese')
    print(f"Creating backup at {backup_file}...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Adding Simplified Chinese translations to Chapter 9...")

    # Find and update Chapter 9
    updated_count = 0
    for section in data['content']:
        if 'chapters' in section:
            for chapter in section['chapters']:
                if chapter.get('title') == 'WHAT IS RECOVERY DHARMA?':
                    # Add Simplified Chinese title
                    chapter['Chinese_Simplified_title'] = SIMPLIFIED_CHINESE_TITLE
                    print(f"✓ Updated chapter title")

                    # Update paragraphs
                    for sec in chapter.get('sections', []):
                        for content_item in sec.get('content', []):
                            if content_item.get('type') == 'paragraph':
                                para_id = content_item['id']
                                if para_id in SIMPLIFIED_CHINESE_PARAGRAPHS:
                                    content_item['Chinese_Simplified_text'] = SIMPLIFIED_CHINESE_PARAGRAPHS[para_id]
                                    updated_count += 1
                                    print(f"✓ Updated {para_id}")

    print(f"\nSaving updated JSON...")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Simplified Chinese translations added successfully!")
    print(f"   Updated: 1 title + {updated_count} paragraphs")
    print(f"   Backup saved at: {backup_file}")

if __name__ == "__main__":
    main()
