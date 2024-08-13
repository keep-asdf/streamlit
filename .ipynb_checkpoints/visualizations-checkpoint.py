import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_notebook, output_file
from bokeh.io import push_notebook
from bokeh.models import ColumnDataSource, Band, Legend, HoverTool, BoxSelectTool, CustomJS
from bokeh.palettes import Category10
from bokeh.layouts import column, gridplot, layout
import matplotlib.pyplot as plt
from bokeh.models import DatetimeTicker
from scipy.stats import gaussian_kde




# def visualize_moving_averages_with_bokeh(dataframe, selected_datetime, show_blue_line):
#     dataframe = dataframe.copy()  # 캐싱된 데이터프레임을 수정하기 전에 복사본을 만듭니다.
#     dataframe['Time'] = pd.to_datetime(dataframe['Time'])

#     p = figure(x_axis_type="datetime", 
#                width=1600, 
#                height=400, 
#                title="Predicted MHC Water Level with Confidence Intervals, Moving Averages and Status Lines",
#                min_border_left=0,  
#                min_border_right=0,
#                min_border_top=0,
#                min_border_bottom=0)
#     source = ColumnDataSource(dataframe)

#     # Plot the Predicted Water Level
#     p.line('Time', 'Predicted_MHC_Water_Level', source=source, color="darkred", legend_label="예측된 미호천교 수위", line_width = 3)

#     # Plot confidence intervals
#     band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkred')
#     p.add_layout(band)

    # Plot the moving averages
    # Define a mapping from column names to desired legend labels
#     legend_mapping = {
#         "12H_MA": "12시간 이동평균",
#         "72H_MA": "72시간 이동평균",
#         "96H_MA": "96시간 이동평균",
#         "120H_MA": "120시간 이동평균"
#     }

#     ma_colors = iter(Category10[10])
#     for column in dataframe.columns:
#         if "MA" in column:
#             color = next(ma_colors)
#             legend_name = legend_mapping.get(column, column)  # Use the mapped name if it exists, otherwise use the column name
#             p.line('Time', column, source=source, color=color, legend_label=legend_name)


#     # Adding the status lines using fixed values
#     p.line(x=dataframe['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
#     p.line(x=dataframe['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
#     p.line(x=dataframe['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
#     p.line(x=dataframe['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")


#     if show_blue_line:  # show_blue_line 값이 True인 경우만 파란선을 그림
#         p.line(x=[selected_datetime, selected_datetime], y=[dataframe['Predicted_MHC_Water_Level'].min(), dataframe['Predicted_MHC_Water_Level'].max()], 
#                color='#000080', line_dash="dotted", line_width = 3)

    
#     # Modify the hover tool to display information for each status line
#     hover = HoverTool(
#         tooltips=[
#             ("Time", "@Time{%F %T}"),
#             ("Water Level", "@Predicted_MHC_Water_Level"),
#             ("Confidence Interval", "(@CI_Lower, @CI_Upper)")
#         ],
#         formatters={"@Time": "datetime"},
#         mode='mouse'
#     )
#     p.add_tools(hover)


#     p.legend.location = "top_left"

    
#     return p


####################################################################################
####################################################################################


def create_individual_graphs(dataframe):
    dataframe = dataframe.copy()  # 캐싱된 데이터프레임을 수정하기 전에 복사본을 만듭니다.
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])  # 'Time' 열을 datetime 형식으로 변환
    dataframe = dataframe.iloc[10368:, :]  # 원하는 범위의 데이터만 사용
    features = ['MHC_Water_Level', 'MH_Water_Level', 'PG_Water_Level', 'HH_Water_Level', 'GG_Water_Level']
    graphs = []

    legend_mapping = {
        "MHC_Water_Level": "미호천교 관측 수위",
        "MH_Water_Level": "미호교 관측 수위",
        "PG_Water_Level": "팔결교 관측 수위",
        "HH_Water_Level": "환희교 관측 수위",
        "GG_Water_Level": "금곡교 관측 수위"
    }
    
    for feature in features:
        p = figure(title=legend_mapping[feature], 
                   x_axis_type="datetime",
                   sizing_mode="stretch_both",
                   height=300)  # 크기 자동 조절
        
        # 라인 생성 및 렌더러 저장
        line_renderer = p.line(dataframe['Time'][-7:], dataframe[feature][-7:], line_width=2)
        
        p.xaxis.axis_label = 'Time'
        p.yaxis.axis_label = legend_mapping[feature]  # y축 레이블 설정
        
        # 통일된 크기를 위해 그래프의 최소 및 최대 범위 설정
        p.min_border = 10
        p.min_border_left = 50
        p.min_border_right = 10
        p.min_border_top = 10
        p.min_border_bottom = 30

        # Hover tool 추가
        hover = HoverTool(
            renderers=[line_renderer],  # 이 라인에만 HoverTool 적용
            tooltips=[
                ("Time", "@x{%F %H:%M}"),
                (legend_mapping[feature], "@y")
            ],
            formatters={
                "@x": "datetime"
            },
            mode='vline'  # 수직선 기준으로 툴팁 표시
        )
        p.add_tools(hover)

        graphs.append(p)

    return graphs


