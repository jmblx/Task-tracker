import React from "react";
import * as AiIcons from "react-icons/ai";
import ProfileIcon from "../assets/logoProfile.png";

export const SidebarData = [
    {
        title: "Green Homie",
        path: "/profile",
        icon: <img src={ProfileIcon} />,
        cName: "nav-text"
    },
    {
        title: "Таймер",
        path: "/calendar",
        icon: <AiIcons.AiOutlineClockCircle />,
        cName: "nav-text",
    },
    {
        title: "Анализ задач",
        path: "/projects",
        icon: <AiIcons.AiFillSignal />,
        cName: "nav-text",
    },
    {
        title: "Мои задачи",
        path: "/",
        icon: <AiIcons.AiTwotoneCalendar />,
        cName: "nav-text",
    },
    {
        title: "Свой график",
        path: "/load",
        icon: <AiIcons.AiOutlineUser />,
        cName: "nav-text",
    },
    {
        title: "Организации",
        path: "/organisation",
        icon: <AiIcons.AiOutlineTeam />,
        cName: "nav-text",
    },
];
