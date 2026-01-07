#!/usr/bin/env python3
"""
Split rdg_en_v3.json into Thai-specific file with correction fields.

Keeps:
- English: text, title
- Thai: thai_text, thai_title
- Adds: corrected_thai_text, thai_status, thai_approved_by_id,
        thai_approved_by_name, thai_approved_at

Removes all other language fields.
"""

import json
import sys
from pathlib import Path

def process_paragraph(para):
    """Process a paragraph, keeping only English and Thai fields."""
    result = {
        "type": para.get("type"),
        "id": para.get("id"),
        "text": para.get("text", ""),
    }

    # Add Thai translation
    thai_text = para.get("thai_text", "")
    result["thai_text"] = thai_text

    # Add correction fields
    result["corrected_thai_text"] = thai_text  # Initially same as AI translation
    result["thai_status"] = "unchecked"
    result["thai_approved_by_id"] = None
    result["thai_approved_by_name"] = None
    result["thai_approved_at"] = None

    return result

def process_subsection(subsec):
    """Process a subsection."""
    result = {
        "type": subsec.get("type"),
        "id": subsec.get("id"),
        "heading": subsec.get("heading", ""),
    }

    # Process paragraphs
    if "content" in subsec:
        result["content"] = [process_paragraph(p) for p in subsec["content"]]

    return result

def process_section(sect):
    """Process a section."""
    result = {
        "type": sect.get("type"),
        "id": sect.get("id"),
        "heading": sect.get("heading", ""),
    }

    # Process content (subsections or paragraphs)
    if "content" in sect:
        processed_content = []
        for item in sect["content"]:
            if item.get("type") == "subsection":
                processed_content.append(process_subsection(item))
            elif item.get("type") == "paragraph":
                processed_content.append(process_paragraph(item))
        result["content"] = processed_content

    return result

def process_chapter(chapter):
    """Process a chapter, keeping only English and Thai titles."""
    result = {
        "type": chapter.get("type"),
        "id": chapter.get("id"),
        "status": chapter.get("status", "draft"),
        "title": chapter.get("title", ""),
        "thai_title": chapter.get("thai_title", ""),
    }

    # Process sections
    if "sections" in chapter:
        result["sections"] = [process_section(s) for s in chapter["sections"]]

    return result

def process_content_section(section):
    """Process a top-level content section."""
    result = {
        "type": section.get("type"),
        "id": section.get("id"),
        "status": section.get("status", "draft"),
        "title": section.get("title", ""),
    }

    # Process chapters
    if "chapters" in section:
        result["chapters"] = [process_chapter(ch) for ch in section["chapters"]]

    return result

def main():
    # Input and output paths
    input_path = Path("/mnt/c/Users/scott/Documents/AIProjects/Markdown/docs-websystems/projects/inquirycircle/SideMatters/Translation/rdg_en_v3.json")
    output_path = Path("/mnt/c/Users/scott/Documents/AIProjects/Markdown/docs-websystems/projects/inquirycircle/Documentation/rdg_thai.json")

    print(f"Reading {input_path}...")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    print("Processing JSON structure...")

    # Keep metadata, update for Thai
    result = {
        "metadata": {
            "title": data["metadata"]["title"],
            "edition": data["metadata"]["edition"],
            "source_file": data["metadata"]["source_file"],
            "extraction_date": data["metadata"]["extraction_date"],
            "extraction_method": data["metadata"]["extraction_method"],
            "license": data["metadata"]["license"],
            "json_version": "4.0-thai",
            "language": "thai",
            "note": "Thai translation with correction tracking fields"
        }
    }

    # Process content sections
    if "content" in data:
        result["content"] = [process_content_section(s) for s in data["content"]]

    print(f"Writing {output_path}...")

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)

    # Get file sizes
    input_size = input_path.stat().st_size / 1024  # KB
    output_size = output_path.stat().st_size / 1024  # KB

    print(f"\n✅ Success!")
    print(f"Input:  {input_size:.1f} KB")
    print(f"Output: {output_size:.1f} KB")
    print(f"Reduction: {((input_size - output_size) / input_size * 100):.1f}%")

if __name__ == "__main__":
    main()
