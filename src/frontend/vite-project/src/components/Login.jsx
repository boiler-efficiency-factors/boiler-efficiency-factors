import { useState } from 'react'
import './Login.css'

function Login({ onCreateAccount, onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()

    // 입력값 검증
    const trimmedUsername = username.trim()
    const trimmedPassword = password.trim()

    if (!trimmedUsername) {
      alert('아이디를 입력해주세요.')
      return
    }

    if (!trimmedPassword) {
      alert('비밀번호를 입력해주세요.')
      return
    }

    if (trimmedUsername.length < 3) {
      alert('아이디는 3자 이상이어야 합니다.')
      return
    }

    if (trimmedPassword.length < 4) {
      alert('비밀번호는 4자 이상이어야 합니다.')
      return
    }

    setLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_name: trimmedUsername,
          password: trimmedPassword,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        // 토큰 저장
        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        localStorage.setItem('username', trimmedUsername)

        onLogin(trimmedUsername)
      } else {
        const text = await response.text()
        console.error('Server error:', text)
        try {
          const data = JSON.parse(text)
          alert(data.error || data.detail || '로그인에 실패했습니다.')
        } catch {
          alert('서버 오류가 발생했습니다. 콘솔을 확인해주세요.')
        }
      }
    } catch (error) {
      console.error('Login error:', error)
      alert('서버와 연결할 수 없습니다.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1 className="title">대림로얄이엔피</h1>
        <p className="subtitle">보일러 열량 분석 AI 모델 연구</p>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="User Name"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="input-field"
            required
            minLength={3}
            disabled={loading}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
            required
            minLength={4}
            disabled={loading}
          />

          <button type="submit" className="login-button" disabled={loading}>
            {loading ? '로그인 중...' : '로그인'}
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
