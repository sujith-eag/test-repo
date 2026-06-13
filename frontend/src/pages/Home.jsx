import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Home() {
  const { user } = useAuth()

  return (
    <section className="hero">
      <span className="invisible-fragment">{"CTF{home_invisible_fragment}"}</span>
      <div className="eyebrow">Live CTF Operation</div>
      <h1>Enter the Shadow Protocol</h1>
      <p>
        Recover hidden fragments from browser traces, forgotten files, encoded transmissions,
        and exposed web routes. Submit confirmed flags to climb the operator board.
      </p>
      <div className="hero-actions">
        <Link className="btn btn-primary" to="/challenges">Open Challenge Board</Link>
        <Link className="btn btn-ghost" to="/intel">Read Intel</Link>
        {user ? <Link className="btn btn-ghost" to="/submit">Transmit Flag</Link> : <Link className="btn btn-ghost" to="/register">Create Operator</Link>}
      </div>
      <div className="grid three">
        <div className="panel"><h3>Recon</h3><p>Check forgotten files and exposed signals.</p></div>
        <div className="panel"><h3>Frontend Forensics</h3><p>Inspect the browser, storage, attributes, and console.</p></div>
        <div className="panel"><h3>Web Exploitation</h3><p>Probe challenge-only routes for protocol fragments.</p></div>
      </div>
    </section>
  )
}
