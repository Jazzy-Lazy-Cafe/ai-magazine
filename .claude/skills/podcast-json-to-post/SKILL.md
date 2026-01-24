---
name: podcast-json-to-post
description: 이중언어 JSON 파일을 언어 토글 기능이 있는 Jekyll 매거진 포스트 HTML로 변환합니다.
---

# Podcast JSON to Post

## 목적
`.claude/skills/podcast-summary/transcripts/json/` 폴더의 이중언어 JSON 파일을 Jekyll 매거진 포스트 형식의 HTML로 변환합니다. 생성된 HTML에는 영어/한국어 전환 버튼이 포함됩니다.

---

## 사용법

### 기본 사용
```
/podcast-json-to-post [파일명-bilingual.json]
```

### 예시
```
/podcast-json-to-post anthropic-ceo-summary-bilingual.json
```

**참고**: 이 스킬은 이중언어 JSON 파일 (`-bilingual.json`)을 처리합니다. 영문 단독 또는 한국어 단독 JSON은 지원하지 않습니다.

---

## 변환 절차

- 주의 : 이미 존재하는 파일이라면 기존 파일에 적힌 yyyy-MM-dd 를 **반드시** 그대로 따라야 합니다. 

### Step 1: 이중언어 JSON 파일 확인
1. JSON 파일 위치 확인:
   ```
   .claude/skills/podcast-summary/transcripts/json/[파일명]-bilingual.json
   ```

2. 필수 필드 존재 여부 확인:
   - `metadata.date` → 포스트 파일명에 사용
   - `metadata.title` (이중언어 구조: `{en: "...", ko: "..."}`)
   - `hero`, `opening_insight`, `sections`, `footer`

3. 이중언어 구조 확인:
   - 번역 가능 필드가 `{en: "...", ko: "..."}` 형식인지 확인
   - 예: `sections[0].question`이 객체인지 문자열인지 확인

### Step 2: 출력 파일명 결정
JSON의 `metadata.date`와 파일명을 조합하여 출력 파일명 생성:
```
_posts/[YYYY-MM-DD]-[slug].html
```

**예시**:
- 입력: `anthropic-ceo-summary.json` (date: 2025-01-22)
- 출력: `_posts/2025-01-22-anthropic-ceo-davos.html`

### Step 3: 이중언어 변환 스크립트 실행
```bash
python .claude/skills/podcast-summary/json_to_magazine_bilingual.py \
  .claude/skills/podcast-summary/transcripts/json/[입력파일]-bilingual.json \
  _posts/[출력파일].html
```

**주의**: 반드시 `json_to_magazine_bilingual.py` 스크립트를 사용해야 합니다. 기존 `json_to_magazine.py`는 이중언어 JSON을 처리할 수 없습니다.

### Step 4: 결과 확인
- 생성된 HTML 파일 확인
- 문자 수 확인 (보통 60,000-80,000자, 영어+한국어 포함)
- 언어 토글 버튼이 포함되어 있는지 확인
- 브라우저에서 열어 EN/KO 전환이 정상 작동하는지 테스트

---

## 언어 토글 기능

생성된 HTML에는 다음 기능이 포함됩니다:

### 토글 버튼
- 위치: 화면 우측 상단 고정
- 기능: EN/KO 버튼 클릭으로 언어 전환
- 디자인: 흰색 배경, 검은색 테두리, 활성 언어는 검은색 배경

### 동작 방식
- 모든 번역 가능 텍스트에 `bilingual-text` 클래스 적용
- 각 요소는 `data-en`과 `data-ko` 속성으로 양쪽 언어 저장
- JavaScript로 클릭 시 모든 텍스트를 선택 언어로 전환
- 사용자 선호도를 localStorage에 저장하여 재방문 시 유지

### 기본 언어
- 한국어(KO)로 시작
- 사용자가 이전에 선택한 언어가 있으면 자동으로 적용

---

## JSON 스키마 요구사항

### 필수 필드 (이중언어 구조)
```json
{
  "metadata": {
    "layout": "magazine",
    "title": {
      "en": "English Title",
      "ko": "한국어 제목"
    },
    "description": {
      "en": "English description",
      "ko": "한국어 설명"
    },
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
      "title": {
        "en": "Section Title",
        "ko": "섹션 제목"
      },
      "question": {
        "en": "Question in English?",
        "ko": "한국어 질문?"
      },
      "answer": {
        "en": "Answer in English...",
        "ko": "한국어 답변..."
      },
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

### 1. 새 이중언어 포스트 생성
```bash
# JSON 파일에서 날짜 확인
cat .claude/skills/podcast-summary/transcripts/json/example-bilingual.json | grep date

# 이중언어 변환 실행
python .claude/skills/podcast-summary/json_to_magazine_bilingual.py \
  .claude/skills/podcast-summary/transcripts/json/example-bilingual.json \
  _posts/2025-01-22-example-post.html
```

### 2. 기존 포스트 업데이트
이중언어 JSON 수정 후 동일한 출력 파일로 재실행하면 덮어쓰기됨:
```bash
python .claude/skills/podcast-summary/json_to_magazine_bilingual.py \
  .claude/skills/podcast-summary/transcripts/json/anthropic-ceo-summary-bilingual.json \
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
