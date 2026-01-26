---
name: podcast-to-post
description: 트랜스크립트에서 Jekyll 포스트까지 전체 워크플로우를 자동 실행합니다.
---

## 목적
팟캐스트 트랜스크립트 하나만 제공하면 영문 요약 → 한국어 번역 → 품질 검수 → Jekyll HTML 생성까지 전체 파이프라인을 자동으로 실행합니다.

## 입력
- 트랜스크립트 파일 경로 (선택사항)
- 파일명 미제공 시 가장 최신 트랜스크립트 파일 자동 선택

## 출력
- 영문 JSON 파일
- 이중언어 JSON 파일 (`-bilingual.json`, 영어/한국어 모두 포함)
- 품질 검수 리포트
- 이중언어 Jekyll 매거진 포스트 HTML 파일 (언어 토글 기능 포함)

## 워크플로우 단계

### Step 1: 영문 요약 생성 (podcast-summary)
- **입력**: 트랜스크립트 텍스트 파일
- **스킬**: `/podcast-summary`
- **출력**: 영문 Q&A JSON 파일
- **다음 단계로 전달**: 생성된 JSON 파일 경로

### Step 2: 이중언어 JSON 생성 (podcast-summary-translator)
- **입력**: Step 1에서 생성된 영문 JSON 파일
- **스킬**: `/podcast-summary-translator`
- **출력**: 이중언어 JSON 파일 (`-bilingual.json`, 영어 원문 + 한국어 번역)
- **다음 단계로 전달**: 생성된 `-bilingual.json` 파일 경로

### Step 3: 품질 검수 (podcast-summary-review)
- **입력**: Step 2에서 생성된 이중언어 JSON 파일
- **스킬**: `/podcast-summary-review`
- **출력**: 품질 검수 리포트 (번역투 체크, 유기적 연결성 점수)
- **다음 단계로 전달**: 동일한 `-bilingual.json` 파일 경로

### Step 4: Jekyll 포스트 생성 (podcast-json-to-post)
- **입력**: Step 2에서 생성된 이중언어 JSON 파일
- **스킬**: `/podcast-json-to-post`
- **출력**: 이중언어 Jekyll 매거진 포스트 HTML 파일 (언어 토글 버튼 포함)
- **최종 결과**: 웹사이트에 게시 가능한 HTML 파일 (영어/한국어 전환 기능)

## 사용 예시

### 특정 트랜스크립트로 전체 워크플로우 실행
```
/podcast-to-post transcript.txt
```

### 최신 트랜스크립트로 자동 실행
```
/podcast-to-post
```

## 실행 지침 (Claude에게)

이 스킬을 실행할 때 다음 단계를 순차적으로 수행하세요:

### 1단계: podcast-summary 실행

```
Skill tool 호출:
- skill: "podcast-summary"
- args: [사용자가 제공한 트랜스크립트 파일 또는 최신 파일]
```

완료 후:
- 생성된 JSON 파일 경로를 확인하고 기록
- 파일 경로를 `ENGLISH_JSON` 변수로 저장 (예: `anthropic-ceo-summary.json`)
- **중요**: 이 단계에서는 HTML 파일이 생성되지 않습니다. JSON 파일만 생성됩니다.

### 2단계: podcast-summary-translator 실행

```
Skill tool 호출:
- skill: "podcast-summary-translator"
- args: [1단계에서 생성된 ENGLISH_JSON 파일]
```

완료 후:
- 생성된 `-bilingual.json` 파일 경로를 확인하고 기록
- 파일 경로를 `BILINGUAL_JSON` 변수로 저장 (예: `anthropic-ceo-summary-bilingual.json`)

### 3단계: podcast-summary-review 실행

```
Skill tool 호출:
- skill: "podcast-summary-review"
- args: [2단계에서 생성된 BILINGUAL_JSON 파일]
```

완료 후:
- 품질 검수 리포트를 읽고 주요 발견사항 요약
- 번역투 점수, 유기적 연결성 점수 확인
- 치명적 문제가 있으면 사용자에게 보고하고 계속 진행할지 확인

### 4단계: podcast-json-to-post 실행 (최종 단계 - HTML 생성)

