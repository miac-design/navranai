# Docs

Internal documentation for the Navran platform and its operator tooling
(RedM Command Center V3).

## Product specs

| File                                                    | What it covers                                                                    |
| ------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [`redm-command-spec.md`](./redm-command-spec.md)        | Operator UI spec: Content Calendar, Intelligence, Impact, Compliance.             |
| [`redm-mvp-v3-readme.md`](./redm-mvp-v3-readme.md)      | Setup / quickstart for the distributed RedM MVP V3 ZIP (FastAPI backend + HTML). |
| [`redm-presentation-guide.md`](./redm-presentation-guide.md) | 5-minute demo script for stakeholders; includes roadmap and Q&A.              |

## Scripts

The team's distribution packaging script lives at the repo root:
[`../package_for_distribution.py`](../package_for_distribution.py) — builds
`RedM_MVP_V3_Distribution.zip`, stripping API keys, databases, and
runtime artifacts.

## How to add more docs

- **Frontend specs** → `docs/frontend/<name>.md`
- **Backend specs** → `docs/backend/<name>.md`
- **Design assets / screenshots** → `docs/assets/`
- **Exports from Figma / Notion / Google Docs** → either paste as Markdown or
  drop the PDF into the relevant subfolder

Markdown renders inline on GitHub. PDFs and images are downloadable but also
display in-browser from the file view.

## A note on repo layout

This `navranai` repo currently hosts two products side by side:

1. **RedM Command Center V3** (repo root) — FastAPI backend
   (`backend/`), single-page dashboard (`design_v3.html`), walkthroughs,
   and the `package_for_distribution.py` packaging script. The root
   `README.md` covers this product.
2. **Navran awareness site** (`app/`, `components/`, `lib/`) —
   Next.js 14 marketing site + dispatch reader built in this session.

Both products share one `package.json` (Node tooling for Next.js) and one
Python `backend/requirements.txt`. This is workable short-term but will
get awkward as each product grows — particularly around CI, deploy
targets (Vercel for the Next.js app vs. a Python host for FastAPI), and
lockfile churn. When the time comes, splitting into two repos
(`navranai-site` and `redm-command`) is the cleaner move.
