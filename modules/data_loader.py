import numpy as np
import pandas as pd


def load_flights_clean(path="../data/flights_clean.parquet") -> pd.DataFrame:
    """Carrega o dataset de voos limpo a partir do Parquet."""
    return pd.read_parquet(path)


def _build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Constrói a feature matrix com 26 features (12 numéricas + 14 airline dummies)."""
    feature_cols = ["MONTH", "DAY_OF_WEEK", "DEP_HOUR", "SEASON", "IS_WEEKEND", "DISTANCE",
                    "IS_SHORT_DISTANCE", "IS_LONG_DISTANCE",
                    "IS_MORNING", "IS_AFTERNOON", "IS_NIGHT",
                    "IS_HOLIDAY"]
    airline_dummies = pd.get_dummies(df["AIRLINE"], prefix="AIRLINE")
    return pd.concat([df[feature_cols], airline_dummies], axis=1)


def _split(X, y, seed=42, test_size=0.2):
    """Split determinístico usando np.random.default_rng."""
    rng = np.random.default_rng(seed)
    n = len(X)
    idx = rng.permutation(n)
    split = int(n * (1 - test_size))
    train_idx, test_idx = idx[:split], idx[split:]
    return X.iloc[train_idx], X.iloc[test_idx], y.iloc[train_idx], y.iloc[test_idx]


def build_classification_split(df: pd.DataFrame, seed=42, test_size=0.2):
    """Retorna X_train, X_test, y_train, y_test para classificação (IS_DELAYED)."""
    X = _build_features(df)
    y = df["IS_DELAYED"]
    return _split(X, y, seed, test_size)


def build_regression_split(df: pd.DataFrame, seed=42, test_size=0.2):
    """Retorna X_train, X_test, y_train, y_test para regressão (DEPARTURE_DELAY > 0)."""
    df_delayed = df[df["DEPARTURE_DELAY"] > 0].copy()
    X = _build_features(df_delayed)
    y = df_delayed["DEPARTURE_DELAY"]
    return _split(X, y, seed, test_size)
