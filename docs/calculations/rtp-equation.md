# Main RTP equation

- Rule: additive payouts.
- Outer runs: `[20, 2, 2, 2, 2]`; each outer reel has `L = 28` stops.
- Middle runs: `[n0, n1, n2, n3, n4]`; `N = n0 + n1 + n2 + n3 + n4`.
- Each run is at least two symbols long and has different symbols on either side.

## Inputs

| Symbol | Multiplier | Payout ticks `w` | Outer run | Matching pairs `A` | Matching triples `T` |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.25 | 5 | 20 | 19 | 18 |
| 1 | 0.55 | 11 | 2 | 1 | 0 |
| 2 | 1 | 20 | 2 | 1 | 0 |
| 3 | 3 | 60 | 2 | 1 | 0 |
| 4 | 5 | 100 | 2 | 1 | 0 |

- One tick is `bet / 20`: [payout ticks](payout-ticks.md).
- A middle run `n` supplies `n - 1` matching pairs and `n - 2` matching triples: [pair and triple counts](pair-triple-counts.md).

## Count the payout ticks

For one symbol:

```text
Block ticks       = w × 4 × A × 28 × (n - 1)
Full-screen ticks = w × 5 × T² × (n - 2)
```

- `4`: four block positions.
- `A`: matching pair stops on the outer reel used by a block.
- `28`: every stop of the unused outer reel still counts.
- `n - 1`: matching pair stops on the middle reel.
- `5`: full-screen bonus multiplier, added to the block payouts.
- `T²`: matching triple stops on both independent outer reels.
- `n - 2`: matching triple stops on the middle reel.

## Set RTP to 19/20

- There are `28² × N` equally likely stop combinations.
- Divide total payout ticks by `20 × 28² × N` to obtain RTP.

```text
Σ w × [4 × A × 28 × (n - 1) + 5 × T² × (n - 2)]
-------------------------------------------------- = 19/20
                   20 × 28² × N

Σ w × [4 × A × 28 × (n - 1) + 5 × T² × (n - 2)]
    = 19 × 28² × N
    = 14896 × (n0 + n1 + n2 + n3 + n4)
```

- `14896 = 19 × 784 = 19 × 28²`.
- This `19` comes from the target `19/20`.
- The zero-pair count is also `19`, because `20 - 1 = 19`. These are separate inputs.

## Expand and collect terms

```text
w × [4 × A × 28 × (n - 1) + 5 × T² × (n - 2)]

= w × (4 × A × 28 + 5 × T²) × n
  - w × (4 × A × 28 + 10 × T²)

coefficient = w × (4 × A × 28 + 5 × T²) - 14896
constant    = w × (4 × A × 28 + 10 × T²)
```

| Symbol | Before subtracting 14896 | Final coefficient | Constant |
| --- | ---: | ---: | ---: |
| 0 | 18740 | [3844](coefficient-3844.md) | 26840 |
| 1 | 1232 | [-13664](coefficient-minus-13664.md) | 1232 |
| 2 | 2240 | [-12656](coefficient-minus-12656.md) | 2240 |
| 3 | 6720 | [-8176](coefficient-minus-8176.md) | 6720 |
| 4 | 11200 | [-3696](coefficient-minus-3696.md) | 11200 |
| Total constants | | | [48232](constant-48232.md) |

```text
18740n0 + 1232n1 + 2240n2 + 6720n3 + 11200n4 - 48232
    = 14896n0 + 14896n1 + 14896n2 + 14896n3 + 14896n4

3844n0 - 13664n1 - 12656n2 - 8176n3 - 3696n4 = 48232
```

- Negative coefficients are terms after subtracting the target baseline. They are not negative payouts.
- The equation checks RTP only. The generator separately checks win rate.

## Substitute the saved runs

```text
n1 = 2, n2 = 9, n3 = 15, n4 = 5

3844n0 = 48232 + 13664×2 + 12656×9 + 8176×15 + 3696×5
       = 48232 + 27328 + 113904 + 122640 + 18480
       = 330584

n0 = 330584 / 3844 = 86
```

- Result: `[86, 2, 9, 15, 5]`.
- [Search and saved reels](search-and-reels.md)
- [Replacement equation](replacement-equation.md)
- [Back to README](../../README.md)
