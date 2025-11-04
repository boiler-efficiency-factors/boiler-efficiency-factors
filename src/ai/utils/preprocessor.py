import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from IPython.display import display

def safe_copy(df: pd.DataFrame) -> pd.DataFrame:
    # 원본 데이터프레임을 복사하여 사용 (원본 데이터 보존)
    return df.copy()

def object_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    # 문자형(object)인데 숫자로 변환 가능한 컬럼을 숫자로 변환
    df = safe_copy(df)
    object_cols = df.select_dtypes(include=['object']).columns
    for col in object_cols:
        converted = pd.to_numeric(df[col], errors='ignore')
        # 숫자로 변환되었으면 dtype이 변경
        if not isinstance(converted, pd.Series) or converted.dtype != df[col].dtype:
            df[col] = converted
    return df

# --- 불필요한 컬럼 제거 ---
def drop_unnecessary_columns(
    df: pd.DataFrame,
    columns_to_drop: Optional[list] = None,
) -> pd.DataFrame:
    df = safe_copy(df)
    if columns_to_drop is None:
        columns_to_drop = [
            '생성일', '소비전류', '진동센서1', '진동센서2', '운전시간', '정상 운전 확률', '송풍기 고장 확률',
            'AIR 댐퍼 고장 확률', 'GAS 앰퍼 고장 확률', '확률 업데이트 시간', '순간 스팀량', '입출력법 효율',
            '열 손실법 효율', '효율(입출력법-스팀)'
        ]
    print(f"✅ 1. 불필요한 컬럼 {len(columns_to_drop)}개 제거 완료")
    return df.drop(columns=columns_to_drop, errors='ignore')

# --- '효율(순간)' 컬럼 필터링 ---
def filter_instant_efficiency(df: pd.DataFrame) -> pd.DataFrame:
    df = safe_copy(df)
    if '효율(순간)' in df.columns:
        df = df[df['효율(순간)'] < 100] # 효율(순간) 값이 100 미만인 행만 남깁니다
        print("✅ 2. '효율(순간)' 컬럼 값 100 미만으로 필터링 완료")
    else:
        print("ℹ️ 2. '효율(순간)' 컬럼이 데이터에 없습니다.")
    return df

# --- 결측치 처리 및 범주형 변수 변환 ---
# (코드에서는 결측치 처리 후 인코딩을 수행하고 있습니다)

def impute_categorical_and_label_encode(df: pd.DataFrame) -> pd.DataFrame:
    # 범주형 데이터 결측치 처리 및 변수 변환
    df = safe_copy(df)
    # 1. 범주형 데이터 결측치 처리 (최빈값으로 대체)
    categorical_cols = df.select_dtypes(include=['object']).columns
    if not categorical_cols.empty:
        cat_imputer = SimpleImputer(strategy='most_frequent')
        df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])
        print("✅ 3-1. 범주형 데이터 결측치 처리 완료")
    
        # 2. 범주형 변수 변환 (레이블 인코딩)
        label_encoder = LabelEncoder()
        for col in categorical_cols:
            df[col] = label_encoder.fit_transform(df[col])
        print("✅ 3-2. 범주형 변수 변환 완료")
    else:
        print("ℹ️ 3-2. 처리할 범주형 데이터가 없습니다.")
    return df

def impute_numeric(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=np.number).columns
    if df[numeric_cols].isnull().sum().sum() > 0:
        num_imputer = SimpleImputer(strategy=strategy)
        df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])
        print("✅ 3-3. 수치형 데이터 결측치 처리 완료")
    else:
        print("ℹ️ 3-3. 처리할 수치형 결측치가 없습니다.")
    return df

# --- 피처 스케일링 ---
def scale_numeric(df: pd.DataFrame, scaler: Optional[StandardScaler] = None) -> pd.DataFrame:
    df = safe_copy(df)
    numeric_cols = df.select_dtypes(include=np.number).columns
    if len(numeric_cols) == 0:
        return df

    scaler = scaler if scaler is not None else StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    print("✅ 4. 피처 스케일링 완료")
    return df

# --- 전체 파이프라인 ---
def preprocessor(
    raw_df: pd.DataFrame,
    *,
    columns_to_drop: Optional[list] = None,
    numeric_impute_strategy: str = 'mean',
    ) -> pd.DataFrame:
    """
    원본 데이터를 복사한 뒤, 아래 순서로 전처리를 수행합니다:
    1) 불필요한 컬럼 제거
    2) 도메인 규칙 필터링 (효율(순간) < 100)
    3) 범주형 결측치 대체 & LabelEncoding
    4) 수치형 결측치 대체
    5) 수치형 스케일링
    """
    print("--- 데이터 전처리 시작 ---")

    df = raw_df.copy()

    df = drop_unnecessary_columns(df, columns_to_drop)
    print("✅ 1. 불필요한 컬럼 제거 완료")

    df = filter_instant_efficiency(df)

    df = impute_categorical_and_label_encode(df)

    df = impute_numeric(df, strategy=numeric_impute_strategy)

    df = scale_numeric(df)

    print("--- 데이터 전처리 완료 ---")
    return df

'''def preprocessor(raw_df: pd.DataFrame) -> pd.DataFrame:
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
    
    return df'''