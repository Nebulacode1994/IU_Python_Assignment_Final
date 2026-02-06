"""
Data loader module with inheritance-based classes.

This module provides classes for loading CSV data into the database,
following an inheritance pattern where BaseDataLoader defines the interface
and specialized loaders inherit from it.
"""

import os
import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from models import (
    DatabaseManager,
    TrainingData,
    IdealFunctions,
    TestResults
)


class DataLoadError(Exception):
    """Base exception class for data loading errors."""
    pass


class FileNotFoundError(DataLoadError):
    """Exception raised when a required file is not found."""
    pass


class InvalidDataError(DataLoadError):
    """Exception raised when data validation fails."""
    pass


class BaseDataLoader(ABC):
    """
    Abstract base class for data loaders.
    
    This class defines the interface that all data loaders must implement.
    Subclasses should implement the load_data and validate_data methods.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the base data loader.
        
        Args:
            db_manager: DatabaseManager instance for database operations
        """
        if not isinstance(db_manager, DatabaseManager):
            raise TypeError("db_manager must be an instance of DatabaseManager")
        self.db_manager = db_manager
    
    def load_csv(self, file_path: str, delimiter: str = ';') -> pd.DataFrame:
        """
        Load data from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            delimiter: Delimiter used in CSV file (default: ';')
            
        Returns:
            pd.DataFrame: Loaded data as a pandas DataFrame
            
        Raises:
            FileNotFoundError: If the file does not exist
            InvalidDataError: If the file cannot be read or is empty
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            df = pd.read_csv(file_path, delimiter=delimiter)
            if df.empty:
                raise InvalidDataError(f"CSV file is empty: {file_path}")
            return df
        except pd.errors.EmptyDataError:
            raise InvalidDataError(f"CSV file is empty: {file_path}")
        except Exception as e:
            raise InvalidDataError(f"Error reading CSV file {file_path}: {str(e)}")
    
    @abstractmethod
    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate the loaded data.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            bool: True if data is valid
            
        Raises:
            InvalidDataError: If data validation fails
        """
        pass
    
    @abstractmethod
    def load_data(self, file_path: str) -> Any:
        """
        Load and save data to database.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Any: Result of the load operation (varies by subclass)
            
        Raises:
            FileNotFoundError: If file is not found
            InvalidDataError: If data validation fails
            DataLoadError: For other loading errors
        """
        pass


