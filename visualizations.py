import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.io import push_notebook
from bokeh.models import ColumnDataSource, Band, Legend, HoverTool
from bokeh.palettes import Category10
from bokeh.layouts import column, gridplot

def visualize_moving_averages_with_bokeh(dataframe):
    dataframe = dataframe.copy()  # 캐싱된 데이터프레임을 수정하기 전에 복사본을 만듭니다.
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])

    p = figure(x_axis_type="datetime", width=1600, height=400, 
               title="Predicted MHC Water Level with Confidence Intervals, Moving Averages and Status Lines",
               min_border_left=0,   min_border_right=0,
               min_border_top=0, min_border_bottom=0)
    source = ColumnDataSource(dataframe)

    # Plot the Predicted Water Level
    p.line('Time', 'Predicted_MHC_Water_Level', source=source, color="blue", legend_label="Predicted Water Level")

    # Plot confidence intervals
    band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='blue')
    p.add_layout(band)

    # Plot the moving averages
    ma_colors = iter(Category10[10])
    for column in dataframe.columns:
        if "MA" in column:
            color = next(ma_colors)
            p.line('Time', column, source=source, color=color, legend_label=column)

    # Adding the status lines using fixed values
    p.line(x=dataframe['Time'], y=9.2, color='red', line_dash="dashed", legend_label="Severe")
    p.line(x=dataframe['Time'], y=8.0, color='orange', line_dash="dashed", legend_label="Alert")
    p.line(x=dataframe['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="Caution")
    p.line(x=dataframe['Time'], y=5.0, color='green', line_dash="dashed", legend_label="Attention")

    # Modify the hover tool to display information for each status line
    hover = HoverTool(
        tooltips=[
            ("Time", "@Time{%F %T}"),
            ("Water Level", "@Predicted_MHC_Water_Level"),
            ("Confidence Interval", "(@CI_Lower, @CI_Upper)")
        ],
        formatters={"@Time": "datetime"},
        mode='mouse'
    )
    p.add_tools(hover)

    return p


def create_individual_graphs(dataframe):
    
    dataframe = dataframe.copy()  # 캐싱된 데이터프레임을 수정하기 전에 복사본을 만듭니다.
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])  # Convert 'Time' column to datetime
    features = ['MHC_Water_Level', 'MH_Water_Level', 'PG_Water_Level', 'HH_Water_Level', 'GG_Water_Level']
    graphs = []

   
    for feature in features:
        p = figure(width=500, height=250, title=feature, 
                   min_border_left=0, min_border_right=0, 
                   min_border_top=0, min_border_bottom=0) 
        
        p.line(dataframe['Time'], dataframe[feature], line_width=2)
        p.xaxis.axis_label = 'Time'
        p.yaxis.axis_label = feature
        graphs.append(p)

    return graphs



def visualize_true_pred_with_CI_and_status_lines_bokeh(dataframe):
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])
    source = ColumnDataSource(dataframe)

    p = figure(x_axis_type="datetime", width=1600, height=400, 
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



def visualize_last_6h_moving_averages(data):
    # 데이터를 ColumnDataSource로 변환
    source = ColumnDataSource(data)

    # 그래프 생성
    p = figure(title="Moving Averages for Last 6H", x_axis_type="datetime", x_axis_label="Time", y_axis_label="Water Level")
    
    # Predicted_MHC_Water_Level와 이동 평균들을 그래프에 추가
    p.line(x='Time', y='Predicted_MHC_Water_Level', source=source, legend_label="Predicted Water Level", color="blue", alpha=0.6)
    p.line(x='Time', y='12H_MA', source=source, legend_label="12H Moving Average", color="red", alpha=0.6)
    p.line(x='Time', y='72H_MA', source=source, legend_label="72H Moving Average", color="green", alpha=0.6)
    p.line(x='Time', y='96H_MA', source=source, legend_label="96H Moving Average", color="purple", alpha=0.6)
    p.line(x='Time', y='120H_MA', source=source, legend_label="120H Moving Average", color="orange", alpha=0.6)
    
    # Plot confidence intervals
    band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='blue')
    p.add_layout(band)
    
    # Hover tool 추가
    hover = HoverTool()
    hover.tooltips = [("Time", "@Time{%F %H:%M}"), 
                      ("Predicted Level", "@Predicted_MHC_Water_Level"),
                      ("12H MA", "@12H_MA"), 
                      ("72H MA", "@72H_MA"),
                      ("96H MA", "@96H_MA"),
                      ("120H MA", "@120H_MA")]
    hover.formatters = {"@Time": "datetime"}
    p.add_tools(hover)

    return p
