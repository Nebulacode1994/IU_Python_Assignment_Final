"""
SQLAlchemy database models module.

This module defines the three database tables required by the assignment:
1. TrainingData - 5 columns (X, Y1, Y2, Y3, Y4)
2. IdealFunctions - 51 columns (X, Y1-Y50)
3. TestResults - 4 columns (X, Y, Delta Y, No. of ideal func)
"""

from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional

Base = declarative_base()


class TrainingData(Base):
    """
    Database model for training data.
    
    Table structure as per Table 1:
    - X: x-values
    - Y1, Y2, Y3, Y4: y-values for training functions 1-4
    """
    __tablename__ = 'training_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float, nullable=False)
    y1 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)
    y3 = Column(Float, nullable=False)
    y4 = Column(Float, nullable=False)
    
    def __repr__(self):
        """String representation of TrainingData."""
        return f"<TrainingData(x={self.x}, y1={self.y1}, y2={self.y2}, y3={self.y3}, y4={self.y4})>"


class IdealFunctions(Base):
    """
    Database model for ideal functions.
    
    Table structure as per Table 2:
    - X: x-values
    - Y1 through Y50: y-values for 50 ideal functions
    """
    __tablename__ = 'ideal_functions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float, nullable=False)
    y1 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)
    y3 = Column(Float, nullable=False)
    y4 = Column(Float, nullable=False)
    y5 = Column(Float, nullable=False)
    y6 = Column(Float, nullable=False)
    y7 = Column(Float, nullable=False)
    y8 = Column(Float, nullable=False)
    y9 = Column(Float, nullable=False)
    y10 = Column(Float, nullable=False)
    y11 = Column(Float, nullable=False)
    y12 = Column(Float, nullable=False)
    y13 = Column(Float, nullable=False)
    y14 = Column(Float, nullable=False)
    y15 = Column(Float, nullable=False)
    y16 = Column(Float, nullable=False)
    y17 = Column(Float, nullable=False)
    y18 = Column(Float, nullable=False)
    y19 = Column(Float, nullable=False)
    y20 = Column(Float, nullable=False)
    y21 = Column(Float, nullable=False)
    y22 = Column(Float, nullable=False)
    y23 = Column(Float, nullable=False)
    y24 = Column(Float, nullable=False)
    y25 = Column(Float, nullable=False)
    y26 = Column(Float, nullable=False)
    y27 = Column(Float, nullable=False)
    y28 = Column(Float, nullable=False)
    y29 = Column(Float, nullable=False)
    y30 = Column(Float, nullable=False)
    y31 = Column(Float, nullable=False)
    y32 = Column(Float, nullable=False)
    y33 = Column(Float, nullable=False)
    y34 = Column(Float, nullable=False)
    y35 = Column(Float, nullable=False)
    y36 = Column(Float, nullable=False)
    y37 = Column(Float, nullable=False)
    y38 = Column(Float, nullable=False)
    y39 = Column(Float, nullable=False)
    y40 = Column(Float, nullable=False)
    y41 = Column(Float, nullable=False)
    y42 = Column(Float, nullable=False)
    y43 = Column(Float, nullable=False)
    y44 = Column(Float, nullable=False)
    y45 = Column(Float, nullable=False)
    y46 = Column(Float, nullable=False)
    y47 = Column(Float, nullable=False)
    y48 = Column(Float, nullable=False)
    y49 = Column(Float, nullable=False)
    y50 = Column(Float, nullable=False)
    
    def get_y_value(self, function_number: int) -> float:
        """
        Get y-value for a specific ideal function number.
        
        Args:
            function_number: Ideal function number (1-50)
            
        Returns:
            float: Y-value for the specified function
            
        Raises:
            ValueError: If function_number is not in range 1-50
        """
        if not 1 <= function_number <= 50:
            raise ValueError(f"Function number must be between 1 and 50, got {function_number}")
        return getattr(self, f'y{function_number}')
    
    def __repr__(self):
        """String representation of IdealFunctions."""
        return f"<IdealFunctions(x={self.x}, y1={self.y1}, ..., y50={self.y50})>"


class TestResults(Base):
    """
    Database model for test results with mapping.
    
    Table structure as per Table 3:
    - X: x-value from test data
    - Y: y-value from test data
    - Delta Y: deviation between test data and ideal function
    - Ideal Function Number: Number of the ideal function this test point was mapped to
    """
    __tablename__ = 'test_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    delta_y = Column(Float, nullable=False)
    ideal_func_number = Column(Integer, nullable=False)
    
    def __repr__(self):
        """String representation of TestResults."""
        return f"<TestResults(x={self.x}, y={self.y}, delta_y={self.delta_y}, ideal_func={self.ideal_func_number})>"


class DatabaseManager:
    """
    Database manager class for SQLite operations.
    
    This class handles database initialization, session management,
    and provides convenience methods for database operations.
    """
    
    def __init__(self, database_url: str = 'sqlite:///assignment_db.sqlite'):
        """
        Initialize the database manager.
        
        Args:
            database_url: SQLAlchemy database URL (default: sqlite:///assignment_db.sqlite)
        """
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()
    
    def _create_tables(self):
        """
        Create all database tables if they don't exist.
        
        This method creates the three required tables:
        - training_data
        - ideal_functions
        - test_results
        """
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """
        Get a new database session.
        
        Returns:
            Session: SQLAlchemy session object
        """
        return self.Session()
    
    def close(self):
        """
        Close the database engine.
        
        This should be called when done with database operations.
        """
        self.engine.dispose()

