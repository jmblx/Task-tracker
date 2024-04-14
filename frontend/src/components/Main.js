import ModalNewProject from "./ModalNewProject";
import React, {useState} from "react";
import imageNoProjects from '../assets/img.png';
import Navbar from "./Navbar";
import {Link} from "react-router-dom";
import '../styles/Main.css';

const Main = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    return (
        <>
            <main>
                <Navbar />
                <nav className="header">
                    <Link className="headerLink" to="/projects">Все проекты</Link>
                    <Link className="headerLink" to="/projects/active">Активные</Link>
                    <Link className="headerLink" to="/projects/complete">Завершенные</Link>
                    <Link className="headerLink" to="/projects/command">Командные проекты</Link>
                    <Link className="headerLink" to="/projects/archive">Архив проектов</Link>
                </nav>
                <div className="container">
                    <div className="textNoProjects">
                        <img src={imageNoProjects} alt="Можно я с тобой?"/>
                        <h2>Пустое время - </h2>
                        <h2>неиспользованный потенциал</h2>
                        <p>Отсчитай успех и создай свой первый проект!</p>
                        <button className="btn" onClick={openModal}>Добавить проект +</button>
                        <ModalNewProject isOpen={isModalOpen} onClose={closeModal}/>
                    </div>
                </div>
            </main>
        </>
    );
};

export default Main;
