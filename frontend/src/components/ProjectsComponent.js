import React from 'react';
import styles from '../styles/ProjectsComponent.module.css';
import Navbar from "./Navbar";
import footnote from '../assets/footnote.png'

const ProjectsComponent = () => {
    return (
        <><Navbar />
            <div className={styles.projectsContainer}>
                <img src={footnote} className={styles.footnote}/><p className={styles.title}>Анализ ваших спланированных задач</p><p className={styles.title}>можно посмотреть отдельно!</p>
                <div className={styles.containerButtons}>
                    <button>День</button>
                    <button>Месяц</button>
                    <button>Год</button>
                </div>
                <div className={styles.listProjectsContainer}>
                    <p>#1</p>
                    <p>Принять душ</p>
                    <p className={styles.activeProjectContainer}>Active</p>
                    <p><span>Members:</span> Zorenko Konstantin, Podpivasnick, Meff...</p>
                </div>
            </div>
        </>
    );
};

export default ProjectsComponent;
