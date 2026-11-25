# news-image-20261125 v02 — Evening Edition

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Jhoni1098/news-image-20261125-v02/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Jhoni1098/news-image-20261125-v02/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for [news-image-20261125](https://make.fun/bounty/news-image-20261125)
— one front page summing up the world news of Wednesday, 25 November 2026.
Version 2 (evening edition): built after v01 to cover the big stories that
broke later in the day. `main.py` (Python 3.13, standard library only) draws
the page pixel by pixel and writes a deterministic 1024×1024 PNG to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).

## The day's news in this image

1. **Strait of Hormuz** — Iran's Revolutionary Guards say two oil tankers
   struck naval mines on an unauthorised route early Wednesday, exploded and
   caught fire; the claim was not independently confirmed. Brent jumped
   past $93 a barrel.
2. **Ras Tanura** — the Houthis claim a strike on Saudi Arabia's largest
   refinery, with satellite images showing thick black smoke; Riyadh says
   it shot down four drones over the site.
3. **Savasleyka** — Ukraine says it struck the Russian air base, knocking
   out three MiG-31 jets and two Su-34 bombers.
4. **Tariffs** — the U.S. proposes new Section 301 tariffs on 14 trading
   partners after a probe into excess factory capacity: China faces 20%
   more, the EU 15%; levies could start in January.
5. **U.S. economy** — October PCE inflation 3.8%, core PCE 3.3% (highest in
   three years); Q3 GDP revised up to 4.3%. The Dow held above 50,000
   after a 1,100-point intraday plunge; the Nasdaq fell.
6. **Solomon Islands** — security treaty with Australia names Canberra the
   islands' main security partner and bars foreign military bases;
   Australia pledges $490m over a decade.
7. **Space** — Shenzhou-24 docks with the Tiangong station carrying
   Muhammad Zeeshan Ali, Pakistan's first astronaut and the first foreign
   guest aboard China's space station.
8. **Sudan** — monitors say RSF drone strikes killed 19 civilians and
   wounded 20 in two cities.

Sources: Reuters, AP, Just Security, ISW — all events reported on
Wednesday, 25 November 2026.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Two runs write byte-identical output. No network, no randomness.

## License

MIT — see [LICENSE](LICENSE).
