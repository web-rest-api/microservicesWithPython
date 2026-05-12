import { Routes, Route, Link } from 'react-router-dom'
import UsersPage from './pages/UsersPage'
import GamesPage from './pages/GamesPage'

const App = () => {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="p-4 flex gap-6 border-b border-gray-800">
        <Link to="/users" className="hover:text-blue-400">Users</Link>
        <Link to="/games" className="hover:text-blue-400">Games</Link>
      </nav>
      <main className="p-6">
        <Routes>
          <Route path="/users" element={<UsersPage />} />
          <Route path="/games" element={<GamesPage />} />
          <Route path="*" element={<p className="text-gray-400">Select a section above.</p>} />
        </Routes>
      </main>
    </div>
  )
}

export default App