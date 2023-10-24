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
    p.line('Time', 'Predicted_MHC_Water_Level', source=source, color="darkred", legend_label="예측된 미호천교 수위", line_width = 3)

    # Plot confidence intervals
    band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkred')
    p.add_layout(band)

    # Plot the moving averages
    # Define a mapping from column names to desired legend labels
    legend_mapping = {
        "12H_MA": "12시간 이동평균",
        "72H_MA": "72시간 이동평균",
        "96H_MA": "96시간 이동평균",
        "120H_MA": "120시간 이동평균"
    }

    ma_colors = iter(Category10[10])
    for column in dataframe.columns:
        if "MA" in column:
            color = next(ma_colors)
            legend_name = legend_mapping.get(column, column)  # Use the mapped name if it exists, otherwise use the column name
            p.line('Time', column, source=source, color=color, legend_label=legend_name)


    # Adding the status lines using fixed values
    p.line(x=dataframe['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
    p.line(x=dataframe['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
    p.line(x=dataframe['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
    p.line(x=dataframe['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")

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
    dataframe = dataframe.iloc[10368:, :]
    features = ['MHC_Water_Level', 'MH_Water_Level', 'PG_Water_Level', 'HH_Water_Level', 'GG_Water_Level']
    graphs = []

    legend_mapping = {
        "MHC_Water_Level": "미호천교 관측 수위",
        "MH_Water_Level": "미호교 관측 수위 수위",
        "PG_Water_Level": "팔결교 관측 수위 수위",
        "HH_Water_Level": "환희교 관측 수위 수위",
        "GG_Water_Level": "금곡교 관측 수위 수위"
    }    
    
   
    for feature in features:
        p = figure(width=500, height=250, title = legend_mapping[feature], 
                   x_axis_type="datetime",
                   min_border_left=0, min_border_right=0, 
                   min_border_top=0, min_border_bottom=0) 
        
        p.line(dataframe['Time'][-7:], dataframe[feature][-7:], line_width=2)
        p.xaxis.axis_label = 'Time'
        p.yaxis.axis_label = legend_mapping[feature]  # Use the mapped y-axis label
        graphs.append(p)

    return graphs



def visualize_true_pred_with_CI_and_status_lines_bokeh(dataframe):
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])
    source = ColumnDataSource(dataframe)

    p = figure(x_axis_type="datetime", width=1600, height=400, 
               title="True vs Predicted Values with Confidence Intervals and Status Lines")

    # Plot the True Values
    p.line('Time', 'True_Value', source=source, color="#464646", legend_label="관측된 미호천교 수위")

    # Plot the Predicted Values
    p.line('Time', 'Predicted_Value', source=source, color="darkred", legend_label="예측된 미호천교 수위" , line_width = 3)

    # Plot confidence intervals
    band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkred')
    p.add_layout(band)


    
    # Adding the status lines using fixed values
    p.line(x=dataframe['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
    p.line(x=dataframe['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
    p.line(x=dataframe['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
    p.line(x=dataframe['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")
    


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

    # y축 범위 설정
    y_min = 0
    y_max = 9.5

    # 그래프 생성 with adjusted y_range
    p = figure(title="Predicted MHC Water Level with Confidence Intervals, Moving Averages and Status Lines for Last 6H", 
               x_axis_type="datetime", x_axis_label="Time",  y_range=(y_min, y_max),
              width=750, height=430)
    
    # 그래프에 데이터 추가
    p.line(x='Time', y='Predicted_MHC_Water_Level', source=source, color="darkred", line_width = 3)
    p.line(x='Time', y='12H_MA', source=source, color="red", alpha=0.6)
    p.line(x='Time', y='72H_MA', source=source, color="green", alpha=0.6)
    p.line(x='Time', y='96H_MA', source=source, color="purple", alpha=0.6)
    p.line(x='Time', y='120H_MA', source=source, color="orange", alpha=0.6)
    
    # Plot confidence intervals
    band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkred')
    p.add_layout(band)
    

    # Adding the status lines using fixed values
    p.line(x=data['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
    p.line(x=data['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
    p.line(x=data['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
    p.line(x=data['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")
    
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
    
    # Hide the legend
    p.legend.visible = False

    return p



def visualize_true_vs_predicted_last_6h(data):
    # 데이터를 ColumnDataSource로 변환
    source = ColumnDataSource(data)

    # y축 범위 설정
    y_min = 0
    y_max = 9

    # 그래프 생성 with adjusted y_range
    p = figure(title="True vs Predicted MHC Water Level with Confidence Intervals for Last 6H", 
               x_axis_type="datetime", x_axis_label="Time", y_range=(y_min, y_max),
               min_border_left=0,   min_border_right=0,
               min_border_top=0, min_border_bottom=0,
               width=750, height=430)
    
    # 그래프에 데이터 추가
    p.line(x='Time', y='True_Value', source=source, color="#464646", alpha=0.6, legend_label="True Value")
    p.line(x='Time', y='Predicted_Value', source=source, color="darkred", legend_label="Predicted Value",  line_width = 3)
    
    # Plot confidence intervals
    band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkred')
    p.add_layout(band)
    
    # Adding the status lines using fixed values
    p.line(x=data['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
    p.line(x=data['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
    p.line(x=data['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
    p.line(x=data['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")
    
    # Hover tool 추가
    hover = HoverTool()
    hover.tooltips = [("Time", "@Time{%F %H:%M}"), 
                      ("True Value", "@True_Value"),
                      ("Predicted Value", "@Predicted_Value")]
    hover.formatters = {"@Time": "datetime"}
    p.add_tools(hover)
    
    # Hide the legend
    p.legend.visible = False

    return p

