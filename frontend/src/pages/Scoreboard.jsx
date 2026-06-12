import { useEffect, useState } from 'react'
import { apiRequest } from '../api.js'

export default function Scoreboard() {
  const [rows, setRows] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiRequest('/api/scoreboard')
      .then(data => setRows(data.scoreboard))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <section>
      <div className="page-heading">
        <div className="eyebrow">Operator Rankings</div>
        <h1>Scoreboard</h1>
        <p>Operators ranked by recovered protocol fragments.</p>
      </div>
      {loading && <p>Synchronizing rankings...</p>}
      {error && <p className="alert error">{error}</p>}
      <div className="panel">
        <table>
          <thead><tr><th>Rank</th><th>Operator</th><th>Score</th><th>Solves</th></tr></thead>
          <tbody>
            {rows.map(row => <tr key={row.username}><td>#{row.rank}</td><td>{row.username}</td><td>{row.score}</td><td>{row.solved_count}</td></tr>)}
            {!rows.length && !loading && <tr><td colSpan="4">No operators ranked yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </section>
  )
}