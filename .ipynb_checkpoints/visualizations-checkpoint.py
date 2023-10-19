# import pandas as pd
# from bokeh.plotting import figure, show, output_notebook
# from bokeh.io import push_notebook
# from bokeh.models import ColumnDataSource, Band, Legend, HoverTool
# from bokeh.palettes import Category10
# from bokeh.layouts import column

# def visualize_moving_averages_with_bokeh(dataframe):
#     dataframe['Time'] = pd.to_datetime(dataframe['Time'])

#     p = figure(x_axis_type="datetime", width=800, height=400, 
#                title="Predicted MHC Water Level with Confidence Intervals, Moving Averages and Status Lines")
#     source = ColumnDataSource(dataframe)

#     # Plot the Predicted Water Level
#     line = p.line('Time', 'Predicted_MHC_Water_Level', source=source, color="blue", legend_label="Predicted Water Level")

#     # Plot confidence intervals
#     band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='blue')
#     p.add_layout(band)

#     # Plot the moving averages
#     ma_colors = iter(Category10[10])
#     for column in dataframe.columns:
#         if "MA" in column:
#             color = next(ma_colors)
#             ma_line = p.line('Time', column, source=source, color=color, legend_label=column)
    
#     # Create a new source for the status lines
#     status_data = {
#         'Time': [dataframe.Time.min(), dataframe.Time.max()],

#     }
#     status_source = ColumnDataSource(status_data)

#     # Adding the status lines using the status source
#     p.line('Time', 'Severe',  color='red', line_dash="dashed", legend_label="Severe")
#     p.line('Time', 'Alert',  color='orange', line_dash="dashed", legend_label="Alert")
#     p.line('Time', 'Caution',  color='yellow', line_dash="dashed", legend_label="Caution")
#     p.line('Time', 'Attention',  color='green', line_dash="dashed", legend_label="Attention")

#     # Modify the hover tool to display information for each status line
#     hover = HoverTool(
#         tooltips=[
#             ("Time", "@Time{%F %T}"),
#             ("Water Level", "@Predicted_MHC_Water_Level"),
#             ("Confidence Interval", "(@CI_Lower, @CI_Upper)"),

#         ],
#         formatters={
#             "@Time": "datetime"
#         },
#         mode='vline'
#     )
#     p.add_tools(hover)

#     return p


import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.io import push_notebook
from bokeh.models import ColumnDataSource, Band, Legend, HoverTool
from bokeh.palettes import Category10
from bokeh.layouts import column

def visualize_moving_averages_with_bokeh(dataframe):
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])

    p = figure(x_axis_type="datetime", width=800, height=400, 
               title="Predicted MHC Water Level with Confidence Intervals, Moving Averages and Status Lines",
               legend_label_text_font_size="85%")  # <-- Adjust the legend label font size here

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
        'Time': [dataframe.Time.min(), dataframe.Time.max()]
    }
    status_source = ColumnDataSource(status_data)

    # Adding the status lines using the status source
    p.line('Time', 9.2, source=status_source, color='red', line_dash="dashed", legend_label="Severe")
    p.line('Time', 8.0, source=status_source, color='orange', line_dash="dashed", legend_label="Alert")
    p.line('Time', 7.0, source=status_source, color='yellow', line_dash="dashed", legend_label="Caution")
    p.line('Time', 5.0, source=status_source, color='green', line_dash="dashed", legend_label="Attention")

    # Modify the hover tool to display information for each status line
    hover = HoverTool(
        tooltips=[
            ("Time", "@Time{%F %T}"),
            ("Water Level", "@Predicted_MHC_Water_Level"),
            ("Confidence Interval", "(@CI_Lower, @CI_Upper)")
        ],
        formatters={
            "@Time": "datetime"
        },
        mode='mouse'
    )
    p.add_tools(hover)

    return p
