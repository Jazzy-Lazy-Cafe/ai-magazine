---
name: youtube-transcript
description: Downloads YouTube transcript using the ytt CLI tool.
---

## 목적
YouTube URL을 입력받아 `ytt` CLI 도구를 사용하여 트랜스크립트를 다운로드하고, 팟캐스트 워크플로우에서 사용할 수 있도록 저장합니다.

## 입력
- YouTube URL (필수)
- 출력 파일명 (선택사항, 미제공 시 자동 생성)

## 출력
- `.claude/skills/podcast-summary/transcripts/` 폴더에 저장된 텍스트 트랜스크립트 파일
- 저장된 파일의 절대 경로

## 실행 지침

### Step 1: YouTube URL 확인
1. 사용자가 제공한 YouTube URL이 유효한지 확인합니다
2. URL 형식 예시:
   - `https://www.youtube.com/watch?v=VIDEO_ID`
   - `https://youtu.be/VIDEO_ID`

### Step 2: 출력 파일명 결정
1. 사용자가 파일명을 제공한 경우: 해당 파일명 사용
2. 파일명 미제공 시: 비디오 제목이나 ID 기반으로 자동 생성
3. 파일 확장자는 `.txt` 사용
4. 파일명에 공백이 있는 경우 하이픈(`-`)으로 대체

### Step 3: ytt 명령어 실행
다음 형식으로 `ytt` 명령어를 실행합니다:

```bash
ytt [YOUTUBE_URL] -o /Users/gahee/WebstormProjects/ai-magazine/.claude/skills/podcast-summary/transcripts/[FILENAME].txt
```

**중요 옵션:**
- `-o` 또는 `--output`: 출력 파일 경로 지정
- 출력 디렉토리가 존재하지 않는 경우 자동 생성

### Step 4: 결과 확인
1. 파일이 성공적으로 생성되었는지 확인
2. 파일 크기가 0보다 큰지 확인
3. 파일 내용이 유효한 텍스트 트랜스크립트인지 간단히 확인

### Step 5: 결과 보고
다음 정보를 사용자에게 제공:

```markdown
✅ YouTube 트랜스크립트 다운로드 완료!

📺 비디오: [비디오 제목 또는 URL]
📁 저장 위치: [절대 경로]
📊 파일 크기: [크기]

🚀 다음 단계:
이 트랜스크립트로 요약을 생성하려면 다음 명령어를 사용하세요:
/podcast-summary [파일명]

또는 전체 워크플로우를 실행하려면:
/podcast-to-post [파일명]
```

## 사용 예시

### YouTube URL로 트랜스크립트 다운로드
```
/youtube-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 파일명 지정하여 다운로드
```
/youtube-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ rick-astley-interview.txt
```

## 에러 처리

### URL 오류
- 잘못된 URL 형식 → 올바른 YouTube URL 형식 안내
- 비디오를 찾을 수 없음 → URL 확인 요청
- 비공개 비디오 → 공개 비디오만 다운로드 가능함을 안내

### 트랜스크립트 없음
- 자동 생성 자막이 없는 경우 → 트랜스크립트를 사용할 수 없음을 안내
- 지원하지 않는 언어 → 지원 언어 목록 표시

### 파일 시스템 오류
- 디렉토리 생성 실패 → 권한 확인
- 파일 쓰기 실패 → 디스크 공간 확인

### ytt 도구 없음
- `ytt` 명령어를 찾을 수 없는 경우:
  ```bash
  command -v ytt
  ```
  실행하여 설치 여부 확인 후 설치 방법 안내

## 워크플로우 상의 위치

```
YouTube URL
    ↓
[이 스킬] youtube-transcript → Transcript (.txt)
    ↓
podcast-summary → English JSON
    ↓
podcast-summary-translator → Bilingual JSON
    ↓
podcast-summary-review → Quality Report
    ↓
podcast-json-to-post → Bilingual HTML
```

이 스킬은 팟캐스트 콘텐츠 파이프라인의 **첫 단계**에서 YouTube 비디오로부터 트랜스크립트를 가져오는 역할을 합니다.

## 품질 체크리스트

실행 완료 후 다음을 확인하세요:

- [ ] 트랜스크립트 파일이 `.claude/skills/podcast-summary/transcripts/` 폴더에 생성되었는가?
- [ ] 파일 크기가 0보다 큰가?
- [ ] 파일 내용이 텍스트 형식인가?
- [ ] 파일명에 특수문자나 공백이 없는가?
- [ ] 사용자에게 다음 단계 안내가 제공되었는가?

## ytt CLI 도구 정보

`ytt`는 YouTube 트랜스크립트 다운로더입니다. 다음 기능을 지원합니다:

- YouTube 비디오 자동/수동 자막 다운로드
- 타임스탬프 포함/제외 옵션
- 다양한 언어 지원
- 텍스트 파일 출력

**기본 사용법:**
```bash
ytt [URL] -o [OUTPUT_FILE]
```

## 관련 스킬
- [podcast-summary](../podcast-summary/SKILL.md): 트랜스크립트를 영문 JSON으로 변환
- [podcast-to-post](../podcast-to-post/SKILL.md): 전체 워크플로우 자동 실행

## 구현 노트

**중요**: 이 스킬은 `ytt` CLI 도구가 시스템에 설치되어 있어야 합니다. 설치되어 있지 않은 경우 사용자에게 안내하세요.

**경로 주의**: 출력 파일 경로는 항상 절대 경로를 사용하며, `.claude/skills/podcast-summary/transcripts/` 디렉토리를 기본 위치로 사용합니다.

**파일명 규칙**: 파일명은 소문자와 하이픈을 사용하며, 공백이나 특수문자를 피합니다 (예: `sam-altman-interview.txt`).
