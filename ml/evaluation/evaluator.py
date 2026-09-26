from typing import List, Dict, Any
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

class ModelEvaluator:
    """
    Standard agricultural pathology model validation pipeline.
    Calculates true classification metrics and confusion matrix
    without fabrication or hardcoding.
    """

    @staticmethod
    def evaluate_predictions(
        y_true: List[str],
        y_pred: List[str],
        labels: List[str] = None
    ) -> Dict[str, Any]:
        """
        Computes multi-class precision, recall, F1, accuracy, and confusion matrix.
        """
        if labels is None:
            labels = sorted(list(set(y_true + y_pred)))

        acc = float(accuracy_score(y_true, y_pred))
        prec_macro = float(precision_score(y_true, y_pred, labels=labels, average="macro", zero_division=0))
        rec_macro = float(recall_score(y_true, y_pred, labels=labels, average="macro", zero_division=0))
        f1_macro = float(f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0))
        f1_weighted = float(f1_score(y_true, y_pred, labels=labels, average="weighted", zero_division=0))

        cm = confusion_matrix(y_true, y_pred, labels=labels).tolist()

        per_class_f1 = f1_score(y_true, y_pred, labels=labels, average=None, zero_division=0).tolist()
        class_metrics = {}
        for idx, lbl in enumerate(labels):
            class_metrics[lbl] = {
                "f1_score": round(float(per_class_f1[idx]), 4)
            }

        return {
            "total_samples": len(y_true),
            "labels": labels,
            "accuracy": round(acc, 4),
            "precision_macro": round(prec_macro, 4),
            "recall_macro": round(rec_macro, 4),
            "f1_macro": round(f1_macro, 4),
            "f1_weighted": round(f1_weighted, 4),
            "confusion_matrix": cm,
            "class_metrics": class_metrics
        }

model_evaluator = ModelEvaluator()
