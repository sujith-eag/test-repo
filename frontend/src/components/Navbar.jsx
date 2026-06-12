import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Navbar() {
  const { user, logout } = useAuth()

  return (
    <header className="navbar" data-shadow-nav="CTF{navbar_trace}">
      <Link to="/" className="brand">
        <span className="brand-mark" aria-hidden="true">
          <img src="/assets/favicon.jpeg" alt="" className="brand-logo" />
        </span>
        <span>Shadow Protocol</span>
      </Link>

      <nav className="nav-links">
        <NavLink to="/intel">Intel</NavLink>
        <NavLink to="/rules">Rules</NavLink>
        <NavLink to="/challenges">Challenges</NavLink>
        <NavLink to="/submit">Submit</NavLink>
        <NavLink to="/scoreboard">Scoreboard</NavLink>
        {user && <NavLink to="/submissions">Submissions</NavLink>}
      </nav>

      <div className="nav-auth">
        {user ? (
          <>
            <span className="user-chip">{user.username} · {user.score} pts</span>
            <button className="btn btn-ghost" onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link className="btn btn-ghost" to="/login">Login</Link>
            <Link className="btn btn-primary" to="/register">Join</Link>
          </>
        )}
      </div>
    </header>
  )
}