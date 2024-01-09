import React from "react";
import EditableTextParams from "./EditableTextParams";

const RoleTable = ({
  headers,
  data,
  dataColumns,
  editableCell,
  additionalColumns = [],
  isDeleteMode = false,
  selectedItems = [],
  handleSelection = () => {},
}) => {
  return (
    <table className="table table-bordered">
      <thead>
        <tr>
          {headers.map((header, index) => (
            <th key={index}>{header}</th>
          ))}
          {isDeleteMode && <th>Delete</th>}
          {additionalColumns.map((column, index) => (
            <th key={index}>{column}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id}>
            {Object.keys(item)
              .filter((key) => dataColumns.includes(key))
              .map((key) => (
                <td key={key}>
                  {key === editableCell ? (
                    <EditableTextParams
                      initialText={item[key]}
                      type="number"
                      field={editableCell}
                      ParamId={item.id}
                    />
                  ) : (
                    item[key]
                  )}
                </td>
              ))}
            {isDeleteMode && (
              <td>
                <input
                  type="checkbox"
                  checked={selectedItems.includes(item.id)}
                  onChange={() => handleSelection(item.id)}
                />
              </td>
            )}
            {additionalColumns.map((column, index) => (
              <td key={index}>
                {renderCell({
                  item,
                  field: column,
                  isEditable: false,
                })}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default RoleTable;
