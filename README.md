# Navran

Landing site for **Navran** — an AI-powered awareness platform. Tagline: *Navigate what's hidden.*

## Stack

- **Next.js 14** (app router)
- **Framer Motion** — all animation
- **Tailwind CSS** — styling, with brand palette exposed as CSS variables
- **next/font** — Fraunces (display) + Instrument Sans (body), preloaded and self-hosted by Next

## Run it

```bash
npm install
npm run dev
```

Visit `http://localhost:3000`.

## Structure

```
app/
  layout.tsx      fonts, metadata, grain overlay
  page.tsx        section composition
  globals.css     palette vars, reduced-motion rules, drop cap, grain
components/
  Hero.tsx        compass star assembly + letter-by-letter wordmark
  Problem.tsx     scroll-blur headline + tile grid "hidden → seen"
  WhatWeDo.tsx    three staggered columns with line-drawn icons
  Articles.tsx    horizontal parallax rail (drag on mobile)
  Mission.tsx     drop-capped editorial paragraph + pull quote
  BuiltBy.tsx     quiet single-sentence credits
  Footer.tsx      CTA button, email form, N·A·V·R·A·N letter-by-letter
  Cursor.tsx      spring-following saffron dot, hover expand
  CompassStar.tsx stroke-drawn brand mark
lib/
  useReducedMotion.ts
```

## Motion choices

- **One motion library.** Framer Motion throughout; no GSAP mixing. Consistency
  over flexibility.
- **Stagger, don't explode.** Every group animates with staggered children so
  elements cascade in order — never a wall of fade-ins landing together.
- **Transform + opacity only.** No animated layout properties. Scroll-driven
  work uses `useScroll` + `useTransform`, and every tile in the Problem grid is
  its own component so hooks stay legal.
- **Hero entrance** (page load): compass rays draw themselves in sequence via
  `pathLength`, inner dot scales in, then the wordmark reveals letter by letter
  with letter-spacing expanding from `-0.12em` to `-0.04em`. Tagline fades in
  last.
- **Problem reveal** (scroll): a full-width grid of 18×8 tiles, each one
  thresholded by its diagonal position. As the section progresses, tiles cross
  from Twilight to Saffron along the diagonal — invisible becoming visible.
  The editorial sentence above sharpens from `blur(14px)` to `0`.
- **Article rail**: desktop uses a scroll-linked horizontal parallax
  (`useTransform` on scroll progress → `x`). Mobile uses native snap scrolling.
- **Pull quote**: saffron left border draws from top to bottom via `scaleY`,
  then words fade in one by one.
- **CTA button**: saffron fill sweeps in from the left via `scaleX` on a
  cubic-bezier spring; label color inverts from Dawn to Twilight.
- **Footer wordmark**: `N·A·V·R·A·N` letters stagger in when the footer
  enters view — each a small vertical rise.
- **Custom cursor**: saffron dot, spring-followed (stiffness 260, damping 28),
  expands and goes translucent over `a`, `button`, `input`, and any element
  with `data-cursor-target`. Disabled on touch, on narrow viewports, and
  whenever `prefers-reduced-motion` is set.
- **Reduced motion**: `globals.css` collapses all durations to `0.01ms` when
  the user requests reduced motion. Custom cursor also silently disables.

## Where to edit copy

| Surface | File | What to change |
|---|---|---|
| Hero tagline | `components/Hero.tsx` | `Navigate what's hidden` |
| Problem headline | `components/Problem.tsx` | The "Harm hides…" paragraph |
| Three pillars | `components/WhatWeDo.tsx` | `items` array |
| Dispatches | `components/Articles.tsx` | `articles` array |
| Mission paragraph | `components/Mission.tsx` | First `<motion.p>` |
| Pull quote | `components/Mission.tsx` | `quote` const |
| Credits sentence | `components/BuiltBy.tsx` | Single paragraph |
| CTA + newsletter | `components/Footer.tsx` | Headline, button, form copy |

## Brand tokens

Set in `tailwind.config.ts` and `app/globals.css`:

```
dawn       #FBF7ED   page background
parchment  #F2EBD9   secondary surface
saffron    #C67C3E   primary accent
clay       #A85A3A   warm grounding
twilight   #3D2B5C   hidden / punctuation
ink        #2B2419   body text
```

Fraunces: weights 300 / 400, italic variants used for emphasis.
Instrument Sans: 400 / 500 / 600.
