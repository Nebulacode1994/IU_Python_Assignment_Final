from bokeh.colors.named import orange
from bokeh.plotting import figure , output_file, show
from bokeh.layouts import gridplot , column
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from sqlalchemy import create_engine
import pandas as pd
import os
import pandas as pd



def visualize_results():
    """Creates a bokeh visualization as per assignment requirements"""
    print("connecting to Database...")
    base_path = os.path.dirname(os.path.abspath(__file__))
    actual_db_file = os.path.join(base_path, 'assignment_database.db')
    db_path = f'sqlite:///{actual_db_file}'
    if not os.path.exists(actual_db_file):
        print("Error: database file not found! run mains.py first")
        return
    
    
    engine = create_engine(db_path)
    
    try:
        print("loading tables...")
        train_df = pd.read_sql("training_data",  engine)
        test_results_df = pd.read_sql("test_results",engine)
        ideal_df = pd.read_sql("ideal_functions", engine)
    
    
        chosen_ideals = test_results_df['ideal_function_no'].unique().tolist()
        chosen_ideals = [x for x in chosen_ideals if x is not None]
        chosen_ideals.sort()
    
        output_file(os.path.join(base_path, 'assignment_visualization.html'))
        
        individual_plots = []
        colors = ['red' , 'blue','green' , 'orange']
        ideal_colors = ['black','purple','brown','cyan']
        
    
        # plot the training Data ( y1 ,y2 ,y3, y4)
        for i, function_name in enumerate ( chosen_ideals):
            title_text = f"Analysis: Training Set vs. Ideal Function {function_name}"
            p_sub = figure(title = title_text, width = 450, height = 350, x_axis_label = 'x', y_axis_label = 'y')
            
            p_sub.scatter(train_df['x'], train_df[f'y{i+1}'], color = colors[i], alpha = 0.4, legend_label = f'Train Y{i+1}')
            
            p_sub.line(ideal_df['x'], ideal_df[function_name], color = 'black', legend_label=f'Ideal{function_name}')
            
            p_sub.add_tools(HoverTool(tooltips=[('x', '@x'),('y','@y')]))
            p_sub.legend.location = 'top_left'
            individual_plots.append(p_sub)
            
        
        p_master = figure(title = "Final Result: All Mapped Test Points ( Gold)", x_axis_label = 'x',y_axis_label='y' , width = 910, height = 500)
        
        source = ColumnDataSource(test_results_df)
        p_master.circle('x','y',source = source , size = 8, color = 'gold',legend_label = 'Mapped test Points', alpha = 0.7)
        p_master.add_tools(HoverTool(tooltips=[('x','@x'),('y','@y'),('Ideal','@ideal_function_no'),('Dev','@delta_y')]))
        
        grid = gridplot([[individual_plots[0],individual_plots[1]],[individual_plots[2],individual_plots[3]]])
        layout = column(grid, p_master)
        

        print("Success! Opening browser with 5 separate graphs...")
        show(layout)
       
    except Exception as e:
        print(f" AN ERROR OCCURRED: {e}")
        
if __name__== "__main__":
    visualize_results()
        
  
    
        
        