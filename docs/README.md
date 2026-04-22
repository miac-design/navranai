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

| File                                                          | Purpose                                                                          |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [`scripts/build_distribution.py`](./scripts/build_distribution.py) | Package RedM MVP V3 for distribution — strips API keys and runtime artifacts. |

## How to add more docs

- **Frontend specs** → `docs/frontend/<name>.md`
- **Backend specs** → `docs/backend/<name>.md`
- **Design assets / screenshots** → `docs/assets/`
- **Exports from Figma / Notion / Google Docs** → either paste as Markdown or
  drop the PDF into the relevant subfolder

Markdown renders inline on GitHub. PDFs and images are downloadable but also
display in-browser from the file view.

## A note on repo boundaries

This `navranai` repo currently hosts:

1. The **Navran awareness site** — Next.js 14 marketing site and dispatch
   reader (`/app`, `/components`).
2. **Docs and specs for the RedM Command Center V3** — an adjacent Python /
   FastAPI product the team is also building (see the docs above).

The RedM V3 **code** itself lives outside this repo (local path:
`E:\Internship\Fully_functional_MVP_V3`). When that code is ready to push
to GitHub, consider a separate repository (`miac-design/redm-command` or
similar) rather than merging both products into one. Keeping the specs
here is fine — they're lightweight and useful as shared context.
