import ModalNewProject from "./ModalNewProject";
import React, {useState} from "react";
import imageNoProjects from '../assets/img.png';
import Navbar from "./Navbar";
import {Link} from "react-router-dom";
import '../styles/Main.css';
import ModalNewOrganisation from "./ModalNewOrganisation";

const Organisation = () => {
    const [isModalOpen, setModalOpen] = useState(false);

    const handleOpenModal = () => {
        setModalOpen(true);
    };

    const handleCloseModal = () => {
        setModalOpen(false);
    };

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
                        <h2>Вы не состоите не в одной организации - </h2>
                        <h2>создайте её сейчас</h2>
                        <button className="btn" onClick={handleOpenModal}>Создать организацию +</button>
                        <ModalNewOrganisation isOpen={isModalOpen} onClose={handleCloseModal} />
                    </div>
                </div>
            </main>
        </>
    );
};

export default Organisation;
