# SEO 설정 가이드

## 완료된 작업

### 1. ✅ 기본 SEO 설정
- `_config.yml`에 SEO 관련 설정 추가
- 언어 설정 (ko), locale (ko_KR)
- Author, Social 정보 추가
- SEO 플러그인 활성화

### 2. ✅ Sitemap & Robots.txt
- `sitemap.xml` 생성 (검색엔진에 페이지 구조 제공)
- `robots.txt` 생성 (크롤링 허용/차단 설정)

### 3. ✅ SEO 메타 태그
- `_includes/seo.html` 생성
- Open Graph 태그 (Facebook 공유)
- Twitter Card 태그
- Schema.org 구조화된 데이터
- Canonical URL
- 모든 layout에 SEO 포함

### 4. ✅ Gemfile 업데이트
- jekyll-sitemap
- jekyll-seo-tag
- jekyll-feed

---

## 추가로 해야 할 작업

### 1. 🎨 OG 이미지 추가
기본 OG 이미지를 추가하세요:
```
/assets/images/default-og.png (1200x630px 권장)
/assets/images/logo.png (로고 이미지)
```

각 포스트마다 고유한 이미지를 추가하려면 front matter에:
```yaml
---
image: /ai-magazine/assets/images/post-specific-image.png
---
```

### 2. 📦 Jekyll 플러그인 설치
```bash
bundle install
```

### 3. 🔧 각 포스트에 keywords 추가 (선택사항)
각 포스트의 front matter에 keywords를 추가하면 더 좋습니다:
```yaml
---
title: "Your Title"
description: "Your Description"
keywords: "AI, 머신러닝, Eric Schmidt, 초지능"
---
```

### 4. 🌐 검색엔진 등록

#### Google Search Console
1. https://search.google.com/search-console 방문
2. 속성 추가 → URL 접두어: `https://jazzy-lazy-cafe.github.io/ai-magazine`
3. 소유권 확인 (HTML 파일 또는 메타 태그 방식)
4. Sitemap 제출: `https://jazzy-lazy-cafe.github.io/ai-magazine/sitemap.xml`

#### Naver 웹마스터 도구
1. https://searchadvisor.naver.com 방문
2. 사이트 등록
3. 소유 확인
4. Sitemap 제출: `https://jazzy-lazy-cafe.github.io/ai-magazine/sitemap.xml`

#### Bing Webmaster Tools
1. https://www.bing.com/webmasters 방문
2. 사이트 추가
3. Sitemap 제출

### 5. 📊 Analytics 추가 (선택사항)
Google Analytics를 추가하려면:

`_includes/analytics.html` 생성:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

그리고 layouts에 추가:
```html
{% include analytics.html %}
```

### 6. 🔗 소셜 미디어 연결
`_config.yml`에서 Twitter username 업데이트:
```yaml
twitter:
  username: your_twitter_handle
```

---

## 검증 방법

### 1. SEO 메타 태그 확인
브라우저에서 페이지 소스 보기 (Ctrl+U 또는 Cmd+Option+U)
- `<title>` 태그 확인
- `<meta name="description">` 확인
- Open Graph 태그 확인
- Schema.org JSON-LD 확인

### 2. 온라인 도구 사용
- **Facebook Debugger**: https://developers.facebook.com/tools/debug/
- **Twitter Card Validator**: https://cards-dev.twitter.com/validator
- **Rich Results Test**: https://search.google.com/test/rich-results
- **Structured Data Validator**: https://validator.schema.org/

### 3. Sitemap 확인
브라우저에서 접속:
```
https://jazzy-lazy-cafe.github.io/ai-magazine/sitemap.xml
```

### 4. Robots.txt 확인
브라우저에서 접속:
```
https://jazzy-lazy-cafe.github.io/ai-magazine/robots.txt
```

---

## 추가 최적화 팁

### 성능 최적화
1. 이미지 최적화 (WebP 형식 사용)
2. CSS/JS 압축
3. 캐싱 활성화

### 콘텐츠 최적화
1. 각 포스트마다 고유한 description 작성 (150-160자)
2. 제목에 핵심 키워드 포함 (60자 이내)
3. 이미지에 alt 태그 추가
4. 내부 링크 추가 (관련 포스트 연결)

### 소셜 공유 최적화
1. 각 포스트마다 매력적인 OG 이미지 추가
2. 제목과 설명을 SNS에 맞게 최적화

---

## 문제 해결

### Sitemap이 생성되지 않음
```bash
bundle exec jekyll build --verbose
```
로그를 확인하여 플러그인 오류 체크

### SEO 태그가 보이지 않음
- Jekyll을 재시작 (`_config.yml` 변경 시 필수)
- 캐시 삭제 (`_site` 폴더 삭제 후 재빌드)

### GitHub Pages에서 플러그인 작동 안 함
GitHub Pages는 제한된 플러그인만 지원합니다.
- jekyll-sitemap ✅ 지원
- jekyll-seo-tag ✅ 지원
- jekyll-feed ✅ 지원

---

## 체크리스트

- [x] _config.yml SEO 설정
- [x] sitemap.xml 생성
- [x] robots.txt 생성
- [x] SEO 메타 태그 include 생성
- [x] layouts에 SEO 포함
- [x] Gemfile 플러그인 추가
- [ ] OG 이미지 추가
- [ ] bundle install 실행
- [ ] Google Search Console 등록
- [ ] Naver 웹마스터 등록
- [ ] 소셜 미디어 메타 태그 테스트
- [ ] 각 포스트에 keywords 추가 (선택)
- [ ] Google Analytics 추가 (선택)