```
Skill tool 호출:
- skill: "podcast-json-to-post"
- args: [2단계에서 생성된 BILINGUAL_JSON 파일]
```

완료 후:
- 생성된 HTML 파일 경로 확인
- 최종 결과 파일 경로를 사용자에게 보고
- **중요**: 이 단계가 전체 워크플로우에서 HTML을 생성하는 유일한 단계입니다. 이중언어 JSON을 입력으로 받아 언어 토글 기능이 있는 이중언어 HTML을 생성합니다.

### 최종 리포트

모든 단계 완료 후 다음 정보를 사용자에게 제공:

```markdown
✅ 워크플로우 완료!

📁 생성된 파일:
- 영문 요약: [ENGLISH_JSON 경로]
- 이중언어 JSON: [BILINGUAL_JSON 경로]
- 이중언어 Jekyll 포스트: [HTML 경로]

📊 품질 검수 결과:
- 번역투 점수: [점수]/100
- 유기적 연결성: [점수]/100
- 주요 발견사항: [요약]

🌐 언어 토글 기능:
- 영어/한국어 전환 버튼 포함
- 사용자 언어 선호도 localStorage 저장
- 기본 언어: 한국어

🚀 다음 단계:
[HTML 파일]을 웹사이트에 배포하세요.
```

## 에러 처리

### Step 1 실패 시
- 트랜스크립트 파일 형식 오류 → 파일 형식 확인 안내
- 트랜스크립트 파일 없음 → 사용 가능한 파일 목록 표시
- 워크플로우 중단, 이후 단계 실행 안 함

### Step 2 실패 시
- JSON 파싱 오류 → Step 1에서 생성된 JSON 검증
- 이미 한국어 파일 존재 → 덮어쓰기 확인 후 진행
- 워크플로우 중단, 이후 단계 실행 안 함

### Step 3 실패 시
- 품질 검수 실패해도 경고만 표시하고 계속 진행
- 치명적 문제 발견 시 사용자에게 확인 요청

### Step 4 실패 시
- HTML 생성 오류 → 템플릿 또는 JSON 구조 문제 보고
- 생성된 파일들은 유지 (삭제 안 함)

## 중간 확인 옵션

사용자가 각 단계 후 확인을 원하면 `--step-by-step` 모드 제공:

```
/podcast-to-post --step-by-step transcript.txt
```

이 모드에서는:
- 각 단계 완료 후 결과를 보여주고 다음 단계 진행 여부 확인
- 사용자가 "계속" 또는 "중단" 선택 가능

## 워크플로우 다이어그램

```
트랜스크립트 (.txt)
    ↓
[Step 1] /podcast-summary
    ↓
영문 JSON (.json)
    ↓
[Step 2] /podcast-summary-translator
    ↓
이중언어 JSON (-bilingual.json)
    ↓        
[Step 3]    
review     
    ↓            
품질 리포트 생성
-> 품질 리포트 점수 95점 미만시 다시 review 루프를 돈다. 총 3회 동안 개선을 진행한다. 
-> [Step 4]
이중언어 Jekyll HTML (언어 토글)
```

## 관련 스킬
- [podcast-summary](../podcast-summary/SKILL.md): 트랜스크립트를 영문 JSON으로 변환
- [podcast-summary-translator](../podcast-summary-translator/SKILL.md): 영문 JSON을 한국어로 번역
- [podcast-summary-review](../podcast-summary-review/SKILL.md): 한국어 품질 검수
- [podcast-json-to-post](../podcast-json-to-post/SKILL.md): Jekyll HTML 생성

## 구현 노트

**중요**: 이 스킬은 다른 스킬들을 순차적으로 호출하는 오케스트레이터입니다. 각 단계는 **Skill tool**을 사용해 호출하며, 이전 단계의 출력을 다음 단계의 입력으로 전달합니다.

**파일 경로 추적**: 각 스킬 실행 후 생성된 파일의 정확한 경로를 확인하고 다음 스킬에 전달해야 합니다. 경로를 추측하지 말고 반드시 확인하세요.

**에러 복구**: 중간 단계에서 실패하더라도 이미 생성된 파일들은 유지되므로, 사용자가 수동으로 나머지 단계를 실행할 수 있습니다.
