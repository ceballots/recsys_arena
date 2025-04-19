import pandas as pd


def win_rate(df: pd.DataFrame, model: str) -> float:
    """Computes the win rate for a model"""
    return len(df[df["winner"] == model]) / len(df)
