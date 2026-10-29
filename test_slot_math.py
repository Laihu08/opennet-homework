"""Tests for scoring, circular reels, and the saved solution."""

from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from generate import construct
from slot_math import (CONFIG_PATHS, DEFAULT_CONFIG, analytic_rtp, evaluate,
                       load_configuration, score_screen, validate_reels, windows)


class SlotMathTests(unittest.TestCase):
    def test_no_match(self):
        self.assertEqual(score_screen(((0, 1, 2), (1, 2, 3), (2, 3, 4))), 0)

    def test_each_block_location_and_multiplier(self):
        for symbol, ticks in enumerate((5, 11, 20, 60, 100)):
            for left in range(2):
                for top in range(2):
                    with self.subTest(symbol=symbol, left=left, top=top):
                        # An alternating background cannot itself form a block.
                        screen = [[(symbol + 1 + (col + row) % 2) % 5
                                   for row in range(3)] for col in range(3)]
                        for col in (left, left + 1):
                            for row in (top, top + 1):
                                screen[col][row] = symbol
                        self.assertEqual(score_screen(screen), ticks)

    def test_overlapping_blocks_add(self):
        self.assertEqual(score_screen(((0, 0, 1), (0, 0, 2), (0, 0, 3))), 10)

    def test_full_screen_policy(self):
        self.assertEqual(score_screen(((0, 0, 0),) * 3), 45)
        self.assertEqual(score_screen(((0, 0, 0),) * 3, "replace-blocks"), 25)
        self.assertEqual(score_screen(((4, 4, 4),) * 3), 900)

    def test_circular_windows(self):
        self.assertEqual(windows([0, 1, 2, 3]),
                         [(0, 1, 2), (1, 2, 3), (2, 3, 0), (3, 0, 1)])
        self.assertEqual(windows([4]), [(4, 4, 4)])

    def test_duplicate_windows_retain_stop_probability(self):
        stats = evaluate([[0], [0, 0, 0, 1], [0]])
        self.assertEqual(stats.histogram, {0: 1, 10: 2, 45: 1})
        self.assertEqual(stats.outcomes, 4)
        self.assertEqual(stats.rtp, Fraction(13, 16))
        self.assertEqual(stats.win_rate, Fraction(3, 4))
        self.assertEqual(stats.profit_rate, Fraction(1, 4))

    def test_analytical_formula_on_small_asymmetric_reels(self):
        cases = [
            [[0], [0, 0, 0, 1], [0]],
            [[1, 1, 2], [2, 2, 1, 1], [1, 1, 1, 2, 2]],
            [[4, 4, 0], [4, 0, 4, 4], [4, 4, 4, 0, 0]],
        ]
        for reels in cases:
            for policy in ("additive", "replace-blocks"):
                with self.subTest(reels=reels, policy=policy):
                    self.assertEqual(analytic_rtp(reels, policy), evaluate(reels, policy).rtp)

    def test_invalid_reels_and_policy(self):
        for reels in ([], [[0], [0]], [[0], [], [0]], [[0], [5], [0]],
                      [[0], [True], [0]], [[0], [0.0], [0]]):
            with self.subTest(reels=reels), self.assertRaises(ValueError):
                validate_reels(reels)
        with self.assertRaises(ValueError):
            evaluate([[0], [0], [0]], "unknown")
        with self.assertRaises(ValueError):
            construct("unknown")

    def test_configuration_policy(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "reels.json"
            configuration = {"reels": [[0], [0], [0]]}
            path.write_text(json.dumps(configuration))
            self.assertEqual(load_configuration(path)[1], "additive")
            configuration["full_screen_policy"] = "replace-blocks"
            path.write_text(json.dumps(configuration))
            self.assertEqual(load_configuration(path)[1], "replace-blocks")
            self.assertEqual(load_configuration(path, "additive")[1], "additive")
            configuration["full_screen_policy"] = "unknown"
            path.write_text(json.dumps(configuration))
            with self.assertRaises(ValueError):
                load_configuration(path)

    def test_committed_solution_and_reproducibility(self):
        expected = {
            "additive": (91728, Fraction(32405, 45864)),
            "replace-blocks": (755776, Fraction(348333, 377888)),
        }
        for policy, (outcomes, win_rate) in expected.items():
            with self.subTest(policy=policy):
                reels, saved_policy = load_configuration(CONFIG_PATHS[policy])
                self.assertEqual(saved_policy, policy)
                regenerated, _ = construct(policy)
                self.assertEqual(regenerated, reels)
                self.assertTrue(all(set(reel) == set(range(5)) for reel in reels))
                stats = evaluate(reels, policy)
                self.assertEqual(stats.outcomes, outcomes)
                self.assertEqual(stats.rtp, Fraction(19, 20))
                self.assertEqual(stats.win_rate, win_rate)
                self.assertEqual(analytic_rtp(reels, policy), stats.rtp)
                self.assertTrue(stats.meets_targets)

    def test_cli_verifies_saved_policy_and_rejects_wrong_rule(self):
        script = Path(__file__).with_name("slot_math.py")
        cases = [
            ([], 0, "additive"),
            ([str(CONFIG_PATHS["replace-blocks"])], 0, "replace-blocks"),
            ([str(DEFAULT_CONFIG), "--full-screen-policy", "replace-blocks"],
             1, "replace-blocks"),
        ]
        for arguments, exit_code, policy in cases:
            with self.subTest(arguments=arguments):
                result = subprocess.run([sys.executable, str(script), *arguments],
                                        capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, exit_code, result.stderr)
                self.assertIn(f"Payout policy: {policy}", result.stdout)
                self.assertIn("PASS" if exit_code == 0 else "FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()
