"""Check reel payouts and win rate using exact arithmetic."""

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


# One tick is bet / 20. Keep payouts as integers to avoid rounding.
MULTIPLIER_TICKS = (5, 11, 20, 60, 100)
TARGET_RTP = Fraction(19, 20)
MIN_WIN_RATE = Fraction(11, 20)
POLICIES = ("additive", "replace-blocks")
DEFAULT_CONFIG = Path(__file__).with_name("reels.json")
CONFIG_PATHS = {
    "additive": DEFAULT_CONFIG,
    "replace-blocks": Path(__file__).with_name("reels_replace_blocks.json"),
}


def validate_reels(reels):
    if not isinstance(reels, (list, tuple)) or len(reels) != 3:
        raise ValueError("Exactly three reels are required.")
    for reel in reels:
        if not isinstance(reel, (list, tuple)) or not reel:
            raise ValueError("Each reel must be a nonempty sequence.")
        if any(type(symbol) is not int or symbol not in range(5) for symbol in reel):
            raise ValueError("Symbols must be integers from 0 through 4.")


def windows(reel):
    """Return one column per stop, including duplicates."""
    return [tuple(reel[(stop + row) % len(reel)] for row in range(3))
            for stop in range(len(reel))]


def score_screen(columns, policy="additive"):
    """Return payout ticks for three columns of three symbols each."""
    if policy not in POLICIES:
        raise ValueError(f"Unknown payout policy: {policy}")
    symbol = columns[0][0]
    full_screen = all(value == symbol for column in columns for value in column)
    if full_screen and policy == "replace-blocks":
        return 5 * MULTIPLIER_TICKS[symbol]

    ticks = 0
    for column, row in product(range(2), repeat=2):
        symbol = columns[column][row]
        if (symbol == columns[column][row + 1]
                == columns[column + 1][row] == columns[column + 1][row + 1]):
            ticks += MULTIPLIER_TICKS[symbol]
    if full_screen:
        ticks += 5 * MULTIPLIER_TICKS[columns[0][0]]
    return ticks


@dataclass(frozen=True)
class Statistics:
    histogram: dict[int, int]

    @property
    def outcomes(self):
        return sum(self.histogram.values())

    @property
    def rtp(self):
        return Fraction(sum(ticks * count for ticks, count in self.histogram.items()),
                        20 * self.outcomes)

    @property
    def win_rate(self):
        return Fraction(sum(count for ticks, count in self.histogram.items() if ticks > 0),
                        self.outcomes)

    @property
    def profit_rate(self):
        return Fraction(sum(count for ticks, count in self.histogram.items() if ticks > 20),
                        self.outcomes)

    @property
    def meets_targets(self):
        return self.rtp == TARGET_RTP and self.win_rate >= MIN_WIN_RATE


def evaluate(reels, policy="additive"):
    """Score every combination of reel stops."""
    validate_reels(reels)
    if policy not in POLICIES:
        raise ValueError(f"Unknown payout policy: {policy}")
    histogram = Counter(score_screen(screen, policy)
                        for screen in product(*(windows(reel) for reel in reels)))
    return Statistics(dict(sorted(histogram.items())))


def analytic_rtp(reels, policy="additive"):
    """Calculate RTP from pair and triple probabilities.

    Expected payouts add even when patterns overlap. Win probabilities do
    not, so evaluate() counts winning outcomes separately.
    """
    validate_reels(reels)
    if policy not in POLICIES:
        raise ValueError(f"Unknown payout policy: {policy}")
    pairs, triples = [], []
    for reel in reels:
        views = windows(reel)
        pairs.append([Fraction(sum(a == b == s for a, b, _ in views), len(reel))
                      for s in range(5)])
        triples.append([Fraction(sum(a == b == c == s for a, b, c in views), len(reel))
                        for s in range(5)])
    # The block term already pays 4x on a full screen. Add 1x for a
    # replacement payout of 5x, or another 5x for the additive rule.
    full_screen_extra = 5 if policy == "additive" else 1
    return sum((Fraction(MULTIPLIER_TICKS[s], 20) * (
        2 * pairs[1][s] * (pairs[0][s] + pairs[2][s])
        + full_screen_extra * triples[0][s] * triples[1][s] * triples[2][s])
        for s in range(5)), Fraction(0))


def load_configuration(path, policy_override=None):
    configuration = json.loads(path.read_text())
    policy = configuration.get("full_screen_policy", "additive")
    if policy not in POLICIES:
        raise ValueError(f"Unknown saved payout policy: {policy}")
    policy = policy_override if policy_override is not None else policy
    if policy not in POLICIES:
        raise ValueError(f"Unknown payout policy: {policy}")
    reels = configuration["reels"]
    validate_reels(reels)
    return reels, policy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("configuration", nargs="?", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--full-screen-policy", choices=POLICIES,
                        help="Override the rule saved in the configuration.")
    args = parser.parse_args()
    try:
        reels, policy = load_configuration(args.configuration, args.full_screen_policy)
        stats = evaluate(reels, policy)
        expected = analytic_rtp(reels, policy)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.error(str(error))
    if expected != stats.rtp:
        raise RuntimeError("Enumeration disagrees with analytical RTP.")
    print(f"Payout policy: {policy}")
    print(f"Reel lengths: {[len(reel) for reel in reels]}")
    print(f"Stop combinations: {stats.outcomes:,}")
    print(f"RTP: {stats.rtp} = {float(stats.rtp):.8%}")
    print(f"Expected payout per 100 units: {100 * stats.rtp}")
    print(f"Win rate (payout > 0): {stats.win_rate} = {float(stats.win_rate):.8%}")
    print(f"Net-profit rate (payout > bet): {stats.profit_rate} = {float(stats.profit_rate):.8%}")
    print("Analytical RTP agrees with exhaustive enumeration.")
    print(f"Requirements under stated assumptions: {'PASS' if stats.meets_targets else 'FAIL'}")
    return 0 if stats.meets_targets else 1


if __name__ == "__main__":
    raise SystemExit(main())
