---
name: podcast-summary-translator
description: podcast-summary로 생성된 영문 JSON 파일을 자연스러운 한국어로 번역하여 -bilingual.json 파일을 생성합니다.
---

## 이 파일의 목적

**이 파일은 Claude가 번역 작업을 실행할 때 따라야 할 기술적 워크플로우를 정의합니다.**

- 어떤 파일을 읽고 어떤 형식으로 출력할지 (JSON 구조)
- 어떤 순서로 작업을 진행할지 (Step 1-6)
- 어떤 품질 기준을 확인할지 (체크리스트)

**번역 품질 향상 방법**은 [translation-prompting-guide.md](./translation-prompting-guide.md)를 참조하세요.

---

## 목적
영문 Q&A JSON을 자연스러운 한국어로 번역하여 이중언어 JSON을 생성합니다.

## 입력
- 위치: `.claude/skills/podcast-summary/transcripts/json/*.json`
- 파일명 지정 또는 최신 파일 자동 선택

## 출력
- `[원본파일명]-bilingual.json` 형식으로 동일 디렉토리에 저장
- 예: `anthropic-ceo-summary.json` → `anthropic-ceo-summary-bilingual.json`
- 영어 원문과 한국어 번역을 모두 포함한 이중언어 JSON 구조

## 번역 워크플로우

### Step 1: 파일 선택 및 검증
1. 사용자가 파일명 제공 시 해당 파일 사용
2. 미제공 시 가장 최근 .json 파일 사용 (-ko.json 제외)
3. JSON 유효성 검증

### Step 2: 언어 감지
1. `sections[0].question`에서 한글 또는 이중언어 구조 감지
2. 한국어 또는 이중언어 감지 시: 경고 및 재번역 확인
3. 영어 감지 시: 번역 진행

### Step 3: 번역 준비
1. natural-korean-guide.md 로드 (100가지 패턴)
2. 번역 원칙 설정:
   - 동사 중심 표현 사용
   - 능동태 선호
   - 자연스러운 한국어 관용 표현
   - 구체적 예시 유지

### Step 4: 이중언어 JSON 생성

영문 JSON을 읽어서 이중언어 구조로 변환합니다. 번역 가능한 모든 필드를 `{en: "...", ko: "..."}` 구조로 변환합니다.

**이중언어 구조로 변환할 필드**:
- `metadata.title` → `{en: "원문", ko: "번역"}`
- `metadata.description` → `{en: "원문", ko: "번역"}`
- `hero.split.title` → `{en: "원문", ko: "번역"}`
- `hero.split.subtitle` → `{en: "원문", ko: "번역"}`
- `opening_insight.label` → `{en: "원문", ko: "번역"}`
- `opening_insight.text` → 원문 유지 (영어)
- `opening_insight.translation` → 번역 제공 (한국어)
- `interview_context.title` → `{en: "원문", ko: "번역"}`
- `interview_context.content` → `{en: "원문", ko: "번역"}`
- `sections[].title` → `{en: "원문", ko: "번역"}`
- `sections[].question` → `{en: "원문", ko: "번역"}`
- `sections[].answer` → `{en: "원문", ko: "번역"}`
- `sections[].follow_up_question` → `{en: "원문", ko: "번역"}`
- `sections[].follow_up_answer` → `{en: "원문", ko: "번역"}`
- `sections[].knowledge_items[].description` → `{en: "원문", ko: "번역"}`
- `highlights[].label` → `{en: "원문", ko: "번역"}`
- `highlights[].text` → 원문 유지 (영어)
- `highlights[].translation` → 번역 제공 (한국어)
- `statistics.stats[].label` → `{en: "원문", ko: "번역"}`
- `bonus_section.*` (모든 텍스트 필드) → `{en: "원문", ko: "번역"}`
- `footer.quote` → `{en: "원문", ko: "번역"}`

**보존 필드 (변환 안 함)**:
- 날짜, 숫자, 에피소드 정보
- 레이아웃 사양 (`layout`, `type`, `position` 등)
- 용어명 (`term_en`, `term_ko`)
- 게스트 정보 (`guest1`, `guest2`)

**출력 JSON 구조 예시**:
```json
{
  "metadata": {
    "title": {
      "en": "Jensen Huang: Building the AI Revolution",
      "ko": "Jensen Huang: AI 혁명을 일으키다"
    }
  },
  "sections": [
    {
      "question": {
        "en": "How did your early experiences shape NVIDIA?",
        "ko": "초기 경험이 NVIDIA에 어떤 영향을 주었나요?"
      },
      "answer": {
        "en": "My mother taught me English...",
        "ko": "어머니는 영어를 못하시지만..."
      }
    }
  ]
}
```

### Step 5: 번역 품질 검수

**A. 번역 완결성 확인 (최우선)**
1. **문장 누락 검증**: 원문의 모든 주절이 번역에 포함되었는지 확인
2. **대시(—), 세미콜론(;) 처리**: 앞뒤 내용 모두 번역되었는지 확인
3. **복합 문장 분리**: 긴 문장은 2-3개로 나누어 자연스럽게 번역

