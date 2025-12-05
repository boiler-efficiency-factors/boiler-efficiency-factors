import { useState, useEffect } from 'react'
import './Dashboard.css'
import { authenticatedFetch } from '../utils/api'

function Dashboard({ username, onLogout }) {
  const [workspaceName, setWorkspaceName] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [modelType, setModelType] = useState('모델 선택')
  const [hyperparameters, setHyperparameters] = useState([
    { key: 'learning_rate', value: '0.9' },
    { key: 'n_estimators', value: '0.8' }
  ])
  const [variableSelection, setVariableSelection] = useState('출력 변수')
  const [independentVars, setIndependentVars] = useState([
    { key: '종속(조건)', value: '' }
  ])

  const addHyperparameter = () => {
    setHyperparameters([...hyperparameters, { key: '', value: '' }])
  }

  const removeHyperparameter = (index) => {
    setHyperparameters(hyperparameters.filter((_, i) => i !== index))
  }

  const addIndependentVar = () => {
    setIndependentVars([...independentVars, { key: '', value: '' }])
  }

  const removeIndependentVar = (index) => {
    setIndependentVars(independentVars.filter((_, i) => i !== index))
  }

  // 컴포넌트 로드 시 프로필 확인 (토큰 테스트)
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await authenticatedFetch('/auth/profile/')
        if (response.ok) {
          const data = await response.json()
          console.log('인증 성공:', data)
        }
      } catch (error) {
        console.error('인증 실패:', error)
      }
    }
    checkAuth()
  }, [])

  const handleSubmit = async () => {
    console.log('학습 시작하기')
    // 예시: 인증된 API 호출
    try {
      const response = await authenticatedFetch('/your-endpoint/', {
        method: 'POST',
        body: JSON.stringify({
          workspace_name: workspaceName,
          model_type: modelType,
        }),
      })
      
      if (response.ok) {
        const data = await response.json()
        console.log('성공:', data)
      }
    } catch (error) {
      console.error('에러:', error)
    }
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="user-info">
          [{username}]의 연구실
        </div>
        <button onClick={onLogout} className="logout-button">
          로그아웃
        </button>
      </header>

      <div className="dashboard-content">
        <aside className="sidebar">
          <h3>워크스페이스</h3>
          <ul className="workspace-list">
            <li>워크스페이스1</li>
            <li>워크스페이스2</li>
            <li>테스트</li>
            <li>테스트2</li>
            <li>테스트3</li>
            <li>테스트4</li>
            <li>테스트5</li>
            <li>테스트6</li>
            <li>테스트7</li>
            <li>테스트8</li>
          </ul>
        </aside>

        <main className="main-content">
          <div className="form-container">
            <div className="form-group">
              <label>워크스페이스 이름*</label>
              <input
                type="text"
                placeholder="워크스페이스 이름"
                value={workspaceName}
                onChange={(e) => setWorkspaceName(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>데이터 기간 선택*</label>
              <div className="date-range">
                <input
                  type="text"
                  placeholder="시작 날짜"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                />
                <input
                  type="text"
                  placeholder="끝 날짜"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                />
              </div>
            </div>

            <div className="form-group">
              <label>모델 선택*</label>
              <select value={modelType} onChange={(e) => setModelType(e.target.value)}>
                <option>모델 선택</option>
                <option>Linear Regression</option>
                <option>Random Forest</option>
                <option>XGBoost</option>
              </select>
            </div>

            <div className="form-group">
              <label>하이퍼파라미터 선택</label>
              <select>
                <option>파라미터</option>
              </select>
              {hyperparameters.map((param, index) => (
                <div key={index} className="param-item">
                  <input
                    type="text"
                    value={`${param.key} : ${param.value}`}
                    readOnly
                  />
                  <button onClick={() => removeHyperparameter(index)}>×</button>
                </div>
              ))}
            </div>

            <div className="form-group">
              <label>종속 변수 선택*</label>
              <select value={variableSelection} onChange={(e) => setVariableSelection(e.target.value)}>
                <option>출력 변수</option>
                <option>효율</option>
                <option>온도</option>
              </select>
            </div>

            <div className="form-group">
              <label>제외할 독립 변수 선택</label>
              <select>
                <option>제외할 독립 변수</option>
              </select>
              {independentVars.map((varItem, index) => (
                <div key={index} className="param-item">
                  <input
                    type="text"
                    value={varItem.key}
                    placeholder="종속(조건)"
                    readOnly
                  />
                  <button onClick={() => removeIndependentVar(index)}>×</button>
                </div>
              ))}
            </div>

            <div className="button-group">
              <button className="btn-secondary">학습 저장하기</button>
              <button className="btn-primary" onClick={handleSubmit}>학습하기</button>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Dashboard
