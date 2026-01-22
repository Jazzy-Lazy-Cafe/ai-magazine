---
name: podcast-json-to-post
description: podcast-summary로 생성된 JSON 파일을 Jekyll 매거진 포스트 HTML로 변환합니다.
---

# Podcast JSON to Post

## 목적
`.claude/skills/podcast-summary/transcripts/json/` 폴더의 JSON 파일을 Jekyll 매거진 포스트 형식의 HTML로 변환합니다.

---

## 사용법

### 기본 사용
```
/podcast-json-to-post [파일명.json]
```

### 예시
```
/podcast-json-to-post anthropic-ceo-summary.json
```

---

## 변환 절차

### Step 1: JSON 파일 확인
1. JSON 파일 위치 확인:
   ```
   .claude/skills/podcast-summary/transcripts/json/[파일명].json
   ```

2. 필수 필드 존재 여부 확인:
   - `metadata.date` → 포스트 파일명에 사용
   - `metadata.title` → 포스트 제목
   - `hero`, `opening_insight`, `sections`, `footer`

### Step 2: 출력 파일명 결정
JSON의 `metadata.date`와 파일명을 조합하여 출력 파일명 생성:
```
_posts/[YYYY-MM-DD]-[slug].html
```

**예시**:
- 입력: `anthropic-ceo-summary.json` (date: 2025-01-22)
- 출력: `_posts/2025-01-22-anthropic-ceo-davos.html`

### Step 3: 변환 스크립트 실행
```bash
python .claude/skills/podcast-summary/json_to_magazine.py \
  .claude/skills/podcast-summary/transcripts/json/[입력파일].json \
  _posts/[출력파일].html
```

### Step 4: 결과 확인
- 생성된 HTML 파일 확인
- 문자 수 확인 (보통 15,000-25,000자)

---

## JSON 스키마 요구사항

### 필수 필드
```json
{
  "metadata": {
    "layout": "magazine",
    "title": "제목",
    "description": "설명",
    "date": "YYYY-MM-DD"
  },
  "hero": {
    "type": "split",
    "header": { "logo_text", "logo_highlight", "episode_info" },
    "split": { "label", "title", "subtitle", "guest1", "guest2", "visual_text" }
  },
  "opening_insight": {
    "label": "핵심 통찰",
    "text": "영문 인용",
    "translation": "한국어 번역"
  },
  "sections": [
    {
      "number": "01",
      "title": "섹션 제목",
      "question": "질문",
      "answer": "답변",
      "layout": "normal|reverse",
      "knowledge_items": [...]
    }
  ],
  "footer": {
    "quote": "마무리 인용문",
    "meta_text": "메타 정보"
  }
}
```

### 선택 필드
```json
{
  "hero.original_link": "원본 링크 URL",
  "interview_context": {
    "title": "인터뷰 배경",
    "content": "배경 설명 텍스트"
  },
  "highlights": [
    {
      "position": "after_section_N",
      "label": "라벨",
      "text": "영문",
      "translation": "한국어"
    }
  ],
  "statistics": {
    "enabled": true,
    "position": "after_section_N",
    "stats": [{ "number": "값", "label": "설명" }]
  },
  "bonus_section": {
    "enabled": true,
    "title": "제목",
    "question": "질문",
    "answer": "답변",
    "knowledge_items": [...]
  }
}
```

---

## 일반적인 워크플로우

### 1. 새 포스트 생성
```bash
# JSON 파일에서 날짜 확인
cat .claude/skills/podcast-summary/transcripts/json/example.json | grep date

# 변환 실행
python .claude/skills/podcast-summary/json_to_magazine.py \
  .claude/skills/podcast-summary/transcripts/json/example.json \
  _posts/2025-01-22-example-post.html
```

### 2. 기존 포스트 업데이트
JSON 수정 후 동일한 출력 파일로 재실행하면 덮어쓰기됨:
```bash
python .claude/skills/podcast-summary/json_to_magazine.py \
  .claude/skills/podcast-summary/transcripts/json/anthropic-ceo-summary.json \
  _posts/2026-01-21-anthropic-ceo-davos.html
```

---

## 오류 해결

### "string indices must be integers" 오류
`interview_context`가 문자열이 아닌 객체여야 함:
```json
// 잘못된 형식
"interview_context": "설명 텍스트"

// 올바른 형식
"interview_context": {
  "title": "인터뷰 배경",
  "content": "설명 텍스트"
}
```

### "Input file not found" 오류
파일 경로 확인:
```bash
ls .claude/skills/podcast-summary/transcripts/json/
```

### "Invalid JSON" 오류
JSON 문법 검증:
```bash
python -m json.tool .claude/skills/podcast-summary/transcripts/json/[파일명].json
```

---

## 관련 스킬
- `/podcast-summary`: 트랜스크립트에서 JSON 생성
- `/podcast-summary-review`: JSON 품질 검수
