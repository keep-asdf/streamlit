import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def visualize_moving_averages_with_cross_highlighted(dataframe):
    """
    Visualize the predicted MHC water level, its moving averages, confidence intervals, and status lines from the given dataframe.
    
    Parameters:
    - dataframe: A pandas DataFrame with columns 'Time', 'Predicted_MHC_Water_Level', 'CI_Lower', 'CI_Upper', 
    and other columns for moving averages.
    """
    # Convert the Time column to datetime format for better plotting in a copied dataframe
    df_copy = dataframe.copy()
    df_copy['Time'] = pd.to_datetime(df_copy['Time'])

    # Set the theme
    sns.set_theme(style="darkgrid")

    # Create the plot
    plt.figure(figsize=(15, 6))
    sns.lineplot(x='Time', y='Predicted_MHC_Water_Level', data=df_copy, label='Predicted Water Level', color='blue')
    plt.fill_between(df_copy['Time'], df_copy['CI_Lower'], df_copy['CI_Upper'], color='blue', alpha=0.3)
    
    # Check for crosses where 12H_MA crosses other MAs
    prev_12H = None
    for i, row in df_copy.iterrows():
        for column in df_copy.columns:
            if "MA" in column and column != "12H_MA":
                if prev_12H is not None and prev_12H < df_copy.at[i-1, column] and row["12H_MA"] > row[column]:
                    plt.scatter(row['Time'], row['12H_MA'], color='gold', marker='x', s=100)
        prev_12H = row["12H_MA"]
    
    # Adding the moving averages
    for column in df_copy.columns:
        if "MA" in column:
            if column == "12H_MA":
                sns.lineplot(x='Time', y=column, data=df_copy, label=column, linewidth=2.5, color='darkred')
            else:
                sns.lineplot(x='Time', y=column, data=df_copy, label=column)
    
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

    # Display the plot
    plt.show()
    plt.close()
