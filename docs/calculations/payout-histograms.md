# Counts for every payout

[Back to README](../../README.md)

- Histogram -> number of stop combinations paying each tick amount.
- One tick -> [bet / 20](payout-ticks.md).
- Production verifier -> visits every combination and scores its screen.
- Below -> a separate count calculation for these particular run-based reels.

## 1. Count outcomes for one symbol

| Name | Meaning |
| --- | --- |
| `L` | Length of either outer reel |
| `A` | Outer matching-pair count |
| `T` | Outer matching-triple count |
| `G = L - T - 2` | Outer stops with no matching pair for this symbol |
| `m = middle run - 2` | Middle matching-triple count |
| `w` | Symbol payout in ticks |

- Middle pair-only windows -> exactly two: `s s next` and `previous s s`.
- Middle triple windows -> `m` copies of `s s s`.
- Every middle window belongs to one such group because all runs have length at least two.

For one pair-only middle window:

```text
No block:   (L - A)^2
One block:  2 x A x (L - A)
Two blocks: A^2
```

For one triple middle window:

- Each outer reel -> `G` no-pair stops, `2` one-pair stops, `T` triple stops.
- Two independent outer stops -> multiply their counts.

```text
No block:     G^2
One block:    2 x G x 2 = 4G
Two blocks:   2 x G x T + 2 x 2 = 2GT + 4
Three blocks: 2 x 2 x T = 4T
Full screen:  T^2
```

Combine the two pair-only windows and the `m` triple windows:

```text
C0 = 2(L - A)^2 + mG^2
C1 = 4A(L - A) + 4mG
C2 = 2A^2 + m(2GT + 4)
C3 = 4mT
CF = mT^2
```

| Count | Payout |
| --- | --- |
| `C0` | `0` |
| `C1` | `w` |
| `C2` | `2w` |
| `C3` | `3w` |
| `CF` | `9w` additive; `5w` replacement |

## 2. Additive: calculate the counts

Symbol 0: `L = 28`, `A = 19`, `T = 18`, `G = 28 - 18 - 2 = 8`, `m = 86 - 2 = 84`.

```text
C0 = 2(28 - 19)^2 + 84 x 8^2       = 162 + 5,376   = 5,538
C1 = 4 x 19 x 9 + 4 x 84 x 8       = 684 + 2,688   = 3,372
C2 = 2 x 19^2 + 84(2 x 8 x 18 + 4) = 722 + 24,528  = 25,250
C3 = 4 x 84 x 18                                  = 6,048
CF = 84 x 18^2                                    = 27,216
```

Other symbols: `A = 1`, `T = 0`, `G = 28 - 0 - 2 = 26`.

```text
C0 = 2 x 27^2 + m x 26^2 = 1,458 + 676m
C1 = 4 x 1 x 27 + 4m x 26 = 108 + 104m
C2 = 2 x 1^2 + m(0 + 4) = 2 + 4m
C3 = CF = 0
```

| Symbol | `m` | `C0` | `C1` | `C2` |
| --- | ---: | ---: | ---: | ---: |
| 1 | `2 - 2 = 0` | `1,458 + 676 x 0 = 1,458` | `108 + 104 x 0 = 108` | `2 + 4 x 0 = 2` |
| 2 | `9 - 2 = 7` | `1,458 + 676 x 7 = 6,190` | `108 + 104 x 7 = 836` | `2 + 4 x 7 = 30` |
| 3 | `15 - 2 = 13` | `1,458 + 676 x 13 = 10,246` | `108 + 104 x 13 = 1,460` | `2 + 4 x 13 = 54` |
| 4 | `5 - 2 = 3` | `1,458 + 676 x 3 = 3,486` | `108 + 104 x 3 = 420` | `2 + 4 x 3 = 14` |

```text
Zero-payout outcomes = 5,538 + 1,458 + 6,190 + 10,246 + 3,486
                     = 26,918
```

Map counts to their tick amounts:

