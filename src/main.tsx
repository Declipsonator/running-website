import React from 'react';
import ReactDOM from 'react-dom/client';
import './style.css';
import TheTable from './components/Table';
import Relays from "./relays";

// @ts-ignore
const root = ReactDOM.createRoot(document.getElementById('app'));
root.render(
    <React.StrictMode>
        <div>
            <h1>Fairport Runners!</h1>
            <div id="runnerList">
                <TheTable />
            </div>
            <h1>Top Relays! (30 each)</h1>
            <Relays />
        </div>
    </React.StrictMode>
);