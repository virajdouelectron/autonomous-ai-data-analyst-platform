import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from utils.db import get_dataset


def detect_problem_type(target: pd.Series) -> str:
    """Detect whether the problem is classification or regression."""
    unique_count = int(target.nunique(dropna=True))
    if target.dtype == object or not np.issubdtype(target.dtype, np.number):
        return "classification"

    if unique_count <= 10:
        return "classification"

    return "regression"


def prepare_features(df: pd.DataFrame, target_column: str) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset")

    df = df.copy()
    X = df.drop(columns=[target_column])
    y = df[target_column]

    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

    transformers = []
    if numeric_features:
        transformers.append(("num", StandardScaler(), numeric_features))
    if categorical_features:
        transformers.append(("cat", OneHotEncoder(handle_unknown="ignore", sparse=False), categorical_features))

    if transformers:
        preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
        X_transformed = preprocessor.fit_transform(X)
        feature_names: list[str] = []
        if numeric_features:
            feature_names.extend(numeric_features)
        if categorical_features:
            ohe = preprocessor.named_transformers_["cat"]
            categories = ohe.categories_
            for col, cats in zip(categorical_features, categories):
                feature_names.extend([f"{col}_{cat}" for cat in cats])
        X = pd.DataFrame(X_transformed, columns=feature_names, index=X.index)
    else:
        X = X.copy()
        feature_names = X.columns.tolist()

    return X, y, feature_names


def fit_models(X_train: pd.DataFrame, y_train: pd.Series, problem_type: str) -> dict[str, object]:
    if problem_type == "classification":
        return {
            "RandomForestClassifier": RandomForestClassifier(n_estimators=100, random_state=42),
            "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        }

    return {
        "RandomForestRegressor": RandomForestRegressor(n_estimators=100, random_state=42),
        "LinearRegression": LinearRegression(),
    }


def evaluate_model(model: object, X_test: pd.DataFrame, y_test: pd.Series, problem_type: str) -> dict[str, float]:
    predictions = model.predict(X_test)
    if problem_type == "classification":
        return {
            "accuracy": float(accuracy_score(y_test, predictions)),
            "f1_score": float(f1_score(y_test, predictions, average="weighted", zero_division=0)),
        }

    return {
        "mse": float(mean_squared_error(y_test, predictions)),
        "r2": float(r2_score(y_test, predictions)),
    }


def train_dataset_model(dataset_id: str, target_column: str, test_size: float = 0.2, random_state: int = 42) -> dict:
    df = get_dataset(dataset_id)
    if df.empty:
        raise ValueError("The dataset is empty and cannot be used for training.")

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")

    problem_type = detect_problem_type(df[target_column])
    X, y, feature_names = prepare_features(df, target_column)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y if problem_type == "classification" and y.nunique() > 1 else None
    )

    candidate_models = fit_models(X_train, y_train, problem_type)
    results: dict[str, dict] = {}

    for model_name, model in candidate_models.items():
        model.fit(X_train, y_train)
        metrics = evaluate_model(model, X_test, y_test, problem_type)

        feature_importance = None
        if hasattr(model, "feature_importances_"):
            feature_importance = {
                feature: float(value)
                for feature, value in zip(feature_names, model.feature_importances_)
            }
        elif hasattr(model, "coef_"):
            coef = model.coef_
            if coef.ndim == 1:
                values = coef
            else:
                values = coef.ravel()
            feature_importance = {
                feature: float(value)
                for feature, value in zip(feature_names, values[: len(feature_names)])
            }

        results[model_name] = {
            "metrics": metrics,
            "model_type": model.__class__.__name__,
            "feature_importance": feature_importance,
        }

    if problem_type == "classification":
        best_model_name = max(results, key=lambda name: results[name]["metrics"]["accuracy"])
    else:
        best_model_name = max(results, key=lambda name: results[name]["metrics"]["r2"])

    return {
        "dataset_id": dataset_id,
        "target_column": target_column,
        "problem_type": problem_type,
        "best_model": best_model_name,
        "best_model_metrics": results[best_model_name]["metrics"],
        "best_model_feature_importance": results[best_model_name]["feature_importance"],
        "candidate_models": results,
        "feature_columns": feature_names,
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
    }
