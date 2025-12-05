# Swagger API 문서 가이드

## 🎯 Swagger란?

Swagger는 REST API를 **자동으로 문서화**하고 **테스트**할 수 있는 도구입니다.

### 장점
- ✅ API 명세서 자동 생성
- ✅ 웹 브라우저에서 API 테스트 가능
- ✅ 프론트엔드 개발자와 협업 용이
- ✅ OpenAPI 표준 준수

---

## 📍 접속 URL

서버를 실행한 후 다음 URL로 접속하세요:

### 1. Swagger UI (추천)
```
http://localhost:8000/api/docs/
```
- 가장 많이 사용되는 인터페이스
- API를 직접 테스트할 수 있음
- 예쁜 UI

### 2. ReDoc
```
http://localhost:8000/api/redoc/
```
- 문서 읽기에 최적화된 인터페이스
- 깔끔한 디자인

### 3. OpenAPI Schema (JSON)
```
http://localhost:8000/api/schema/
```
- 원본 OpenAPI 스키마 파일
- 다른 도구와 연동할 때 사용

---

## 🚀 사용 방법

### 1. 서버 실행
```bash
cd src/backend
python manage.py runserver
```

### 2. Swagger UI 접속
브라우저에서 `http://localhost:8000/api/docs/` 열기

### 3. API 테스트하기

#### Step 1: 인증 (필요시)
1. 우측 상단 "Authorize" 버튼 클릭
2. 사용자 인증 정보 입력

#### Step 2: API 선택
- 카테고리별로 API가 분류되어 있음
  - 📁 프로젝트 관리
  - 📊 데이터 관리
  - 🤖 모델 훈련
  - 📈 분석 결과

#### Step 3: API 실행
1. 원하는 API 클릭
2. "Try it out" 버튼 클릭
3. 필요한 파라미터 입력
4. "Execute" 버튼 클릭
5. 응답 결과 확인

---

## 📋 API 카테고리

### 프로젝트 관리
- `GET /api/projects/` - 프로젝트 목록
- `POST /api/projects/` - 프로젝트 생성
- `GET /api/projects/{id}/` - 프로젝트 상세
- `PUT /api/projects/{id}/` - 프로젝트 수정
- `DELETE /api/projects/{id}/` - 프로젝트 삭제

### 데이터 관리
- `POST /api/projects/{id}/upload_csv/` - CSV 업로드
- `GET /api/projects/{id}/data_preview/` - 데이터 미리보기

### 모델 훈련
- `POST /api/projects/{id}/train_model/` - 모델 훈련
- `POST /api/models/{id}/update_parameters/` - 파라미터 수정

### 분석 결과
- `GET /api/projects/{id}/analysis_results/` - 결과 목록
- `GET /api/results/{id}/feature_importance_chart/` - 특성 중요도
- `GET /api/results/{id}/prediction_chart/` - 예측 결과

---

## 💡 Swagger UI 주요 기능

### 1. 요청 예시 (Request Sample)
각 API마다 요청 예시가 자동으로 생성됩니다.

**예시: 모델 훈련**
```json
{
  "model_type": "lightgbm",
  "parameters": {
    "num_leaves": 31,
    "learning_rate": 0.05
  }
}
```

### 2. 응답 예시 (Response Sample)
가능한 응답 형식을 미리 볼 수 있습니다.

### 3. 스키마 (Schema)
데이터 구조와 필드 설명을 확인할 수 있습니다.

### 4. 파라미터 설명
- **Path Parameters**: URL에 포함되는 파라미터 (예: {id})
- **Query Parameters**: URL 뒤에 붙는 파라미터 (예: ?page=1)
- **Request Body**: POST/PUT 요청의 본문 데이터

---

## 🎨 Swagger UI 화면 구성

```
┌─────────────────────────────────────────┐
│  보일러 효율 분석 API v1.0.0            │
│  [Authorize]                            │
├─────────────────────────────────────────┤
│                                         │
│  📁 프로젝트 관리                       │
│    ▼ GET /api/projects/                │
│    ▼ POST /api/projects/               │
│                                         │
│  📊 데이터 관리                         │
│    ▼ POST /api/projects/{id}/upload_csv│
│    ▼ GET /api/projects/{id}/data_preview│
│                                         │
│  🤖 모델 훈련                           │
│    ▼ POST /api/projects/{id}/train_model│
│                                         │
│  📈 분석 결과                           │
│    ▼ GET /api/results/                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔧 설정 정보

### settings.py에 추가된 설정
```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',  # Swagger 라이브러리
]

REST_FRAMEWORK = {
    ...
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': '보일러 효율 분석 API',
    'DESCRIPTION': '보일러 효율 영향인자 분석을 위한 REST API',
    'VERSION': '1.0.0',
}
```

### urls.py에 추가된 URL
```python
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

---

## 📤 OpenAPI 스키마 파일 생성

명세서를 파일로 저장하려면:

```bash
python manage.py spectacular --color --file schema.yml
```

생성된 `schema.yml` 파일을:
- 프론트엔드 팀과 공유
- Postman에서 import
- 다른 API 도구에서 사용

---

## 🎓 발표 시 활용 방법

### 1. 라이브 데모
- Swagger UI를 화면에 띄워놓고
- 실제로 API를 호출하면서 설명
- 응답 결과를 실시간으로 보여줌

### 2. API 명세서 공유
- Swagger UI URL을 공유
- 팀원들이 직접 테스트 가능
- 문서화 작업 불필요

### 3. 프론트엔드 협업
- API 구조를 명확하게 전달
- 요청/응답 형식 합의
- 통합 테스트 용이

---

## ⚠️ 주의사항

### 프로덕션 환경
프로덕션에서는 Swagger를 비활성화하거나 인증을 추가하세요:

```python
# settings.py
if not DEBUG:
    SPECTACULAR_SETTINGS['SERVE_INCLUDE_SCHEMA'] = False
```

### 인증 필요
현재 API는 인증이 필요합니다:
- Django admin에서 사용자 생성
- Swagger UI에서 "Authorize" 버튼으로 로그인

---

## 📚 참고 자료

- drf-spectacular 공식 문서: https://drf-spectacular.readthedocs.io/
- OpenAPI 명세: https://swagger.io/specification/
- Swagger UI 사용법: https://swagger.io/tools/swagger-ui/

---

## ✅ 체크리스트

발표 전 확인사항:
- [ ] 서버가 정상 실행되는지 확인
- [ ] Swagger UI가 열리는지 확인
- [ ] 각 API가 문서에 표시되는지 확인
- [ ] 예시 데이터가 올바른지 확인
- [ ] 인증이 필요한 경우 테스트 계정 준비