# Why the coefficient of n4 is -3696

- `n4`: length of symbol 4's middle run.
- Rule: additive payouts.

## Inputs

| Input | Value | Source |
| --- | ---: | --- |
| Payout ticks `w` | 100 | `5 × 20` |
| Outer reel length `L` | 28 | `20 + 2 + 2 + 2 + 2` |
| Symbol 4 pair count `A` | 1 | Outer run length `2 - 1` |
| Symbol 4 triple count `T` | 0 | Outer run length `2 - 2` |
| Block count | 4 | Four 2×2 patterns |
| Full-screen extra `k` | 5 | Additive bonus |
| Target baseline | 14896 | `19 × 28²`, from RTP `19/20` |

## Calculation

```text
coefficient = w × (4 × A × L + k × T²) - 19 × L²

            = 100 × (4 × 1 × 28 + 5 × 0²) - 19 × 28²
            = 100 × (112 + 0) - 14896
            = 11200 - 14896
            = -3696
```

- `28` in the block term counts stops on the unused outer reel.
- No full-screen contribution: neither outer reel has a triple of symbol 4.
- Adding one symbol 4 to its middle run adds `11200` aggregate payout ticks and `14896` required target ticks.
- The difference contributes `-3696n4` to the rearranged equation.
- This negative coefficient is a shortfall relative to the target, not a negative payout.
- The `19` in `19 × 28²` is the target numerator, not the zero-pair count.

[Full RTP equation](rtp-equation.md) · [Back to README](../../README.md)
