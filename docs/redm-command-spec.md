# redM Command — Product Spec

> Captured from team mockup. Admin / operator interface for the Navran awareness
> platform's social-media content loop. Powered by Austin AI Hub.

## Summary

redM Command is the internal tool that turns verified trafficking news into a
scheduled, compliance-checked, human-approved content calendar across
Instagram, X, Facebook, and LinkedIn. The loop:

1. **Intelligence** auto-scans news sources for qualifying stories.
2. **AI** generates a week of posts for the selected story, with quality scores.
3. A **Content Volunteer** reviews, edits, and approves each post.
4. Posts are scheduled, dispatched, and their impact (reach, hotline clicks)
   is tracked.

Always visible header: **National Human Trafficking Hotline — 1-888-373-7888
— Text BEFREE to 233733.**

---

## Left-hand navigation

```
Workspace
├── Content Calendar          (5)
├── Intelligence              (3)
├── Impact Tracker
├── Content Library
Configure
├── Content Rules
├── Social Accounts
├── Team                      (2)
├── System Settings
```

Status chip: **System Online** (top), **Backend offline — demo mode** (bottom).
System version: `V3.0.0`.

---

## Dashboard header

- **Next Awareness Day** — *World Day Against Trafficking in Persons* —
  *100 days — auto-campaign ready*
- **Active user card** — avatar, name (e.g., "Sarah M."), role
  (*Content Volunteer*)

### This Week's Mission

Cards display the originating news story for the active campaign:

- Headline: *DOJ Charges 12 in Multi-State Labor Trafficking Ring*
- Source: *Reuters · Verified · Campaign active*

Week summary KPIs:

| Metric         | Example | Notes                          |
| -------------- | ------- | ------------------------------ |
| Reached        | 24.5K   | Cumulative impressions         |
| Hotline Clicks | 847     | Attributable via tracked links |
| Posts Ready    | 5/5     | Approved vs. scheduled         |
| Streak         | 14d     | Consecutive days posted        |

---

## Content Calendar

Range header: `Apr 21 – 25, 2026`. Primary action: **Approve All**.

Campaign provenance banner:

> Campaign generated from
> *DOJ Announces Charges Against 12 in Multi-State Labor Trafficking Ring*
> Reuters · Scanned 2 hours ago · AI confidence: High
> `[Pick Different Story]`

### Post card anatomy

Each day renders one card:

```
┌──────────────────────────────────────────────────────────────────┐
│ Mon  Apr 21       12:00 PM    AI: 12 PM CT    [Breaking] 8.4     │
│ ────────────────────────────────────────────────────────────     │
│ FEDERAL PROSECUTORS INDICT 12 IN MAJOR TRAFFICKING OPERATION     │
│ Multi-state labor trafficking ring dismantled by DOJ.            │
│ Source: Reuters · Verified                                       │
│                                                                  │
│ AI-Generated · Human-Approved · rM                               │
│                                                                  │
│ <post copy>                                                      │
│                                                                  │
│ Audience: General Public                                         │
│ IG: 287/2200 · X: 287/280 !                                      │
│ [IG] [X]           Compliant          [Caption] [Approve] [Edit] │
└──────────────────────────────────────────────────────────────────┘
```

Field reference:

| Element              | Meaning                                                                 |
| -------------------- | ----------------------------------------------------------------------- |
| Day + date           | Mon · Apr 21                                                            |
| Scheduled time       | Author-set + suggested (`AI: 12 PM CT`)                                 |
| Post type tag        | `Breaking`, `Stat Card`, `Explainer`, `Action`, `Hope`                  |
| Quality score        | `0–10`, AI confidence in the generated copy (e.g., `8.4`, `9.1`)        |
| Headline / hook      | Capitalized title surface                                               |
| Source line          | Publisher + verified flag                                               |
| Attribution footer   | `AI-Generated · Human-Approved · rM`                                    |
| Audience             | `General Public`, `Educators`, `Parents`, `College Students`, etc.      |
| Character counters   | Per-platform, `used/limit`. A `!` indicates over-limit on that platform |
| Platform icons       | `IG`, `X`, `FB`, `LI` — present icons = post targets                    |
| Compliance badge     | `Compliant`, or flagged with auto-fix suggestion                        |
| Card actions         | `Caption`, `Approve` / `Approved`, `Edit`                               |

### Post type examples captured

| Day       | Type        | Score | Audience          | Platforms    | Status     |
| --------- | ----------- | ----- | ----------------- | ------------ | ---------- |
| Mon 4/21  | Breaking    | 8.4   | General Public    | IG, X        | Needs approve (X over limit) |
| Tue 4/22  | Stat Card   | 9.1   | Educators         | IG, X, LI    | Needs approve |
| Wed 4/23  | Explainer   | ✓     | Parents           | IG, FB, LI   | Approved   |
| Thu 4/24  | Action      | ✓     | College Students  | IG, X, FB    | Approved   |
| Fri 4/25  | Hope        | ✓     | General Public    | IG, LI       | Approved   |

Footer: *AI-Generated Content · Human-Approved · Powered by Austin AI Hub*

---

## Activity feed (right rail)

Live audit log:

```
Just now     Sarah approved Explainer post
2 min ago    Sarah approved Action post
3 min ago    Sarah approved Hope post
3 min ago    AI generated 5 posts — quality avg: 8.4
14 min ago   Auto-scan found 3 new stories
45 min ago   Compliance: "rescued" in Explainer — auto-fixed
1 hour ago   System connected V3.0.0
```

Feed surfaces four event classes: **approval**, **generation**,
**scan**, and **compliance** (auto-fix or manual escalation).

---

## Compliance

- **Forbidden / flagged terms** example: `rescued` → auto-corrected to a
  survivor-first alternative.
- **Per-platform limits** enforced at card level with visible over-count
  markers.
- **Source verification required** — every post ties to a Verified story.
- **Human approval required** — AI never posts without sign-off.

---

## Keyboard shortcuts

| Key        | Action            |
| ---------- | ----------------- |
| `J` / `K`  | Navigate posts    |
| `A`        | Approve           |
| `E`        | Edit              |
| `C`        | Caption           |
| `1` – `5`  | Jump to day       |
| `?`        | All shortcuts     |

---

## Open questions / to clarify with the team

- **Is "redM" a sub-brand or the same as Navran?** Landing brand is Navran;
  internal tool is branded redM. Confirm relationship for copy and legal.
- **Demo mode vs. live mode** — how is the backend-offline state reached
  and communicated to volunteers?
- **Story qualification rules** — what causes a story to surface in
  Intelligence? Rubric needed for consistency.
- **Compliance dictionary ownership** — who owns the "rescued → …"
  mapping? Legal? Survivor advisory council?
- **Per-audience voice guidelines** — do Educators / Parents / College
  Students each have their own voice spec the AI reads from?
- **Attribution line `rM`** — is it rendered in posted assets or only
  internally?
- **Impact attribution** — how are Hotline Clicks measured? Tracked
  redirect, UTM, direct reporting from Polaris?
