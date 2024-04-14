import React, { useState, useEffect } from 'react';
import styles from '../styles/TimerComponent.module.css';

const TimerComponent = () => {
    const [seconds, setSeconds] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setSeconds(seconds => seconds + 1);
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    const formatTime = () => {
        const getSeconds = `0${(seconds % 60)}`.slice(-2);
        const minutes = `${Math.floor(seconds / 60)}`;
        const getMinutes = `0${minutes % 60}`.slice(-2);
        const getHours = `0${Math.floor(minutes / 60)}`.slice(-2);

        return `${getHours}:${getMinutes}:${getSeconds}`;
    };

    return (
        <div className={styles.timerContainer}>
            <div className={styles.time}>
                {formatTime()}
            </div>
            <div className={styles.timerControls}>
                {}
            </div>
        </div>
    );
};

export default TimerComponent;