**B. 번역투 제거 확인**
- [natural-korean-guide.md](../podcast-summary-review/natural-korean-guide.md)의 120가지 패턴 준수 여부 확인
- 주요 확인 항목:
  - 명사형 과다 사용 (예: "~하는 것")
  - 수동태 표현 (예: "~에 의해")
  - 메타 발화 직역 (예: "~라고 말하는 건")
  - 정치 표현 직역 (예: "정치적으로 코딩된")

상세 패턴은 natural-korean-guide.md 참조

### Step 6: 출력 생성
1. `-bilingual.json` 파일 저장
2. JSON 구조 검증 (모든 번역 가능 필드가 `{en: "...", ko: "..."}` 구조인지 확인)
3. 번역 요약 리포트 (변환된 필드 수, 파일 크기 등)

## 번역 품질 원칙

1. **완결성**: 원문의 모든 문장 번역 (최우선)
2. **의미 보존**: 핵심 의미와 뉘앙스 유지
3. **자연스러움**: 번역투 제거, 원어민 수준 표현
4. **전문용어**: 영문 유지 또는 병기 (예: "Scaling Laws (스케일링 법칙)")

번역 기법 및 프롬프팅 전략은 [translation-prompting-guide.md](./translation-prompting-guide.md) 참조

## 사용 예시

### 특정 파일 번역
```
/podcast-summary-translator anthropic-ceo-summary.json
```

### 최신 파일 번역
```
/podcast-summary-translator
```

### 강제 재번역
```
/podcast-summary-translator --force anthropic-ceo-summary.json
```

## 오류 처리

- **파일 없음**: 사용 가능한 파일 목록 표시
- **이미 한국어**: 경고 후 사용자 확인 요청
- **잘못된 JSON**: 구체적 오류 위치 표시

## 워크플로우 통합

```
Transcript → /podcast-summary → English JSON
                ↓
           /podcast-summary-translator → Bilingual JSON (-bilingual.json)
                ↓
           /podcast-summary-review → Quality Report
                ↓
           /podcast-json-to-post → Bilingual Jekyll HTML (language toggle)
```

## 관련 문서
- [natural-korean-guide.md](../podcast-summary-review/natural-korean-guide.md): 100가지 자연스러운 한국어 패턴
- [quality-checklist.md](../podcast-summary-review/quality-checklist.md): 품질 기준
- [magazine-template.json](../podcast-summary/magazine-template.json): JSON 구조 참조

## 번역 실행 지침

Claude에게 이 스킬을 실행할 때:

1. **파일 선택**:
   - 사용자가 파일명을 제공하면 해당 파일 사용
   - 제공하지 않으면 `.claude/skills/podcast-summary/transcripts/json/` 디렉토리에서 가장 최근 `-ko.json`이 아닌 `.json` 파일 선택

2. **언어 감지**:
   - JSON 파일의 `sections[0].question` 필드를 읽어 한글 또는 이중언어 구조 포함 여부 확인
   - 한글이나 `{en: "...", ko: "..."}` 구조가 있으면 "이미 번역된 것 같습니다. 재번역하시겠습니까?" 경고
   - `--force` 플래그가 있으면 경고 없이 진행

3. **번역 준비**:
   - `.claude/skills/podcast-summary-review/natural-korean-guide.md` 파일을 읽어 100가지 자연스러운 한국어 패턴 로드
   - 번역 시 이 패턴들을 체계적으로 적용

4. **이중언어 JSON 생성**:
   - 영문 JSON을 읽어서 모든 번역 가능 필드를 `{en: "원문", ko: "번역"}` 구조로 변환
   - 위의 "이중언어 구조로 변환할 필드" 섹션에 명시된 필드 변환
   - "보존 필드" 섹션의 필드는 그대로 유지
   - 번역 시 5가지 번역투 제거 패턴을 체계적으로 적용
   - 영어 원문은 `en` 키에, 한국어 번역은 `ko` 키에 저장

5. **품질 검증**:
   - **[최우선] 번역 완결성 검증**: Step 5-A 체크리스트 확인
   - **번역투 제거 확인**: Step 5-B 항목 확인
   - **자연스러움 검증**: 한국어 원어민이 실제로 사용하는 표현인지 확인

   상세 품질 기준은 [natural-korean-guide.md](../podcast-summary-review/natural-korean-guide.md) 참조

6. **출력 생성**:
   - 원본 파일과 같은 디렉토리에 `-bilingual.json` 접미사를 붙여 저장
   - 예: `anthropic-ceo-summary.json` → `anthropic-ceo-summary-bilingual.json`
   - JSON 구조 검증: 모든 번역 가능 필드가 `{en: "...", ko: "..."}` 형식인지 확인
   - 번역 완료 후 요약 리포트 제공:
     - 변환된 필드 수
     - 파일 위치
     - 파일 크기 (영문 단독 대비 증가량)
     - 언어 토글 기능 지원 여부 확인

7. **오류 처리**:
   - 파일을 찾을 수 없으면 사용 가능한 파일 목록 표시
   - JSON 파싱 오류 시 구체적인 오류 위치 표시
   - 이미 한국어 파일인 경우 경고 및 확인 요청
