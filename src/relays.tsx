import topRelays from './results/top_relays.json';
import runners from './results/people.json';
import React from 'react';

const Relays = () => {


    return (
        <div>
            {Object.keys(topRelays).map((relay) => <div>
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
                        {topRelays[relay].map(team => <tr>
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