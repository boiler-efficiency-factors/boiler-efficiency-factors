import { useState } from 'react'
import './CreateAccount.css'

function CreateAccount({ onBack }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [verifyPassword, setVerifyPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (password !== verifyPassword) {
      alert('비밀번호가 일치하지 않습니다.')
      return
    }
    
    console.log('Create Account:', { username, password })
    // TODO: 백엔드 API 연동
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
          />
          
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
          />
          
          <input
            type="password"
            placeholder="Verify Password"
            value={verifyPassword}
            onChange={(e) => setVerifyPassword(e.target.value)}
            className="input-field"
          />
          
          <button type="submit" className="register-button">
            회원가입
          </button>
        </form>
      </div>
    </div>
  )
}

export default CreateAccount
