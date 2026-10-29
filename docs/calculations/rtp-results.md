# Exact RTP results

[Back to README](../../README.md)

## Formula

- RTP -> expected gross payout divided by bet.
- Every stop combination -> equally likely.
- One bet -> [20 ticks](payout-ticks.md).

```text
RTP = total payout ticks / (20 x stop combinations)
```

## Additive: add the histogram payouts

Source: [every payout count and product](payout-histograms.md).

```text
Total ticks = 0 + 16,860 + 252,500 + 1,188 + 90,720 + 16,720
              + 44 + 1,200 + 1,224,720 + 87,600 + 42,000
              + 6,480 + 2,800
            = 1,742,832

Denominator = 20 x 91,728 = 1,834,560
RTP = 1,742,832 / 1,834,560
    = (19 x 91,728) / (20 x 91,728)
    = 19/20
    = 95%
```

## Replacement: add the histogram payouts

```text
Total ticks = 0 + 44,300 + 1,701,780 + 2,420 + 618,240 + 4,400
              + 44 + 11,849,600 + 80 + 90,960 + 43,600
              + 3,120 + 1,200
            = 14,359,744

Denominator = 20 x 755,776 = 15,115,520
RTP = 14,359,744 / 15,115,520
    = (19 x 755,776) / (20 x 755,776)
    = 19/20
    = 95%
```

## Independent check: expected payouts by symbol

Inputs: [pair/triple counts](pair-triple-counts.md) and [reel lengths](stop-combinations.md).

```text
L = outer reel length
A = outer pair count for this symbol
T = outer triple count for this symbol
n = middle run length
w = symbol payout in ticks
k = 5 for additive; 1 for replacement

Symbol's total ticks across all stops:
w x [4 x A x L x (n - 1) + k x T^2 x (n - 2)]
```

- `4` -> four block positions.
- `L` in the block term -> stops on the unused third reel.
- `T^2` -> matching triples on both outer reels.
- `k` -> [full-screen adjustment](payout-ticks.md#why-does-the-analytical-formula-use-5-or-1).
- Expected payouts add even when patterns overlap.

Additive substitution:

| Symbol | Block ticks | Extra full-screen ticks | Total ticks |
| --- | --- | --- | ---: |
| 0 | `5 x 4 x 19 x 28 x 85 = 904,400` | `5 x 5 x 18^2 x 84 = 680,400` | 1,584,800 |
| 1 | `11 x 4 x 1 x 28 x 1 = 1,232` | `0` | 1,232 |
| 2 | `20 x 4 x 1 x 28 x 8 = 17,920` | `0` | 17,920 |
| 3 | `60 x 4 x 1 x 28 x 14 = 94,080` | `0` | 94,080 |
| 4 | `100 x 4 x 1 x 28 x 4 = 44,800` | `0` | 44,800 |

```text
1,584,800 + 1,232 + 17,920 + 94,080 + 44,800 = 1,742,832
```

Replacement substitution:

| Symbol | Block ticks | Extra full-screen ticks | Total ticks |
| --- | --- | --- | ---: |
| 0 | `5 x 4 x 47 x 56 x 225 = 11,844,000` | `5 x 1 x 46^2 x 224 = 2,369,920` | 14,213,920 |
| 1 | `11 x 4 x 1 x 56 x 1 = 2,464` | `0` | 2,464 |
| 2 | `20 x 4 x 1 x 56 x 1 = 4,480` | `0` | 4,480 |
| 3 | `60 x 4 x 1 x 56 x 7 = 94,080` | `0` | 94,080 |
| 4 | `100 x 4 x 1 x 56 x 2 = 44,800` | `0` | 44,800 |

```text
14,213,920 + 2,464 + 4,480 + 94,080 + 44,800 = 14,359,744
```

- Symbols 1-4 -> zero outer triples, so zero full-screen contribution.
- Both totals -> match exhaustive enumeration.

## Meaning at bet 100

```text
Expected gross payout = 100 x 19/20 = 95
Expected net result   = 95 - 100 = -5
```

- Expected value -> an average over the probability model.
- Individual spin -> may pay more, less, or zero.
- No guarantee of exactly 95 returned on a particular spin or session.
