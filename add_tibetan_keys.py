#!/usr/bin/env python3
"""
Add tibetan_title and tibetan_text keys throughout rdg_en_v3.json
"""

import json
from collections import OrderedDict
from pathlib import Path

def add_tibetan_keys_to_chapter(chapter):
    """Add tibetan_title key to a chapter after Chinese_Simplified_title."""
    if "title" not in chapter:
        return chapter

    # Create new ordered dict with correct key order
    new_chapter = OrderedDict()

    for key, value in chapter.items():
        new_chapter[key] = value
        # Insert tibetan_title after Chinese_Simplified_title
        if key == "Chinese_Simplified_title":
            new_chapter["tibetan_title"] = chapter.get("tibetan_title", "")

    return new_chapter

def add_tibetan_keys_to_paragraph(paragraph):
    """Add tibetan_text key to a paragraph after Chinese_Simplified_text."""
    if "text" not in paragraph:
        return paragraph

    # Create new ordered dict with correct key order
    new_para = OrderedDict()

    for key, value in paragraph.items():
        new_para[key] = value
        # Insert tibetan_text after Chinese_Simplified_text
        if key == "Chinese_Simplified_text":
            new_para["tibetan_text"] = paragraph.get("tibetan_text", "")

    return new_para

def process_item(item):
    """Recursively process JSON items to add Tibetan keys."""
    if not isinstance(item, dict):
        return item

    # Check if this is a chapter
    if item.get("type") == "chapter" and "title" in item:
        item = add_tibetan_keys_to_chapter(item)

    # Check if this is a paragraph
    if item.get("type") == "paragraph" and "text" in item:
        item = add_tibetan_keys_to_paragraph(item)

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
    """Add Tibetan keys throughout the JSON file."""
    input_file = Path("/mnt/c/Users/scott/Documents/AIProjects/Markdown/ThaiTranslation/rdg_en_v3.json")
    output_file = input_file
    backup_file = input_file.with_name('rdg_en_v3.json.backup_before_tibetan_keys')

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    # Create backup
    print(f"Creating backup at {backup_file}...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Adding Tibetan keys to JSON structure...")

    # Process the content
    if 'content' in data:
        data['content'] = [process_item(item) for item in data['content']]

    print(f"Saving modified JSON to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ Tibetan keys added successfully!")

    # Verify the changes
    print("\nVerifying changes...")
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    counts = {
        'tibetan_title': content.count('"tibetan_title"'),
        'tibetan_text': content.count('"tibetan_text"'),
    }

    print("Key counts:")
    for key, count in counts.items():
        print(f"  {key}: {count}")

if __name__ == "__main__":
    main()
