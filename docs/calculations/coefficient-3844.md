# Why the coefficient of n0 is 3844

- `n0`: number of zeros in the middle reel's zero run.
- Rule: additive payouts.

## Inputs

| Input | Value | Source |
| --- | ---: | --- |
| Payout ticks `w` | 5 | `0.25 × 20` |
| Outer reel length `L` | 28 | `20 + 2 + 2 + 2 + 2` |
| Zero-pair count `A` | 19 | `20 - 1` |
| Zero-triple count `T` | 18 | `20 - 2` |
| Block count | 4 | Four 2×2 patterns |
| Full-screen extra `k` | 5 | Additive bonus |
| Target baseline | 14896 | `19 × 28²`, from RTP `19/20` |

## Calculation

```text
coefficient = w × (4 × A × L + k × T²) - 19 × L²

            = 5 × (4 × 19 × 28 + 5 × 18²) - 19 × 28²
            = 5 × (2128 + 1620) - 14896
            = 5 × 3748 - 14896
            = 18740 - 14896
            = 3844
```

- `28` in the block term counts stops on the unused outer reel.
- The first `5` is payout ticks; the inner `5` is the full-screen bonus.
- `19` inside the block term is a pair count. The final `19` is the target numerator.
- Adding one zero to the middle run adds `18740` aggregate payout ticks and `14896` required target ticks.
- The difference contributes `+3844n0` to the rearranged RTP equation.

[Full RTP equation](rtp-equation.md) · [Back to README](../../README.md)
