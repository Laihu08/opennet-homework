# Reel lengths and stop combinations

[Back to README](../../README.md)

## Additive configuration

- Saved run lengths -> configuration values found by the search.
- Reel lengths and outcome count -> derived below.

```text
Left length   = 20 + 2 + 2 + 2 + 2 = 28
Middle length = 86 + 2 + 9 + 15 + 5 = 117
Right length  = 20 + 2 + 2 + 2 + 2 = 28

Stop combinations = 28 x 117 x 28
                  = 3,276 x 28
                  = 91,728
```

## Replacement configuration

```text
Left length   = 48 + 2 + 2 + 2 + 2 = 56
Middle length = 226 + 2 + 2 + 8 + 3 = 241
Right length  = 48 + 2 + 2 + 2 + 2 = 56

Stop combinations = 56 x 241 x 56
                  = 13,496 x 56
                  = 755,776
```

## Why multiply?

- Choose one left stop, one middle stop, and one right stop.
- Independent, uniform stops -> every combination has the same probability.
- Main configuration -> each combination has probability `1 / 91,728`.
- Replacement configuration -> each combination has probability `1 / 755,776`.
- Different stops may show the same screen -> keep every combination.
- These are stop counts, not counts of distinct screen images.
- Enumeration cost -> `O(left length x middle length x right length)`.

Next: [counts for every payout](payout-histograms.md).
