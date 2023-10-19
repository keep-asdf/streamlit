from bokeh.plotting import figure, show, output_file, save
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource, HoverTool, Legend

def visualize_last_6_hours_with_moving_averages_bokeh(dataframe, save_path="streamlit/graph/with_moving_averages_last_6_hours.html"):
    """
    Visualize the predicted MHC water level, its moving averages, confidence intervals, and status lines from the last 6 hours of 
    the given dataframe and save the plot to the specified path using Bokeh.
    
    Parameters:
    - dataframe: A pandas DataFrame with columns 'Time', 'Predicted_MHC_Water_Level', 'CI_Lower', and 'CI_Upper', 
    and other columns for moving averages.
    - save_path: Path to save the plot. Default is "streamlit/graph/with_moving_averages_last_6_hours.html".
    """
    # Filter the dataframe to only include the last 6 hours of data
    end_time = dataframe['Time'].max()
    start_time = end_time - datetime.timedelta(hours=6)
    dataframe = dataframe[(dataframe['Time'] >= start_time) & (dataframe['Time'] <= end_time)]
    
    source = ColumnDataSource(dataframe)
    
    # Create a new plot with a datetime axis type
    p = figure(width=900, height=400, x_axis_type="datetime", title="Predicted MHC Water Level from Last 6 Hours with Confidence Intervals, Moving Averages and Status Lines")
    
    # Adding the status lines
    p.line(dataframe['Time'], [9.2]*len(dataframe), color="red", legend_label="Severe")
    p.line(dataframe['Time'], [8.0]*len(dataframe), color="orange", legend_label="Alert")
    p.line(dataframe['Time'], [7.0]*len(dataframe), color="yellow", legend_label="Caution")
    p.line(dataframe['Time'], [5.0]*len(dataframe), color="green", legend_label="Attention")
    
    # Adding the predicted values
    p.line('Time', 'Predicted_MHC_Water_Level', source=source, color="blue", legend_label="Predicted Water Level")
    
    # Filling the confidence intervals
    p.varea(x='Time', y1='CI_Lower', y2='CI_Upper', color="blue", alpha=0.3, source=source)
    
    # Adding the moving averages
    for column in dataframe.columns:
        if "MA" in column:
            p.line('Time', column, source=source, legend_label=column)
    
    # Hover tool
    hover = HoverTool()
    hover.tooltips = [("Time", "@Time{%Y-%m-%d %H:%M:%S}"), 
                      ("Value", "$y"), 
                      ("Lower CI", "@CI_Lower"), 
                      ("Upper CI", "@CI_Upper")]
    hover.formatters = {'@Time': 'datetime'}
    p.add_tools(hover)
    
    # Styling
    p.legend.location = "top_left"
    
    # Save the plot to the specified path
    output_file(save_path)
    save(p)
    output_notebook()
    show(p)

# Testing the function with the provided data
visualize_last_6_hours_with_moving_averages_bokeh(moving_averages)
