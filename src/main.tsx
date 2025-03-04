import React from 'react';
import ReactDOM from 'react-dom/client';
import './style.css';
import TheTable from './components/Table';
import Relays from "./relays";

// Gender can be changed in query string
let queryParams = new URLSearchParams(window.location.search);
let gender = queryParams.get('gender');
gender = gender ? gender : 'M';
let text = gender == 'M' ? 'Girls' : 'Boys';

// @ts-ignore
const root = ReactDOM.createRoot(document.getElementById('app'));
root.render(
    <React.StrictMode>
        <div>
            <h1>Fairport Runners</h1>
            <button
            onClick={() => {
                queryParams.set('gender', gender == 'M' ? 'F' : 'M');
                window.location.search = queryParams.toString();
            }}
            >{text}</button>
            <br/>
            <br/>
            <br/>
            <div id="runnerList">
                <TheTable />
            </div>
            <h1>Top Relays (30 each)</h1>
            <Relays />
        </div>
    </React.StrictMode>
);