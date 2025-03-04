import topRelays from './results/top_relays.json';
import f_topRelays from './results/top_relays-F.json';
import runners from './results/people.json';
import f_runners from './results/people-F.json';
import React from 'react';

const Relays = () => {
    let queryParams = new URLSearchParams(window.location.search);
    let gender = queryParams.get('gender');
    gender = gender ? gender : 'M';


    return (
        <div>
            {Object.keys(gender == 'M' ? topRelays : f_topRelays).map((relay) => <div>
                <h2>{relay}</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>{relay.split(', ')[0]}</th>
                            <th>{relay.split(', ')[1]}</th>
                            <th>{relay.split(', ')[2]}</th>
                            <th>{relay.split(', ')[3]}</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {(gender == 'M' ? topRelays : f_topRelays)[relay].map(team => <tr>
                            {team['team'].map((runner) => <td>{runner[0]} - {secondsToTime(runner[1])}</td>)}
                            <td>{secondsToTime(team['total_time'])}</td>
                        </tr>)}
                    </tbody>
                </table>
            </div>)}
        </div>
    );
}

function secondsToTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${Math.round(remainingSeconds * 100) / 100}`;
}

export default Relays;