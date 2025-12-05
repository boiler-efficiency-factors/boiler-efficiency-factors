import { useState } from 'react'
import './CreateAccount.css'

function CreateAccount({ onBack, onSignupComplete }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [verifyPassword, setVerifyPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // 입력값 검증
    const trimmedUsername = username.trim()
    const trimmedPassword = password.trim()
    const trimmedVerifyPassword = verifyPassword.trim()
    
    if (!trimmedUsername) {
      alert('아이디를 입력해주세요.')
      return
    }
    
    if (!trimmedPassword) {
      alert('비밀번호를 입력해주세요.')
      return
    }
    
    if (!trimmedVerifyPassword) {
      alert('비밀번호 확인을 입력해주세요.')
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
    
    if (trimmedPassword !== trimmedVerifyPassword) {
      alert('비밀번호가 일치하지 않습니다.')
      return
    }
    
    setLoading(true)
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/register/', {
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
        alert('회원가입이 완료되었습니다!')
        onSignupComplete()
      } else {
        const text = await response.text()
        console.error('Server error:', text)
        try {
          const data = JSON.parse(text)
          alert(data.error || '회원가입에 실패했습니다.')
        } catch {
          alert('서버 오류가 발생했습니다. 콘솔을 확인해주세요.')
        }
      }
    } catch (error) {
      console.error('Signup error:', error)
      alert('서버와 연결할 수 없습니다.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="create-account-container">
      <div className="create-account-box">
        <div className="header">
          <button onClick={onBack} className="back-button">
            ←
          </button>
          <h1 className="title">Create Account</h1>
        </div>
        
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
          
          <input
            type="password"
            placeholder="Verify Password"
            value={verifyPassword}
            onChange={(e) => setVerifyPassword(e.target.value)}
            className="input-field"
            required
            minLength={4}
            disabled={loading}
          />
          
          <button type="submit" className="register-button" disabled={loading}>
            {loading ? '가입 중...' : '회원가입'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default CreateAccount
