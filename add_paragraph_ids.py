#!/usr/bin/env python3
"""
Add paragraph IDs to Recovery Dharma JSON file.
Format: p{chapter_id}-{sequence}
"""

import json
import sys
from pathlib import Path


def add_paragraph_ids(data, renumber=False):
    """
    Add or renumber paragraph IDs in the JSON structure.

    Args:
        data: The JSON data structure
        renumber: If True, renumber all paragraphs even if they have IDs

    Returns:
        Modified data structure with paragraph IDs added
    """
    if 'content' not in data:
        return data

    # Iterate through sections
    for section in data['content']:
        if section.get('type') == 'section' and 'chapters' in section:
            # Iterate through chapters
            for chapter in section['chapters']:
                if chapter.get('type') == 'chapter':
                    chapter_id = str(chapter.get('id', 'unknown'))

                    # Process paragraphs in this chapter
                    process_chapter_paragraphs(chapter, chapter_id, renumber)

    return data


def process_chapter_paragraphs(chapter, chapter_id, renumber):
    """
    Recursively process all paragraphs in a chapter and add IDs.

    Args:
        chapter: Chapter object
        chapter_id: The chapter ID to use in paragraph IDs
        renumber: If True, renumber all paragraphs
    """
    para_sequence = [1]  # Use list to maintain reference across recursive calls

    def process_content(content_list):
        """Recursively process content arrays."""
        for item in content_list:
            if isinstance(item, dict):
                # If it's a paragraph, add/update ID
                if item.get('type') == 'paragraph':
                    if renumber or 'id' not in item:
                        item['id'] = f"p{chapter_id}-{para_sequence[0]}"
                        para_sequence[0] += 1

                # Recursively process nested content
                if 'content' in item and isinstance(item['content'], list):
                    process_content(item['content'])

                # Also check sections array
                if 'sections' in item and isinstance(item['sections'], list):
                    process_content(item['sections'])

    # Start processing from chapter's sections
    if 'sections' in chapter and isinstance(chapter['sections'], list):
        process_content(chapter['sections'])


def main():
    """Main function to add paragraph IDs to JSON file."""
    if len(sys.argv) < 2:
        print("Usage: python3 add_paragraph_ids.py <input_json_file> [--renumber]")
        print("  --renumber: Renumber all paragraphs (default: only add missing IDs)")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    renumber = '--renumber' in sys.argv

    if not input_file.exists():
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    # Read JSON file
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Add paragraph IDs
    action = "Renumbering" if renumber else "Adding"
    print(f"{action} paragraph IDs...")
    data = add_paragraph_ids(data, renumber)

    # Create output filename
    output_file = input_file.parent / f"{input_file.stem}_with_ids{input_file.suffix}"

    # Write output
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Done!")
    print(f"Output saved to: {output_file}")


if __name__ == '__main__':
    main()
