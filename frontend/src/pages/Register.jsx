import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      await register(form.username, form.password)
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
        <h1>Create Operator</h1>
        <label>Username</label>
        <input value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} required />
        <label>Password</label>
        <input type="password" minLength="8" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required />
        {error && <p className="alert error">{error}</p>}
        <button className="btn btn-primary" disabled={loading}>{loading ? 'Creating...' : 'Register'}</button>
        <p>Already enlisted? <Link to="/login">Login here</Link>.</p>
      </form>
    </section>
  )
}
