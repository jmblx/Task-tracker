import React from "react";
import {AiOutlineCheck, AiOutlinePauseCircle, AiOutlineRightCircle} from "react-icons/ai";
import styles from "../styles/ActiveTask.module.css"


function ActiveTask() {
    return (
        <>
            <div className={styles.task}>
                <div className={styles.taskTime}>
                    <h2>7ч:22 минуты</h2>
                </div>
                <div className={styles.taskInfo}>
                    <h2>Задача:</h2>
                    <p>Не проснуться</p>
                </div>
                <div className={styles.taskButtons}>
                    <button><AiOutlinePauseCircle className={styles.stopTask}/></button>
                    <button><AiOutlineCheck className={styles.stopTask}/></button>
                </div>
                <div className={styles.containerTask}>
                    <AiOutlineRightCircle className={styles.nextTask}/>
                </div>
            </div>
        </>
    )
}

export default ActiveTask;
