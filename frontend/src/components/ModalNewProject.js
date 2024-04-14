import React, {useState} from 'react';
import '../styles/ModalNewProject.css';
import logo from '../assets/logo.png';
import * as AiIcons from "react-icons/ai";
import {Link} from "react-router-dom";

const ModalNewProject = ({ isOpen, onClose,setModalOpen }) => {

    if (!isOpen) return null;


    return (
        <div className="modalOverlay" onClick={onClose}>
            <div className="modalContent" onClick={e => e.stopPropagation()}>
                <AiIcons.AiOutlineClose onClick={onClose} className="modalCloseBtn"/>
                <h3 className="modalTitle">Создать новый проект</h3>
                <div className="modalInputContainer">
                    <input className="modalInput" placeholder="Название проекта..."></input>
                    <input className="modalInput" placeholder="Описание проекта..."></input>
                </div>
                <div className="modalMembersContainer">
                    <div className="modalMember">
                        <img src={logo} />
                        <h2>Green Homie</h2>
                        <div className="modalSelectContainer">
                            <select className="modalSelect">
                                <option value="0">worker</option>
                                <option value="1">manager</option>
                            </select>
                        </div>
                    </div>
                    <div className="modalInsertId">
                        <div className="modalInsertIdTitle">
                            <AiIcons.AiOutlineKey className="modalImg"/><h2>Есть проект в Asana?</h2>
                        </div>
                        <div className="modalInsertIdText">
                            <p>Вы можете отслеживать свою задачи интегрировав сюда ваш проект из Asana! Для этого достаточно вставить ключ вашего проекта</p>
                            <p>Благодаря нашему сервису вы легко можете импортировать проект и все его задачи из Asana!</p>
                        </div>
                        <div className="modalInputContainer">
                            <input className="modalInputId" placeholder="Ваш идентификатор..."></input>
                        </div>
                        <div className="modalCreateProject">
                            <button className="modalBtn">Создать проект</button>
                        </div>
                        <Link to={'/instruction'} className="instruction">Где взять ID из Asana?</Link>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default ModalNewProject;
