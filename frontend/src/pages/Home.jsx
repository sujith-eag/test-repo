import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Home() {
  const { user } = useAuth()

  return (
    <section className="hero">
      <span className="invisible-fragment">{"CTF{lights_spell_the_warning}"}</span>
      <div className="eyebrow">Live CTF Operation</div>
      <h1>Enter the Hawkins Shadow Protocol</h1>
      <p>
        A cyber breach has opened around Hawkins Lab systems. Recover hidden fragments from browser traces, forgotten files, encoded transmissions, and exposed web routes. No series knowledge is required — every clue is technical.
      </p>
      <div className="hero-actions">
        <Link className="btn btn-primary" to="/challenges">Open Challenge Board</Link>
        <Link className="btn btn-ghost" to="/intel">Read Briefing</Link>
        {user ? <Link className="btn btn-ghost" to="/submit">Transmit Flag</Link> : <Link className="btn btn-ghost" to="/register">Join Operation</Link>}
      </div>
      <div className="grid three">
        <div className="panel"><h3>Recon</h3><p>Check forgotten files and gate-related signals.</p></div>
        <div className="panel"><h3>Frontend Forensics</h3><p>Inspect browser storage, attributes, console output, and source.</p></div>
        <div className="panel"><h3>Web Exploitation</h3><p>Probe challenge-only lab routes for hidden fragments.</p></div>
      </div>
    </section>
  )
}