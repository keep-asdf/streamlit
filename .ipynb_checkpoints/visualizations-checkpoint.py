import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.io import push_notebook
from bokeh.models import ColumnDataSource, Band, Legend, HoverTool
from bokeh.palettes import Category10
from bokeh.layouts import column

def visualize_moving_averages_with_bokeh(dataframe):
    
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])

    p = figure(x_axis_type="datetime", width=800, height=400, 
               title="Predicted MHC Water Level with Confidence Intervals, Moving Averages and Status Lines")
    source = ColumnDataSource(dataframe)

    # Plot the Predicted Water Level
    line = p.line('Time', 'Predicted_MHC_Water_Level', source=source, color="blue", legend_label="Predicted Water Level")

    # Plot confidence intervals
    band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='blue')
    p.add_layout(band)

    # Plot the moving averages
    ma_colors = iter(Category10[10])
    for column in dataframe.columns:
        if "MA" in column:
            color = next(ma_colors)
            ma_line = p.line('Time', column, source=source, color=color, legend_label=column)
    
    # Create a new source for the status lines
    status_data = {
        'Time': [dataframe.Time.min(), dataframe.Time.max()],

    }
    status_source = ColumnDataSource(status_data)

    # Adding the status lines using the status source
    p.line('Time', 'Severe',  color='red', line_dash="dashed", legend_label="Severe")
    p.line('Time', 'Alert',  color='orange', line_dash="dashed", legend_label="Alert")
    p.line('Time', 'Caution',  color='yellow', line_dash="dashed", legend_label="Caution")
    p.line('Time', 'Attention',  color='green', line_dash="dashed", legend_label="Attention")

    # Modify the hover tool to display information for each status line
    hover = HoverTool(
        tooltips=[
            
            ("Time", "@Time{%F %T}"),
            ("Water Level", "@Predicted_MHC_Water_Level"),
            ("Confidence Interval", "(@CI_Lower, @CI_Upper)"),

        ],
        formatters={
            "@Time": "datetime"
        },
        mode='mouse'
    )
    p.add_tools(hover)

    return p


def visualize_true_pred_with_CI_and_status_lines_bokeh(dataframe):
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])
    source = ColumnDataSource(dataframe)

    p = figure(x_axis_type="datetime", width=800, height=400, 
               title="True vs Predicted Values with Confidence Intervals and Status Lines")

    # Plot the True Values
    p.line('Time', 'True_Value', source=source, color="green", legend_label="True Value")

    # Plot the Predicted Values
    p.line('Time', 'Predicted_Value', source=source, color="blue", legend_label="Predicted Value")

    # Plot confidence intervals
    band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='blue')
    p.add_layout(band)

    # Adding the status lines
    p.line([dataframe.Time.min(), dataframe.Time.max()], [9.2, 9.2], color='red', line_dash="dashed", legend_label="Severe")
    p.line([dataframe.Time.min(), dataframe.Time.max()], [8.0, 8.0], color='orange', line_dash="dashed", legend_label="Alert")
    p.line([dataframe.Time.min(), dataframe.Time.max()], [7.0, 7.0], color='yellow', line_dash="dashed", legend_label="Caution")
    p.line([dataframe.Time.min(), dataframe.Time.max()], [5.0, 5.0], color='green', line_dash="dashed", legend_label="Attention")

    # Hover tool
    hover = HoverTool(
        tooltips=[
            ("Time", "@Time{%F %T}"),
            ("True Value", "@True_Value"),
            ("Predicted Value", "@Predicted_Value"),
            ("Confidence Interval", "(@CI_Lower, @CI_Upper)")
        ],
        formatters={
            "@Time": "datetime"
        },
        mode='mouse'
    )
    p.add_tools(hover)

    return p
