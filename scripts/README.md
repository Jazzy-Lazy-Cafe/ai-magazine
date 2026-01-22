# Magazine JSON to HTML Converter

Convert structured JSON data into beautiful magazine-style Jekyll posts.

## Quick Start

### 1. Create Your Article JSON

Use `_data/magazine-template.json` as a starting point or see `_data/example-article.json` for a complete example.

```bash
cp _data/magazine-template.json _data/my-article.json
```

Edit `my-article.json` with your content.

### 2. Convert to HTML

```bash
python3 scripts/json_to_magazine.py _data/my-article.json _posts/2026-01-20-my-article.html
```

### 3. Build and Preview

```bash
bundle exec jekyll serve
```

Visit `http://localhost:4000/ai-magazine/` to see your article.

## JSON Structure

### Metadata
```json
{
  "metadata": {
    "layout": "magazine",
    "title": "Your Article Title",
    "description": "Brief description",
    "date": "YYYY-MM-DD"
  }
}
```

### Hero Types

**Split Screen Hero** (like Yejin Choi post):
```json
{
  "hero": {
    "type": "split",
    "header": {
      "logo_text": "Magazine",
      "logo_highlight": "Name",
      "episode_info": "Episode XX · Date"
    },
    "split": {
      "label": "CATEGORY",
      "title": "Main Title",
      "subtitle": "Subtitle text",
      "guest1": {
        "initials": "AB",
        "name": "Guest Name",
        "role": "Role"
      },
      "guest2": { ... },
      "visual_text": "AI"
    }
  }
}
```

**Fullscreen Hero** (like Bill & Sam post):
```json
{
  "hero": {
    "type": "fullscreen",
    "fullscreen": {
      "issue_tag": "Series · Episode",
      "title": "Main Title",
      "subtitle": "Subtitle",
      "quote_en": "English quote",
      "quote_ko": "한국어 번역"
    }
  }
}
```

### Sections

```json
{
  "sections": [
    {
      "number": "01",
      "title": "Section Title",
      "question": "What question does this answer?",
      "answer": "Your detailed answer here...",
      "layout": "normal",  // "normal", "reverse", or "full-width"
      "knowledge_items": [
        {
          "term_ko": "용어",
          "term_en": "Term",
          "description": "Explanation..."
        }
      ]
    }
  ]
}
```

**Layout Options:**
- `"normal"` - Sidebar on right
- `"reverse"` - Sidebar on left
- `"full-width"` - No sidebar

### Highlights

Insert highlight boxes between sections:

```json
{
  "highlights": [
    {
      "position": "after_section_2",
      "label": "Key Insight",
      "text": "Important quote or insight..."
    }
  ]
}
```

### Statistics

Add a statistics section:

```json
{
  "statistics": {
    "enabled": true,
    "position": "after_section_3",
    "stats": [
      {
        "number": "42",
        "label": "Important Metric"
      }
    ]
  }
}
```

### Bonus Section

```json
{
  "bonus_section": {
    "enabled": true,
    "title": "Bonus Content",
    "question": "Final question?",
    "answer": "Final thoughts...",
    "knowledge_items": []
  }
}
```

### Footer

```json
{
  "footer": {
    "quote": "Optional closing quote",
    "meta_text": "Publication · Episode · Date"
  }
}
```

## Advanced Usage

### Make Script Executable

```bash
chmod +x scripts/json_to_magazine.py
```

Then use it directly:

```bash
./scripts/json_to_magazine.py _data/my-article.json _posts/2026-01-20-my-article.html
```

### Batch Conversion

Convert multiple articles:

```bash
for file in _data/articles/*.json; do
    filename=$(basename "$file" .json)
    python3 scripts/json_to_magazine.py "$file" "_posts/2026-01-23-${filename}.html"
done
```

## Tips

### 1. HTML in Content
You can use HTML tags in your JSON content:

```json
{
  "answer": "This is <strong>bold</strong> and this has a <span class='highlight'>highlight</span>."
}
```

### 2. Line Breaks
Use `\\n\\n` for paragraph breaks in JSON:

```json
{
  "answer": "First paragraph.\\n\\nSecond paragraph."
}
```

### 3. Quotes
Escape quotes in your JSON content:

```json
{
  "text": "He said, \\\"This is amazing!\\\""
}
```

### 4. Special Characters
For Korean text, ensure your JSON file is saved with UTF-8 encoding.

### 5. Positioning Elements
- Highlights can be positioned after any section using `"position": "after_section_X"`
- Statistics section uses the same positioning system
- Multiple highlights can be added at different positions

## Validation

Before converting, validate your JSON:

```bash
python3 -m json.tool _data/my-article.json
```

If valid, it will print formatted JSON. If invalid, it will show the error.

## Examples

See `_data/example-article.json` for a complete, working example with:
- Split-screen hero
- 3 main sections with different layouts
- Knowledge items
- Highlight box
- Statistics section
- Bonus section
- Footer with quote

## Troubleshooting

**Script not found:**
```bash
cd /Users/gahee/WebstormProjects/ai-magazine
python3 scripts/json_to_magazine.py ...
```

**Invalid JSON:**
- Check for missing commas
- Check for unescaped quotes
- Use a JSON validator online

**Output looks wrong:**
- Run `bundle exec jekyll build` to regenerate
- Clear browser cache
- Check that `magazine.css` is properly linked

## Need Help?

Open an issue at the repository or refer to existing posts:
- `_posts/2023-11-16-unconfuse-me-yejin-choi.html` - Split hero example
- `_posts/2026-01-22-bill-and-sam.html` - Fullscreen hero example
