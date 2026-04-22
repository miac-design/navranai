# RedM Command Center V3 — 5-Minute Presentation Guide

> Live UI Demo script for RedM stakeholders. Format: live browser demo
> (`design_v3.html`). Duration: 5 minutes. Date: April 19, 2026.

**National Human Trafficking Hotline: 1-888-373-7888 · Text BeFree to 233733**

---

## Before you start

### Setup checklist

- Open `design_v3.html` in Chrome (full screen — F11)
- Ensure Light mode is selected (better for projectors)
- If you want a live scan: run backend (`cd backend && python server.py`)
- If backend is NOT running, the static UI still shows all demo data — skip live scan
- Test your screen sharing / projector connection
- Have this guide printed or on a second screen

### Delivery tips

- Speak slowly and confidently — 5 minutes is plenty of time
- Point at the screen when mentioning specific elements
- Don't read captions word-for-word — summarize what they say
- End with the hotline number — it grounds the mission
- The Calendar is the star — spend the most time there

### Navigation order (quick reference)

| Time  | Tab          | Duration | What to Show                                   |
| ----- | ------------ | -------- | ---------------------------------------------- |
| 0:00  | Onboarding   | 30 sec   | State the problem + one-sentence pitch         |
| 0:30  | Intelligence | 45 sec   | Scan + story cards + "Generate Campaign"       |
| 1:15  | Calendar ⭐  | 75 sec   | 5-day grid + carousel + captions                |
| 2:30  | Calendar     | 45 sec   | Approve / Edit / Regen flow                    |
| 3:15  | Rules        | 45 sec   | 3-tier compliance system                       |
| 4:00  | Impact → Library | 30 sec | KPIs + past campaigns                        |
| 4:30  | —            | 30 sec   | Closing statement + hotline                    |

---

## The script

### 0:00 – 0:30 · Opening — The Problem

**Onboarding** — stay on the welcome overlay or Calendar view.

> "This is the RedM Command Center — an AI-powered tool we built to solve a
> real problem: anti-trafficking organizations need to post consistent,
> ethical social media content, but they're understaffed and stretched thin.
>
> This system takes a single news story and automatically generates a full
> week of social media content — 5 posts, each with captions, AI-generated
> images, and compliance checks — ready for human review in under 3 minutes."

**Screen action**: if the onboarding overlay shows, click *Get Started*
through all 3 steps, then dismiss.

### 0:30 – 1:15 · Intelligence Feed

**Intelligence** — click it in the sidebar.

> "Everything starts here — the Intelligence Feed. The system scans 12
> trusted news sources — Reuters, AP, BBC, Polaris Project, the DOJ — for
> breaking human trafficking stories.
>
> Each story is ranked and displayed as a card. The team picks the most
> relevant one and clicks *Generate Campaign*. That's it — one click
> triggers the entire AI pipeline."

**Point out**:

- The *Scan Now* button at the top
- The *AI Pick* badge on the top story
- The *Generate Campaign* button on any story card
- The *Manual URL* input — "They can also paste any article URL directly"

### 1:15 – 2:30 · Content Calendar ⭐ THE MAIN EVENT

**Calendar** — click it in the sidebar.

> "This is the heart of the system — the Content Calendar. From one news
> story, the AI generates 5 posts for the week, each with a different purpose."

| Day       | Type        | What to Say                                                         |
| --------- | ----------- | ------------------------------------------------------------------- |
| Monday    | Reactive    | "The breaking news hook. Gets immediate attention."                 |
| Tuesday   | Stat Card   | "A key data point from the story — builds credibility."             |
| Wednesday | Explainer   | "Educational deep-dive — what does this mean?"                      |
| Thursday  | Action      | "A direct call to action — call the hotline, report suspicious activity." |
| Friday    | Hope        | "A positive progress story — prevents compassion fatigue."          |

> "Every post has an AI-generated image tailored to the audience, a quality
> score from our AI judge, and a compliance badge confirming it meets
> ethical standards."

**Demo actions** (in order):

1. Click on a post image → Carousel Modal opens — "This is the review view"
2. Show the headline, caption, quality score, compliance badge
3. Click → to navigate to the next post
4. Close the carousel (× or Esc)
5. Click *Caption* on any post to expand the full text
6. Point out the character counts — "IG: /2200, X: /280"

