# Payout ticks and targets

[Back to README](../../README.md)

## Given rules

- Bet -> 100 units in the assignment's example.
- Symbols -> `0, 1, 2, 3, 4`.
- Block multipliers -> `0.25, 0.55, 1, 3, 5`.
- Full-screen multiplier -> `5` times the symbol payout.
- RTP target -> `95 / 100 = 19 / 20`.
- Minimum win rate -> `55 / 100 = 11 / 20`.

## Why 20 ticks per bet?

```text
0.25 = 1/4
0.55 = 11/20
1 = 1/1; 3 = 3/1; 5 = 5/1

Smallest shared denominator = LCM(4, 20, 1) = 20
1 tick = bet / 20
At bet 100: 1 tick = 100 / 20 = 5 units
```

| Symbol | Multiplier | Ticks per block | Payout at bet 100 |
| --- | ---: | ---: | ---: |
| 0 | 0.25 | `0.25 x 20 = 5` | `5 x 5 = 25` |
| 1 | 0.55 | `0.55 x 20 = 11` | `11 x 5 = 55` |
| 2 | 1 | `1 x 20 = 20` | `20 x 5 = 100` |
| 3 | 3 | `3 x 20 = 60` | `60 x 5 = 300` |
| 4 | 5 | `5 x 20 = 100` | `100 x 5 = 500` |

- Positive payout -> more than `0` ticks.
- Break even -> exactly `20` ticks, or one bet.
- Net profit -> more than `20` ticks.
- Integer ticks -> no decimal rounding while adding payouts.

Example: one zero block at bet 100.

```text
Gross payout = 100 x 0.25 = 25
Net result = 25 - 100 = -75
```

## Why four blocks?

```text
Screen size = 3 rows x 3 columns
Block size = 2 rows x 2 columns

Possible starting rows = 3 - 2 + 1 = 2
Possible starting columns = 3 - 2 + 1 = 2
Block positions = 2 x 2 = 4
Total winning patterns = 4 blocks + 1 full screen = 5
```

## Full-screen payout

- Additive -> all four blocks plus the full-screen award.
- Replacement -> only the full-screen award.
- Both -> interpretation choices; the assignment does not resolve stacking.

| Rule | Symbol-0 full screen in ticks | Payout at bet 100 |
| --- | ---: | ---: |
| Additive | `(4 + 5) x 5 = 45` | `45 x 5 = 225` |
| Replacement | `5 x 5 = 25` | `25 x 5 = 125` |

## Why does the analytical formula use 5 or 1?

- Its block term already includes four blocks on a full screen.
- Additive extra -> `9 - 4 = 5` symbol payouts.
- Replacement extra -> `5 - 4 = 1` symbol payout.
- The extra `1` is a formula adjustment; the actual replacement award is `5`.

Next: [matching pairs and triples](pair-triple-counts.md).
