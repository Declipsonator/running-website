import React from 'react';
import ReactDOM from 'react-dom/client';
import './style.css';
import TheTable from './components/Table';

// @ts-ignore
const root = ReactDOM.createRoot(document.getElementById('app'));
root.render(
    <React.StrictMode>
        <div>
            <h1>Fairport Runners!</h1>
            <div id="runnerList">
                <TheTable />
            </div>
        </div>
    </React.StrictMode>
);