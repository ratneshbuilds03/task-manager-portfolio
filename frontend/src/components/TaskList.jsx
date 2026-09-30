import TaskCard from './TaskCard'
import './TaskList.css'

export default function TaskList({ tasks, onUpdate, onDelete }) {
  return (
    <div className="task-list">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