### 2:30 – 3:15 · Approve & Edit Flow

Stay on the **Calendar** view.

> "The system is human-in-the-loop — nothing publishes without approval. The
> reviewer can approve each post individually, edit any caption directly,
> regenerate an image with custom instructions, or batch-approve all 5 with
> one click."

**Demo actions**:

- Point at the *Approve* button on a post
- Point at the *Approve All 5 Posts* button (top right)
- Click *Edit* on one post → show the edit modal → click Cancel

> "Once approved, they can download the entire campaign as a ZIP or
> translate it to Spanish, French, or Portuguese — one click."

**Point at**: the *Download* and *Translate* buttons in the top action bar.

### 3:15 – 4:00 · Content Rules — The Differentiator

**Rules** — click it in the sidebar.

> "This is what makes this system different from generic AI tools. We built
> in ethical guardrails — a rules engine that every piece of content must
> pass through."

| Tier                | Color          | What to Say                                                                                               |
| ------------------- | -------------- | --------------------------------------------------------------------------------------------------------- |
| Legal & Compliance  | Red (locked)   | "These are locked — can't disable them. Never identify survivors. Always cite sources."                   |
| Ethical Language    | Orange         | "Replaces harmful terms. For example, it won't say *rescued* — it says *identified*, because *rescued* implies the survivor lacked agency." |
| Brand Voice         | Gray           | "Customizable rules — *no sensationalized imagery*, *at least one hope post per week*."                   |

> "The compliance checker runs both a regex-based quick check and an AI deep
> analysis. If it finds a violation, it auto-fixes it before the human even
> sees it."

**Point at**: the 98% compliance score bar at the top of the Rules page.

### 4:00 – 4:30 · Impact & Library (Quick)

**Impact** — click, stay for 10 seconds.

> "The Impact page tracks reach, engagement, hotline clicks, and API costs
> per campaign."

**Library** — click, stay for 15 seconds.

> "And the Content Library stores every campaign ever generated — with
> thumbnails. Click any past campaign to reload it into the calendar."

### 4:30 – 5:00 · Closing

> "To summarize: one news story in, five platform-ready posts out — each
> written, illustrated, scored, and compliance-checked by AI, with full
> human control.
>
> The system uses GPT-4o for strategic planning, GPT-4o-mini for writing and
> quality, and Google Gemini for image generation. Everything is logged,
> auditable, and translatable.
>
> We built this so a team of 2–3 volunteers can produce what used to take a
> social media agency a full week."

Final beat — point at the sidebar:

> "And that number at the bottom — **1-888-373-7888** — that's the National
> Human Trafficking Hotline. Every single post we generate includes it.
> That's why we built this."

---

## With continued support

What you've seen today is the working MVP. With continued support, here is
what the next phase of development unlocks.

### 1. Agent Security & Data Protection

*Current state: API keys in `.env`, open CORS, no authentication layer.*

| Enhancement                  | What It Means |
| ---------------------------- | ------------- |
| LLM Prompt Hardening         | Injection guards and output sanitization to prevent adversarial manipulation of AI-generated content. |
| Role-Based Access Control    | Separate Creator, Reviewer, and Admin roles with JWT authentication. |
| API Key Vault                | Migrate from `.env` files to a secrets manager (AWS Secrets Manager or Azure Key Vault) with key rotation. |
| Rate Limiting & Abuse Prevention | Per-user generation limits, IP-based throttling, anomaly alerts. |
| Audit Encryption             | End-to-end encryption of the audit trail database. |

### 2. Sophisticated Content & Higher-Quality Images

*Current state: Gemini 3.1 Flash for images, basic Pillow text overlay, 3 font files.*

| Enhancement               | What It Means |
| ------------------------- | ------------- |
| Premium Image Models      | Upgrade to DALL-E 3, Midjourney API, or Gemini 2.0 Pro. |
| Brand Template System     | Pre-designed templates with RedM logo, typography, gradient overlays. |
| Video Content Generation  | Extend from static images to short-form video (15s Reels/TikToks). |
| Multi-Story Campaigns     | Generate campaigns weaving multiple news stories into a unified arc. |
| A/B Testing Built In      | Wire the PromptRegistry to automatically rotate high-performing prompts. |

