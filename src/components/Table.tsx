import { useState, useEffect } from "react";
import React from 'react';
// @ts-ignore
import runners from "../results/people.json";
import f_runners from "../results/people-F.json";
import TableBody from "./TableBody";
import TableHead from "./TableHead";

const TheTable = () => {
    let queryParams = new URLSearchParams(window.location.search);
    let gender = queryParams.get('gender');
    gender = gender ? gender : 'M';

    const runnerList = [];
    for(let runner of Object.keys(gender == 'M' ? runners : f_runners)) {
        let newRunner = (gender == 'M' ? runners : f_runners)[runner];
        newRunner.name = runner;
        runnerList.push(newRunner);
    }
    const [tableData, setTableData] = useState(runnerList);
    const [sortConfig, setSortConfig] = useState({ key: 'name', direction: 'ascending' });


    let columns = [
        { label: "Name", accessor: "name" },
        { label: "Grade", accessor: "grade" },
        { label: "55m", accessor: "55m" },
        { label: "200m", accessor: "200m" },
        { label: "300m", accessor: "300m" },
        { label: "400m", accessor: "400m" },
        { label: "600m", accessor: "600m" },
        { label: "800m", accessor: "800m" },
        { label: "1000m", accessor: "1000m" },
        { label: "1200m", accessor: "1200m" },
        { label: "1600m", accessor: "1600m" },
        { label: "Mile", accessor: "1609m" },
        { label: "3200m", accessor: "3200m" },
    ];

    if(gender == 'F') {
        columns = [
            { label: "Name", accessor: "name" },
            { label: "Grade", accessor: "grade" },
            { label: "55m", accessor: "55m" },
            { label: "200m", accessor: "200m" },
            { label: "300m", accessor: "300m" },
            { label: "400m", accessor: "400m" },
            { label: "600m", accessor: "600m" },
            { label: "800m", accessor: "800m" },
            { label: "1000m", accessor: "1000m" },
            { label: "1200m", accessor: "1200m" },
            { label: "1500m", accessor: "1500m" },
            { label: "1600m", accessor: "1600m" },
            { label: "Mile", accessor: "1609m" },
            { label: "3000m", accessor: "3000m" },
        ];
    }

    const convertToSeconds = (time) => {
        if (!time) return Number.MAX_SAFE_INTEGER; // Return a large number for missing times
        const parts = time.split(':');
        return parts.reduce((acc, part) => acc * 60 + parseFloat(part), 0);
    };

    const handleSort = (accessor: string, d= null) => {
        let direction = 'ascending';
        if (sortConfig.key === accessor && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        direction = d ? d : direction;
        setSortConfig({ key: accessor, direction });

        const sortedData = [...tableData].sort((a, b) => {
            if (accessor === 'name' || accessor === 'grade') {
                if (a[accessor] < b[accessor]) return direction === 'ascending' ? -1 : 1;
                if (a[accessor] > b[accessor]) return direction === 'ascending' ? 1 : -1;
                return 0;
            } else {
                const aTime = convertToSeconds(a[accessor]);
                const bTime = convertToSeconds(b[accessor]);
                if (aTime === Number.MAX_SAFE_INTEGER) return 1;
                if (bTime === Number.MAX_SAFE_INTEGER) return -1;
                return direction === 'ascending' ? aTime - bTime : bTime - aTime;
            }
        });
        setTableData(sortedData);
    };

    useEffect(() => {
        handleSort('name', 'ascending');
    }, []);

    return (
        <>
            <table className="table">
                <caption>
                    Click on event headers to sort by that event.
                </caption>
                <TableHead columns={columns} handleSort={handleSort} sortConfig={sortConfig} />
                <TableBody columns={columns} tableData={tableData} />
            </table>
        </>
    );
};

export default TheTable;