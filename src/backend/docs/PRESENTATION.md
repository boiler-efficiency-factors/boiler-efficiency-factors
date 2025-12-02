# 보일러 효율 분석 백엔드 구현 내용

## 📋 프로젝트 개요
보일러 효율 영향인자를 분석하기 위한 Django REST API 백엔드 시스템

---

## 🏗️ 시스템 아키텍처

### 기술 스택
- **프레임워크**: Django 5.2.7 + Django REST Framework
- **데이터베이스**: SQLite (개발용)
- **AI/ML 라이브러리**: scikit-learn, LightGBM, XGBoost
- **데이터 처리**: pandas, numpy

### 프로젝트 구조
```
src/backend/
├── boiler_analysis/          # 메인 애플리케이션
│   ├── models.py            # 데이터베이스 모델
│   ├── views.py             # API 엔드포인트
│   ├── serializers.py       # 데이터 직렬화
│   ├── services.py          # 비즈니스 로직
│   ├── preprocessor.py      # 데이터 전처리
│   ├── urls.py              # URL 라우팅
│   └── admin.py             # 관리자 페이지
├── mysite/                  # Django 설정
└── media/                   # 업로드 파일 저장소
```

---

## 💾 데이터베이스 설계

### 1. AnalysisProject (분석 프로젝트)
- 사용자별 분석 프로젝트 관리
- 프로젝트명, 설명, 생성일 등 메타데이터 저장

### 2. DataFile (CSV 파일)
- 업로드된 보일러 데이터 CSV 파일 관리
- 파일 경로, 크기, 전처리 상태 추적

### 3. ModelConfiguration (AI 모델 설정)
- 선택한 AI 모델 타입 저장
- 하이퍼파라미터 설정 (JSON 형태)
- 훈련 완료 여부 관리

### 4. AnalysisResult (분석 결과)
- 특성 중요도 (효율 영향인자)
- 성능 지표 (RMSE, MAE, R², MAPE)
- 예측 결과 데이터

---

## 🔧 핵심 기능 구현

### 1. CSV 파일 업로드 및 전처리
**엔드포인트**: `POST /api/projects/{id}/upload_csv/`

**처리 과정**:
1. CSV 파일 업로드 (최대 50MB)
2. 자동 전처리 파이프라인 실행
   - 불필요한 컬럼 제거 (생성일, 진동센서, 고장 확률 등 14개)
   - 결측치 처리 (수치형: 평균, 범주형: 최빈값)
   - 범주형 변수 레이블 인코딩
   - 피처 스케일링 (StandardScaler)
   - 이상치 제거 (IQR 방법)
3. 전처리된 데이터 저장

**코드 위치**: `preprocessor.py`, `services.py`

### 2. AI 모델 선택 및 훈련
**엔드포인트**: `POST /api/projects/{id}/train_model/`

**지원 모델** (4가지):
1. **LightGBM**
   - 빠른 훈련 속도
   - 기본 파라미터: num_leaves=31, learning_rate=0.05

2. **XGBoost**
   - 강력한 부스팅 알고리즘
   - 기본 파라미터: max_depth=6, learning_rate=0.1

3. **Random Forest**
   - 안정적인 앙상블 방법
   - 기본 파라미터: n_estimators=100

4. **Gradient Boosting Machine**
   - 순차적 부스팅
   - 기본 파라미터: max_depth=3, subsample=0.8

**훈련 프로세스**:
1. 전처리된 데이터 로드
2. 타겟 변수 자동 식별 (효율 관련 컬럼)
3. 데이터 분할 (Train 80% / Test 20%)
4. 모델 훈련 및 특성 중요도 계산
5. 성능 평가 및 결과 저장

**코드 위치**: `services.py` - `ModelTrainingService`

### 3. 효율 영향인자 분석
**엔드포인트**: `GET /api/results/{id}/feature_importance_chart/`

**제공 정보**:
- 각 특성(변수)의 중요도 점수
- 효율에 가장 큰 영향을 미치는 인자 순위
- 모델별 특성 중요도 비교 가능

### 4. 모델 파라미터 조정
**엔드포인트**: `POST /api/models/{id}/update_parameters/`

**기능**:
- 실시간 하이퍼파라미터 수정
- JSON 형태로 유연한 파라미터 관리
- 재훈련 없이 설정 변경 가능

### 5. 성능 평가 및 예측 결과
**엔드포인트**: `GET /api/results/{id}/prediction_chart/`

**제공 지표**:
- **RMSE**: 예측 오차의 제곱근
- **MAE**: 평균 절대 오차
- **R² Score**: 결정계수 (모델 설명력)
- **MAPE**: 평균 절대 백분율 오차

