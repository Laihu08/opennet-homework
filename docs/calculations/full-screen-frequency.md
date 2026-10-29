# Full-screen frequency

[Back to README](../../README.md)

## What must match?

- All three reels must show a triple of the same symbol.
- Counts -> [matching pairs and triples](pair-triple-counts.md).
- Reels stop independently -> multiply the three counts.
- Symbols 1-4 -> outer runs have length `2`; triple count `2 - 2 = 0`.
- Therefore only symbol `0` can fill the screen in these configurations.

## Additive configuration

```text
Left zero triples   = 20 - 2 = 18
Middle zero triples = 86 - 2 = 84
Right zero triples  = 20 - 2 = 18

Full-screen outcomes = 18 x 84 x 18
                     = 324 x 84
                     = 27,216

Probability = 27,216 / 91,728
            = 27 / 91             (divide both by 1,008)
            = 29.67032967%        (rounded)
```

## Replacement configuration

```text
Left zero triples   = 48 - 2 = 46
Middle zero triples = 226 - 2 = 224
Right zero triples  = 48 - 2 = 46

Full-screen outcomes = 46 x 224 x 46
                     = 2,116 x 224
                     = 473,984

Probability = 473,984 / 755,776
            = 1,058 / 1,687       (divide both by 448)
            = 62.71487848%        (rounded)
```

## Limitation

- Long zero runs -> frequent, repetitive full screens.
- Replacement configuration -> even higher full-screen frequency.
- Validity target -> RTP and win rate; the assignment gives no variety target.
- Possible next search -> shorter zero runs and more varied arrangements.

```text
Short run: 0 0
Matching pairs = 2 - 1 = 1
Matching triples = 2 - 2 = 0
```

- Pairs without triples -> still allow blocks.
- Changing runs -> changes both RTP and win rate; solve and verify again.
