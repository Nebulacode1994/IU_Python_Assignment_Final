import numpy as np
import pandas as pd

class DataValidationError(Exception):
    # user defined exception for data processing errors
    """Custom exception for handling data-related error"""
    pass
class DataProcessor:
    # base class for processing functions
    """ Base class providing a template for data processig objects"""
    def __init__(self, data):
        self.data = data
        
class MathEngine(DataProcessor):
    # inheritance example: mathengine inherits fro dataprocessor 
    """ Engine for performing least squares and deviation calculations"""
    def calculate_least_squares(self, train_y, ideal_y):
        # calculates the sum of squares as per assignemnt criterion
       """Calcualtes the sum of squared errors (sse) between two datasets"""
       return ((train_y - ideal_y)** 2).sum()
    def get_threshold(self, train_y, ideal_y):
        """calculate the max deviation multiplied by sqrt(2)"""
        max_diff = np.max(np.abs(train_y - ideal_y))
        return max_diff * np.sqrt(2)