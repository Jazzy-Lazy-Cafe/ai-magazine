#!/usr/bin/env python3
"""
Convert JSON data to Jekyll magazine post format.

Usage:
    python scripts/json_to_magazine.py input.json output.html
"""

import json
import sys
from datetime import datetime


def escape_html(text):
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def generate_front_matter(metadata):
    """Generate Jekyll front matter."""
    return f"""---
layout: {metadata['layout']}
title: "{metadata['title']}"
description: "{metadata['description']}"
date: {metadata['date']}
---
"""


def generate_hero_split(hero_data):
    """Generate split-screen hero section."""
    header = hero_data['header']
    split = hero_data['split']

    # Handle optional original_link
    original_link = hero_data.get('original_link', '')
    original_link_param = f'\n   original_link="{original_link}"' if original_link else ''

    result = f"""
{{% include magazine/header.html
   logo_text="{header['logo_text']}"
   logo_highlight="{header['logo_highlight']}"
   episode_info="{header['episode_info']}" %}}

{{% include magazine/hero-split.html
   label="{split['label']}"
   title="{split['title']}"
   subtitle="{split['subtitle']}"
   guest1_initials="{split['guest1']['initials']}"
   guest1_name="{split['guest1']['name']}"
   guest1_role="{split['guest1']['role']}"
   guest2_initials="{split['guest2']['initials']}"
   guest2_name="{split['guest2']['name']}"
   guest2_role="{split['guest2']['role']}"
   visual_text="{split['visual_text']}"{original_link_param} %}}
"""
    return result


def generate_hero_fullscreen(hero_data):
    """Generate full-screen hero section."""
    fs = hero_data['fullscreen']

    result = f"""
{{% include magazine/hero-fullscreen.html
   issue_tag="{fs['issue_tag']}"
   title="{fs['title']}"
   subtitle="{fs['subtitle']}"
   quote_en="{fs['quote_en']}"
   quote_ko="{fs['quote_ko']}" %}}
"""
    return result


def generate_highlight(highlight_data):
    """Generate highlight/insight box."""
    translation = highlight_data.get('translation', '')
    translation_param = f'\n   translation="{translation}"' if translation else ''

    return f"""
{{% include magazine/highlight-box.html
   label="{highlight_data['label']}"
   text="{highlight_data['text']}"{translation_param} %}}
"""


def generate_knowledge_items(items):
    """Generate knowledge sidebar items HTML."""
    if not items:
        return ""

    result = """
            <aside class="sidebar-knowledge">
                <span class="sidebar-label">관련 배경지식</span>
"""

    for item in items:
        result += f"""                <div class="knowledge-item">
                    <h4 class="knowledge-term">{item['term_ko']} <span class="en">{item['term_en']}</span></h4>
                    <p class="knowledge-desc">{item['description']}</p>
                </div>
"""

    result += "            </aside>\n"
    return result


def generate_section(section):
    """Generate article section HTML."""
    layout_class = ""
    if section['layout'] == 'reverse':
        layout_class = " reverse"

    result = f"""
        <!-- SECTION {section['number']}: {section['title']} -->
        <article class="article-section{layout_class} fade-in">
            <div class="main-article">
                <span class="section-number">{section['number']}</span>
                <h2 class="section-title">{section['title']}</h2>
                <p class="question">{section['question']}</p>
                <div class="text-content">
                    <p class="answer">{section['answer']}</p>
                </div>
            </div>
"""

    if section['knowledge_items']:
        result += generate_knowledge_items(section['knowledge_items'])

    result += "        </article>\n"
    return result


def generate_statistics(stats_data):
    """Generate statistics section."""
    if not stats_data.get('enabled'):
        return ""

    result = """
        <!-- Statistics Section -->
        <section class="full-width-section">
"""

    for stat in stats_data['stats']:
        result += f"""            <div class="stat-card">
                <div class="stat-number">{stat['number']}</div>
                <div class="stat-label">{stat['label']}</div>
            </div>
"""

    result += "        </section>\n"
    return result


def generate_bonus_section(bonus_data):
    """Generate bonus section if enabled."""
    if not bonus_data.get('enabled'):
        return ""

    result = f"""
        <!-- BONUS SECTION -->
        <div class="section-divider">
            <span class="line"></span>
            <span class="icon">✦</span>
            <span class="line"></span>
        </div>

        <article class="article-section fade-in">
            <div class="main-article">
                <span class="section-number">+</span>
                <h2 class="section-title">{bonus_data['title']}</h2>
                <p class="question">{bonus_data['question']}</p>
                <div class="text-content single-column">
                    <p class="answer">{bonus_data['answer']}</p>
                </div>
            </div>
"""

    if bonus_data.get('knowledge_items'):
        result += generate_knowledge_items(bonus_data['knowledge_items'])

    result += "        </article>\n"
    return result


def generate_footer(footer_data):
    """Generate footer section."""
    quote_param = f'\n   quote="{footer_data["quote"]}"' if footer_data.get('quote') else ''

    return f"""
{{% include magazine/footer.html{quote_param}
   meta_text="{footer_data['meta_text']}" %}}
"""


def convert_json_to_html(json_data):
    """Convert JSON data to magazine HTML format."""
    html = generate_front_matter(json_data['metadata'])

    # Hero section - always use split
    html += generate_hero_split(json_data['hero'])

    # Opening insight
    if json_data.get('opening_insight'):
        html += generate_highlight(json_data['opening_insight'])

    # Main content grid
    html += "\n<!-- Main Content Grid -->\n<main class=\"magazine-grid\">\n"

    # Sections
    for i, section in enumerate(json_data['sections'], 1):
        html += generate_section(section)

        # Add highlights if positioned after this section
        for highlight in json_data.get('highlights', []):
            if highlight.get('position') == f'after_section_{i}':
                html += generate_highlight(highlight)

        # Add statistics if positioned after this section
        stats = json_data.get('statistics', {})
        if stats.get('position') == f'after_section_{i}':
            html += generate_statistics(stats)

    # Bonus section
    if json_data.get('bonus_section'):
        html += generate_bonus_section(json_data['bonus_section'])

    html += "\n</main>\n"

    # Footer
    html += generate_footer(json_data['footer'])

    return html


def main():
    if len(sys.argv) != 3:
        print("Usage: python json_to_magazine.py input.json output.html")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        html = convert_json_to_html(json_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ Successfully converted {input_file} to {output_file}")
        print(f"📄 Generated {len(html)} characters")

    except FileNotFoundError:
        print(f"❌ Error: Input file '{input_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{input_file}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
