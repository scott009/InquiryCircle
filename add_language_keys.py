#!/usr/bin/env python3
"""
Add language keys to rdg_en_v3.json according to Stage 2.2 specifications.

This script adds empty keys for Vietnamese, Korean, Japanese, Traditional Chinese,
and Simplified Chinese to all chapters (titles) and paragraphs (text) throughout
the entire JSON document.
"""

import json
from collections import OrderedDict
from pathlib import Path

# Define the language keys in the correct order
TITLE_KEYS = [
    "thai_title",
    "vietnamese_title",
    "korean_title",
    "japanese_title",
    "Chinese_Tradition_title",
    "Chinese_Simplified_title"
]

TEXT_KEYS = [
    "thai_text",
    "vietnamese_text",
    "korean_text",
    "japanese_text",
    "Chinese_Tradition_text",
    "Chinese_Simplified_text"
]

def add_title_keys(chapter):
    """Add language title keys to a chapter in the correct order."""
    if "title" not in chapter:
        return chapter

    # Create new ordered dict with keys in correct order
    new_chapter = OrderedDict()

    # Add all existing keys first, except language title keys
    for key, value in chapter.items():
        if key not in TITLE_KEYS:
            new_chapter[key] = value

    # Add language title keys in correct order after "title"
    keys_list = list(new_chapter.keys())
    if "title" in keys_list:
        title_index = keys_list.index("title") + 1

        # Insert language title keys
        for lang_key in TITLE_KEYS:
            # Preserve existing value or set to empty string
            new_chapter[lang_key] = chapter.get(lang_key, "")

        # Now rebuild with correct order
        final_chapter = OrderedDict()
        for i, key in enumerate(keys_list):
            final_chapter[key] = new_chapter[key]
            # Insert language keys after "title"
            if key == "title":
                for lang_key in TITLE_KEYS:
                    final_chapter[lang_key] = new_chapter[lang_key]

        # Add any remaining keys
        for key in new_chapter:
            if key not in final_chapter and key not in keys_list:
                final_chapter[key] = new_chapter[key]

        return final_chapter

    return new_chapter

def add_text_keys(paragraph):
    """Add language text keys to a paragraph in the correct order."""
    if "text" not in paragraph:
        return paragraph

    # Create new ordered dict with keys in correct order
    new_para = OrderedDict()

    # Add all existing keys first, except language text keys
    for key, value in paragraph.items():
        if key not in TEXT_KEYS:
            new_para[key] = value

    # Add language text keys in correct order after "text"
    keys_list = list(new_para.keys())
    if "text" in keys_list:
        text_index = keys_list.index("text") + 1

        # Insert language text keys
        for lang_key in TEXT_KEYS:
            # Preserve existing value or set to empty string
            new_para[lang_key] = paragraph.get(lang_key, "")

        # Now rebuild with correct order
        final_para = OrderedDict()
        for i, key in enumerate(keys_list):
            final_para[key] = new_para[key]
            # Insert language keys after "text"
            if key == "text":
                for lang_key in TEXT_KEYS:
                    final_para[lang_key] = new_para[lang_key]

        # Add any remaining keys
        for key in new_para:
            if key not in final_para and key not in keys_list:
                final_para[key] = new_para[key]

        return final_para

    return new_para

def process_item(item):
    """Recursively process JSON items to add language keys."""
    if not isinstance(item, dict):
        return item

    # Check if this is a chapter (has "title" key and "type" == "chapter")
    if item.get("type") == "chapter" and "title" in item:
        item = add_title_keys(item)

    # Check if this is a paragraph (has "text" key and "type" == "paragraph")
    if item.get("type") == "paragraph" and "text" in item:
        item = add_text_keys(item)

    # Recursively process nested structures
    result = OrderedDict()
    for key, value in item.items():
        if isinstance(value, list):
            result[key] = [process_item(sub_item) for sub_item in value]
        elif isinstance(value, dict):
            result[key] = process_item(value)
        else:
            result[key] = value

    return result

def main():
    """Main function to process the JSON file."""
    input_file = Path("/mnt/c/Users/scott/Documents/AIProjects/Markdown/ThaiTranslation/rdg_en_v3.json")
    output_file = input_file  # Overwrite the original
    backup_file = input_file.with_suffix('.json.backup')

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    # Create backup
    print(f"Creating backup at {backup_file}...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Processing JSON structure...")
    # Process the content
    if 'content' in data:
        data['content'] = [process_item(item) for item in data['content']]

    print(f"Saving modified JSON to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ Language keys added successfully!")
    print(f"   Backup saved at: {backup_file}")

    # Verify the changes
    print("\nVerifying changes...")
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    counts = {
        'vietnamese_title': content.count('"vietnamese_title"'),
        'vietnamese_text': content.count('"vietnamese_text"'),
        'korean_title': content.count('"korean_title"'),
        'korean_text': content.count('"korean_text"'),
        'japanese_title': content.count('"japanese_title"'),
        'japanese_text': content.count('"japanese_text"'),
    }

    print("Key counts:")
    for key, count in counts.items():
        print(f"  {key}: {count}")

if __name__ == "__main__":
    main()
