import React, { useState } from 'react';
import '../styles/ModalNewEvent.css';
import * as AiIcons from "react-icons/ai";

const Modal = ({ isOpen, onClose, onAddEvent }) => {
    const [title, setTitle] = useState('');

    if (!isOpen) return null;

    const handleSubmit = (e) => {
        e.preventDefault();
        onAddEvent(title);
        setTitle('');
    };

    return (
        <div className="modalOverlay">
            <div className="modalContent">
                <AiIcons.AiOutlineClose onClick={onClose} className="modalCloseBtn"/>
                <h2>Добавить новое событие</h2>
                <form className="modalForm" onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Название события..."
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                        className={"modalInput"}
                    />
                    <button className="modalBtn" type="submit">Добавить событие</button>
                </form>
            </div>
        </div>
    );
};

export default Modal;
