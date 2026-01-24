#!/usr/bin/env python3
"""
Convert bilingual JSON data to Jekyll magazine post format with language toggle.

Usage:
    python json_to_magazine_bilingual.py input.json output.html
"""

import json
import sys
from datetime import datetime


def get_text(field, lang='ko'):
    """
    Extract text from field that can be either string or {en:..., ko:...} object.
    Defaults to Korean for bilingual content.
    """
    if isinstance(field, dict):
        return field.get(lang, field.get('en', ''))
    return field


def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ""
    return (str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def generate_bilingual_span(field, css_class=""):
    """Generate bilingual span with both languages."""
    if isinstance(field, dict):
        en = field.get('en', '')
        ko = field.get('ko', '')
        class_attr = f' class="{css_class}"' if css_class else ''
        return f'<span{class_attr} data-en="{escape_html(en)}" data-ko="{escape_html(ko)}">{ko}</span>'
    return field


def generate_front_matter(metadata):
    """Generate Jekyll front matter."""
    title = get_text(metadata['title'])
    description = get_text(metadata['description'])

    return f"""---
layout: {metadata['layout']}
title: "{title}"
description: "{description}"
date: {metadata['date']}
---
"""


def generate_language_toggle():
    """Generate language toggle button."""
    return """
<!-- Language Toggle -->
<div class="language-toggle">
    <button id="lang-toggle" class="lang-toggle-btn" aria-label="Toggle language">
        <span class="lang-option lang-en">EN</span>
        <span class="lang-option lang-ko active">KO</span>
    </button>
</div>
"""


def generate_hero_split(hero_data):
    """Generate split-screen hero section with bilingual support."""
    header = hero_data['header']
    split = hero_data['split']

    title = get_text(split['title'])
    subtitle = get_text(split['subtitle'])

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
   title="{title}"
   subtitle="{subtitle}"
   guest1_initials="{split['guest1']['initials']}"
   guest1_name="{split['guest1']['name']}"
   guest1_role="{split['guest1']['role']}"
   guest2_initials="{split['guest2']['initials']}"
   guest2_name="{split['guest2']['name']}"
   guest2_role="{split['guest2']['role']}"
   visual_text="{split['visual_text']}"{original_link_param} %}}
"""
    return result


def generate_highlight(highlight_data):
    """Generate highlight/insight box with bilingual support."""
    label = get_text(highlight_data['label'])

    # For opening_insight, use text (EN) and translation (KO)
    if 'translation' in highlight_data:
        text_en = highlight_data['text']
        text_ko = highlight_data['translation']

        return f"""
{{% include magazine/highlight-box.html
   label="{label}"
   text="{text_en}"
   translation="{text_ko}" %}}
"""

    # For other highlights
    text = get_text(highlight_data['text'])
    translation = get_text(highlight_data.get('translation', ''))
    translation_param = f'\n   translation="{translation}"' if translation else ''

    return f"""
{{% include magazine/highlight-box.html
   label="{label}"
   text="{text}"{translation_param} %}}
"""


def generate_interview_context(context_data):
    """Generate interview context/background section with bilingual support."""
    if not context_data:
        return ""

    title = get_text(context_data['title'])
    content_en = get_text(context_data['content'], 'en')
    content_ko = get_text(context_data['content'], 'ko')

    return f"""
<!-- Interview Context -->
<section class="interview-context fade-in">
    <h3 class="context-title">{title}</h3>
    <p class="context-content bilingual-text" data-en="{escape_html(content_en)}" data-ko="{escape_html(content_ko)}">{content_ko}</p>
</section>
"""


def generate_knowledge_items(items):
    """Generate knowledge sidebar items HTML with bilingual support."""
    if not items:
        return ""

    result = """
            <aside class="sidebar-knowledge">
                <span class="sidebar-label">관련 배경지식</span>
"""

    for item in items:
        desc_en = get_text(item['description'], 'en')
        desc_ko = get_text(item['description'], 'ko')

        result += f"""                <div class="knowledge-item">
                    <h4 class="knowledge-term">{item['term_ko']} <span class="en">{item['term_en']}</span></h4>
                    <p class="knowledge-desc bilingual-text" data-en="{escape_html(desc_en)}" data-ko="{escape_html(desc_ko)}">{desc_ko}</p>
                </div>
