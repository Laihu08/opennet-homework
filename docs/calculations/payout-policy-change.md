# Changing the full-screen payout rule

[Back to README](../../README.md)

## Same reels, different payout rule

- Start with `reels.json`: the additive configuration.
- Change only its payout policy to `replace-blocks`.
- Stop probabilities -> unchanged.
- Full-screen payouts -> reduced.

```text
Symbol-0 full screen:
Additive ticks    = (4 + 5) x 5 = 45
Replacement ticks = 5 x 5       = 25
Reduction         = 45 - 25     = 20 ticks

At bet 100: 1 tick = 100 / 20 = 5 units
Additive payout    = 45 x 5 = 225 units
Replacement payout = 25 x 5 = 125 units
Payout reduction   = 225 - 125 = 100 units
```

- Only zero can fill the screen -> no other full-screen reductions.
- Full-screen count -> [27,216](full-screen-frequency.md).

```text
Total tick reduction = 27,216 x 20 = 544,320
Original total ticks = 1,742,832
New total ticks      = 1,742,832 - 544,320 = 1,198,512

New RTP = 1,198,512 / (20 x 91,728)
        = 1,198,512 / 1,834,560
        = 1,189 / 1,820          (divide both by 1,008)
        = 65.32967033%          (rounded)
```

Same result from the full-screen probability:

```text
Each affected spin loses one bet of payout: 20 ticks / 20 = 1
New RTP = 19/20 - 27/91
        = 1,729/1,820 - 540/1,820
        = 1,189/1,820
```

- Positive-payout rate -> unchanged; full-screen payout stays positive.
- Net-profit rate -> unchanged here; both `45` and `25` ticks exceed the `20`-tick stake.
- RTP requirement -> fails.

## Reproduce

```bash
python3 slot_math.py reels.json --full-screen-policy replace-blocks
```

- This deliberate mismatch prints `FAIL` and exits with status `1`.
- Successful target verification exits with status `0`.

## Restore 95% under the replacement rule

- Regenerate using `replace-blocks`.
- Analytical full-screen extra -> `1` instead of `5`.
- New outer runs -> `[48, 2, 2, 2, 2]`.
- New middle runs -> `[226, 2, 2, 8, 3]`.
- New saved file -> `reels_replace_blocks.json`.

```text
New total ticks = 14,359,744
New outcomes = 755,776

RTP = 14,359,744 / (20 x 755,776)
    = 19/20
    = 95% exactly
```

Derivation: [RTP results](rtp-results.md).
