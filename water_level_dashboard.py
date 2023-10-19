
# import streamlit as st
# from visualizations import *


# # Streamlit app
# def main():
#     st.title("Water Level Dashboard")

#     # 데이터를 로드합니다.
#     @st.cache_data
#     def load_data():
#         return pd.read_csv('data/water_level_with_moving_averages.csv').copy()  # 실제 데이터 경로로 바꾸세요.

#     data = load_data()

#     st.bokeh_chart(visualize_moving_averages_with_bokeh(data))
#     st.write(data)  # 데이터 프레임을 표로도 표시합니다.

# if __name__ == '__main__':
#     main()
import streamlit as st
from visualizations import *
import pandas as pd

# Streamlit app
def main():
    st.title("Water Level Dashboard")

    # 사이드바를 사용하여 그래프 선택
    graph_selection = st.sidebar.selectbox("Choose a Graph", ["Moving Averages", "True vs Predicted with CI"])

    if graph_selection == "Moving Averages":
        # 데이터를 로드합니다.
        @st.cache_data
        def load_data_moving_averages():
            return pd.read_csv('data/water_level_with_moving_averages.csv').copy()

        data_moving_averages = load_data_moving_averages()

        st.bokeh_chart(visualize_moving_averages_with_bokeh(data_moving_averages))
        st.write(data_moving_averages)

    elif graph_selection == "True vs Predicted with CI":
        # 데이터를 로드합니다.
        @st.cache_data
        def load_data_true_pred():
            return pd.read_csv('data/true_pred_with_CI.csv').copy()

        data_true_pred = load_data_true_pred()

        st.bokeh_chart(visualize_true_pred_with_CI_and_status_lines_bokeh(data_true_pred))
        st.write(data_true_pred)

if __name__ == '__main__':
    main()
