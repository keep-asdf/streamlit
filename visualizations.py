import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def visualize_moving_averages_with_cross_highlighted(dataframe):
    """
    Visualize the predicted MHC water level, its moving averages, confidence intervals, and status lines from the given dataframe 
    and save the plot to the specified path. English labels are used to avoid font issues.
    
    Parameters:
    - dataframe: A pandas DataFrame with columns 'Time', 'Predicted_MHC_Water_Level', 'CI_Lower', 'CI_Upper', 
    and other columns for moving averages.
    - save_path: Path to save the plot. Default is "streamlit/graph/with_moving_averages_cross_highlighted.png".
    """
    # Convert the Time column to datetime format for better plotting
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])

    # Set the theme
    sns.set_theme(style="darkgrid")

    # Create the plot
    plt.figure(figsize=(15, 6))
    sns.lineplot(x='Time', y='Predicted_MHC_Water_Level', data=dataframe, label='Predicted Water Level', color='blue')
    plt.fill_between(dataframe['Time'], dataframe['CI_Lower'], dataframe['CI_Upper'], color='blue', alpha=0.3)
    
    # Check for crosses where 12H_MA crosses other MAs
    prev_12H = None
    for i, row in dataframe.iterrows():
        for column in dataframe.columns:
            if "MA" in column and column != "12H_MA":
                if prev_12H is not None and prev_12H < dataframe.at[i-1, column] and row["12H_MA"] > row[column]:
                    plt.scatter(row['Time'], row['12H_MA'], color='gold', marker='x', s=100)
        prev_12H = row["12H_MA"]
    
    # Adding the moving averages
    for column in dataframe.columns:
        if "MA" in column:
            if column == "12H_MA":
                sns.lineplot(x='Time', y=column, data=dataframe, label=column, linewidth=2.5, color='darkred')
            else:
                sns.lineplot(x='Time', y=column, data=dataframe, label=column)
    
    # Adding the status lines based on the provided criteria with English labels
    plt.axhline(9.2, color='red', linestyle='--', label='Severe')
    plt.axhline(8.0, color='orange', linestyle='--', label='Alert')
    plt.axhline(7.0, color='yellow', linestyle='--', label='Caution')
    plt.axhline(5.0, color='green', linestyle='--', label='Attention')

    plt.title("Predicted MHC Water Level with Confidence Intervals, Moving Averages and Status Lines")
    plt.ylabel("Water Level")
    plt.xlabel("Time")
    # Position the legend to the top right
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to the specified path
    plt.show()
    plt.close()

