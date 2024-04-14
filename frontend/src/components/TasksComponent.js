import React, { useState } from 'react';
import styles from '../styles/TasksComponent.module.css';

const TasksComponent = () => {
    const [tasks, setTasks] = useState([
        { id: 1, name: 'Task 1', completed: false },
        { id: 2, name: 'Task 2', completed: false },
    ]);

    const toggleTaskCompletion = (taskId) => {
        setTasks(tasks.map(task =>
            task.id === taskId ? { ...task, completed: !task.completed } : task
        ));
    };

    return (
        <div className={styles.tasksContainer}>
            {tasks.map(task => (
                <div key={task.id} className={styles.task}>
                    <label className={styles.taskLabel}>
                        <input
                            type="checkbox"
                            checked={task.completed}
                            onChange={() => toggleTaskCompletion(task.id)}
                        />
                        {task.name}
                    </label>
                </div>
            ))}
        </div>
    );
};

export default TasksComponent;
