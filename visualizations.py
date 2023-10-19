# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd

# def visualize_moving_averages_with_cross_highlighted(dataframe):
#     """
#     Visualize the predicted MHC water level, its moving averages, confidence intervals, and status lines from the given dataframe.
    
#     Parameters:
#     - dataframe: A pandas DataFrame with columns 'Time', 'Predicted_MHC_Water_Level', 'CI_Lower', 'CI_Upper', 
#     and other columns for moving averages.
#     """
#     # Convert the Time column to datetime format for better plotting in a copied dataframe
#     df_copy = dataframe.copy()
#     df_copy['Time'] = pd.to_datetime(df_copy['Time'])

#     # Set the theme
#     sns.set_theme(style="darkgrid")

#     # Create the plot
#     plt.figure(figsize=(15, 6))
#     sns.lineplot(x='Time', y='Predicted_MHC_Water_Level', data=df_copy, label='Predicted Water Level', color='blue')
#     plt.fill_between(df_copy['Time'], df_copy['CI_Lower'], df_copy['CI_Upper'], color='blue', alpha=0.3)
    
#     # Check for crosses where 12H_MA crosses other MAs
#     prev_12H = None
#     for i, row in df_copy.iterrows():
#         for column in df_copy.columns:
#             if "MA" in column and column != "12H_MA":
#                 if prev_12H is not None and prev_12H < df_copy.at[i-1, column] and row["12H_MA"] > row[column]:
#                     plt.scatter(row['Time'], row['12H_MA'], color='gold', marker='x', s=100)
#         prev_12H = row["12H_MA"]
    
#     # Adding the moving averages
#     for column in df_copy.columns:
#         if "MA" in column:
#             if column == "12H_MA":
#                 sns.lineplot(x='Time', y=column, data=df_copy, label=column, linewidth=2.5, color='darkred')
#             else:
#                 sns.lineplot(x='Time', y=column, data=df_copy, label=column)
    
#     # Adding the status lines based on the provided criteria with English labels
#     plt.axhline(9.2, color='red', linestyle='--', label='Severe')
#     plt.axhline(8.0, color='orange', linestyle='--', label='Alert')
#     plt.axhline(7.0, color='yellow', linestyle='--', label='Caution')
#     plt.axhline(5.0, color='green', linestyle='--', label='Attention')

#     plt.title("Predicted MHC Water Level with Confidence Intervals, Moving Averages and Status Lines")
#     plt.ylabel("Water Level")
#     plt.xlabel("Time")
#     # Position the legend to the top right
#     plt.legend(loc='upper right', bbox_to_anchor=(1, 1))
#     plt.xticks(rotation=45)
#     plt.tight_layout()

#     # Display the plot
#     plt.show()
#     plt.close()

    

import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.io import push_notebook
from bokeh.models import ColumnDataSource, Band, Legend, HoverTool
from bokeh.palettes import Category10
from bokeh.layouts import column

def visualize_moving_averages_with_bokeh(dataframe):
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])

    p = figure(x_axis_type="datetime", width=800, height=400, title="Predicted MHC Water Level with Confidence Intervals, Moving Averages and Status Lines")
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
    
    # Adding the status lines
    p.line([dataframe.Time.min(), dataframe.Time.max()], [9.2, 9.2], color='red', line_dash="dashed", legend_label="Severe")
    p.line([dataframe.Time.min(), dataframe.Time.max()], [8.0, 8.0], color='orange', line_dash="dashed", legend_label="Alert")
    p.line([dataframe.Time.min(), dataframe.Time.max()], [7.0, 7.0], color='yellow', line_dash="dashed", legend_label="Caution")
    p.line([dataframe.Time.min(), dataframe.Time.max()], [5.0, 5.0], color='green', line_dash="dashed", legend_label="Attention")

    p.legend.location = "top_left"
    p.legend.click_policy="hide"
    
    hover = HoverTool(
        tooltips=[
            ("Time", "@Time{%F %T}"),
            ("Water Level", "@Predicted_MHC_Water_Level"),
            ("Confidence Interval", "(@CI_Lower, @CI_Upper)")
        ],
        formatters={
            "@Time": "datetime"
        },
        mode='vline'
    )
    p.add_tools(hover)

    return p


