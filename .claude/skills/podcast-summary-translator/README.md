# Podcast Summary Translator

이 스킬은 영문 JSON을 자연스러운 한국어가 포함된 이중언어 JSON으로 번역합니다.

## 파일 구조

```
podcast-summary-translator/
├── SKILL.md                          # Claude 실행 워크플로우
├── translation-prompting-guide.md    # 번역 프롬프팅 전략 가이드
└── README.md                         # 이 파일
```

## 각 파일의 역할

### 1. SKILL.md (기술 워크플로우)
**대상**: Claude (AI 어시스턴트)
**내용**:
- 입력/출력 파일 경로
- JSON 구조 변환 방법
- 작업 실행 순서 (Step 1-6)
- 품질 체크리스트

### 2. translation-prompting-guide.md (프롬프팅 전략)
**대상**: 사용자 (번역 품질 개선 방법을 배우고 싶은 사람)
**내용**:
- Claude에게 효과적으로 번역 요청하는 5가지 전략
- 완전한 프롬프트 템플릿
- 흔한 실수와 해결 방법
- 고급 팁 (A/B 테스트, 역번역 등)

## 관련 문서

- [natural-korean-guide.md](../podcast-summary-review/natural-korean-guide.md): 120가지 자연스러운 한국어 패턴 (번역투 제거)
- [podcast-summary/SKILL.md](../podcast-summary/SKILL.md): 영문 요약 생성 스킬

## 사용 예시

```bash
# 특정 파일 번역
/podcast-summary-translator anthropic-ceo-summary.json

# 최신 파일 자동 번역
/podcast-summary-translator

# 강제 재번역
/podcast-summary-translator --force anthropic-ceo-summary.json
```

## 워크플로우

```
Transcript
    ↓
[podcast-summary] → English JSON
    ↓
[podcast-summary-translator] → Bilingual JSON (-bilingual.json)
    ↓
[podcast-json-to-post] → Jekyll HTML (language toggle)
```
