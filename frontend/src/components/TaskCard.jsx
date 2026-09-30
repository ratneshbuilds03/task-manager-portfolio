import { useEffect, useState } from 'react'
import { FiEdit2, FiTrash2, FiChevronDown, FiCheck, FiRotateCcw } from 'react-icons/fi'
import './TaskCard.css'

export default function TaskCard({ task, onUpdate, onDelete }) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [title, setTitle] = useState(task.title)
  const [description, setDescription] = useState(task.description || '')
  const [priority, setPriority] = useState(task.priority)
  const [status, setStatus] = useState(task.status)

  useEffect(() => {
    setTitle(task.title)
    setDescription(task.description || '')
    setPriority(task.priority)
    setStatus(task.status)
  }, [task])

  const handleSave = async () => {
    try {
      await onUpdate(task.id, { title, description, priority, status })
      setIsEditing(false)
    } catch {
      return
    }
  }

  const handleToggleStatus = async () => {
    try {
      await onUpdate(task.id, {
        status: status === 'completed' ? 'pending' : 'completed',
      })
    } catch {
      return
    }
  }

  const getStatusColor = (taskStatus) => {
    const colors = {
      pending: '#c38c2f',
      in_progress: '#317e70',
      completed: '#526c4d',
    }
    return colors[taskStatus] || '#61736e'
  }

  const getPriorityColor = (taskPriority) => {
    const colors = {
      low: '#39745c',
      medium: '#be762f',
      high: '#b94d3f',
    }
    return colors[taskPriority] || '#61736e'
  }

  return (
    <article className="task-card">
      {!isEditing ? (
        <>
          <div className="task-header">
            <div className="task-title-section">
              <button
                type="button"
                className="btn-expand"
                aria-label={isExpanded ? 'Collapse task details' : 'Expand task details'}
                onClick={() => setIsExpanded(!isExpanded)}
              >
                <FiChevronDown style={{ transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }} />
              </button>
              <h3 className="task-title">{title}</h3>
            </div>
            <div className="task-badges">
              <span className="badge status" style={{ backgroundColor: getStatusColor(status) }}>
                {status.replace('_', ' ')}
              </span>
              <span className="badge priority" style={{ backgroundColor: getPriorityColor(priority) }}>
                {priority}
              </span>
            </div>
          </div>

          {isExpanded && (
            <div className="task-details">
              {description && <p className="task-description">{description}</p>}
              <div className="task-meta">
                <small>{new Date(task.created_at).toLocaleDateString()}</small>
              </div>
            </div>
          )}

          <div className="task-actions">
            <button
              type="button"
              className="btn-action edit"
              onClick={() => setIsEditing(true)}
              title="Edit task"
              aria-label="Edit task"
            >
              <FiEdit2 />
            </button>
            <button
              type="button"
              className="btn-action delete"
              onClick={() => onDelete(task.id)}
              title="Delete task"
              aria-label="Delete task"
            >
              <FiTrash2 />
            </button>
            <button
              type="button"
              className={`btn-action ${status === 'completed' ? 'complete' : ''}`}
              onClick={handleToggleStatus}
              title={status === 'completed' ? 'Mark as incomplete' : 'Mark as complete'}
              aria-label={status === 'completed' ? 'Mark as incomplete' : 'Mark as complete'}
            >
              {status === 'completed' ? <FiRotateCcw /> : <FiCheck />}
            </button>
          </div>
        </>
      ) : (
        <div className="task-edit-form">
          <input
            type="text"
            aria-label="Task title"
            value={title}
            maxLength={200}
            onChange={(event) => setTitle(event.target.value)}
            className="edit-input"
          />
          <textarea
            aria-label="Task description"
            value={description}
            maxLength={5000}
            onChange={(event) => setDescription(event.target.value)}
            className="edit-textarea"
            rows={3}
          />
          <div className="edit-selects">
            <select aria-label="Task status" value={status} onChange={(event) => setStatus(event.target.value)}>
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
            <select aria-label="Task priority" value={priority} onChange={(event) => setPriority(event.target.value)}>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <div className="edit-actions">
            <button type="button" className="btn-cancel" onClick={() => setIsEditing(false)}>
              Cancel
            </button>
            <button type="button" className="btn-save" onClick={handleSave}>
              Save
            </button>
          </div>
        </div>
      )}
    </article>
  )
}
