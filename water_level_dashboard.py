
# # import streamlit as st
# # from visualizations import *


# # # Streamlit app
# # def main():
# #     st.title("Water Level Dashboard")

# #     # 데이터를 로드합니다.
# #     @st.cache_data
# #     def load_data():
# #         return pd.read_csv('data/water_level_with_moving_averages.csv').copy()  # 실제 데이터 경로로 바꾸세요.

# #     data = load_data()

# #     st.bokeh_chart(visualize_moving_averages_with_bokeh(data))
# #     st.write(data)  # 데이터 프레임을 표로도 표시합니다.

# # if __name__ == '__main__':
# #     main()
# import streamlit as st
# from visualizations import *
# import pandas as pd

# # Streamlit app
# def main():
#     st.title("Water Level Dashboard")

#     # 사이드바를 사용하여 그래프 선택
#     graph_selection = st.sidebar.selectbox("Choose a Graph", ["Moving Averages", "True vs Predicted with CI"])

#     if graph_selection == "Moving Averages":
#         # 데이터를 로드합니다.
#         @st.cache_data
#         def load_data_moving_averages():
#             return pd.read_csv('data/water_level_with_moving_averages.csv').copy()

#         data_moving_averages = load_data_moving_averages()

#         st.bokeh_chart(visualize_moving_averages_with_bokeh(data_moving_averages))
#         st.write(data_moving_averages)

#     elif graph_selection == "True vs Predicted with CI":
#         # 데이터를 로드합니다.
#         @st.cache_data
#         def load_data_true_pred():
#             return pd.read_csv('data/true_pred_with_CI.csv').copy()

#         data_true_pred = load_data_true_pred()

#         st.bokeh_chart(visualize_true_pred_with_CI_and_status_lines_bokeh(data_true_pred))
#         st.write(data_true_pred)

# if __name__ == '__main__':
#     main()

# import streamlit as st
# from visualizations import *
# import pandas as pd

# # Streamlit app
# def main():
#     st.title("Water Level Dashboard")

#     # 사이드바에 버튼을 추가합니다.
#     update_button = st.sidebar.button("Update Data")

#     # 사이드바를 사용하여 그래프 선택
#     graph_selection = st.sidebar.selectbox("Choose a Graph", ["Moving Averages", "True vs Predicted with CI"])

#     if graph_selection == "Moving Averages":
#         # 데이터를 로드합니다.
#         @st.cache(allow_output_mutation=True)
#         def load_data_moving_averages():
#             return pd.read_csv('data/water_level_with_moving_averages.csv').copy()

#         data_moving_averages = load_data_moving_averages()

#         st.bokeh_chart(visualize_moving_averages_with_bokeh(data_moving_averages))
#         st.write(data_moving_averages)

#     elif graph_selection == "True vs Predicted with CI":
#         # 데이터를 로드합니다.
#         @st.cache(allow_output_mutation=True)
#         def load_data_true_pred():
#             return pd.read_csv('data/true_pred_with_CI.csv').copy()

#         data_true_pred = load_data_true_pred()

#         st.bokeh_chart(visualize_true_pred_with_CI_and_status_lines_bokeh(data_true_pred))
#         st.write(data_true_pred)

# if __name__ == '__main__':
#     main()


# import streamlit as st
# from visualizations import *
# import pandas as pd

# # Streamlit app
# def main():
#     st.title("Water Level Dashboard")

#     # 사이드바에 버튼을 추가합니다.
#     update_button = st.sidebar.button("Update Data")

#     # 사이드바를 사용하여 그래프 선택
#     graph_selection = st.sidebar.selectbox("Choose a Graph", ["Moving Averages", "True vs Predicted with CI"])

#     if graph_selection == "Moving Averages":
#         # 데이터를 로드합니다.
#         @st.cache_data
#         def load_data_moving_averages():
#             return pd.read_csv('data/water_level_with_moving_averages.csv').copy()

#         data_moving_averages = load_data_moving_averages()

#         st.bokeh_chart(visualize_moving_averages_with_bokeh(data_moving_averages))
#         st.write(data_moving_averages)

#     elif graph_selection == "True vs Predicted with CI":
#         # 데이터를 로드합니다.
#         @st.cache_data
#         def load_data_true_pred():
#             return pd.read_csv('data/true_pred_with_CI.csv').copy()

#         data_true_pred = load_data_true_pred()

#         st.bokeh_chart(visualize_true_pred_with_CI_and_status_lines_bokeh(data_true_pred))
#         st.write(data_true_pred)

# if __name__ == '__main__':
#     main()


import streamlit as st
from visualizations import *
import pandas as pd
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import plotly.express as px
import io


# Streamlit app
def main():
    st.title("Water Level Dashboard")

    # 사이드바에 버튼을 추가합니다.
    update_button = st.sidebar.button("Update Data")

    # 사이드바를 사용하여 그래프 선택
    # graph_selection = st.sidebar.selectbox("Choose a Graph", ["Moving Averages", "True vs Predicted with CI"])
    with st.sidebar:
    choice = option_menu("Menu", ["Moving Averages", "True vs Predicted with CI", ],
                         # icons=['house', 'kanban', 'bi bi-robot'],
    #                      menu_icon="app-indicator", default_index=0,
    #                      styles={
    #     "container": {"padding": "4!important", "background-color": "#fafafa"},
    #     "icon": {"color": "black", "font-size": "25px"},
    #     "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
    #     "nav-link-selected": {"background-color": "#08c7b4"},
    # }
    )
    
    
    if graph_selection == "Moving Averages":
        # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
        @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
        def load_data_moving_averages():
            return pd.read_csv('data/water_level_with_moving_averages.csv').copy()

        data_moving_averages = load_data_moving_averages()

        st.bokeh_chart(visualize_moving_averages_with_bokeh(data_moving_averages))
        st.write(data_moving_averages)

    elif graph_selection == "True vs Predicted with CI":
        # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
        @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
        def load_data_true_pred():
            return pd.read_csv('data/true_pred_with_CI.csv').copy()

        data_true_pred = load_data_true_pred()

        st.bokeh_chart(visualize_true_pred_with_CI_and_status_lines_bokeh(data_true_pred))
        st.write(data_true_pred)

if __name__ == '__main__':
    main()
