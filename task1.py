import pandas as pd
import numpy as np


def calculate(df: pd.DataFrame) -> tuple:
    # Calculate daily returns
    # Formula = (Current Close/Prev Close) - 1
    df['Daily Returns'] = df['Close'] / df['Close'].shift(periods=1) - 1

    # Calculate daily volatility
    daily_volatility = np.std(df['Daily Returns'])

    # Calculate annualized volatility
    annualized_volatility = daily_volatility * np.sqrt(len(df))
    
    # print(f"Daily Returns: {df['Daily Returns']}")

    return daily_volatility, annualized_volatility


if __name__ == '__main__':

    # Load the dataset
    df = pd.read_csv(filepath_or_buffer="NIFTY 50.csv")

    # Strip leading/trailing space in Col names
    df.columns = df.columns.str.strip()

    # Ensure the dataset has a 'Close' column
    if 'Close' not in df.columns:
        raise ValueError("The dataset must contain a 'Close' column.")

    daily_volatility, annualized_volatility = calculate(df=df)

    # Print the results
    print(f"Daily Volatility: {daily_volatility}")
    print(f"Annualized Volatility: {annualized_volatility}")
