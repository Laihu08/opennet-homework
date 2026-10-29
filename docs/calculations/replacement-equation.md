# Replacement payout equation

- Configuration: [reels_replace_blocks.json](../../reels_replace_blocks.json).
- A full screen pays `5 × multiplier × bet` in total.
- The block term already pays `4×` on that screen.
- Add only `k = 1` more in the RTP formula: `4 + 1 = 5`.
- Matching blocks still pay separately on other screens.

## Inputs

- Outer runs: `[48, 2, 2, 2, 2]`.
- Outer length: `L = 48 + 2 + 2 + 2 + 2 = 56`.
- Middle runs: `[n0, n1, n2, n3, n4]`; their sum is `N`.
- Payout ticks: `w = [5, 11, 20, 60, 100]`.
- Pair counts: `A = [47, 1, 1, 1, 1]`.
- Triple counts: `T = [46, 0, 0, 0, 0]`.
- Target: `19/20`.
- Target baseline: `19 × L² = 19 × 56² = 19 × 3136 = 59584`.

## Set and rearrange RTP

```text
RTP = Σ w × [4 × A × 56 × (n - 1) + 1 × T² × (n - 2)]
      / (20 × 56² × N)

RTP = 19/20

Σ w × [4 × A × 56 × (n - 1) + T² × (n - 2)]
    = 59584 × (n0 + n1 + n2 + n3 + n4)

coefficient = w × (4 × A × 56 + T²) - 59584
constant    = w × (4 × A × 56 + 2 × T²)
```

- `4`: four block positions.
- `56`: stops of the unused outer reel for each block.
- `T²`: matching triples on both outer reels.
- `2 × T²` in the constant comes from expanding `n - 2`.

## Calculate all coefficients

```text
Zero block factor = 4 × 47 × 56 = 10528
Zero triple factor = 46² = 2116
Other block factor = 4 × 1 × 56 = 224
```

| Symbol | Weighted coefficient before target | Subtract baseline | Final coefficient |
| --- | --- | --- | ---: |
| 0 | `5 × (10528 + 2116) = 63220` | `63220 - 59584` | 3636 |
| 1 | `11 × (224 + 0) = 2464` | `2464 - 59584` | -57120 |
| 2 | `20 × (224 + 0) = 4480` | `4480 - 59584` | -55104 |
| 3 | `60 × (224 + 0) = 13440` | `13440 - 59584` | -46144 |
| 4 | `100 × (224 + 0) = 22400` | `22400 - 59584` | -37184 |

- Negative coefficients are shortfalls relative to the target baseline, not negative payouts.

## Calculate the constant

| Symbol | Substitution | Constant |
| --- | --- | ---: |
| 0 | `5 × (10528 + 2 × 2116) = 5 × 14760` | 73800 |
| 1 | `11 × (224 + 0)` | 2464 |
| 2 | `20 × (224 + 0)` | 4480 |
| 3 | `60 × (224 + 0)` | 13440 |
| 4 | `100 × (224 + 0)` | 22400 |

```text
73800 + 2464 + 4480 + 13440 + 22400 = 116584

3636n0 - 57120n1 - 55104n2 - 46144n3 - 37184n4 = 116584
```

## Solve the saved candidate

```text
n1 = 2, n2 = 2, n3 = 8, n4 = 3

3636n0 = 116584 + 57120×2 + 55104×2 + 46144×8 + 37184×3
       = 116584 + 114240 + 110208 + 369152 + 111552
       = 821736

n0 = 821736 / 3636 = 226
N = 226 + 2 + 2 + 8 + 3 = 241
```

## Check the totals

```text
Stop combinations = 56 × 241 × 56 = 755776

Total payout ticks
    = 63220×226 + 2464×2 + 4480×2 + 13440×8 + 22400×3 - 116584
    = 14359744

RTP = 14359744 / (20 × 755776)
    = 14359744 / 15115520
    = 19/20
```

- This equation checks RTP. Enumeration separately checks the win rate.
- [Main RTP equation](rtp-equation.md)
- [Search and saved reels](search-and-reels.md)
- [Back to README](../../README.md)
