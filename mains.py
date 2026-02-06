import pandas as pd
from sqlalchemy import create_engine
from models import Base
from processors import MathEngine, DataValidationError
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def run_assignment():
    "main execution function to process data and save to SQLITE"
    """main pipleline: loads CSVs, selects ideal functions,
    maps test data, and saves results to SQLite"""
    try:
        
        # initialize database engine
        base_path = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_path, "assignment_database.db")
        engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.drop_all(engine)# clear old tables to prevent errors
        Base.metadata.create_all(engine)
        
       
        # define data source path
        folder_path = base_path

        # load Dataset CSV
        train_df = pd.read_csv(os.path.join(folder_path, "train.csv") , sep = ";", engine = 'python')
        test_df  = pd.read_csv(os.path.join(folder_path, "test.csv") , sep = ";", engine = 'python')
        ideal_df = pd.read_csv(os.path.join(folder_path, "ideal.csv") , sep = ";", engine = 'python')

        
        # use the math engine ( inheritance/ OOP requirement)
        """Initialize math logic"""
        engine_logic = MathEngine(train_df)
        selected_ideals = {}
        
        # identify the 4 best fit ideal functions using least squares
        for i in range(1,5):
            train_col = f'y{i}'
            best_fit_name = None
            min_sse = float('inf')
            
            for j in range(1,51):
                ideal_col = f'y{j}'
                sse = engine_logic.calculate_least_squares(train_df[train_col],ideal_df[ideal_col])
                if sse < min_sse:
                    min_sse = sse
                    best_fit_name = ideal_col
                    
            selected_ideals[train_col] = best_fit_name
            print(f"Best fit for{train_col} is {best_fit_name}")
        # map test data
        print("starting test data mapping...")
        test_results_list = [] 
        
        for _, row in test_df.iterrows():
            x_val,y_val = row['x'], row['y']
            best_map = None
            min_deviation = float('inf') 
            
            for train_col, ideal_col in selected_ideals.items():
                ideal_y = ideal_df.loc[ideal_df['x'] == x_val, ideal_col].values[0]
                deviation = abs(y_val - ideal_y)
                
                threshold = engine_logic.get_threshold(train_df[train_col], ideal_df[ideal_col])
            
                if deviation <= threshold:
                    if deviation < min_deviation:
                        min_deviation = deviation
                        best_map = ideal_col
                    
            if best_map:
                test_results_list.append({'x': x_val, 'y': y_val, 'delta_y': min_deviation,'ideal_function_no': best_map})
                 
        # save to SQL
        print("Saving all 50 ideal functions")
        ideal_df.to_sql('ideal_functions',engine, if_exists = 'replace', index = False, method = 'multi')
        print("Saving training data...")
        train_df.to_sql('training_data',engine, if_exists='replace',index = False,method = 'multi')
        test_results_df = pd.DataFrame(test_results_list)
        if not test_results_df.empty:
            test_results_df.to_sql('test_results', engine, if_exists = 'replace', index = False, method = 'multi')
            print(f"success!{len(test_results_list)}rows saved to database")
        else:
            print("Warning: No test results were found to save")
            
        print(f"Mapping complete. {len(test_results_list)} points mapped to ideal functions.")
        
    except Exception as e:
        # custom error hanlding requirment
        raise DataValidationError(f"an error occurred during processing: {e}")
if __name__=="__main__":
    run_assignment()