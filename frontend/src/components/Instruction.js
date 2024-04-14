import React, {useState} from "react";
import screenshot from '../assets/screen.png'
import screenshot1 from '../assets/screen_1.png'
import '../styles/Instruction.css';
import * as AiIcons from "react-icons/ai";
import {useNavigate} from "react-router-dom";

const Instruction = () => {
    const navigate = useNavigate()
    const [isModalOpen, setIsModalOpen] = useState(false);

    return (
        <>
            <main>
                <div className="container">
                    <AiIcons.AiOutlineArrowLeft onClick={() => navigate('/')} className="goBackBtn"/>
                    <h2>1. Перейдите в Asana</h2>
                    <h2>2. Перейдите на страницу вашего проекта</h2>
                    <h2>3. Скопируйте в адресной строке ваш ID проекта</h2>
                    <img src={screenshot}/>
                    <h2>4. Перейдите во вкладку "Обзор" вашего проекта, нажмите добавить участника и пригласите участника с данной электронной почтой <span className="email">zhora.zhilin.06@mail.ru</span></h2>
                    <img src={screenshot1}/>
                    <h2>5. Все готово!</h2>
                </div>
            </main>
        </>
    );
};

export default Instruction;
