import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(form.username, form.password)
      navigate('/challenges')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="auth-page">
      <form className="panel form" onSubmit={handleSubmit}>
        <h1>Operator Login</h1>
        <label>Username</label>
        <input value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} required />
        <label>Password</label>
        <input type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required />
        {error && <p className="alert error">{error}</p>}
        <button className="btn btn-primary" disabled={loading}>{loading ? 'Authenticating...' : 'Login'}</button>
        <p>Need clearance? <Link to="/register">Register here</Link>.</p>
      </form>
    </section>
  )
}
