import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { taskAPI } from '../services/api'
import TaskForm from '../components/TaskForm'
import TaskList from '../components/TaskList'
import { FiPlus, FiLogOut, FiFilter } from 'react-icons/fi'
import './Dashboard.css'

export default function Dashboard({ setIsAuthenticated }) {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [filters, setFilters] = useState({ status: '', priority: '' })
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [user, setUser] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    }
    fetchTasks()
  }, [filters, page])

  const fetchTasks = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await taskAPI.getTasks(
        filters.status || null,
        filters.priority || null,
        page,
        10
      )
      setTasks(response.data.tasks)
      setTotalPages(response.data.pages)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load tasks. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleAddTask = async (taskData) => {
    try {
      await taskAPI.createTask(taskData.title, taskData.description, taskData.priority)
      setShowForm(false)
      await fetchTasks()
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create task. Please try again.')
      throw err
    }
  }

  const handleUpdateTask = async (taskId, updates) => {
    try {
      await taskAPI.updateTask(taskId, updates)
      await fetchTasks()
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update task. Please try again.')
      throw err
    }
  }

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return

    try {
      await taskAPI.deleteTask(taskId)
      if (tasks.length === 1 && page > 1) {
        setPage((currentPage) => currentPage - 1)
      } else {
        await fetchTasks()
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete task. Please try again.')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    navigate('/login')
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <div>
            <h1>Task Manager</h1>
            {user && <p className="welcome-text">Welcome, {user.name}!</p>}
          </div>
          <button className="btn-logout" onClick={handleLogout}>
            <FiLogOut /> Logout
          </button>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-container">
          {error && <div className="error-message" role="alert">{error}</div>}

          <div className="controls-section">
            <button
              className="btn-add-task"
              onClick={() => setShowForm(!showForm)}
              aria-expanded={showForm}
            >
              <FiPlus /> New Task
            </button>

            <div className="filters">
              <div className="filter-group">
                <FiFilter className="filter-icon" />
                <select
                  aria-label="Filter tasks by status"
                  value={filters.status}
                  onChange={(event) => {
                    setFilters({ ...filters, status: event.target.value })
                    setPage(1)
                  }}
                >
                  <option value="">All Status</option>
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                </select>

                <select
                  aria-label="Filter tasks by priority"
                  value={filters.priority}
                  onChange={(event) => {
                    setFilters({ ...filters, priority: event.target.value })
                    setPage(1)
                  }}
                >
                  <option value="">All Priority</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>
          </div>

          {showForm && (
            <div className="form-container">
              <TaskForm onSubmit={handleAddTask} onCancel={() => setShowForm(false)} />
            </div>
          )}

          {loading ? (
            <div className="loading" role="status">Loading tasks...</div>
          ) : tasks.length > 0 ? (
            <TaskList tasks={tasks} onUpdate={handleUpdateTask} onDelete={handleDeleteTask} />
          ) : (
            <div className="no-tasks">
              <p>No tasks found. Create one to get started.</p>
            </div>
          )}

          {totalPages > 1 && (
            <nav className="pagination" aria-label="Task pages">
              <button disabled={page === 1} onClick={() => setPage(page - 1)}>
                Previous
              </button>
              <span>Page {page} of {totalPages}</span>
              <button disabled={page === totalPages} onClick={() => setPage(page + 1)}>
                Next
              </button>
            </nav>
          )}
        </div>
      </main>
    </div>
  )
}
