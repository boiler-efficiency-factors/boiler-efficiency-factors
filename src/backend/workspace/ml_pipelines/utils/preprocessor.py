import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

def process_boiler_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()

    # 1. 불필요 컬럼 제거
    cols_to_drop = [
        '생성일', '소비전류', '진동센서1', '진동센서2', '운전시간', '정상 운전 확률', 
        '송풍기 고장 확률', 'AIR 댐퍼 고장 확률', 'GAS 앰퍼 고장 확률', 
        '확률 업데이트 시간', '순간 스팀량', '입출력법 효율',
        '열 손실법 효율', '효율(입출력법-스팀)'
    ]
    df = df.drop(columns=cols_to_drop, errors='ignore')

    # 2. 결측치 처리 및 인코딩 (범주형)
    cat_cols = df.select_dtypes(include=['object']).columns
    if not cat_cols.empty:
        # 결측치 -> 최빈값
        imputer = SimpleImputer(strategy='most_frequent')
        df[cat_cols] = imputer.fit_transform(df[cat_cols])
        
        # 인코딩
        le = LabelEncoder()
        for col in cat_cols:
            df[col] = df[col].astype(str)
            df[col] = le.fit_transform(df[col])

    # 3. 결측치 처리 및 스케일링 (수치형)
    num_cols = df.select_dtypes(include=np.number).columns
    if not num_cols.empty:
        # 결측치 -> 평균
        num_imputer = SimpleImputer(strategy='mean')
        df[num_cols] = num_imputer.fit_transform(df[num_cols])
        
        # 스케일링
        scaler = StandardScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])

    return df