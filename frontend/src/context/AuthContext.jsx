import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { apiRequest, clearToken, getToken, setToken } from '../api.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  async function refreshUser() {
    if (!getToken()) {
      setUser(null)
      setLoading(false)
      return null
    }

    try {
      const data = await apiRequest('/api/auth/me')
      setUser(data.user)
      return data.user
    } catch (error) {
      clearToken()
      setUser(null)
      return null
    } finally {
      setLoading(false)
    }
  }

  async function login(username, password) {
    const data = await apiRequest('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
    setToken(data.token)
    setUser(data.user)
    return data.user
  }

  async function register(username, password) {
    const data = await apiRequest('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
    setToken(data.token)
    setUser(data.user)
    return data.user
  }

  function logout() {
    clearToken()
    setUser(null)
  }

  useEffect(() => {
    refreshUser()
  }, [])

  const value = useMemo(() => ({
    user,
    loading,
    isAuthenticated: Boolean(user),
    login,
    register,
    logout,
    refreshUser,
    setUser
  }), [user, loading])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
