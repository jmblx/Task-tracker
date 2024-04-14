import React from 'react';
import '../styles/ModalNewProject.css';
import * as AiIcons from "react-icons/ai";

const ModalNewOrganisation = ({ isOpen, onClose }) => {
    if (!isOpen) return null;

    return (
        <div className="modalOverlay" onClick={onClose}>
            <div className="modalContent" onClick={e => e.stopPropagation()}>
                <AiIcons.AiOutlineClose onClick={onClose} className="modalCloseBtn"/>
                <h3 className="modalTitle">Создать новую организацию</h3>
                <div className="modalInputContainer">
                    <input className="modalInput" placeholder="Название организации..."></input>
                    <input className="modalInput" placeholder="Описание организации..."></input>
                </div>
                <div className="modalMembersContainer">
                <div className="modalCreateProject">
                    <button className="modalBtn">Создать проект</button>
                </div>
                </div>
            </div>
        </div>
    );
};
export default ModalNewOrganisation;