####################################################################################
####################################################################################


# def visualize_true_pred_with_CI_and_status_lines_bokeh(dataframe,
#                                                        selected_datetime, 
#                                                        show_blue_line):
    
#     dataframe['Time'] = pd.to_datetime(dataframe['Time'])
#     source = ColumnDataSource(dataframe)

#     p = figure(x_axis_type="datetime", 
#                width=1600,
#                height=700, 
#                sizing_mode="stretch_both",
#                title="True vs Predicted Values with Confidence Intervals and Status Lines")

#     # Plot the True Values
#     p.line('Time', 'True_Value', source=source, color="#464646", legend_label="관측된 미호천교 수위", line_width = 2)

#     # Plot the Predicted Values
#     p.line('Time', 'Predicted_Value', source=source, color="darkred", legend_label="예측된 미호천교 수위" , line_width = 3)

#     # Plot confidence intervals
#     band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkred')
#     p.add_layout(band)


    
#     # Adding the status lines using fixed values
#     p.line(x=dataframe['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
#     p.line(x=dataframe['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
#     p.line(x=dataframe['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
#     p.line(x=dataframe['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")
    

#     if show_blue_line:  # show_blue_line 값이 True인 경우만 파란선을 그림
#         p.line(x=[selected_datetime, selected_datetime], 
#                y=[0, 
#                   dataframe['True_Value'].max()],
#                color='#000080', 
#                line_dash="dotted", 
#                line_width = 3)


#     # Hover tool
#     hover = HoverTool(
#         tooltips=[
#             ("Time", "@Time{%F %T}"),
#             ("True Value", "@True_Value"),
#             ("Predicted Value", "@Predicted_Value"),
#             ("Confidence Interval", "(@CI_Lower, @CI_Upper)")
#         ],
#         formatters={
#             "@Time": "datetime"
#         },
#         mode='mouse'
#     )
#     p.add_tools(hover)

    

#     p.legend.location = "top_left"

    
#     return p

