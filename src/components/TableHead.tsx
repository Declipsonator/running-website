import React from "react";

// @ts-ignore
const TableHead = ({ columns, handleSort, sortConfig }) => {
    return (
        <thead>
        <tr>
            {columns.map(({ label, accessor }) => {
                const isSorted = sortConfig.key === accessor;
                return (
                    <th
                        key={accessor}
                        onClick={() => handleSort(accessor)}
                        className={isSorted ? 'sorted' : ''}
                    >
                        {label}
                    </th>
                );
            })}
        </tr>
        </thead>
    );
};

export default TableHead;