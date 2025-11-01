import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from IPython.display import display

def preprocessor(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    보일러 원본 데이터를 받아 전처리 파이프라인을 수행하는 함수

    Args:
        raw_df (pd.DataFrame): 전처리 전의 원본 데이터프레임

    Returns:
        pd.DataFrame: 전처리가 완료된 데이터프레임
    """
    
    print("--- 데이터 전처리 시작 ---")
    # 원본 데이터프레임을 복사하여 사용 (원본 데이터 보존)
    df = raw_df.copy()

    # --- 1. 불필요한 컬럼 제거 ---
    columns_to_drop = [
        '생성일', '소비전류', '진동센서1', '진동센서2', '운전시간', '정상 운전 확률', '송풍기 고장 확률',
        'AIR 댐퍼 고장 확률', 'GAS 앰퍼 고장 확률', '확률 업데이트 시간', '순간 스팀량', '입출력법 효율',
        '열 손실법 효율', '효율(입출력법-스팀)'
    ]
    df = df.drop(columns=columns_to_drop)
    print(f"✅ 1. 불필요한 컬럼 {len(columns_to_drop)}개 제거 완료")

    # --- 2. '효율(순간)' 컬럼 필터링 ---
    # (효율(순간) 값이 100 미만인 행만 남깁니다)
    if '효율(순간)' in df.columns:
        df = df[df['효율(순간)'] < 100]
        print("✅ 2. '효율(순간)' 컬럼 값 100 미만으로 필터링 완료")
    else:
        print("ℹ️ 2. '효율(순간)' 컬럼이 데이터에 없습니다.")

    # --- 3. 결측치 처리 및 범주형 변수 변환 ---
    # (코드에서는 결측치 처리 후 인코딩을 수행하고 있습니다)

    # 3-1. 범주형 데이터 결측치 처리 (최빈값으로 대체)
    categorical_cols = df.select_dtypes(include=['object']).columns
    if not categorical_cols.empty:
        cat_imputer = SimpleImputer(strategy='most_frequent')
        df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])
        print("✅ 3-1. 범주형 데이터 결측치 처리 완료")
    
        # 3-2. 범주형 변수 변환 (레이블 인코딩)
        label_encoder = LabelEncoder()
        for col in categorical_cols:
            df[col] = label_encoder.fit_transform(df[col])
        print("✅ 3-2. 범주형 변수 변환 완료")
    else:
        print("ℹ️ 3-2. 처리할 범주형 데이터가 없습니다.")

    # 3-3. 수치형 데이터 결측치 처리 (평균으로 대체)
    # (사용자 코드에는 없었지만, 일반적으로 수치형 결측치 처리도 필요합니다)
    numeric_cols = df.select_dtypes(include=np.number).columns
    if df[numeric_cols].isnull().sum().sum() > 0:
        num_imputer = SimpleImputer(strategy='mean')
        df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])
        print("✅ 3-3. 수치형 데이터 결측치 처리 완료")
    else:
        print("ℹ️ 3-3. 처리할 수치형 결측치가 없습니다.")


    # --- 4. 피처 스케일링 ---
    scaler = StandardScaler()
    # 스케일링은 수치형 데이터에만 적용됩니다.
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    print("✅ 4. 피처 스케일링 완료")
    
    print("--- 데이터 전처리 완료 ---")
    
    return df