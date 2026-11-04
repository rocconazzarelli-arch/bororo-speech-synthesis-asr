import unittest

import numpy as np

from bilingo.audio import add_white_noise, sanitize_filename


class AudioUtilityTests(unittest.TestCase):
    def test_filename_is_deterministic_and_safe(self) -> None:
        first = sanitize_filename("Bororo term / example")
        second = sanitize_filename("Bororo term / example")
        self.assertEqual(first, second)
        self.assertRegex(first, r"^[a-z0-9_-]+$")

    def test_different_terms_have_different_names(self) -> None:
        self.assertNotEqual(sanitize_filename("a b"), sanitize_filename("a-b"))

    def test_noise_is_reproducible_and_shape_preserving(self) -> None:
        waveform = np.full(4_000, 0.1, dtype=np.float32)
        first = add_white_noise(waveform, 20.0, np.random.default_rng(42))
        second = add_white_noise(waveform, 20.0, np.random.default_rng(42))
        np.testing.assert_allclose(first, second)
        self.assertEqual(first.shape, waveform.shape)
        self.assertEqual(first.dtype, np.float32)
        self.assertFalse(np.array_equal(first, waveform))

    def test_silent_signal_remains_silent(self) -> None:
        waveform = np.zeros(128, dtype=np.float32)
        noisy = add_white_noise(waveform, 20.0, np.random.default_rng(0))
        np.testing.assert_array_equal(noisy, waveform)


if __name__ == "__main__":
    unittest.main()
