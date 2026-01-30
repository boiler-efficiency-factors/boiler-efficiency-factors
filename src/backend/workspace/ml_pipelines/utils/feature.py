import io
import base64
import platform
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

def feature(model, X_train: pd.DataFrame, top_n: int = 10) -> tuple[str, pd.DataFrame]:
    """
    모델의 feature_importances_ 기반으로
    상위 top_n 피처 중요도 그래프를 만들고 base64 PNG 문자열로 반환
    상위 top_n 피처 중요도와 그래프 반환
    """
    system_name = platform.system()
    if system_name == 'Windows':
        rc('font', family='Malgun Gothic')
    elif system_name == 'Darwin':
        rc('font', family='AppleGothic')
    else:
        try:
            rc('font', family='NanumGothic')
        except:
            pass
    plt.rcParams['axes.unicode_minus'] = False

    importance = model.feature_importances_

    # 컬럼명 추출
    feature_names = (
        list(X_train.columns)
        if hasattr(X_train, "columns")
        else [f"f{i}" for i in range(len(importance))]
    )

    importance_df = (
        pd.DataFrame({"feature": feature_names, "importance": importance})
        .sort_values(by="importance", ascending=False)
    )

    top_features = importance_df.head(top_n).iloc[::-1]

    # 시각화
    plt.figure(figsize=(12, 6))
    plt.barh(top_features["feature"], top_features["importance"])
    plt.xlabel("Importance", fontsize=12)
    plt.ylabel("Feature", fontsize=12)
    plt.title(f"Top {top_n} Important Features", fontsize=14)
    plt.tight_layout()

    # PNG → base64 변환
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    img_base64: str = base64.b64encode(buffer.read()).decode("utf-8")
    return img_base64, top_features
