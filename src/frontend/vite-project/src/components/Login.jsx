import { useState } from 'react'
import './Login.css'

function Login({ onCreateAccount }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Login:', { username, password })
    // TODO: 백엔드 API 연동
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1 className="title">대원글로벌에셋</h1>
        <p className="subtitle">보일러 열량 분석 AI 모델 연구</p>
        
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="User Name"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="input-field"
          />
          
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
          />
          
          <button type="submit" className="login-button">
            로그인
          </button>
        </form>
        
        <button onClick={onCreateAccount} className="create-account-link">
          Create Account
        </button>
      </div>
    </div>
  )
}

export default Login
