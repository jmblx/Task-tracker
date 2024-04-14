import React from "react";
import bg from '../assets/bg.png';
import logo from '../assets/logoProfile.png';
import '../styles/Profile.css';
import * as AiIcons from "react-icons/ai";
import { useNavigate } from 'react-router-dom';

const Profile = () => {
    const navigate = useNavigate()
    return (
        <>
            <AiIcons.AiOutlineArrowLeft onClick={() => navigate('/')} className="goBack"/>
            <img className="backGround" src={bg}  alt={"Я мечтаю"}/>
            <div className="profileInfoContainer">
                <img className="profileLogo" src={logo}/>
                <div className="profileNameInfo">
                    <h2>Green Homie</h2>
                    <p>konstantinzorenko3@gmail.com</p>
                </div>
            </div>
            <div className="personalData">
                <div className="personalDataContainer">
                    <h2>Персональные данные</h2>
                    <div className="personalDataRow">
                        <div className="personalDataInfo">
                            <h3>Полное имя</h3>
                            <p>Green Homie</p>
                        </div>
                        <div className="personalDataInfo">
                            <h3>Почта</h3>
                            <p>konstantinzorenko3@gmail.com</p>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Profile
