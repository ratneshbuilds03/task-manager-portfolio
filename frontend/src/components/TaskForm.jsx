import { useState } from 'react'
import { FiX } from 'react-icons/fi'
import './TaskForm.css'

export default function TaskForm({ onSubmit, onCancel }) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState('medium')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (!title.trim()) {
      setError('Title is required')
      return
    }

    setLoading(true)
    try {
      await onSubmit({ title, description, priority })
      setTitle('')
      setDescription('')
      setPriority('medium')
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to create task')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2>Create New Task</h2>
        <button type="button" className="btn-close" onClick={onCancel}>
          <FiX />
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="form-group">
        <label htmlFor="title">Task Title *</label>
        <input
          id="title"
          type="text"
          placeholder="What needs to be done?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          maxLength={200}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          placeholder="Add more details about this task..."
          value={description}
          maxLength={5000}
          onChange={(e) => setDescription(e.target.value)}
          rows={4}
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="priority">Priority</label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
      </div>

      <div className="form-actions">
        <button type="button" className="btn-cancel" onClick={onCancel}>
          Cancel
        </button>
        <button type="submit" className="btn-submit" disabled={loading}>
          {loading ? 'Creating...' : 'Create Task'}
        </button>
      </div>
    </form>
  )
}
