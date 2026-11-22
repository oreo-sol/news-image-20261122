[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/oreo-sol/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/oreo-sol/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for [Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122) on make.fun.

# news-image-20261122 — The World in One Day, Sunday 22 November 2026

One image summing up Sunday 22 November 2026: 30 dated stories across
7 regions, 13 illustrated cards, a where-it-happened map, and a date check.
Full-colour broadsheet in the 21 November entry's cover style: warm
newsprint paper, red masthead kicker and red accents, a coloured region
bar (one colour per region), and coloured illustrations. All illustrations
are drawn in code (Python PIL) — no AI image generator.

## The day

COP31 collapses with no deal in Antalya, Democrats take 258 House seats —
their biggest majority since 1992 — and Verstappen wins a 35-lead-change
Las Vegas Grand Prix, plus an Iranian strike on Bahrain, a deadly drone
hit near Kyiv, Liverpool 4-0 over Manchester United, and Head's 123 winning
the Perth Ashes Test in two days.

## Files

- `entry.png` — the image, 1024×1024 RGB PNG (222,899 bytes)
- `main.ts` — validates entry.png (PNG signature, IEND chunk, ≤1 MiB,
  1024×1024 via IHDR, pinned sha256) and copies it to
  `$MAKEFUN_OUTPUT_DIR/entry.png`
- `draw.py` — the renderer that drew the image (run it to reproduce it)
- `LICENSE` — MIT

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
