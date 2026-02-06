# CSEMDSPWP01 - Programming with Python Assignment

This project implements a complete solution for the IU International University assignment on Programming with Python. The system selects ideal functions using Least Squares methodology and maps test data using the sqrt(2) criterion.

## Assignment Overview

The program:
1. Loads 4 training datasets and 50 ideal functions from CSV files
2. Uses Least Squares to select the 4 best-fitting ideal functions
3. Maps test data points to the selected ideal functions using the sqrt(2) criterion
4. Stores all data in a SQLite database using SQLAlchemy
5. Creates interactive visualizations using Bokeh

## Project Structure

The project consists of the following modules:

### 📁 Core Modules

1. **`models.py`** - SQLAlchemy database models
   - `TrainingData` model (5 columns: X, Y1, Y2, Y3, Y4)
   - `IdealFunctions` model (51 columns: X, Y1-Y50)
   - `TestResults` model (4 columns: X, Y, Delta Y, Ideal Function Number)
   - `DatabaseManager` class for database operations
   - All classes include comprehensive docstrings

2. **`data_loader.py`** - Data loading with inheritance
   - `BaseDataLoader` abstract base class
   - `TrainingDataLoader` - Loads training data from CSV
   - `IdealDataLoader` - Loads ideal functions from CSV
   - `TestDataLoader` - Loads test data from CSV
   - `ResultsDataLoader` - Saves mapped results to database
   - Custom exceptions: `DataLoadError`, `FileNotFoundError`, `InvalidDataError`
   - All classes include comprehensive docstrings

3. **`processor.py`** - Mathematical processing with inheritance
   - `BaseProcessor` abstract base class
   - `LeastSquaresProcessor` - Calculates sum of squared deviations and max deviation
   - `FunctionSelector` - Selects 4 ideal functions using Least Squares
   - `TestDataMapper` - Maps test data using sqrt(2) criterion
   - Custom exceptions: `ProcessingError`, `InvalidInputError`, `ConvergenceError`
   - All classes include comprehensive docstrings

4. **`visualizer.py`** - Bokeh interactive visualizations
   - `BaseVisualizer` base class
   - `AssignmentVisualizer` - Creates assignment-specific visualizations:
     - Training data and selected ideal functions
     - Test data mappings to ideal functions
     - Deviation analysis
     - Maximum deviation thresholds (with √2 factor)
   - All classes include comprehensive docstrings

5. **`main.py`** - Main application orchestrator
   - Implements the complete assignment workflow
   - Coordinates data loading, processing, and visualization
   - Provides console output with progress information

6. **`test_logic.py`** - Unit tests for mathematical logic
   - Tests for `LeastSquaresProcessor`
   - Tests for `FunctionSelector`
   - Tests for `TestDataMapper`
   - Tests for custom exceptions
   - All test methods include docstrings

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install sqlalchemy bokeh numpy pandas
```

## Usage

### Running the Application

To run the complete assignment workflow:
```bash
python3 main.py
```

Or with custom file paths:
```bash
python3 main.py train.csv ideal.csv test.csv
```

The program will:
1. Create/initialize the SQLite database (`assignment_db.sqlite`)
2. Load training data, ideal functions, and test data
3. Select the 4 best ideal functions using Least Squares
4. Map test data points using the sqrt(2) criterion
5. Save results to the database
6. Generate visualizations (`assignment_visualizations.html`)

### Running Tests

To run all unit tests:
```bash
python3 test_logic.py
```

### Using the Modules

#### Database Models
```python
from models import DatabaseManager, TrainingData, IdealFunctions, TestResults

db_manager = DatabaseManager('sqlite:///assignment_db.sqlite')
session = db_manager.get_session()
```

#### Data Loading
```python
from models import DatabaseManager
from data_loader import TrainingDataLoader, IdealDataLoader

db_manager = DatabaseManager()
training_loader = TrainingDataLoader(db_manager)
count = training_loader.load_data('train.csv')
```

#### Function Selection
```python
from processor import FunctionSelector