### 3. Post-Publish Monitoring & Analytics

*Current state: Impact page shows placeholder KPIs; no live social media data.*

| Enhancement                      | What It Means |
| -------------------------------- | ------------- |
| Live Social Media Integration    | Instagram Graph, X API v2, LinkedIn Marketing, Facebook Pages. |
| Hotline Click Attribution        | UTM-tagged links in every post. |
| Sentiment Analysis Dashboard     | AI-powered comment monitoring with escalation alerts. |
| Content Performance Feedback Loop | Feed engagement data back into the Campaign Planner. |
| Weekly Report Generation         | Automated PDF reports sent every Monday. |

### 4. Operational Cost Optimization

*Current state: ~$0.05–0.15 per campaign (43–48 LLM calls). Gemini images on free tier.*

| Enhancement                | Impact |
| -------------------------- | ------ |
| Intelligent Caching        | Cache common LLM responses; 30–40% call reduction for recurring topics. |
| Model Routing Optimization | Local models / rule-based logic for simple tasks; reserve GPT-4o for planning. |
| Batch API Calls            | OpenAI Batch API (50% cost reduction) for non-urgent tasks. |
| Cost Budget Alerts         | Monthly spending caps with email/Slack alerts at 50%, 80%, 100%. |
| Monthly Cost Projection    | Current: 4 campaigns/mo ≈ $0.40–0.60. At scale: 20 campaigns/mo ≈ $2–3 AI + $5–10 hosting. |

### 5. Direct Social Media Publishing

*Current state: ZIP download only. No API-level publishing.*

| Enhancement                | What It Means |
| -------------------------- | ------------- |
| One-Click Publish          | Publish directly to IG, X, LinkedIn, FB via official APIs. |
| Scheduled Publishing       | Wire APScheduler to platform APIs for time-optimized posting. |
| Cross-Platform Adaptation  | Auto-adjust caption length, hashtag count, image format per platform. |

### Estimated timeline with support

| Phase   | Duration   | Deliverables                                                        |
| ------- | ---------- | ------------------------------------------------------------------- |
| Phase 1 | 2–3 weeks  | Security layer (auth, RBAC, key vault) + font fix + publishing MVP  |
| Phase 2 | 3–4 weeks  | Premium images + brand templates + monitoring + live API            |
| Phase 3 | 4–6 weeks  | Video content + feedback loop + cost optimization + weekly reports  |

---

## Anticipated Q&A

| Question                                   | Your Answer |
| ------------------------------------------ | ----------- |
| "How long does generation take?"           | "About 2-3 minutes for all 5 posts with images." |
| "What if the AI writes something wrong?"   | "Every post passes through a Quality Gate (0–10) and a Compliance Checker that auto-fixes banned terms. Nothing publishes without human approval." |
| "Can we customize the rules?"              | "Yes — the Brand Voice tier is fully editable. Ethical language rules are toggleable. Legal rules are locked by design." |
| "What AI models does it use?"              | "GPT-4o for campaign planning, GPT-4o-mini for writing and quality, Gemini for image generation." |
| "How much does it cost per campaign?"      | "Roughly $0.05–0.15 per campaign. At scale, 20 campaigns/month costs about $2–3 in AI. Hosting adds ~$5-10/month." |
| "Can it post directly to social media?"    | "Not yet — currently ZIP downloads. Direct API publishing is Phase 1 of our roadmap." |
| "What languages does it support?"          | "English, Spanish, French, Portuguese. One-click translation from the calendar." |
| "What news sources does it scan?"          | "12 trusted domains: Reuters, AP, BBC, Guardian, Al Jazeera, UNODC, Polaris, HRW, IJM, ILO, Thorn." |
| "Is the system secure?"                    | "The MVP runs locally. Phase 1 adds JWT auth, RBAC, and a secrets vault before any cloud deployment." |
| "How do we measure real impact?"           | "Phase 2 adds live social API connections and UTM-tagged hotline links." |

---

### Remember

- 🔴 **Start strong** — lead with the problem, not the tech
- 🎯 **Calendar is the star** — spend the most time there (75 sec)
- 🛡️ **Emphasize ethics** — the Rules page is your differentiator
- 🚀 **Close with the roadmap** — show what's possible with support

**1-888-373-7888 · Text BeFree to 233733**
