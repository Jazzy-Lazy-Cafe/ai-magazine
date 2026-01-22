# Google AdSense Setup Guide

This guide will help you set up Google AdSense to monetize your Jekyll magazine site.

## Prerequisites

Before applying for Google AdSense, ensure your site meets these requirements:

- **Original Content**: Your site must have unique, valuable content (not copied from other sites)
- **Sufficient Content**: At least 20-30 quality posts/articles
- **Clean Design**: Professional-looking site with good user experience
- **Domain**: Custom domain is preferred (github.io domains can be accepted but custom domains have higher approval rates)
- **Traffic**: While not strictly required, having some organic traffic helps
- **Compliance**: Content must follow [AdSense Program Policies](https://support.google.com/adsense/answer/48182)

## Step 1: Apply for Google AdSense

1. Go to [Google AdSense](https://www.google.com/adsense/)
2. Click "Get Started" and sign in with your Google account
3. Fill in your website URL: `https://jazzy-lazy-cafe.github.io/ai-magazine/`
4. Complete the application form with your details
5. Accept the AdSense Terms and Conditions

## Step 2: Add AdSense Code to Your Site

After applying, Google will provide you with an AdSense code snippet. You need to add this to your site for verification.

1. **Get Your AdSense Client ID**:
   - In your AdSense dashboard, find your publisher ID (looks like `ca-pub-1234567890123456`)

2. **Update `_config.yml`**:
   ```yaml
   google_adsense:
     enabled: true  # Change from false to true
     client_id: "ca-pub-1234567890123456"  # Your AdSense client ID
     slots:
       article_top: ""     # Leave empty for now
       in_article: ""      # Leave empty for now
       article_bottom: ""  # Leave empty for now
       sidebar: ""         # Leave empty for now
   ```

3. **Deploy Your Changes**:
   ```bash
   git add _config.yml
   git commit -m "Add AdSense verification code"
   git push
   ```

4. **Wait for Approval**:
   - Google will review your site (usually takes 1-7 days, sometimes up to 2 weeks)
   - You'll receive an email when your application is approved or if any changes are needed

## Step 3: Create Ad Units (After Approval)

Once approved, create specific ad units for different placements:

1. Go to your AdSense dashboard
2. Navigate to **Ads** → **By ad unit**
3. Create these ad units:
   - **Article Top Ad**: Display ad (responsive)
   - **In-Article Ad**: In-article ad (responsive)
   - **Article Bottom Ad**: Display ad (responsive)
   - **Sidebar Ad**: Display ad (vertical or square)

4. For each ad unit, copy the `data-ad-slot` ID (looks like `1234567890`)

5. **Update `_config.yml` with your ad slot IDs**:
   ```yaml
   google_adsense:
     enabled: true
     client_id: "ca-pub-1234567890123456"
     slots:
       article_top: "1234567890"     # Your article top ad slot ID
       in_article: "0987654321"      # Your in-article ad slot ID
       article_bottom: "1122334455"  # Your article bottom ad slot ID
       sidebar: "5566778899"         # Your sidebar ad slot ID
   ```

## Step 4: Add Ads to Your Posts

The ad infrastructure is already set up. To add ads to your posts, simply include the ad placeholders at strategic locations.

### Example: Adding Ads to a Post

Edit your post HTML file (e.g., `_posts/2026-01-21-anthropic-ceo-davos.html`):

```html
---
layout: magazine
title: "Your Post Title"
---

{% include magazine/header.html ... %}
{% include magazine/hero-split.html ... %}

<!-- Top of Article Ad -->
{% include ads/article-top.html %}

<!-- Main Content -->
<main class="magazine-grid">
    <!-- First few sections -->
    <article class="article-section fade-in">
        ...
    </article>

    <article class="article-section reverse fade-in">
        ...
    </article>

    <!-- In-Article Ad (after 2-3 sections) -->
    {% include ads/in-article.html %}

    <!-- More sections -->
    <article class="article-section fade-in">
        ...
    </article>

    <!-- More content... -->
</main>

<!-- Bottom of Article Ad -->
{% include ads/article-bottom.html %}

{% include magazine/footer.html ... %}
```

## Step 5: Deploy and Monitor

1. **Deploy your changes**:
   ```bash
   git add _posts/ _config.yml
   git commit -m "Add AdSense ad placements"
   git push
   ```

2. **Wait for ads to appear**:
   - New ad units may take a few hours to start showing ads
   - Initially, you might see blank spaces or PSA (Public Service Announcement) ads

3. **Monitor performance**:
   - Check your AdSense dashboard regularly
   - Track metrics: impressions, clicks, CTR (Click-Through Rate), earnings
   - Experiment with different ad placements to optimize revenue

## Available Ad Placements

The site has 4 pre-configured ad placement options:

1. **Article Top**: `{% include ads/article-top.html %}`
   - Appears at the top of the article, after the hero section
   - Responsive display ad
   - High visibility

2. **In-Article**: `{% include ads/in-article.html %}`
   - Appears between article sections
   - Designed to blend with content
   - Place after 2-3 sections for best results

3. **Article Bottom**: `{% include ads/article-bottom.html %}`
   - Appears at the end of the article
   - Good for readers who finish the article
   - Responsive display ad

4. **Sidebar**: `{% include ads/sidebar.html %}`
   - Sticky sidebar ad (desktop only)
   - Hidden on mobile devices
   - Good for long-form articles

## Best Practices

1. **Don't Over-Advertise**:
   - Use 2-3 ads per article maximum
   - Too many ads hurt user experience and may violate AdSense policies

2. **Strategic Placement**:
   - Place ads where they're visible but not intrusive
   - In-article ads perform well but should be placed naturally

3. **Mobile Optimization**:
   - All ads are responsive and mobile-friendly
   - Sidebar ads are hidden on mobile to avoid clutter

4. **Content First**:
   - Focus on creating quality content
   - Better content = more traffic = more ad revenue

5. **Policy Compliance**:
   - Never click your own ads
   - Don't encourage others to click ads
   - Ensure your content complies with [AdSense policies](https://support.google.com/adsense/answer/48182)

## Troubleshooting

### Ads Not Showing

- **Recently added**: Wait 24-48 hours for new ad units to activate
- **Low traffic**: Sites with very low traffic may show blank ads initially
- **Policy violation**: Check AdSense dashboard for policy warnings
- **Ad blockers**: Test in incognito mode without ad blockers

### Blank Ad Spaces

- Normal for new sites with low traffic
- Google shows ads based on available inventory
- As your site grows, fill rate will improve

### Revenue Lower Than Expected

- AdSense revenue depends on:
  - Traffic volume (pageviews)
  - Traffic quality (geographic location, interests)
  - Content niche (tech content generally has good CPM)
  - Ad placement and user engagement

## Alternative: Auto Ads

If you want a simpler approach, you can use Google's Auto Ads feature:

1. Enable Auto Ads in your AdSense dashboard
2. Set `enabled: true` in `_config.yml`
3. Google will automatically place ads on your site

Note: Auto ads give less control over ad placement but are easier to manage.

## Support

- [AdSense Help Center](https://support.google.com/adsense)
- [AdSense Community](https://support.google.com/adsense/community)
- [AdSense Policy Center](https://support.google.com/adsense/answer/48182)

## Next Steps

1. Apply for AdSense
2. Add verification code to `_config.yml`
3. Wait for approval
4. Create ad units
5. Add ad placements to your posts
6. Monitor and optimize

Good luck with monetizing your site!
