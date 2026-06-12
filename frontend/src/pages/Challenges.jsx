import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiRequest } from '../api.js'
import ChallengeCard from '../components/ChallengeCard.jsx'

export default function Challenges() {
  const [challenges, setChallenges] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiRequest('/api/challenges')
      .then(data => setChallenges(data.challenges))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <section>
      <div className="page-heading">
        <div className="eyebrow">Challenge Board</div>
        <h1>Recover Protocol Fragments</h1>
        <p>Each card contains the intel needed to begin. Use only the intended app and <code>/vuln/*</code> routes.</p>
      </div>
      {loading && <p>Loading classified board...</p>}
      {error && <p className="alert error">{error}</p>}
      <div className="grid">
        {challenges.map(challenge => <ChallengeCard key={challenge.id} challenge={challenge} />)}
      </div>
      <div className="center-block">
        <Link className="btn btn-primary" to="/submit">Submit Recovered Flag</Link>
      </div>
    </section>
  )
}