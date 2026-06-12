import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function ProtectedRoute({ children }) {
  const { loading, isAuthenticated } = useAuth()

  if (loading) {
    return <section className="panel"><p>Checking clearance...</p></section>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}
