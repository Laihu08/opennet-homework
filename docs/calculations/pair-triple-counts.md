# Matching pairs and triples

[Back to README](../../README.md)

## Where the counts come from

- Configuration choice -> one consecutive run per symbol.
- Every run -> at least two positions.
- Neighboring runs -> different symbols, including the circular `4 -> 0` boundary.
- No matching pair or triple crosses a run boundary.

```text
Run: 0 0 0 0

Pair starts:   positions 1, 2, 3 -> 4 - 1 = 3
Triple starts: positions 1, 2    -> 4 - 2 = 2

Run length n:
Pair starts   = n - 1
Triple starts = n - 2
```

- These formulas apply to this run structure.
- An all-identical circular reel would need different counts: every stop matches.

## Additive configuration

- Saved runs -> left/right `[20, 2, 2, 2, 2]`; middle `[86, 2, 9, 15, 5]`.
- Reel lengths -> [28, 117, 28](stop-combinations.md).

| Symbol | Outer run | Outer pairs | Outer triples | Middle run | Middle pairs | Middle triples |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 20 | `20 - 1 = 19` | `20 - 2 = 18` | 86 | `86 - 1 = 85` | `86 - 2 = 84` |
| 1 | 2 | `2 - 1 = 1` | `2 - 2 = 0` | 2 | `2 - 1 = 1` | `2 - 2 = 0` |
| 2 | 2 | `2 - 1 = 1` | `2 - 2 = 0` | 9 | `9 - 1 = 8` | `9 - 2 = 7` |
| 3 | 2 | `2 - 1 = 1` | `2 - 2 = 0` | 15 | `15 - 1 = 14` | `15 - 2 = 13` |
| 4 | 2 | `2 - 1 = 1` | `2 - 2 = 0` | 5 | `5 - 1 = 4` | `5 - 2 = 3` |

## Replacement configuration

- Saved runs -> left/right `[48, 2, 2, 2, 2]`; middle `[226, 2, 2, 8, 3]`.
- Reel lengths -> [56, 241, 56](stop-combinations.md).

| Symbol | Outer run | Outer pairs | Outer triples | Middle run | Middle pairs | Middle triples |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 48 | `48 - 1 = 47` | `48 - 2 = 46` | 226 | `226 - 1 = 225` | `226 - 2 = 224` |
| 1 | 2 | `2 - 1 = 1` | `2 - 2 = 0` | 2 | `2 - 1 = 1` | `2 - 2 = 0` |
| 2 | 2 | `2 - 1 = 1` | `2 - 2 = 0` | 2 | `2 - 1 = 1` | `2 - 2 = 0` |
| 3 | 2 | `2 - 1 = 1` | `2 - 2 = 0` | 8 | `8 - 1 = 7` | `8 - 2 = 6` |
| 4 | 2 | `2 - 1 = 1` | `2 - 2 = 0` | 3 | `3 - 1 = 2` | `3 - 2 = 1` |

## Counts -> probabilities

```text
Probability = matching stops / total reel stops

Additive, symbol 0:
Outer pair probability   = 19/28
Outer triple probability = 18/28
Middle pair probability  = 85/117
Middle triple probability = 84/117

Replacement, symbol 0:
Outer pair probability   = 47/56
Outer triple probability = 46/56
Middle pair probability  = 225/241
Middle triple probability = 224/241
```

- Bottom-pair counts -> same as top-pair counts; shift every stop by one position.
- Reels stop independently -> multiply probabilities across reels.
- Symbols within a column -> linked by the reel order; not independent.

```text
Additive, one specified zero block:
P = (19/28) x (85/117) = 1,615 / 3,276

Replacement, one specified zero block:
P = (47/56) x (225/241) = 10,575 / 13,496
```

Next: [RTP calculation](rtp-results.md) and [full-screen frequency](full-screen-frequency.md).
