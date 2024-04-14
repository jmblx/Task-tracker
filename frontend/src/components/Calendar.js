import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import {useState} from "react";
import ModalNewEvent from "./ModalNewEvent";
import { useNavigate } from 'react-router-dom';
import ruLocale from '@fullcalendar/core/locales/ru';
import listPlugin from '@fullcalendar/list';
import styles from '../styles/Main.css';

const Calendar = () => {
    const navigate = useNavigate()

    const [modalOpen, setModalOpen] = useState(false);
    const [events, setEvents] = useState([]); // This will store calendar events
    const [selectedDate, setSelectedDate] = useState(null);

    const handleDateClick = (arg) => {
        setSelectedDate(arg.dateStr);
        setModalOpen(true);
    };

    const handleEventDrop = (info) => {
        const { event, delta } = info;
        const newEvents = [...events];
        const index = newEvents.findIndex((e) => e.id === event.id);
        if (index !== -1) {
            newEvents[index] = {...event, start: event.start.toISOString(), end: event.end.toISOString()};
            setEvents(newEvents);
        }
    };

    const handleEventResize = (info) => {
        const { event, start, end } = info;
        const newEvents = events.map((item) =>
            item.id === event.id ? { ...event, start: start.toISOString(), end: end.toISOString() } : item
        );
        setEvents(newEvents);
    };

    const addEvent = (title) => {
        const newEvent = {
            title: title,
            start: selectedDate,
        };
        setEvents(prevEvents => [...prevEvents, newEvent]);
        setModalOpen(false);
    };

        return (
            <div>
                <button className="getBackBtn" onClick={() => navigate('/')}>Обратно на главную</button>
                <FullCalendar
                    key={events.length}
                    plugins={[interactionPlugin, dayGridPlugin, timeGridPlugin, listPlugin]}
                    initialView='timeGridWeek'
                    weekends={true}
                    events={events}
                    dateClick={handleDateClick}
                    selectable={true}
                    headerToolbar={{
                        left: 'prev,next today',
                        center: 'title',
                        right: 'dayGridMonth,dayGridWeek,dayGridDay,list'
                    }}
                    buttonText={{
                        today: 'Сегодня',
                        month: 'Месяц',
                        week: 'Неделя',
                        day: 'День'
                    }}
                    dayHeaderFormat={{
                        weekday: 'long',
                        omitCommas: true
                    }}
                    firstDay={1}
                    locales={[ruLocale]} // Используем русскую локализацию
                    nowIndicator={true}  // Displays an indicator for the current time
                    slotMinTime="08:00:00"  // Start time for the time grid
                    slotMaxTime="20:00:00"  // End time for the time grid
                    selectMirror={true}
                    expandRows={true}
                    eventDrop={handleEventDrop} // обработчик события перемещения
                    eventResize={handleEventResize} // обработчик события изменения размера
                    height={"90vh"}
                />
                {modalOpen && <ModalNewEvent isOpen={modalOpen} onClose={() => setModalOpen(false)} onAddEvent={addEvent}/>}
            </div>
        );
}
export default Calendar
