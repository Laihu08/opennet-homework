# Search bounds and reel lengths

[Back to README](../../README.md) | [All calculations](README.md)

**Given, chosen, or calculated?**

| Item | Source |
| --- | --- |
| Five symbols; fixed multipliers | Assignment |
| 95% RTP; at least 55% wins | Assignment |
| One consecutive run per symbol | My search design |
| Independent, uniform stops | Modeling assumption |
| Identical outer sequences | My search design |
| Outer runs `[z, 2, 2, 2, 2]` | My search design |
| Outer zero range `20..60` | Chosen search bounds |
| Middle nonzero run range `2..15` | Chosen search bounds |
| Middle zero range `2..250` | Chosen search bounds |
| Specific accepted runs | Search results |
| RTP and win rate | Exact calculations on those results |

- The bounds are not derived from the assignment.
- Two positions per run -> every symbol can form a matching pair.
- One run per symbol -> simple pair and triple counts.
- First valid candidate -> returned immediately.
- No result within the bounds -> expand the search; no impossibility claim.
- No claim that the chosen reel lengths are minimal.

**Search order**

1. Pick `z` in increasing order: `20, 21, ..., 60`.
2. Form the two outer reels: `[z, 2, 2, 2, 2]`.
3. Derive the RTP equation for that outer configuration and payout policy.
4. Skip equations whose coefficients are all nonpositive and whose right side is positive.
5. Enumerate `(n1, n2, n3, n4)` using `product(range(2, 16), repeat=4)`.
6. Solve for `n0`; reject fractional or out-of-range answers.
7. Check the actual RTP and win rate; cross-check analytical RTP.
8. Save the first candidate that passes.

- In the tuple enumeration, `n4` changes fastest.
- The other run lengths are enumerated choices; the zero run is solved.

**Main rule: first candidate is rejected**

- Outer zero run -> `z = 20`.
- First middle nonzero tuple -> `(2, 2, 2, 2)`.
- Equation -> [additive derivation](rtp-equation.md).

```text
n0 = (48232 + 13664×2 + 12656×2 + 8176×2 + 3696×2) / 3844
   = (48232 + 27328 + 25312 + 16352 + 7392) / 3844
   = 124616 / 3844

3844 × 32 = 123008
124616 - 123008 = 1608 remainder
```

- Fractional run length -> rejected.
- The search continues to the next tuple.

**Main rule: accepted middle zero run = 86**

- First passing outer zero run -> `20`.
- First passing nonzero tuple -> `(2, 9, 15, 5)`.

```text
n0 = (48232 + 13664×2 + 12656×9 + 8176×15 + 3696×5) / 3844

13664 × 2  = 27328
12656 × 9  = 113904
8176  × 15 = 122640
3696  × 5  = 18480

Numerator = 48232 + 27328 + 113904 + 122640 + 18480
          = 330584

n0 = 330584 / 3844 = 86
```

```text
Left runs:   [20, 2, 2,  2, 2]
Middle runs: [86, 2, 9, 15, 5]
Right runs:  [20, 2, 2,  2, 2]
```

- The exact win-rate check also passes: [70.65454387%](win-rates.md).

**Replacement rule: accepted middle zero run = 226**

- First passing outer zero run -> `48`.
- First passing nonzero tuple -> `(2, 2, 8, 3)`.
- Equation -> [replacement derivation](replacement-equation.md).

```text
3636 n0 - 57120 n1 - 55104 n2 - 46144 n3 - 37184 n4 = 116584

n0 = (116584 + 57120×2 + 55104×2 + 46144×8 + 37184×3) / 3636

57120 × 2 = 114240
55104 × 2 = 110208
46144 × 8 = 369152
37184 × 3 = 111552

Numerator = 116584 + 114240 + 110208 + 369152 + 111552
          = 821736

n0 = 821736 / 3636 = 226
```

```text
Left runs:   [48,  2, 2, 2, 2]
Middle runs: [226, 2, 2, 8, 3]
Right runs:  [48,  2, 2, 2, 2]
```

- The exact win-rate check also passes: [92.17889957%](win-rates.md).
- Run lengths are expanded into actual symbol arrays in the JSON files.
- Length sums and outcome counts -> [stop combinations](stop-combinations.md).

**Reproduce**

From the repository root:

```bash
python3 generate.py
python3 generate.py --full-screen-policy replace-blocks
```
