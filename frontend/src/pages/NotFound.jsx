import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <section className="panel center-block">
      <h1>404 · Signal Lost</h1>
      <p>This route does not exist in the current protocol map.</p>
      <Link className="btn btn-primary" to="/">Return Home</Link>
    </section>
  )
}
