import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProjectsComponent from './components/ProjectsComponent.js';
import TasksComponent from './components/TasksComponent.js';
import './App.css';
import Main from "./components/Main";
import Calendar from "./components/Calendar";
import Profile from "./components/Profile";
import Organisation from "./components/Organisation";
import Instruction from "./components/Instruction";

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Main />} />
                <Route path="/organisation" element={<Organisation />} />
                <Route path="/instruction" element={<Instruction />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/calendar" element={<Calendar />} />
                <Route path="/projects" element={<ProjectsComponent />} />
                <Route path="/tasks" element={<TasksComponent />} />
            </Routes>
        </Router>
    );
}

export default App;
