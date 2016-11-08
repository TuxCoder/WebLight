import unittest
from app.animation.audio_visulizer import AudioVisulizer


class Test(unittest.TestCase):
    def test_interpolate_value(self):
        self.assertEqual(AudioVisulizer._interpolate_value(0, 1, 0.7), 0.7)

        self.assertAlmostEqual(AudioVisulizer._interpolate_value(2, 8, 0.333333), 2 + 2, delta=0.00001)

        def test_sum_array(self):
            array = [0, 1, 5, 3, 0, 1, 4, 8, 3, 0, 1, 4, 7, 3, 1, 4, 6, 7, 2, 4]

            self.assertEqual(AudioVisulizer._sum_array(array, 0, 1), .5)

            self.assertEqual(AudioVisulizer._sum_array(array, 0, .5), .125)

            self.assertEqual(AudioVisulizer._sum_array(array, 1, 2), 3)

            self.assertEqual(AudioVisulizer._sum_array(array, 0.5, 2.25),
                             (1 / 2 - 1 / 8) + 3 + (5 + 5 - 2 * .25) / 2 * .25)

            self.assertEqual(AudioVisulizer._sum_array(array, 0, len(array) - 1), sum(array) - 4 / 2)
