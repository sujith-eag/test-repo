import { useEffect, useState } from 'react'
import { apiRequest } from '../api.js'

export default function Submissions() {
  const [submissions, setSubmissions] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiRequest('/api/submissions/me')
      .then(data => setSubmissions(data.submissions))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <section>
      <div className="page-heading">
        <h1>Submission History</h1>
        <p>Your personal transmission log.</p>
      </div>
      {loading && <p>Loading log...</p>}
      {error && <p className="alert error">{error}</p>}
      <div className="panel">
        <table>
          <thead><tr><th>Time</th><th>Status</th><th>Challenge</th><th>Points</th></tr></thead>
          <tbody>
            {submissions.map(item => <tr key={item.id}>
              <td>{new Date(item.created_at).toLocaleString()}</td>
              <td>{item.is_correct ? 'Correct' : 'Incorrect'}</td>
              <td>{item.challenge ? item.challenge.title : 'Unknown'}</td>
              <td>{item.points_awarded}</td>
            </tr>)}
            {!submissions.length && !loading && <tr><td colSpan="4">No submissions yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </section>
  )
}