"""

    result += "            </aside>\n"
    return result


def generate_section(section):
    """Generate article section HTML with bilingual support."""
    layout_class = ""
    if section['layout'] == 'reverse':
        layout_class = " reverse"

    title = get_text(section['title'])
    question_en = get_text(section['question'], 'en')
    question_ko = get_text(section['question'], 'ko')
    answer_en = get_text(section['answer'], 'en')
    answer_ko = get_text(section['answer'], 'ko')

    # Handle optional follow-up question and answer
    follow_up_html = ""
    if section.get('follow_up_question'):
        fq_en = get_text(section['follow_up_question'], 'en')
        fq_ko = get_text(section['follow_up_question'], 'ko')
        fa_en = get_text(section.get('follow_up_answer', ''), 'en')
        fa_ko = get_text(section.get('follow_up_answer', ''), 'ko')

        follow_up_html = f'''<p class="follow-up-question bilingual-text" data-en="{escape_html(fq_en)}" data-ko="{escape_html(fq_ko)}">{fq_ko}</p>'''
        if section.get('follow_up_answer'):
            follow_up_html += f'''\n                <div class="follow-up-content">\n                    <p class="follow-up-answer bilingual-text" data-en="{escape_html(fa_en)}" data-ko="{escape_html(fa_ko)}">{fa_ko}</p>\n                </div>'''

    result = f"""
        <!-- SECTION {section['number']}: {title} -->
        <article class="article-section{layout_class} fade-in">
            <div class="main-article">
                <span class="section-number">{section['number']}</span>
                <h2 class="section-title bilingual-text" data-en="{escape_html(get_text(section['title'], 'en'))}" data-ko="{escape_html(get_text(section['title'], 'ko'))}">{title}</h2>
                <p class="question bilingual-text" data-en="{escape_html(question_en)}" data-ko="{escape_html(question_ko)}">{question_ko}</p>
                <div class="text-content">
                    <p class="answer bilingual-text" data-en="{escape_html(answer_en)}" data-ko="{escape_html(answer_ko)}">{answer_ko}</p>
                </div>
                {follow_up_html}
            </div>
"""

    if section['knowledge_items']:
        result += generate_knowledge_items(section['knowledge_items'])

    result += "        </article>\n"
    return result


def generate_statistics(stats_data):
    """Generate statistics section with bilingual support."""
    if not stats_data.get('enabled'):
        return ""

    result = """
        <!-- Statistics Section -->
        <section class="full-width-section">
"""

    for stat in stats_data['stats']:
        label_en = get_text(stat['label'], 'en')
        label_ko = get_text(stat['label'], 'ko')

        result += f"""            <div class="stat-card">
                <div class="stat-number">{stat['number']}</div>
                <div class="stat-label bilingual-text" data-en="{escape_html(label_en)}" data-ko="{escape_html(label_ko)}">{label_ko}</div>
            </div>
