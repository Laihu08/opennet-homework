# Why the constant is 48232

- The middle run lengths are `n0` through `n4`.
- A run of length `n` supplies `n - 1` matching pairs and `n - 2` matching triples.
- Expanding those two terms produces a constant for each symbol.

## Expand one symbol

```text
w × [4 × A × 28 × (n - 1) + 5 × T² × (n - 2)]

= w × (4 × A × 28 + 5 × T²) × n
  - w × (4 × A × 28 + 10 × T²)
```

- `w`: payout ticks; `[5, 11, 20, 60, 100]` for symbols 0–4.
- `4`: four block positions.
- `A`: matching-pair stops on an outer reel.
- `28`: stops on the unused outer reel for each block.
- `T²`: matching-triple stops on both outer reels.
- `10 = 2 × 5`: two positions lost from a triple run, times the additive full-screen bonus.
- Outer pair counts: `[19, 1, 1, 1, 1]`.
- Outer triple counts: `[18, 0, 0, 0, 0]`.

## Calculate each constant

| Symbol | Substitution | Calculation | Constant |
| --- | --- | --- | ---: |
| 0 | `5 × (4 × 19 × 28 + 10 × 18²)` | `5 × (2128 + 3240)` | 26840 |
| 1 | `11 × (4 × 1 × 28 + 10 × 0²)` | `11 × 112` | 1232 |
| 2 | `20 × (4 × 1 × 28 + 10 × 0²)` | `20 × 112` | 2240 |
| 3 | `60 × (4 × 1 × 28 + 10 × 0²)` | `60 × 112` | 6720 |
| 4 | `100 × (4 × 1 × 28 + 10 × 0²)` | `100 × 112` | 11200 |

```text
26840 + 1232 + 2240 + 6720 + 11200 = 48232
```

## Why it is on the right

```text
Σ w × (4 × A × 28 + 5 × T²) × n - 48232
    = 14896 × (n0 + n1 + n2 + n3 + n4)

Σ [w × (4 × A × 28 + 5 × T²) - 14896] × n
    = 48232
```

- `14896 = 19 × 28²` comes from the target RTP `19/20`.
- The `19` in the zero-pair count comes from `20 - 1`; it is unrelated to the target numerator.
- `48232` is an algebraic constant, not the payout of a screen.

[Full RTP equation](rtp-equation.md) · [Back to README](../../README.md)
