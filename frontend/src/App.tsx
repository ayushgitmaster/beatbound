import { Routes, Route, Outlet } from 'react-router-dom'
import { Sidebar } from './components/Sidebar'
import Landing from './pages/Landing'
import Chat from './pages/Chat'
import Symptom from './pages/Symptom'
import Lab from './pages/Lab'
import Risk from './pages/Risk'
import Resources from './pages/Resources'
import About from './pages/About'
import Explain from './pages/Explain'

function Layout() {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="ml-60 flex-1 overflow-hidden flex flex-col">
        <Outlet />
      </main>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route element={<Layout />}>
        <Route path="/chat"      element={<Chat />} />
        <Route path="/symptom"   element={<Symptom />} />
        <Route path="/lab"       element={<Lab />} />
        <Route path="/risk"      element={<Risk />} />
        <Route path="/explain"   element={<Explain />} />
        <Route path="/resources" element={<Resources />} />
        <Route path="/about"     element={<About />} />
      </Route>
    </Routes>
  )
}