| Payout ticks | Stop combinations | Ticks x count |
| ---: | ---: | ---: |
| 0 | 26,918 | `0 x 26,918 = 0` |
| 5 | 3,372 | `5 x 3,372 = 16,860` |
| 10 | 25,250 | `10 x 25,250 = 252,500` |
| 11 | 108 | `11 x 108 = 1,188` |
| 15 | 6,048 | `15 x 6,048 = 90,720` |
| 20 | 836 | `20 x 836 = 16,720` |
| 22 | 2 | `22 x 2 = 44` |
| 40 | 30 | `40 x 30 = 1,200` |
| 45 | 27,216 | `45 x 27,216 = 1,224,720` |
| 60 | 1,460 | `60 x 1,460 = 87,600` |
| 100 | 420 | `100 x 420 = 42,000` |
| 120 | 54 | `120 x 54 = 6,480` |
| 200 | 14 | `200 x 14 = 2,800` |
| **Sum** | **91,728** | **1,742,832** |

## 3. Replacement: calculate the counts

Symbol 0: `L = 56`, `A = 47`, `T = 46`, `G = 56 - 46 - 2 = 8`, `m = 226 - 2 = 224`.

```text
C0 = 2(56 - 47)^2 + 224 x 8^2        = 162 + 14,336    = 14,498
C1 = 4 x 47 x 9 + 4 x 224 x 8        = 1,692 + 7,168   = 8,860
C2 = 2 x 47^2 + 224(2 x 8 x 46 + 4)  = 4,418 + 165,760 = 170,178
C3 = 4 x 224 x 46                                     = 41,216
CF = 224 x 46^2                                       = 473,984
```

Other symbols: `A = 1`, `T = 0`, `G = 56 - 0 - 2 = 54`.

```text
C0 = 2 x 55^2 + m x 54^2 = 6,050 + 2,916m
C1 = 4 x 1 x 55 + 4m x 54 = 220 + 216m
C2 = 2 x 1^2 + m(0 + 4) = 2 + 4m
C3 = CF = 0
```

| Symbol | `m` | `C0` | `C1` | `C2` |
| --- | ---: | ---: | ---: | ---: |
| 1 | `2 - 2 = 0` | `6,050 + 2,916 x 0 = 6,050` | `220 + 216 x 0 = 220` | `2 + 4 x 0 = 2` |
| 2 | `2 - 2 = 0` | `6,050 + 2,916 x 0 = 6,050` | `220 + 216 x 0 = 220` | `2 + 4 x 0 = 2` |
| 3 | `8 - 2 = 6` | `6,050 + 2,916 x 6 = 23,546` | `220 + 216 x 6 = 1,516` | `2 + 4 x 6 = 26` |
| 4 | `3 - 2 = 1` | `6,050 + 2,916 x 1 = 8,966` | `220 + 216 x 1 = 436` | `2 + 4 x 1 = 6` |

```text
Zero-payout outcomes = 14,498 + 6,050 + 6,050 + 23,546 + 8,966
                     = 59,110
```

| Payout ticks | Stop combinations | Ticks x count |
| ---: | ---: | ---: |
| 0 | 59,110 | `0 x 59,110 = 0` |
| 5 | 8,860 | `5 x 8,860 = 44,300` |
| 10 | 170,178 | `10 x 170,178 = 1,701,780` |
| 11 | 220 | `11 x 220 = 2,420` |
| 15 | 41,216 | `15 x 41,216 = 618,240` |
| 20 | 220 | `20 x 220 = 4,400` |
| 22 | 2 | `22 x 2 = 44` |
| 25 | 473,984 | `25 x 473,984 = 11,849,600` |
| 40 | 2 | `40 x 2 = 80` |
| 60 | 1,516 | `60 x 1,516 = 90,960` |
| 100 | 436 | `100 x 436 = 43,600` |
| 120 | 26 | `120 x 26 = 3,120` |
| 200 | 6 | `200 x 6 = 1,200` |
| **Sum** | **755,776** | **14,359,744** |

## 4. Reproduce with the actual evaluator

Run from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
from slot_math import evaluate, load_configuration

for name in ("reels.json", "reels_replace_blocks.json"):
    reels, policy = load_configuration(Path(name))
    stats = evaluate(reels, policy)
    print(name, policy)
    for ticks, count in stats.histogram.items():
        print(ticks, count, ticks * count)
    print("Outcomes:", stats.outcomes)
    print("Total ticks:", sum(t * c for t, c in stats.histogram.items()))
PY
```

Next: [RTP](rtp-results.md), [win rate](win-rates.md), and [net-profit rate](profit-rates.md).