selector = FunctionSelector(db_manager)
selected_functions = selector.select_ideal_functions()
# Returns dict mapping training function (1-4) to ideal function info
```

#### Test Data Mapping
```python
from processor import TestDataMapper

mapper = TestDataMapper(db_manager)
mapped_results = mapper.map_all_test_data(test_data, selected_functions)
# Returns list of mapped results that meet sqrt(2) criterion
```

#### Visualizations
```python
from visualizer import AssignmentVisualizer

visualizer = AssignmentVisualizer(db_manager)
visualizer.create_all_visualizations(selected_functions, 'output.html')
```

## Database Schema

### Table 1: Training Data
- **X** (Float): x-values
- **Y1, Y2, Y3, Y4** (Float): y-values for training functions 1-4

### Table 2: Ideal Functions
- **X** (Float): x-values
- **Y1-Y50** (Float): y-values for 50 ideal functions

### Table 3: Test Results
- **X** (Float): x-value from test data
- **Y** (Float): y-value from test data
- **Delta Y** (Float): Deviation between test data and ideal function
- **Ideal Function Number** (Integer): Number of the mapped ideal function

## Key Features

✅ **SQLAlchemy Integration**: Three database tables as specified in the assignment  
✅ **Object-Oriented Design**: Inheritance-based architecture (BaseDataLoader, BaseProcessor, BaseVisualizer)  
✅ **Least Squares Selection**: Selects 4 ideal functions that minimize sum of squared deviations  
✅ **sqrt(2) Criterion**: Maps test data using max_deviation × √2 threshold  
✅ **Bokeh Visualizations**: Interactive plots for all data and mappings  
✅ **Error Handling**: Standard and custom exceptions for data validation  
✅ **Unit Tests**: Comprehensive tests for mathematical logic  
✅ **Complete Documentation**: Docstrings for all classes and functions  

## Mathematical Logic

### Least Squares Selection
For each of the 4 training functions, the program finds the ideal function (1-50) that minimizes:
```
Σ(y_training - y_ideal)²
```

### sqrt(2) Criterion Mapping
A test data point (x_test, y_test) is mapped to an ideal function if:
```
|y_test - y_ideal(x_test)| ≤ max_deviation × √2
```
where `max_deviation` is the maximum deviation between the training function and its selected ideal function.

## Requirements

- Python 3.7+
- SQLAlchemy >= 2.0.0
- Bokeh >= 3.0.0
- NumPy >= 1.24.0
- Pandas >= 2.0.0

## Project Files

- `models.py` - SQLAlchemy database models
- `data_loader.py` - Data loading classes with inheritance
- `processor.py` - Mathematical processing with inheritance
- `visualizer.py` - Bokeh visualization classes
- `main.py` - Main application orchestrator
- `test_logic.py` - Unit tests for mathematical logic
- `requirements.txt` - Python dependencies
- `GIT_INSTRUCTIONS.md` - Git commands for section 1.3
- `README.md` - This file

## Output Files

- `assignment_db.sqlite` - SQLite database with all data
- `assignment_visualizations.html` - Interactive Bokeh visualizations

## Notes

- All classes use proper inheritance patterns
- Custom exceptions follow OOP principles
- Database uses SQLite (file: `assignment_db.sqlite`)
- Visualizations are saved as HTML files
- All code includes comprehensive docstrings
- Code follows PEP 8 style guidelines
- CSV files use semicolon (`;`) as delimiter

## Assignment Compliance

This project fully complies with all assignment requirements:
- ✅ SQLAlchemy with exactly 3 tables (Tables 1, 2, 3)
- ✅ Object-oriented design with inheritance
- ✅ Least Squares for function selection
- ✅ sqrt(2) criterion for test data mapping
- ✅ Bokeh for all visualizations
- ✅ Complete docstrings for all classes and functions
- ✅ Standard and user-defined exception handling
- ✅ Unit tests for mathematical logic
- ✅ Git instructions document