def visualize_true_pred_with_CI_and_status_lines_bokeh(dataframe,
                                                       selected_datetime, 
                                                       show_blue_line):
    
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])
    source = ColumnDataSource(dataframe)

    p = figure(x_axis_type="datetime", 
               width=1600,
               height=700, 
               sizing_mode="stretch_both",
               title="Test 데이터에 대한 예측 값과 실제 값")

    # Plot the True Values
    true_values_renderer =p.line('Time', 'True_Value', source=source, color="darkred", legend_label="관측된 미호천교 수위", line_width=3)

    # Plot the Predicted Values
    p.line('Time', 'Predicted_Value', source=source, color="darkblue", legend_label="예측된 미호천교 수위", line_width=3)

    # Plot confidence intervals
    band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkblue')
    p.add_layout(band)

    # Adding the status lines using fixed values
    p.line(x=dataframe['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
    p.line(x=dataframe['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
    p.line(x=dataframe['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
    p.line(x=dataframe['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")
    
    # show_blue_line 값이 True인 경우만 파란선을 그림
    if show_blue_line:
        p.line(x=[selected_datetime, selected_datetime], 
               y=[0, dataframe['True_Value'].max()],
               color='#000080', 
               line_dash="dotted", 
               line_width=3)

    # Hover tool 적용 (True Values 라인에만)
    hover = HoverTool(
        renderers=[true_values_renderer],  # True Values 라인에만 적용
        tooltips=[
            ("Time", "@Time{%F %T}"),
            ("True Value", "@True_Value"),
            ("Predicted Value", "@Predicted_Value"),
            ("Confidence Interval", "(@CI_Lower, @CI_Upper)")
        ],
        formatters={
            "@Time": "datetime"
        },
        mode='vline'  # 수직선 위의 값만 표시
    )
    p.add_tools(hover)

    p.legend.location = "top_left"
    
    return p

####################################################################################
####################################################################################


# def test_visualize_true_pred_with_CI_and_status_lines_bokeh(dataframe, selected_datetime, show_blue_line):
#     dataframe['Time'] = pd.to_datetime(dataframe['Time'])
#     source = ColumnDataSource(dataframe)

#     p = figure(x_axis_type="datetime", width=1600, height=400, 
#                sizing_mode="stretch_both",
#                title="True vs Predicted Values with Confidence Intervals and Status Lines")

#     # Plot the True Values
#     p.line('Time', 'True_Value', source=source, color="#464646", legend_label="관측된 미호천교 수위", line_width = 3)

#     # Plot the Predicted Values
#     p.line('Time', 'Predicted_Value', source=source, color="darkred", legend_label="예측된 미호천교 수위" , line_width = 3)

#     # Plot confidence intervals
#     band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkred')
#     p.add_layout(band)


    
#     # Adding the status lines using fixed values
#     p.line(x=dataframe['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
#     p.line(x=dataframe['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
#     p.line(x=dataframe['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
#     p.line(x=dataframe['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")
    

#     if show_blue_line:  # show_blue_line 값이 True인 경우만 파란선을 그림
#         p.line(x=[selected_datetime, selected_datetime], y=[dataframe['True_Value'].min(), dataframe['True_Value'].max()], 
#                color='#000080', line_dash="dotted", line_width = 3)


#     # Hover tool
#     hover = HoverTool(
#         tooltips=[
#             ("Time", "@Time{%F %T}"),
#             ("True Value", "@True_Value"),
#             ("Predicted Value", "@Predicted_Value"),
#             ("Confidence Interval", "(@CI_Lower, @CI_Upper)")
#         ],
#         formatters={
#             "@Time": "datetime"
#         },
#         mode='mouse'
#     )
#     p.add_tools(hover)

#     return p

####################################################################################
####################################################################################

# def visualize_last_6h_moving_averages(data):
#     # 데이터를 ColumnDataSource로 변환
#     source = ColumnDataSource(data)

#     # y축 범위 설정
#     y_min = 0
#     y_max = 9.5

#     # 그래프 생성 with adjusted y_range
#     p = figure(title="최근 6시간에 대한 예측 값과 실제 값", 
#                x_axis_type="datetime",
#                x_axis_label="Time", 
#                y_range=(y_min, y_max),
#                width=750,
#                height=430, 
#                sizing_mode="stretch_both")
    
#     # 그래프에 데이터 추가
#     p.line(x='Time', y='Predicted_MHC_Water_Level', source=source, color="darkred", line_width = 3)
#     p.line(x='Time', y='12H_MA', source=source, color="red", alpha=0.6)
#     p.line(x='Time', y='72H_MA', source=source, color="green", alpha=0.6)
#     p.line(x='Time', y='96H_MA', source=source, color="purple", alpha=0.6)
#     p.line(x='Time', y='120H_MA', source=source, color="orange", alpha=0.6)
    
#     # Plot confidence intervals
#     band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkred')
#     p.add_layout(band)
    

#     # Adding the status lines using fixed values
#     p.line(x=data['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
#     p.line(x=data['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
#     p.line(x=data['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
#     p.line(x=data['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")
    
#     # Hover tool 추가
#     hover = HoverTool()
#     hover.tooltips = [("Time", "@Time{%F %H:%M}"), 
#                       ("Predicted Level", "@Predicted_MHC_Water_Level"),
#                       ("12H MA", "@12H_MA"), 
#                       ("72H MA", "@72H_MA"),
#                       ("96H MA", "@96H_MA"),
#                       ("120H MA", "@120H_MA")]
#     hover.formatters = {"@Time": "datetime"}
#     p.add_tools(hover)
    
#     # Hide the legend
#     p.legend.visible = False

#     return p

####################################################################################
####################################################################################
def visualize_true_vs_predicted_last_6h(data):
    # 데이터를 ColumnDataSource로 변환
    source = ColumnDataSource(data)

    # y축 범위 설정
    y_min = 0
    y_max = 9

    # 그래프 생성 with adjusted y_range
    p = figure(title="최근 6시간에 대한 예측 값과 실제 값", 
               x_axis_type="datetime", 
               x_axis_label="Time",
               y_range=(y_min, y_max),
               min_border_left=0,   
               min_border_right=0,
               min_border_top=0, 
               min_border_bottom=0,
               width=750, height=430, 
               sizing_mode="stretch_both")
    
    # 그래프에 데이터 추가
    true_value_renderer = p.line(x='Time', y='True_Value', source=source, color="darkred", alpha=0.6, legend_label="관측된 미호천교 수위",line_width=3)
    p.line(x='Time', y='Predicted_Value', source=source, color="darkblue", legend_label="예측된 미호천교 수위", line_width=3)
    
    # 신뢰 구간 추가
    band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkblue')
    p.add_layout(band)
    
    # 상태선 추가
    p.line(x=data['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
    p.line(x=data['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
    p.line(x=data['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
    p.line(x=data['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")
    
    # Hover tool 추가
    hover = HoverTool(
        renderers=[true_value_renderer],  # True Value 라인에만 적용
        tooltips=[
            ("Time", "@Time{%F %H:%M}"), 
            ("True Value", "@True_Value"),
            ("Predicted Value", "@Predicted_Value"),
            ("Confidence Interval", "(@CI_Lower, @CI_Upper)")
        ],
        formatters={"@Time": "datetime"},
        mode='vline'  # 수직선 기준으로 툴팁 표시
    )
    p.add_tools(hover)
    
    p.legend.visible = True
    
    p.legend.location = "top_left"

    return p



####################################################################################
####################################################################################


# def plot_predicted_volatility_bokeh_cleaned(data):
#     """
#     Plot the predicted volatility using Bokeh with cleaner x-axis.
    
#     Args:
#     - data (DataFrame): Data containing timestamps and predicted volatility
    
#     Returns:
#     - p: Bokeh plot object
#     """
#     # 데이터를 ColumnDataSource로 변환
#     source = ColumnDataSource(data)

#     # 그래프 생성
#     p = figure(title="GARCH Predicted Volatility", 
#                x_axis_type="datetime", x_axis_label="Time",
#                y_axis_label="Predicted Volatility",
#                plot_width=750, plot_height=430)
    
#     # 그래프에 데이터 추가
#     p.line(x='Time', y='Predicted_Volatility_1hr_Ahead', source=source, color="darkred", legend_label="Predicted Volatility")
    
#     # x-axis ticker configuration for cleaner display
#     p.xaxis.ticker = DatetimeTicker(desired_num_ticks=10)
    
#     # Hover tool 추가
#     hover = HoverTool()
#     hover.tooltips = [("Time", "@Time{%F %H:%M}"), 
#                       ("Predicted Volatility", "@Predicted_Volatility_1hr_Ahead")]
#     hover.formatters = {"@Time": "datetime"}
#     p.add_tools(hover)
    
#     # Hide the legend
#     p.legend.visible = False

#     return p

# # Create the plot using Bokeh with cleaned x

# # import matplotlib.pyplot as plt



####################################################################################
####################################################################################


# def plot_predicted_volatility(data):
#     """
#     Plot the predicted volatility using Matplotlib with cleaner x-axis.
    
#     Args:
#     - data (DataFrame): Data containing timestamps and predicted volatility
    
#     Returns:
#     - fig: Matplotlib figure object
#     """
#     # Create the figure and axis
#     fig, ax = plt.subplots(figsize=(10, 6))
    
#     # Plot the data
#     ax.plot(data['Time'], data['Predicted_Volatility_1hr_Ahead'], color="darkred", label="Predicted Volatility")
    
#     # Set the title and labels
#     ax.set_title("GARCH Predicted Volatility")
#     ax.set_xlabel("Time")
#     ax.set_ylabel("Predicted Volatility")
#     ax.legend()
    
#     # Format the x-axis for better readability and reduce the number of ticks
#     ax.xaxis.set_major_locator(plt.MaxNLocator(10))
#     ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.Timestamp(x).strftime('%Y-%m-%d %H:%M')))
#     plt.xticks(rotation=45)
    
#     # Add a grid
#     ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
#     plt.tight_layout()
#     return fig


####################################################################################
####################################################################################


# def test_visualize_true_pred_with_CI_and_status_lines_bokeh(dataframe, selected_datetime, show_blue_line):
#     dataframe['Time'] = pd.to_datetime(dataframe['Time'])
    
#     # 신뢰 구간을 벗어나는 값 확인
#     dataframe['Out_Of_CI'] = (dataframe['True_Value'] < dataframe['CI_Lower']) | (dataframe['True_Value'] > dataframe['CI_Upper'])
    
#     source = ColumnDataSource(dataframe)

#     p = figure(x_axis_type="datetime", width=1600, height=400, 
#                title="True vs Predicted Values with Confidence Intervals and Status Lines")

#     # 관측된 값 그리기
#     p.line('Time', 'True_Value', source=source, color="#464646", legend_label="관측된 미호천교 수위", line_width=2)

#     # 예측된 값 그리기
#     p.line('Time', 'Predicted_Value', source=source, color="darkred", legend_label="예측된 미호천교 수위", line_width=3)

#     # 신뢰 구간 그리기
#     band = Band(base='Time', lower='CI_Lower', upper='CI_Upper', source=source, level='underlay', fill_alpha=0.3, fill_color='darkred')
#     p.add_layout(band)

#     # 상태 선 추가 (고정된 값 사용)
#     p.line(x=dataframe['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
#     p.line(x=dataframe['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
#     p.line(x=dataframe['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
#     p.line(x=dataframe['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")

#     # 파란색 선 추가 (show_blue_line 값이 True인 경우에만)
#     if show_blue_line:
#         p.line(x=[selected_datetime, selected_datetime], y=[dataframe['True_Value'].min(), dataframe['True_Value'].max()], 
#                color='#000080', line_dash="dotted", line_width=3)

#     # 신뢰 구간을 벗어난 값들을 톤 다운된 파란색으로 표시
#     out_of_ci_source = ColumnDataSource(dataframe[dataframe['Out_Of_CI']])
#     p.scatter('Time', 'True_Value', source=out_of_ci_source, color='lightblue', size=8, legend_label="신뢰 구간을 벗어난 값")

#     # Hover tool 추가
#     hover = HoverTool(
#         tooltips=[
#             ("Time", "@Time{%F %T}"),
#             ("True Value", "@True_Value"),
#             ("Predicted Value", "@Predicted_Value"),
#             ("Confidence Interval", "(@CI_Lower, @CI_Upper)")
#         ],
#         formatters={
#             "@Time": "datetime"
#         },
#         mode='mouse'
#     )
#     p.add_tools(hover)

#     return p



######################--- 베이지안 관련 시각화 ---#########################


####################################################################################
####################################################################################


# Bokeh를 사용한 시각화 함수 1 : posterior predictive dist


def plot_posterior_predictive_distribution_bokeh(df, time_points):
    """
    Bokeh를 이용해 예측 분포를 시각화하는 함수
    
    매개변수:
    - df: CSV 파일에서 불러온 예측 결과 데이터프레임
    - time_points: 시각화할 시간대 리스트
    """
    
    plots = []
    for time_point in time_points:
        # 특정 시간대의 예측 값들 추출
        # predictions = df[df['Time'] == time_point].iloc[:, 1:].values.flatten()
        predictions = df[df['Time'] == time_point].iloc[:, 6:].values.flatten()

        # KDE를 위해 커널 밀도 추정 생성
        kde = gaussian_kde(predictions)
        x = np.linspace(predictions.min(), predictions.max(), 1000)
        y = kde(x)

        # ColumnDataSource 생성
        source = ColumnDataSource(data=dict(x=x, y=y))

        # Bokeh Figure 생성
        p = figure(title=f'{time_point} 에서의 사후예측분포',
                   x_axis_label='Predicted Value', 
                   y_axis_label='Density',
                   sizing_mode="stretch_both")  # 크기 자동 조절

        # KDE 플롯 추가 (실선)
        line_renderer = p.line('x', 'y', source=source, line_width=2, color='darkblue', alpha=1.0)

        # 실선 아래 영역 채우기
        p.patch('x', 'y', source=source, color='darkblue', alpha=0.5)

        # HoverTool 추가 (mode='vline' 설정으로 수직선 위의 line 값 표시)
        hover = HoverTool(renderers=[line_renderer], tooltips=[
            ("Predicted Value", "@x"),
            ("Density", "@y")
        ], mode='vline')
        p.add_tools(hover)

        plots.append(p)
    
    # 플롯을 그리드 레이아웃으로 배치 (가로로 3개씩)
    grid = gridplot(plots, ncols=3, sizing_mode="stretch_both")
    
    return grid




# Bokeh를 사용한 시각화 함수 2 : 전체 test_data에 대한 prediction vs true value

####################################################################################
####################################################################################





def plot_predictions_with_uncertainty_bokeh(pred_uncer, selected_datetime, show_blue_line):
    """
    Bokeh를 이용한 시간대별 예측 분포 시각화 함수

    매개변수:
    - pred_uncer: 예측 및 불확실성 데이터를 포함한 DataFrame
    """

    # 시간 데이터를 datetime 형태로 변환
    pred_uncer['Time'] = pd.to_datetime(pred_uncer['Time'])

    # DataFrame 생성
    data = {
        'Time': pred_uncer['Time'],
        'Prediction': pred_uncer['Mean_Prediction'],
        'Uncertainty': pred_uncer['Uncertainty']*300,  # 경향성만 판단하면 되므로 보정
        'Lower_Bound': pred_uncer['Lower_Bound'],
        'Upper_Bound': pred_uncer['Upper_Bound'],
        # 'True_Values': pred_uncer['True_Value']
        'True_Values': pred_uncer[pred_uncer.columns[1]]
    }

    df = pd.DataFrame(data)

    # ColumnDataSource 생성
    source = ColumnDataSource(df)

    # Figure 생성
    p = figure(x_axis_type='datetime', 
               width=1900,
               height=700, 
               title="Test 데이터에 대한 예측 값과 실제 값",
               x_axis_label='Time', 
               y_axis_label='MHC Water Level', 
               sizing_mode="stretch_both")

    # True Values 라인 추가
    true_values_renderer = p.line('Time', 'True_Values', source=source, legend_label='관측된 미호천교 수위', line_width=3, color='darkred')

    # Predictions 라인 추가
    p.line('Time', 'Prediction', source=source, legend_label='예측된 미호천교 수위', line_width=3, color='darkblue')

    # Uncertainty 라인 추가
    p.line('Time', 'Uncertainty', source=source, legend_label='예측된 불확실성', line_width=3, color='#464646')

    # 95% Prediction Interval 밴드 추가
    band = Band(base='Time', lower='Lower_Bound', upper='Upper_Bound', source=source, level='underlay',
                fill_alpha=0.3, line_width=1, line_color='darkblue', fill_color='red')
    p.add_layout(band)
    
    # 고정된 값의 상태선 추가
    p.line(x=pred_uncer['Time'], y=9.2, color='purple', line_dash="dashed", legend_label="심각(9.2m)")
    p.line(x=pred_uncer['Time'], y=8.0, color='red', line_dash="dashed", legend_label="경계(8.0m)")
    p.line(x=pred_uncer['Time'], y=7.0, color='yellow', line_dash="dashed", legend_label="주의(7.0m)")
    p.line(x=pred_uncer['Time'], y=5.0, color='green', line_dash="dashed", legend_label="관심(5.0m)")
    
    # show_blue_line 값이 True인 경우 파란선을 추가
    if show_blue_line: 
        p.line(x=[selected_datetime, selected_datetime], 
               y=[0, pred_uncer[pred_uncer.columns[1]].max()],
               color='#000080', line_dash="dotted", line_width=3)

    # HoverTool 생성 및 True Values 라인에만 적용
    hover = HoverTool(
        renderers=[true_values_renderer],  # True Values 라인에만 적용
        tooltips=[
            ("Time", "@Time{%F %T}"),
            ("True Value", "@True_Values"),
            ("Predicted Value", "@Prediction"),
            ("Uncertainty", "@Uncertainty")
        ],
        formatters={
            "@Time": "datetime"
        },
        mode='vline'  # 수직선 위의 값만 표시
    )
    
    # HoverTool 추가
    p.add_tools(hover)
    
    # 레전드 설정
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    # 레이아웃 설정
    layout_obj = layout([[p]])

    return layout_obj


####################################################################################
####################################################################################
