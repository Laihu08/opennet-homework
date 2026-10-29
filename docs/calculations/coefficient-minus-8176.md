# Why the coefficient of n3 is -8176

- `n3`: length of symbol 3's middle run.
- Rule: additive payouts.

## Inputs

| Input | Value | Source |
| --- | ---: | --- |
| Payout ticks `w` | 60 | `3 × 20` |
| Outer reel length `L` | 28 | `20 + 2 + 2 + 2 + 2` |
| Symbol 3 pair count `A` | 1 | Outer run length `2 - 1` |
| Symbol 3 triple count `T` | 0 | Outer run length `2 - 2` |
| Block count | 4 | Four 2×2 patterns |
| Full-screen extra `k` | 5 | Additive bonus |
| Target baseline | 14896 | `19 × 28²`, from RTP `19/20` |

## Calculation

```text
coefficient = w × (4 × A × L + k × T²) - 19 × L²

            = 60 × (4 × 1 × 28 + 5 × 0²) - 19 × 28²
            = 60 × (112 + 0) - 14896
            = 6720 - 14896
            = -8176
```

- `28` in the block term counts stops on the unused outer reel.
- No full-screen contribution: neither outer reel has a triple of symbol 3.
- Adding one symbol 3 to its middle run adds `6720` aggregate payout ticks and `14896` required target ticks.
- The difference contributes `-8176n3` to the rearranged equation.
- This negative coefficient is a shortfall relative to the target, not a negative payout.
- The `19` in `19 × 28²` is the target numerator, not the zero-pair count.

[Full RTP equation](rtp-equation.md) · [Back to README](../../README.md)
