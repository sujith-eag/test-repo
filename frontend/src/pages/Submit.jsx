import { useState } from 'react'
import { apiRequest } from '../api.js'
import { useAuth } from '../context/AuthContext.jsx'

export default function Submit() {
  const { setUser } = useAuth()
  const [flag, setFlag] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setResult(null)
    setLoading(true)
    try {
      const data = await apiRequest('/api/submissions', {
        method: 'POST',
        body: JSON.stringify({ flag })
      })
      setResult(data)
      if (data.user) setUser(data.user)
      setFlag('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="auth-page">
      <form className="panel form wide" onSubmit={handleSubmit} data-shadow-submit="CTF{red_door_accepts_the_signal}">
        <div className="eyebrow">Flag Transmission</div>
        <h1>Submit Signal Fragment</h1>
        <p>Transmit a recovered Hawkins Shadow Protocol flag to the scoring engine.</p>
        <label>Recovered flag</label>
        <input placeholder="CTF{...}" value={flag} onChange={e => setFlag(e.target.value)} required />
        <button className="btn btn-primary" disabled={loading}>{loading ? 'Transmitting...' : 'Submit Flag'}</button>
        {error && <p className="alert error">{error}</p>}
        {result && <div className={`alert ${result.status === 'correct' ? 'success' : result.status === 'duplicate' ? 'warning' : 'error'}`}>
          <strong>{result.status.toUpperCase()}</strong>
          <p>{result.message}</p>
          {result.points_awarded !== undefined && <p>Points awarded: {result.points_awarded}</p>}
        </div>}
      </form>
    </section>
  )
}