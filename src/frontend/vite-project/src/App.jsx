import { useState } from 'react'
import './App.css'
import Login from './components/Login'
import CreateAccount from './components/CreateAccount'

function App() {
  const [showCreateAccount, setShowCreateAccount] = useState(false)

  return (
    <div className="app-container">
      {!showCreateAccount ? (
        <Login onCreateAccount={() => setShowCreateAccount(true)} />
      ) : (
        <CreateAccount onBack={() => setShowCreateAccount(false)} />
      )}
    </div>
  )
}

export default App
