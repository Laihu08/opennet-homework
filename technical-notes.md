# Technical notes

The main configuration gives exactly **95% RTP** and **70.6545% wins**.
A second configuration covers the alternative full-screen payout rule.
Python 3.10+; no dependencies.

## Run

From this folder:

```bash
python3 slot_math.py                           # Verify the main configuration
python3 slot_math.py reels_replace_blocks.json # Verify the alternative
python3 -m unittest -v                         # Run tests
python3 generate.py                           # Regenerate reels.json
python3 generate.py --full-screen-policy replace-blocks
```

The last command writes `reels_replace_blocks.json`. Both files save their payout
policy, which the verifier reads automatically.

## Rules and assumptions

- Reels are circular. A stop shows that position and the next two symbols.
- Every stop is equally likely, and the three reels stop independently.
- Matching 2×2 patterns pay separately, including overlapping blocks.
- Each payout uses the total bet. The stake is not returned separately.
- A win means any positive payout, including payouts below the bet.

The assignment does not say whether a full screen also pays its four matching
blocks. The main configuration uses **additive** payouts:
`(4 + 5) × multiplier × bet`. The alternative uses **replace-blocks**:
`5 × multiplier × bet` on a full screen. These rules need different reels.

## Configurations

Each array below gives consecutive run lengths for symbols `[0, 1, 2, 3, 4]`.
For example, `[20, 2, 2, 2, 2]` means twenty zeros, then two of each remaining
symbol, wrapping back to zero.

| Configuration | Left and right runs | Middle runs | Reel lengths |
| --- | --- | --- | --- |
| [reels.json](reels.json) | `[20, 2, 2, 2, 2]` | `[86, 2, 9, 15, 5]` | 28, 117, 28 |
| [reels_replace_blocks.json](reels_replace_blocks.json) | `[48, 2, 2, 2, 2]` | `[226, 2, 2, 8, 3]` | 56, 241, 56 |

The outer reels have the same sequence but stop independently. Every symbol
can produce block wins. Only symbol 0 can fill the full screen, because the
other symbols have runs of length two on the outer reels.

| Payout rule | Exact RTP | Win rate: payout > 0 | Net-profit rate: payout > bet | Stop combinations |
| --- | ---: | ---: | ---: | ---: |
| Additive | 19/20 | 70.65454387% | 31.82888540% | 91,728 |
| Replace blocks | 19/20 | 92.17889957% | 62.97791938% | 755,776 |

The main configuration misses the 55% target if a win must exceed the stake.
The table reports both definitions.

## Approach

A 2×2 win needs matching adjacent symbols on neighboring reels. A run of length
`n` has `n - 1` matching pairs and `n - 2` matching triples when its neighbors
are different. Long zero runs provide frequent low-paying wins; the other
lengths adjust RTP.

For symbol `s`, let `a[j,s]` be its matching-pair probability on reel `j`,
`t[j,s]` its matching-triple probability, and `m[s]` its multiplier:

```text
RTP = Σ_s m[s] × (
          2 × a[middle,s] × (a[left,s] + a[right,s])
        + k × t[left,s] × t[middle,s] × t[right,s]
      )
```

The first term covers all four blocks. On a full screen it already pays `4×`,
so `k = 5` gives the additive total of `9×`, and `k = 1` gives the replacement
total of `5×`. Expected payouts add even when patterns overlap. Win probabilities
do not, so the verifier counts winning outcomes separately.

For the main configuration, the outer reels give:

```text
L = 28                       # Reel length
A = [19, 1, 1, 1, 1]         # Matching pair counts
T = [18, 0, 0, 0, 0]         # Matching triple counts
w = [5, 11, 20, 60, 100]     # Multipliers × 20
```

Let `n[s]` be each middle run length and `N` their sum. Substituting gives:

```text
RTP = Σ_s w[s] × (4 × A[s] × L × (n[s] - 1)
                  + 5 × T[s]² × (n[s] - 2)) / (20 × L² × N)
```

Setting this to `19/20` and clearing the denominators gives:

```text
3844 n[0] - 13664 n[1] - 12656 n[2] - 8176 n[3] - 3696 n[4] = 48232
```

The generator tries outer runs `[z, 2, 2, 2, 2]` with `z` from 20 through 60.
For each, it tries middle runs of 2–15 for symbols 1–4 and solves the RTP equation
for the zero run. It keeps integer answers from 2–250, checks the win rate,
and returns the first valid configuration. The same method handles either
payout policy by changing `k`.

The search is deterministic and does not optimize reel length. Finding no
result within these bounds would not prove that the assignment is impossible.

## Verification

The verifier scores every stop combination. Repeated screens count separately
when they come from different stops. Payouts use integer ticks of `bet / 20`,
and ratios use `Fraction`, so passing does not depend on rounded decimals.

```text
Main configuration:
Total payout ticks: 1,742,832
RTP = 1,742,832 / (20 × 91,728) = 19/20
Win rate = 64,810 / 91,728 = 70.65454387%
```

A separate calculation using pair and triple probabilities must agree with
enumeration. Tests cover scoring, overlaps, wraparound, repeated stops, invalid
input, both payout policies, and regeneration of both saved configurations.

A policy flag overrides the rule stored in a file. For example:

```bash
python3 slot_math.py reels.json --full-screen-policy replace-blocks
```

This deliberately applies the other rule to the main reels: RTP becomes
65.3297%, and the verifier exits with status 1. A successful verification exits
with status 0. Enumeration takes `O(L_left × L_middle × L_right)` time.

The original requirements are in [assignment.md](assignment.md).

See the [solution walkthrough](README.md) for flowcharts and follow-up questions.
