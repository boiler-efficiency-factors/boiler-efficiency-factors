# 보일러 효율 분석 백엔드

보일러 효율 영향인자 분석을 위한 Django REST API 백엔드입니다.

## 주요 기능

- **CSV 파일 업로드**: 보일러 데이터 CSV 파일 업로드 및 자동 전처리
- **AI 모델 지원**: LightGBM, XGBoost, Random Forest, Gradient Boosting Machine
- **효율 영향인자 분석**: 특성 중요도 분석 및 시각화
- **모델 파라미터 조정**: 실시간 하이퍼파라미터 튜닝
- **예측 및 평가**: 성능 지표 제공 및 예측 결과 분석

## 설치 및 실행

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 데이터베이스 설정
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 슈퍼유저 생성 (선택사항)
```bash
python manage.py createsuperuser
```

### 4. 서버 실행
```bash
python manage.py runserver
```

또는 자동 스크립트 사용:
```bash
python run_server.py
```

## API 엔드포인트

### 프로젝트 관리
- `GET /api/projects/` - 프로젝트 목록 조회
- `POST /api/projects/` - 새 프로젝트 생성
- `POST /api/projects/{id}/upload_csv/` - CSV 파일 업로드
- `GET /api/projects/{id}/data_preview/` - 데이터 미리보기
- `POST /api/projects/{id}/train_model/` - 모델 훈련
- `GET /api/projects/{id}/analysis_results/` - 분석 결과 조회

### 모델 설정
- `GET /api/models/` - 모델 설정 목록
- `POST /api/models/{id}/update_parameters/` - 파라미터 업데이트

### 분석 결과
- `GET /api/results/` - 결과 목록
- `GET /api/results/{id}/feature_importance_chart/` - 특성 중요도 차트
- `GET /api/results/{id}/prediction_chart/` - 예측 결과 차트

## 데이터 전처리

기존 AI 폴더의 `utils/preprocessor.py`를 활용하여 다음과 같은 전처리를 수행합니다:

1. **불필요한 컬럼 제거**: 생성일, 진동센서, 고장 확률 등
2. **결측치 처리**: 수치형(평균), 범주형(최빈값)
3. **범주형 변수 인코딩**: 레이블 인코딩
4. **피처 스케일링**: StandardScaler 적용
5. **이상치 제거**: IQR 방법 사용

## 지원 모델

### LightGBM
- 기본 파라미터: num_leaves=31, learning_rate=0.05
- 빠른 훈련 속도와 높은 성능

### XGBoost  
- 기본 파라미터: max_depth=6, learning_rate=0.1
- 강력한 부스팅 알고리즘

### Random Forest
- 기본 파라미터: n_estimators=100
- 안정적인 앙상블 방법

### Gradient Boosting Machine
- 순차적 부스팅 알고리즘
- 높은 예측 성능과 특성 중요도 제공

## 성능 지표

- **RMSE**: Root Mean Square Error
- **MAE**: Mean Absolute Error  
- **R² Score**: 결정계수
- **MAPE**: Mean Absolute Percentage Error

## 디렉토리 구조

```
src/backend/
├── boiler_analysis/          # 메인 앱
│   ├── models.py            # 데이터베이스 모델
│   ├── views.py             # API 뷰
│   ├── serializers.py       # 데이터 직렬화
│   ├── services.py          # 비즈니스 로직
│   ├── urls.py              # URL 라우팅
│   └── admin.py             # 관리자 페이지
├── mysite/                  # Django 프로젝트 설정
├── media/                   # 업로드된 파일 저장
├── requirements.txt         # 패키지 목록
└── run_server.py           # 서버 실행 스크립트
```

## 개발 참고사항

- Django 4.0.10 사용
- SQLite 데이터베이스 (개발용)
- CORS 설정으로 프론트엔드 연동 지원
- 파일 업로드 크기 제한: 50MB