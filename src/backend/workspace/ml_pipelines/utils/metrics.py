import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error

def calculate_metrics(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """
    회귀 모델 성능 지표(MSE, RMSE, MAE, MAPE) 계산
    """
    y_pred = model.predict(X_test)

    y_test_arr = np.array(y_test)
    y_pred_arr = np.array(y_pred)

    # MSE
    mse: float = mean_squared_error(y_test_arr, y_pred_arr)

    # RMSE
    rmse: float = float(np.sqrt(mse))

    # MAE
    mae: float = mean_absolute_error(y_test_arr, y_pred_arr)

    # MAPE
    non_zero_mask = y_test_arr != 0
    if np.any(non_zero_mask):
        mape: float = float(
            np.mean(
                np.abs(
                    (y_test_arr[non_zero_mask] - y_pred_arr[non_zero_mask])
                    / y_test_arr[non_zero_mask]
                )
            ) * 100.0
        )
    else:
        mape = None

    return {
        "mse": float(mse),
        "rmse": float(rmse),
        "mae": float(mae),
        "mape": float(mape) if mape is not None else None,
    }