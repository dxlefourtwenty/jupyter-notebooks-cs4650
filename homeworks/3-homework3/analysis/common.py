#!/usr/bin/env python3

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
PERMUTATION_REPEATS = 10
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "FRAFirm.csv"
OUTPUT_DIR = ROOT / "outputs"


@dataclass
class EvaluationSummary:
    task_name: str
    labels: list[str]
    class_counts: dict[str, int]
    majority_baseline_accuracy: float
    cv_accuracy: float
    cv_balanced_accuracy: float
    cv_macro_f1: float
    holdout_accuracy: float
    holdout_balanced_accuracy: float
    holdout_macro_f1: float
    confusion_matrix: list[list[int]]
    classification_report: dict[str, Any]
    top_features: list[dict[str, float]]


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def build_pipeline(frame: pd.DataFrame, include_firm: bool) -> Pipeline:
    feature_frame = frame.drop(columns=["class"])
    numeric_columns = [
        column
        for column in feature_frame.columns
        if column != "FIRM" and feature_frame[column].nunique() > 1
    ]
    categorical_columns = ["FIRM"] if include_firm and "FIRM" in feature_frame.columns else []

    transformers: list[tuple[str, Pipeline, list[str]]] = [
        (
            "numeric",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            ),
            numeric_columns,
        )
    ]

    if categorical_columns:
        transformers.append(
            (
                "firm",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_columns,
            )
        )

    return Pipeline(
        [
            ("preprocessor", ColumnTransformer(transformers, remainder="drop")),
            (
                "classifier",
                LogisticRegression(
                    max_iter=5000,
                    class_weight="balanced",
                    solver="lbfgs",
                ),
            ),
        ]
    )


def evaluate_pipeline(
    *,
    frame: pd.DataFrame,
    target: pd.Series,
    task_name: str,
    labels: list[str],
    include_firm: bool,
) -> EvaluationSummary:
    feature_frame = frame.drop(columns=["class"])
    pipeline = build_pipeline(frame, include_firm=include_firm)
    splitter = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    cv_scores = cross_validate(
        pipeline,
        feature_frame,
        target,
        cv=splitter,
        scoring={
            "accuracy": "accuracy",
            "balanced_accuracy": "balanced_accuracy",
            "macro_f1": "f1_macro",
        },
    )

    train_features, test_features, train_target, test_target = train_test_split(
        feature_frame,
        target,
        test_size=TEST_SIZE,
        stratify=target,
        random_state=RANDOM_STATE,
    )

    pipeline.fit(train_features, train_target)
    predictions = pipeline.predict(test_features)

    matrix = confusion_matrix(test_target, predictions)
    report = classification_report(
        test_target,
        predictions,
        output_dict=True,
        target_names=labels,
        zero_division=0,
    )

    importance = permutation_importance(
        pipeline,
        test_features,
        test_target,
        scoring="balanced_accuracy",
        n_repeats=PERMUTATION_REPEATS,
        random_state=RANDOM_STATE,
    )

    importance_frame = pd.DataFrame(
        {
            "feature": test_features.columns,
            "mean_importance": importance.importances_mean,
            "std_importance": importance.importances_std,
        }
    ).sort_values("mean_importance", ascending=False)

    save_confusion_matrix(task_name, matrix, labels)
    save_importance_chart(task_name, importance_frame)
    save_report_csv(task_name, report)

    class_counts = target.value_counts().sort_index()

    return EvaluationSummary(
        task_name=task_name,
        labels=labels,
        class_counts={str(key): int(value) for key, value in class_counts.items()},
        majority_baseline_accuracy=float(class_counts.max() / class_counts.sum()),
        cv_accuracy=float(np.mean(cv_scores["test_accuracy"])),
        cv_balanced_accuracy=float(np.mean(cv_scores["test_balanced_accuracy"])),
        cv_macro_f1=float(np.mean(cv_scores["test_macro_f1"])),
        holdout_accuracy=float(accuracy_score(test_target, predictions)),
        holdout_balanced_accuracy=float(balanced_accuracy_score(test_target, predictions)),
        holdout_macro_f1=float(f1_score(test_target, predictions, average="macro")),
        confusion_matrix=matrix.tolist(),
        classification_report=report,
        top_features=[
            {
                "feature": row.feature,
                "mean_importance": float(row.mean_importance),
                "std_importance": float(row.std_importance),
            }
            for row in importance_frame.head(10).itertuples(index=False)
        ],
    )


def save_confusion_matrix(task_name: str, matrix: np.ndarray, labels: list[str]) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    figure, axis = plt.subplots(figsize=(6, 5))
    display = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=labels)
    display.plot(ax=axis, cmap="Blues", colorbar=False)
    axis.set_title(f"{task_name.replace('_', ' ').title()} Confusion Matrix")
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / f"{task_name}_confusion_matrix.png", dpi=200)
    plt.close(figure)


def save_importance_chart(task_name: str, importance_frame: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    top_rows = importance_frame.head(10).iloc[::-1]
    figure, axis = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top_rows, x="mean_importance", y="feature", ax=axis, color="#4C78A8")
    axis.set_title(f"{task_name.replace('_', ' ').title()} Feature Importance")
    axis.set_xlabel("Average importance")
    axis.set_ylabel("Feature")
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / f"{task_name}_feature_importance.png", dpi=200)
    plt.close(figure)


def save_report_csv(task_name: str, report: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    pd.DataFrame(report).transpose().to_csv(OUTPUT_DIR / f"{task_name}_classification_report.csv")


def write_summary(filename: str, summaries: list[EvaluationSummary]) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    payload = {summary.task_name: asdict(summary) for summary in summaries}
    with (OUTPUT_DIR / filename).open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def print_summary(summary: EvaluationSummary) -> None:
    print(summary.task_name)
    print(f"  holdout_accuracy={summary.holdout_accuracy:.4f}")
    print(f"  holdout_balanced_accuracy={summary.holdout_balanced_accuracy:.4f}")
    print(f"  holdout_macro_f1={summary.holdout_macro_f1:.4f}")
    print(f"  top_feature={summary.top_features[0]['feature']}")
