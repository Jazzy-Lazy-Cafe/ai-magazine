#!/usr/bin/env python3
"""
Merge English and Korean JSON files into a single bilingual JSON.

Usage:
    python merge_bilingual_json.py english.json korean.json output.json
"""

import json
import sys


def merge_bilingual(en_data, ko_data):
    """Merge English and Korean JSON data into bilingual format."""

    bilingual = {
        "metadata": {
            "layout": en_data["metadata"]["layout"],
            "title": {
                "en": en_data["metadata"]["title"],
                "ko": ko_data["metadata"]["title"]
            },
            "description": {
                "en": en_data["metadata"]["description"],
                "ko": ko_data["metadata"]["description"]
            },
            "date": en_data["metadata"]["date"]
        },
        "hero": {
            "type": en_data["hero"]["type"],
            "original_link": en_data["hero"].get("original_link", ""),
            "header": en_data["hero"]["header"],
            "split": {
                "label": en_data["hero"]["split"]["label"],
                "title": {
                    "en": en_data["hero"]["split"]["title"],
                    "ko": ko_data["hero"]["split"]["title"]
                },
                "subtitle": {
                    "en": en_data["hero"]["split"]["subtitle"],
                    "ko": ko_data["hero"]["split"]["subtitle"]
                },
                "guest1": en_data["hero"]["split"]["guest1"],
                "guest2": en_data["hero"]["split"]["guest2"],
                "visual_text": en_data["hero"]["split"]["visual_text"]
            },
            "fullscreen": en_data["hero"]["fullscreen"]
        },
        "opening_insight": {
            "label": {
                "en": en_data["opening_insight"]["label"],
                "ko": ko_data["opening_insight"]["label"]
            },
            "text": en_data["opening_insight"]["text"],
            "translation": ko_data["opening_insight"]["translation"]
        },
        "interview_context": {
            "title": {
                "en": en_data["interview_context"]["title"],
                "ko": ko_data["interview_context"]["title"]
            },
            "content": {
                "en": en_data["interview_context"]["content"],
                "ko": ko_data["interview_context"]["content"]
            }
        },
        "sections": []
    }

    # Merge sections
    for en_sec, ko_sec in zip(en_data["sections"], ko_data["sections"]):
        section = {
            "number": en_sec["number"],
            "title": {
                "en": en_sec["title"],
                "ko": ko_sec["title"]
            },
            "question": {
                "en": en_sec["question"],
                "ko": ko_sec["question"]
            },
            "answer": {
                "en": en_sec["answer"],
                "ko": ko_sec["answer"]
            },
            "layout": en_sec["layout"],
            "knowledge_items": []
        }

        # Add follow-up if exists
        if en_sec.get("follow_up_question"):
            section["follow_up_question"] = {
                "en": en_sec["follow_up_question"],
                "ko": ko_sec["follow_up_question"]
            }
            section["follow_up_answer"] = {
                "en": en_sec["follow_up_answer"],
                "ko": ko_sec["follow_up_answer"]
            }

        # Merge knowledge items
        for en_ki, ko_ki in zip(en_sec["knowledge_items"], ko_sec["knowledge_items"]):
            section["knowledge_items"].append({
                "term_ko": en_ki["term_ko"],
                "term_en": en_ki["term_en"],
                "description": {
                    "en": en_ki["description"],
                    "ko": ko_ki["description"]
                }
            })

        bilingual["sections"].append(section)

    # Merge highlights
    bilingual["highlights"] = []
    for en_hl, ko_hl in zip(en_data.get("highlights", []), ko_data.get("highlights", [])):
        bilingual["highlights"].append({
            "position": en_hl["position"],
            "label": {
                "en": en_hl["label"],
                "ko": ko_hl["label"]
            },
            "text": en_hl["text"],
            "translation": ko_hl["translation"]
        })

    # Merge statistics
    if en_data.get("statistics", {}).get("enabled"):
        bilingual["statistics"] = {
            "enabled": True,
            "position": en_data["statistics"]["position"],
            "stats": []
        }
        for en_stat, ko_stat in zip(en_data["statistics"]["stats"], ko_data["statistics"]["stats"]):
            bilingual["statistics"]["stats"].append({
                "number": en_stat["number"],
                "label": {
                    "en": en_stat["label"],
                    "ko": ko_stat["label"]
                }
            })

    # Merge bonus section
    if en_data.get("bonus_section", {}).get("enabled"):
        en_bonus = en_data["bonus_section"]
        ko_bonus = ko_data["bonus_section"]

        bilingual["bonus_section"] = {
            "enabled": True,
            "title": {
                "en": en_bonus["title"],
                "ko": ko_bonus["title"]
            },
            "question": {
                "en": en_bonus["question"],
                "ko": ko_bonus["question"]
            },
            "answer": {
                "en": en_bonus["answer"],
                "ko": ko_bonus["answer"]
            },
            "knowledge_items": []
        }

        for en_ki, ko_ki in zip(en_bonus.get("knowledge_items", []), ko_bonus.get("knowledge_items", [])):
            bilingual["bonus_section"]["knowledge_items"].append({
                "term_ko": en_ki["term_ko"],
                "term_en": en_ki["term_en"],
                "description": {
                    "en": en_ki["description"],
                    "ko": ko_ki["description"]
                }
            })

    # Merge footer
    bilingual["footer"] = {
        "quote": {
            "en": en_data["footer"]["quote"],
            "ko": ko_data["footer"]["quote"]
        },
        "meta_text": en_data["footer"]["meta_text"]
    }

    return bilingual


def main():
    if len(sys.argv) != 4:
        print("Usage: python merge_bilingual_json.py english.json korean.json output.json")
        sys.exit(1)

    en_file = sys.argv[1]
    ko_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        with open(en_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)

        with open(ko_file, 'r', encoding='utf-8') as f:
            ko_data = json.load(f)

        bilingual = merge_bilingual(en_data, ko_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(bilingual, f, ensure_ascii=False, indent=2)

        print(f"✅ Successfully merged {en_file} + {ko_file} → {output_file}")
        print(f"📄 Generated bilingual JSON with {len(bilingual['sections'])} sections")

    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
