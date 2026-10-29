# Net-profit rates

[Back to README](../../README.md)

## Definition

- One bet -> [20 ticks](payout-ticks.md).
- Net profit -> payout greater than `20` ticks.
- Break even -> payout exactly `20` ticks.
- Net loss -> payout below `20` ticks, including zero.
- Counts below -> [payout histograms](payout-histograms.md).

## Additive

Only these payouts exceed one bet:

```text
Ticks:     22   40      45      60     100   120   200
Outcomes:   2   30   27,216   1,460   420    54    14

Profitable outcomes = 2 + 30 + 27,216 + 1,460 + 420 + 54 + 14
                    = 29,196

Profit rate = 29,196 / 91,728
            = 811 / 2,548       (divide both by 36)
            = 31.82888540%      (rounded)
```

Reconcile all outcomes:

```text
Positive payout below bet = 3,372 + 25,250 + 108 + 6,048 = 34,778
All net losses = 26,918 zero payouts + 34,778 partial returns = 61,696
Break-even outcomes = 836
Profitable outcomes = 29,196

61,696 + 836 + 29,196 = 91,728
```

If the 55% target meant net profit:

```text
29,196 x 20 = 583,920
91,728 x 11 = 1,009,008
583,920 < 1,009,008 -> FAIL
```

## Replacement

```text
Ticks:     22      25     40     60    100   120   200
Outcomes:   2   473,984    2   1,516   436    26     6

Profitable outcomes = 2 + 473,984 + 2 + 1,516 + 436 + 26 + 6
                    = 475,972

Profit rate = 475,972 / 755,776
            = 16,999 / 26,992   (divide both by 28)
            = 62.97791938%      (rounded)
```

Reconcile all outcomes:

```text
Positive payout below bet = 8,860 + 170,178 + 220 + 41,216 = 220,474
All net losses = 59,110 zero payouts + 220,474 partial returns = 279,584
Break-even outcomes = 220
Profitable outcomes = 475,972

279,584 + 220 + 475,972 = 755,776
```

If the 55% target meant net profit:

```text
475,972 x 20 = 9,519,440
755,776 x 11 = 8,313,536
9,519,440 >= 8,313,536 -> PASS
```

- Results use each configuration's saved payout policy.
- Clarify both the win definition and the payout policy before choosing the configuration.
