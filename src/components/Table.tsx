import { useState, useEffect } from "react";
import React from 'react';
// @ts-ignore
import runners from "../results/people.json";
import TableBody from "./TableBody";
import TableHead from "./TableHead";

const TheTable = () => {
    const runnerList = [];
    for(let runner of Object.keys(runners)) {
        let newRunner = runners[runner];
        newRunner.name = runner;
        runnerList.push(newRunner);
    }
    const [tableData, setTableData] = useState(runnerList);
    const [sortConfig, setSortConfig] = useState({ key: 'name', direction: 'ascending' });

    const columns = [
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

    const convertToSeconds = (time) => {
        if (!time) return Number.MAX_SAFE_INTEGER; // Return a large number for missing times
        const parts = time.split(':');
        return parts.reduce((acc, part) => acc * 60 + parseFloat(part), 0);
    };

    const handleSort = (accessor: string) => {
        let direction = 'ascending';
        if (sortConfig.key === accessor && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
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
        handleSort('name');
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