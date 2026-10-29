# Positive-payout win rates

[Back to README](../../README.md)

## Definition

- Win -> total payout greater than zero.
- One spin with multiple matching patterns -> count once.
- Counts -> [payout histogram derivation](payout-histograms.md).
- Target -> `55 / 100 = 11 / 20`.

## Additive

```text
All outcomes = 91,728
Zero-payout outcomes = 26,918

Winning outcomes = 91,728 - 26,918 = 64,810
Win rate = 64,810 / 91,728
         = 32,405 / 45,864       (divide both by 2)
         = 70.65454387%         (rounded)
```

Cross-check: add every positive-payout row.

```text
3,372 + 25,250 + 108 + 6,048 + 836 + 2 + 30
      + 27,216 + 1,460 + 420 + 54 + 14 = 64,810
```

Exact target comparison:

```text
64,810 / 91,728 >= 11/20
64,810 x 20 >= 91,728 x 11
1,296,200 >= 1,009,008 -> PASS
```

## Replacement

```text
All outcomes = 755,776
Zero-payout outcomes = 59,110

Winning outcomes = 755,776 - 59,110 = 696,666
Win rate = 696,666 / 755,776
         = 348,333 / 377,888    (divide both by 2)
         = 92.17889957%        (rounded)
```

Cross-check: add every positive-payout row.

```text
8,860 + 170,178 + 220 + 41,216 + 220 + 2 + 473,984
      + 2 + 1,516 + 436 + 26 + 6 = 696,666
```

Exact target comparison:

```text
696,666 / 755,776 >= 11/20
696,666 x 20 >= 755,776 x 11
13,933,320 >= 8,313,536 -> PASS
```

## Why not add pattern probabilities?

- One screen can match several blocks.
- Adding match probabilities -> can count one spin several times.
- Evaluator -> checks `total payout > 0` once per stop combination.
- Payouts below the bet -> still count here; see [net-profit rates](profit-rates.md).
