import React, { useState } from "react";
import { Link } from "react-router-dom";
import { SidebarData } from "./SidebarData";
import "../styles/Navbar.css";
import { IconContext } from "react-icons";
import ActiveTask from "./ActiveTask";

function Navbar() {
    const [sidebar, setSidebar] = useState(false);

    const showSidebar = () => setSidebar(!sidebar);

    return (
        <>
            <IconContext.Provider value={{ color: "undefined" }}>
                <nav className={sidebar ? "nav-menu active" : "nav-menu"}>
                    <ul className="nav-menu-items" onClick={showSidebar}>
                        {SidebarData.map((item, index) => {
                            return (
                                <li key={index} className={item.cName}>
                                    <Link to={item.path}>
                                        {item.icon}
                                        <span className="sidebarText">{item.title}</span>
                                    </Link>
                                </li>
                            );
                        })}
                        <ActiveTask />
                    </ul>
                </nav>
            </IconContext.Provider>
        </>
    );
}

export default Navbar;
