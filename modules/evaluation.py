import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


def print_classification_report(y_true, y_pred, y_prob, model_name: str) -> dict:
    """Imprime e retorna métricas de classificação."""
    metrics = {
        "model": model_name,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_prob),
    }
    print(f"\n{'='*50}")
    print(f"  {model_name}")
    print(f"{'='*50}")
    for k, v in metrics.items():
        if k != "model":
            print(f"  {k:<12}: {v:.4f}")
    return metrics


def plot_confusion_matrix(y_true, y_pred, model_name: str):
    """Plota heatmap da confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt=",d", cmap="Blues",
                xticklabels=["On-time", "Delayed"],
                yticklabels=["On-time", "Delayed"])
    plt.title(f"Confusion Matrix — {model_name}")
    plt.ylabel("Real")
    plt.xlabel("Predito")
    plt.tight_layout()
    plt.show()


def plot_roc_curves(results: dict):
    """Plota curvas ROC sobrepostas. results = {name: (y_true, y_prob)}."""
    plt.figure(figsize=(8, 6))
    for name, (y_true, y_prob) in results.items():
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        auc = roc_auc_score(y_true, y_prob)
        plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.4f})")
    plt.plot([0, 1], [0, 1], "k--", alpha=0.5)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Curvas ROC — Comparação")
    plt.legend()
    plt.tight_layout()
    plt.show()


def print_regression_report(y_true, y_pred, model_name: str) -> dict:
    """Imprime e retorna métricas de regressão."""
    metrics = {
        "model": model_name,
        "mae": mean_absolute_error(y_true, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
        "r2": r2_score(y_true, y_pred),
    }
    print(f"\n{'='*50}")
    print(f"  {model_name}")
    print(f"{'='*50}")
    for k, v in metrics.items():
        if k != "model":
            print(f"  {k:<12}: {v:.4f}")
    return metrics


def plot_residuals(y_true, y_pred, model_name: str):
    """Scatter de resíduos."""
    residuals = y_true - y_pred
    plt.figure(figsize=(8, 5))
    plt.scatter(y_pred, residuals, alpha=0.05, s=1)
    plt.axhline(0, color="red", linestyle="--")
    plt.xlabel("Predito")
    plt.ylabel("Resíduo (Real - Predito)")
    plt.title(f"Resíduos — {model_name}")
    plt.tight_layout()
    plt.show()


def plot_feature_importance(model, feature_names, model_name: str, top_n=15):
    """Bar chart horizontal de feature importance (compatível com sklearn/xgboost/lightgbm)."""
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_).ravel()
    else:
        print(f"Modelo {model_name} não possui feature_importances_ ou coef_")
        return

    idx = np.argsort(importances)[-top_n:]
    plt.figure(figsize=(8, 6))
    plt.barh(range(len(idx)), importances[idx], color="steelblue")
    plt.yticks(range(len(idx)), [feature_names[i] for i in idx])
    plt.title(f"Feature Importance — {model_name} (top {top_n})")
    plt.xlabel("Importância")
    plt.tight_layout()
    plt.show()
