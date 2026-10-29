"""Find reel run lengths that give 95% RTP and at least 55% wins."""

import argparse
from itertools import product
import json
from pathlib import Path

from slot_math import CONFIG_PATHS, MULTIPLIER_TICKS, POLICIES, analytic_rtp, evaluate


OUTER_ZERO_RUNS = range(20, 61)


def expand_runs(lengths):
    """Expand run lengths into an ordered reel."""
    return [symbol for symbol, length in enumerate(lengths) for _ in range(length)]


def construct(policy="additive"):
    if policy not in POLICIES:
        raise ValueError(f"Unknown payout policy: {policy}")
    full_screen_extra = 5 if policy == "additive" else 1
    # Search one run per symbol, with at least two positions per run.
    # This lets every symbol form a winning block.
    for outer_zero_run in OUTER_ZERO_RUNS:
        outer_runs = (outer_zero_run, 2, 2, 2, 2)
        outer = expand_runs(outer_runs)
        length = len(outer)
        pairs = [count - 1 for count in outer_runs]
        triples = [count - 2 for count in outer_runs]

        # Rearrange RTP = 19/20 into sum(c_s * n_s) = rhs. See README.
        coefficients = [weight * (4 * pair * length + full_screen_extra * triple**2)
                        - 19 * length**2
                        for weight, pair, triple in zip(MULTIPLIER_TICKS, pairs, triples)]
        rhs = sum(weight * (4 * pair * length + 2 * full_screen_extra * triple**2)
                  for weight, pair, triple in zip(MULTIPLIER_TICKS, pairs, triples))
        # Positive run lengths cannot make an all-nonpositive sum equal rhs > 0.
        if all(coefficient <= 0 for coefficient in coefficients):
            continue

        for other_runs in product(range(2, 16), repeat=4):
            numerator = rhs - sum(c * n for c, n in zip(coefficients[1:], other_runs))
            zero_run, remainder = divmod(numerator, coefficients[0])
            if remainder or not 2 <= zero_run <= 250:
                continue
            middle_runs = (zero_run, *other_runs)
            reels = [outer.copy(), expand_runs(middle_runs), outer.copy()]
            stats = evaluate(reels, policy)
            if stats.meets_targets and analytic_rtp(reels, policy) == stats.rtp:
                return reels, middle_runs
    raise RuntimeError("No solution within this search family; expand the bounds.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--full-screen-policy", choices=POLICIES, default="additive")
    args = parser.parse_args()
    reels, middle_runs = construct(args.full_screen_policy)
    output = args.output if args.output is not None else CONFIG_PATHS[args.full_screen_policy]
    # Write one array per reel.
    body = '{\n  "full_screen_policy": ' + json.dumps(args.full_screen_policy)
    body += ',\n  "reels": [\n' + ',\n'.join(
        '    ' + json.dumps(reel) for reel in reels) + '\n  ]\n}\n'
    output.write_text(body)
    print(f"Payout policy: {args.full_screen_policy}")
    print(f"Outer run lengths: {[reels[0].count(symbol) for symbol in range(5)]}")
    print(f"Middle run lengths: {list(middle_runs)}")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