class TrainingDataLoader(BaseDataLoader):
    """
    Data loader for training data.
    
    Loads training data from CSV and saves to training_data table.
    Expected format: x;y1;y2;y3;y4
    """
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate training data format.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            bool: True if data is valid
            
        Raises:
            InvalidDataError: If data validation fails
        """
        required_columns = ['x', 'y1', 'y2', 'y3', 'y4']
        
        # Check if all required columns exist (case-insensitive)
        data_columns_lower = [col.lower() for col in data.columns]
        for req_col in required_columns:
            if req_col not in data_columns_lower:
                raise InvalidDataError(
                    f"Missing required column '{req_col}'. Found columns: {list(data.columns)}"
                )
        
        # Check for null values
        if data[['x', 'y1', 'y2', 'y3', 'y4']].isnull().any().any():
            raise InvalidDataError("Training data contains null values")
        
        return True
    
    def load_data(self, file_path: str) -> int:
        """
        Load training data from CSV and save to database.
        
        Args:
            file_path: Path to training data CSV file
            
        Returns:
            int: Number of records loaded
            
        Raises:
            FileNotFoundError: If file is not found
            InvalidDataError: If data validation fails
            DataLoadError: For other loading errors
        """
        # Load CSV
        df = self.load_csv(file_path)
        
        # Normalize column names to lowercase
        df.columns = df.columns.str.lower()
        
        # Validate data
        self.validate_data(df)
        
        # Get database session
        session = self.db_manager.get_session()
        
        try:
            # Clear existing data (optional - depends on requirements)
            session.query(TrainingData).delete()
            
            # Insert data
            records = []
            for _, row in df.iterrows():
                record = TrainingData(
                    x=float(row['x']),
                    y1=float(row['y1']),
                    y2=float(row['y2']),
                    y3=float(row['y3']),
                    y4=float(row['y4'])
                )
                records.append(record)
            
            session.add_all(records)
            session.commit()
            
            count = len(records)
            return count
            
        except Exception as e:
            session.rollback()
            raise DataLoadError(f"Error saving training data to database: {str(e)}")
        finally:
            session.close()
    
    def get_all_data(self) -> List[TrainingData]:
        """
        Retrieve all training data from database.
        
        Returns:
            List[TrainingData]: List of TrainingData records
        """
        session = self.db_manager.get_session()
        try:
            return session.query(TrainingData).order_by(TrainingData.x).all()
        finally:
            session.close()


class IdealDataLoader(BaseDataLoader):
    """
    Data loader for ideal functions.
    
    Loads ideal functions from CSV and saves to ideal_functions table.
    Expected format: x;y1;y2;...;y50
    """
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate ideal functions data format.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            bool: True if data is valid
            
        Raises:
            InvalidDataError: If data validation fails
        """
        # Check for x column
        data_columns_lower = [col.lower() for col in data.columns]
        if 'x' not in data_columns_lower:
            raise InvalidDataError(f"Missing required column 'x'. Found columns: {list(data.columns)}")
        
        # Check for y1-y50 columns
        required_y_columns = [f'y{i}' for i in range(1, 51)]
        missing_columns = []
        for req_col in required_y_columns:
            if req_col not in data_columns_lower:
                missing_columns.append(req_col)
        
        if missing_columns:
            raise InvalidDataError(
                f"Missing required columns: {missing_columns[:5]}... "
                f"(and {len(missing_columns) - 5} more)" if len(missing_columns) > 5 else ""
            )
        
        # Check for null values
        if data.isnull().any().any():
            raise InvalidDataError("Ideal functions data contains null values")
        
        return True
    
    def load_data(self, file_path: str) -> int:
        """
        Load ideal functions from CSV and save to database.
        
        Args:
            file_path: Path to ideal functions CSV file
            
        Returns:
            int: Number of records loaded
            
        Raises:
            FileNotFoundError: If file is not found
            InvalidDataError: If data validation fails
            DataLoadError: For other loading errors
        """
        # Load CSV
        df = self.load_csv(file_path)
        
        # Normalize column names to lowercase
        df.columns = df.columns.str.lower()
        
        # Validate data
        self.validate_data(df)
        
        # Get database session
        session = self.db_manager.get_session()
        
        try:
            # Clear existing data
            session.query(IdealFunctions).delete()
            
            # Insert data
            records = []
            for _, row in df.iterrows():
                # Build dictionary for all y values
                y_values = {f'y{i}': float(row[f'y{i}']) for i in range(1, 51)}
                
                record = IdealFunctions(
                    x=float(row['x']),
                    **y_values
                )
                records.append(record)
            
            session.add_all(records)
            session.commit()
            
            count = len(records)
            return count
            
        except Exception as e:
            session.rollback()
            raise DataLoadError(f"Error saving ideal functions to database: {str(e)}")
        finally:
            session.close()
    
    def get_all_data(self) -> List[IdealFunctions]:
        """
        Retrieve all ideal functions data from database.
        
        Returns:
            List[IdealFunctions]: List of IdealFunctions records
        """
        session = self.db_manager.get_session()
        try:
            return session.query(IdealFunctions).order_by(IdealFunctions.x).all()
        finally:
            session.close()
    
    def get_function_data(self, function_number: int) -> List[tuple]:
        """
        Get x-y pairs for a specific ideal function.
        
        Args:
            function_number: Ideal function number (1-50)
            
        Returns:
            List[tuple]: List of (x, y) tuples
        """
        if not 1 <= function_number <= 50:
            raise ValueError(f"Function number must be between 1 and 50, got {function_number}")
        
        session = self.db_manager.get_session()
        try:
            data = session.query(IdealFunctions).order_by(IdealFunctions.x).all()
            return [(record.x, record.get_y_value(function_number)) for record in data]
        finally:
            session.close()


