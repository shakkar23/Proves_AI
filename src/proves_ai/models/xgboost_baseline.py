from __future__ import annotations

from typing import Any

import xgboost as xgb


def build_xgboost_model(params: dict[str, Any] | None = None) -> xgb.XGBClassifier:
    default_params: dict[str, Any] = {
        "n_estimators": 300,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.9,
        "colsample_bytree": 0.9,
        "objective": "binary:logistic",
        "eval_metric": "logloss",
    }
    if params:
        default_params.update(params)
    return xgb.XGBClassifier(**default_params)
