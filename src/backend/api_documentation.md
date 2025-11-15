# 보일러 효율 분석 API 문서

## 개요
보일러 효율 영향인자 분석을 위한 REST API입니다.

## 주요 기능
- CSV 파일 업로드 및 전처리
- AI 모델 선택 및 훈련 (LightGBM, XGBoost, Random Forest, Linear Regression)
- 효율 영향인자 분석
- 날짜별 데이터 시각화
- 모델 파라미터 조정
- 예측 결과 분석

## API 엔드포인트

### 1. 프로젝트 관리

#### 프로젝트 생성
```
POST /api/projects/
Content-Type: application/json

{
    "name": "보일러 효율 분석 프로젝트",
    "description": "2024년 보일러 데이터 분석"
}
```

#### 프로젝트 목록 조회
```
GET /api/projects/
```

#### CSV 파일 업로드
```
POST /api/projects/{project_id}/upload_csv/
Content-Type: multipart/form-data

file: [CSV 파일]
```

#### 데이터 미리보기
```
GET /api/projects/{project_id}/data_preview/
```

### 2. 모델 훈련

#### 모델 훈련 시작
```
POST /api/projects/{project_id}/train_model/
Content-Type: application/json

{
    "model_type": "lightgbm",
    "parameters": {
        "num_leaves": 31,
        "learning_rate": 0.05,
        "feature_fraction": 0.9
    }
}
```

#### 분석 결과 조회
```
GET /api/projects/{project_id}/analysis_results/
```

### 3. 모델 설정

#### 모델 파라미터 업데이트
```
POST /api/models/{model_id}/update_parameters/
Content-Type: application/json

{
    "parameters": {
        "num_leaves": 50,
        "learning_rate": 0.1
    }
}
```

### 4. 결과 분석

#### 특성 중요도 차트 데이터
```
GET /api/results/{result_id}/feature_importance_chart/
```

#### 예측 결과 차트 데이터
```
GET /api/results/{result_id}/prediction_chart/
```

## 모델별 기본 파라미터

### LightGBM
```json
{
    "objective": "regression",
    "metric": "rmse",
    "boosting_type": "gbdt",
    "num_leaves": 31,
    "learning_rate": 0.05,
    "feature_fraction": 0.9
}
```

### XGBoost
```json
{
    "objective": "reg:squarederror",
    "max_depth": 6,
    "learning_rate": 0.1,
    "n_estimators": 100
}
```

### Random Forest
```json
{
    "n_estimators": 100,
    "max_depth": null,
    "random_state": 42
}
```

### Gradient Boosting Machine
```json
{
    "n_estimators": 100,
    "learning_rate": 0.1,
    "max_depth": 3,
    "subsample": 0.8,
    "max_features": "sqrt"
}
```

## 응답 형식

### 성공 응답
```json
{
    "message": "성공 메시지",
    "data": {...}
}
```

### 오류 응답
```json
{
    "error": "오류 메시지"
}
```

## 성능 지표
- RMSE (Root Mean Square Error)
- MAE (Mean Absolute Error)
- R² Score
- MAPE (Mean Absolute Percentage Error)