class TestDataLoader(BaseDataLoader):
    """
    Data loader for test data.
    
    Loads test data from CSV. This loader only loads data into memory,
    as test data is processed and then saved via TestResultsLoader.
    Expected format: x;y
    """
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate test data format.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            bool: True if data is valid
            
        Raises:
            InvalidDataError: If data validation fails
        """
        required_columns = ['x', 'y']
        data_columns_lower = [col.lower() for col in data.columns]
        
        for req_col in required_columns:
            if req_col not in data_columns_lower:
                raise InvalidDataError(
                    f"Missing required column '{req_col}'. Found columns: {list(data.columns)}"
                )
        
        # Check for null values
        if data[['x', 'y']].isnull().any().any():
            raise InvalidDataError("Test data contains null values")
        
        return True
    
    def load_data(self, file_path: str) -> List[Dict[str, float]]:
        """
        Load test data from CSV.
        
        Args:
            file_path: Path to test data CSV file
            
        Returns:
            List[Dict[str, float]]: List of dictionaries with 'x' and 'y' keys
            
        Raises:
            FileNotFoundError: If file is not found
            InvalidDataError: If data validation fails
            DataLoadError: For other loading errors
        """
        # Load CSV
        df = self.load_csv(file_path)
        
        # Normalize column names to lowercase
        df.columns = df.columns.str.lower()
        
        # Validate data
        self.validate_data(df)
        
        # Convert to list of dictionaries
        test_data = []
        for _, row in df.iterrows():
            test_data.append({
                'x': float(row['x']),
                'y': float(row['y'])
            })
        
        return test_data


class ResultsDataLoader(BaseDataLoader):
    """
    Data loader for test results.
    
    Loads mapped test results and saves to test_results table.
    """
    
    def validate_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        Validate test results data format.
        
        Args:
            data: List of result dictionaries to validate
            
        Returns:
            bool: True if data is valid
            
        Raises:
            InvalidDataError: If data validation fails
        """
        required_keys = ['x', 'y', 'delta_y', 'ideal_func_number']
        
        for i, result in enumerate(data):
            if not isinstance(result, dict):
                raise InvalidDataError(f"Result at index {i} is not a dictionary")
            
            for key in required_keys:
                if key not in result:
                    raise InvalidDataError(f"Missing required key '{key}' in result at index {i}")
            
            # Validate ideal_func_number is in range
            if not 1 <= result['ideal_func_number'] <= 50:
                raise InvalidDataError(
                    f"Invalid ideal_func_number {result['ideal_func_number']} "
                    f"at index {i}. Must be between 1 and 50."
                )
        
        return True
    
    def load_data(self, results: List[Dict[str, Any]]) -> int:
        """
        Save test results to database.
        
        Args:
            results: List of result dictionaries with keys:
                    - x: test x value
                    - y: test y value
                    - delta_y: deviation
                    - ideal_func_number: mapped ideal function number
        
        Returns:
            int: Number of records saved
            
        Raises:
            InvalidDataError: If data validation fails
            DataLoadError: For other loading errors
        """
        # Validate data
        if not results:
            return 0
        
        self.validate_data(results)
        
        # Get database session
        session = self.db_manager.get_session()
        
        try:
            # Clear existing data
            session.query(TestResults).delete()
            
            # Insert data
            records = []
            for result in results:
                record = TestResults(
                    x=float(result['x']),
                    y=float(result['y']),
                    delta_y=float(result['delta_y']),
                    ideal_func_number=int(result['ideal_func_number'])
                )
                records.append(record)
            
            session.add_all(records)
            session.commit()
            
            count = len(records)
            return count
            
        except Exception as e:
            session.rollback()
            raise DataLoadError(f"Error saving test results to database: {str(e)}")
        finally:
            session.close()
    
    def get_all_results(self) -> List[TestResults]:
        """
        Retrieve all test results from database.
        
        Returns:
            List[TestResults]: List of TestResults records
        """
        session = self.db_manager.get_session()
        try:
            return session.query(TestResults).order_by(TestResults.x).all()
        finally:
            session.close()