"""

    result += "        </section>\n"
    return result


def generate_bonus_section(bonus_data):
    """Generate bonus section if enabled with bilingual support."""
    if not bonus_data.get('enabled'):
        return ""

    title = get_text(bonus_data['title'])
    question_en = get_text(bonus_data['question'], 'en')
    question_ko = get_text(bonus_data['question'], 'ko')
    answer_en = get_text(bonus_data['answer'], 'en')
    answer_ko = get_text(bonus_data['answer'], 'ko')

    # Handle optional follow-up question and answer
    follow_up_html = ""
    if bonus_data.get('follow_up_question'):
        fq_en = get_text(bonus_data['follow_up_question'], 'en')
        fq_ko = get_text(bonus_data['follow_up_question'], 'ko')

        follow_up_html = f'<p class="follow-up-question bilingual-text" data-en="{escape_html(fq_en)}" data-ko="{escape_html(fq_ko)}">{fq_ko}</p>'

        if bonus_data.get('follow_up_answer'):
            fa_en = get_text(bonus_data['follow_up_answer'], 'en')
            fa_ko = get_text(bonus_data['follow_up_answer'], 'ko')
            follow_up_html += f'\n                <div class="follow-up-content">\n                    <p class="follow-up-answer bilingual-text" data-en="{escape_html(fa_en)}" data-ko="{escape_html(fa_ko)}">{fa_ko}</p>\n                </div>'

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
                <h2 class="section-title bilingual-text" data-en="{escape_html(get_text(bonus_data['title'], 'en'))}" data-ko="{escape_html(get_text(bonus_data['title'], 'ko'))}">{title}</h2>
                <p class="question bilingual-text" data-en="{escape_html(question_en)}" data-ko="{escape_html(question_ko)}">{question_ko}</p>
                <div class="text-content single-column">
                    <p class="answer bilingual-text" data-en="{escape_html(answer_en)}" data-ko="{escape_html(answer_ko)}">{answer_ko}</p>
                </div>
                {follow_up_html}
            </div>
"""

    if bonus_data.get('knowledge_items'):
        result += generate_knowledge_items(bonus_data['knowledge_items'])

    result += "        </article>\n"
    return result


def generate_footer(footer_data):
    """Generate footer section with bilingual support."""
    quote_en = get_text(footer_data.get('quote', ''), 'en')
    quote_ko = get_text(footer_data.get('quote', ''), 'ko')

    quote_param = ''
    if quote_ko:
        # Footer include doesn't support bilingual yet, use Korean by default
        quote_param = f'\n   quote="{quote_ko}"'

    return f"""
{{% include magazine/footer.html{quote_param}
   meta_text="{footer_data['meta_text']}" %}}
"""


def generate_language_toggle_script():
    """Generate JavaScript for language toggle functionality."""
    return """
<!-- Language Toggle Script -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('lang-toggle');
    const langOptions = toggleBtn.querySelectorAll('.lang-option');
    let currentLang = 'ko'; // Default language

    toggleBtn.addEventListener('click', function() {
        // Toggle language
        currentLang = currentLang === 'ko' ? 'en' : 'ko';

        // Update toggle button visual
        langOptions.forEach(option => {
            if (option.classList.contains(`lang-${currentLang}`)) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });

        // Update all bilingual text elements
        document.querySelectorAll('.bilingual-text').forEach(element => {
            const text = element.getAttribute(`data-${currentLang}`);
            if (text) {
                element.textContent = text;
            }
        });

        // Save preference
        localStorage.setItem('preferredLanguage', currentLang);
    });

    // Load saved language preference
    const savedLang = localStorage.getItem('preferredLanguage');
    if (savedLang && savedLang !== currentLang) {
        toggleBtn.click();
    }
});
</script>

<style>
.language-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
}

.lang-toggle-btn {
    display: flex;
    gap: 2px;
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid #000;
    border-radius: 20px;
    padding: 4px;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.lang-toggle-btn:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.lang-option {
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
    border-radius: 16px;
    transition: all 0.3s ease;
    color: #666;
}

.lang-option.active {
    background: #000;
    color: #fff;
}

/* Make bilingual text transition smoothly */
.bilingual-text {
    transition: opacity 0.2s ease;
}
</style>
"""


def convert_json_to_html(json_data):
    """Convert bilingual JSON data to magazine HTML format."""
    html = generate_front_matter(json_data['metadata'])

    # Language toggle
    html += generate_language_toggle()

    # Hero section
    html += generate_hero_split(json_data['hero'])

    # Opening insight
    if json_data.get('opening_insight'):
        html += generate_highlight(json_data['opening_insight'])

    # Interview context
    if json_data.get('interview_context'):
        html += generate_interview_context(json_data['interview_context'])

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

    # Language toggle script
    html += generate_language_toggle_script()

    return html


def main():
    if len(sys.argv) != 3:
        print("Usage: python json_to_magazine_bilingual.py input.json output.html")
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
        print(f"🌐 Bilingual content with language toggle enabled")

    except FileNotFoundError:
        print(f"❌ Error: Input file '{input_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{input_file}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
