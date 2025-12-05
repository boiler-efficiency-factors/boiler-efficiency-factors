import { useState, useEffect } from 'react'
import './App.css'
import Login from './components/Login'
import CreateAccount from './components/CreateAccount'
import Dashboard from './components/Dashboard'

function App() {
  const [currentPage, setCurrentPage] = useState('login') // 'login', 'signup', 'dashboard'
  const [username, setUsername] = useState('')

  // 페이지 로드 시 토큰 확인
  useEffect(() => {
    // 개발용: 토큰이 없으면 자동으로 설정 (나중에 삭제!)
    const token = localStorage.getItem('access_token')
    if (!token) {
      localStorage.setItem('access_token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0OTM5MzEwLCJpYXQiOjE3NjQ5MzU3MTAsImp0aSI6IjM2ZmM4MTkyNDliOTQ0ZGFiYjIwYmI2YmVmNzI1YWI1IiwidXNlcl9pZCI6IjEifQ.5ktg0Ok9C-i2frbO9tmQoGQntHvbsvV8m-MnUDxKYrM')
      localStorage.setItem('refresh_token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NTU0MDUxMCwiaWF0IjoxNzY0OTM1NzEwLCJqdGkiOiIwNGM0MjM0YzUxMWI0MDJiYTM1YTUyYjc1YWY1YWRjMCIsInVzZXJfaWQiOiIxIn0.y_o6WwfG-UZ14V0Z-MGbL_sTP6QMd3GdneRLyk09_Fs')
      localStorage.setItem('username', 'admin')
    }

    const savedToken = localStorage.getItem('access_token')
    const savedUsername = localStorage.getItem('username')

    if (savedToken && savedUsername) {
      setUsername(savedUsername)
      setCurrentPage('dashboard')
    }
  }, [])

  const handleLogin = (user) => {
    setUsername(user)
    setCurrentPage('dashboard')
  }

  const handleSignupComplete = () => {
    setCurrentPage('login')
  }

  const handleLogout = () => {
    // 토큰 삭제
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('username')

    setUsername('')
    setCurrentPage('login')
  }

  return (
    <div className="app-container">
      {currentPage === 'login' && (
        <Login
          onCreateAccount={() => setCurrentPage('signup')}
          onLogin={handleLogin}
        />
      )}
      {currentPage === 'signup' && (
        <CreateAccount
          onBack={() => setCurrentPage('login')}
          onSignupComplete={handleSignupComplete}
        />
      )}
      {currentPage === 'dashboard' && (
        <Dashboard
          username={username}
          onLogout={handleLogout}
        />
      )}
    </div>
  )
}

export default App
