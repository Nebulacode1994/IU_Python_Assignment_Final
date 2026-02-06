import unittest
import numpy as np
from processors import MathEngine

class TestAssignmentLogic(unittest.TestCase):
    def setUp(self):
        """ set up the engine for testing"""
        self.engine = MathEngine([])
        
    def test_least_squares_exact_match(self):
        """test if  least sqaures return 0 for identical   datasets"""
        y_train = np.array([1,2,3,4])
        y_ideal = np.array([1,2,3,4])
        result = self.engine.calculate_least_squares(y_train, y_ideal)
        self.assertEqual(result, 0, "least squares for identical data should be 0")
        
    def test_threshold_logic(self):
        """verify the threshold calculation( max deviation * sqrt(2))."""
        
        max_dev = 2.0
        dummy_ideal_y = np.array([0])
        expected = 2.0 * np.sqrt(2)
        result = self.engine.get_threshold(max_dev, dummy_ideal_y) 
        self.assertAlmostEqual(result, expected , places = 5)
        
if __name__ == '__main__':
    unittest.main()
    