**예측 데이터**:
- 실제값 vs 예측값 비교
- 시각화를 위한 데이터 제공

---

## 🔄 API 워크플로우

```
1. 프로젝트 생성
   POST /api/projects/
   
2. CSV 파일 업로드
   POST /api/projects/{id}/upload_csv/
   
3. 데이터 미리보기
   GET /api/projects/{id}/data_preview/
   
4. 모델 선택 및 훈련
   POST /api/projects/{id}/train_model/
   {
     "model_type": "lightgbm",
     "parameters": {...}
   }
   
5. 분석 결과 조회
   GET /api/projects/{id}/analysis_results/
   
6. 특성 중요도 확인
   GET /api/results/{id}/feature_importance_chart/
   
7. 예측 결과 확인
   GET /api/results/{id}/prediction_chart/
```

---

## 🛡️ 보안 및 설정

### CORS 설정
- 프론트엔드 연동을 위한 CORS 허용
- 허용 도메인: localhost:3000, 127.0.0.1:3000

### 인증
- Django 세션 인증
- Token 인증 지원 (REST Framework)
- 사용자별 프로젝트 격리

### 파일 업로드 제한
- 최대 파일 크기: 50MB
- 허용 파일 형식: CSV만

---

## 📊 데이터 전처리 상세

### 제거되는 컬럼 (14개)
```
생성일, 소비전류, 진동센서1, 진동센서2, 운전시간,
정상 운전 확률, 송풍기 고장 확률, AIR 댐퍼 고장 확률,
GAS 앰퍼 고장 확률, 확률 업데이트 시간, 순간 스팀량,
입출력법 효율, 열 손실법 효율, 효율(입출력법-스팀)
```

### 전처리 파이프라인
1. **컬럼 제거**: 분석에 불필요한 메타데이터 제거
2. **결측치 처리**: 
   - 수치형: 평균값으로 대체
   - 범주형: 최빈값으로 대체
3. **인코딩**: 범주형 변수를 숫자로 변환
4. **스케일링**: 표준화 (평균 0, 표준편차 1)
5. **이상치 제거**: IQR 방법 (1.5 * IQR 범위 밖 제거)

---

## 🎯 주요 특징

### 1. 모듈화된 설계
- **Models**: 데이터 구조 정의
- **Views**: API 엔드포인트 처리
- **Services**: 비즈니스 로직 분리
- **Serializers**: 데이터 검증 및 변환

### 2. 확장 가능한 구조
- 새로운 AI 모델 추가 용이
- 전처리 파이프라인 커스터마이징 가능
- 다양한 데이터 형식 지원 가능

### 3. 에러 처리
- 파일 업로드 검증
- 모델 훈련 실패 처리
- 사용자 친화적 에러 메시지

### 4. 성능 최적화
- 조건부 라이브러리 import
- 데이터베이스 쿼리 최적화
- 파일 저장 효율화

---

## 📈 실행 결과

### 데이터베이스 마이그레이션
```bash
✅ 4개 모델 생성 완료
✅ 관계 설정 완료
✅ 인덱스 생성 완료
```

### API 서버 실행
```bash
✅ Django 서버 실행 성공
✅ 포트: 8000
✅ API 브라우저: http://localhost:8000/api/
✅ 관리자 페이지: http://localhost:8000/admin/
```

---

## 🔮 향후 개선 방향

1. **데이터베이스**: PostgreSQL로 전환 (프로덕션)
2. **캐싱**: Redis 도입으로 성능 향상
3. **비동기 처리**: Celery로 모델 훈련 백그라운드 처리
4. **모니터링**: 로깅 및 성능 모니터링 강화
5. **배포**: Docker 컨테이너화 및 CI/CD 구축

---

## 📝 개발 환경

- **Python**: 3.12
- **Django**: 5.2.7
- **DRF**: 3.16.1
- **OS**: Windows
- **개발 도구**: VS Code, Kiro IDE

---

## 👥 역할 분담

**백엔드 담당**:
- Django REST API 설계 및 구현
- 데이터베이스 모델링
- AI 모델 통합
- 데이터 전처리 파이프라인 구축
- API 문서화

---

## 📚 참고 자료

- Django 공식 문서: https://docs.djangoproject.com/
- DRF 공식 문서: https://www.django-rest-framework.org/
- scikit-learn 문서: https://scikit-learn.org/
- LightGBM 문서: https://lightgbm.readthedocs.io/
- XGBoost 문서: https://xgboost.readthedocs.io/