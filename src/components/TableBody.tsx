import React from "react";
import runners from "../results/people.json";

const TableBody = ({ tableData, columns }) => {
    return (
        <tbody>
        {tableData.map((data) => {
            return (
                <tr key={data.id}>
                    {columns.map(({ accessor }) => {
                        const tData = data[accessor] ? data[accessor] : "——";
                        return <td key={accessor}>{tData}</td>;
                    })}
                </tr>
            );
        })}
        </tbody>
    );
};

export default TableBody;