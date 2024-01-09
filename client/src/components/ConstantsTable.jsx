import { useEffect, useState } from "react";
import {
  getAllConstants,
  createConstant,
  deleteConstant,
} from "../api/workers.api";

function ConstantsTable() {
  const [constants, setConstants] = useState([]);
  const [selectedConstants, setSelectedConstants] = useState([]);
  const [isDeleteMode, setIsDeleteMode] = useState(false);
  const [isAddingConstant, setIsAddingConstant] = useState(false);
  const [newConstantName, setNewConstantName] = useState("");
  const [newConstantValue, setNewConstantValue] = useState("");

  const loadConstants = async () => {
    const res = await getAllConstants();
    console.log(res);
    setConstants(res.data);
  };

  useEffect(() => {
    loadConstants();
  }, []);

  const handleConstantSelection = (constantId) => {
    if (selectedConstants.includes(constantId)) {
      setSelectedConstants(selectedConstants.filter((id) => id !== constantId));
    } else {
      setSelectedConstants([...selectedConstants, constantId]);
    }
  };

  const handleDeleteSelectedConstants = async () => {
    // Se elimina el Constant seleccionado de la base de datos
    for (const constantId of selectedConstants) {
      await deleteConstant(constantId);
    }
    // Se recargan los Constants y se reinician variables
    loadConstants();
    setSelectedConstants([]);
    setIsDeleteMode(false);
  };

  const handleAddConstant = async () => {
    // Se llama la API para crear un rol
    const newConstant = {
      name: newConstantName,
      value: newConstantValue,
    };

    await createConstant(newConstant);
    //Se recargan los Constants y se reinician variables
    loadConstants();
    setIsAddingConstant(false);
    setNewConstantName("");
  };
  return (
    <div className="child">
      <table className="table table-striped table-bordered table-hover">
        <thead>
          <tr>
            <th>Name</th>
            <th>Value</th>
            {isDeleteMode && <th>Delete</th>}
          </tr>
        </thead>
        <tbody className="text-center" style={{ verticalAlign: "middle" }}>
          {constants.map((constant, index) => (
            <tr key={index}>
              <td>{constant.name}</td>
              <td>{constant.value}</td>
              {isDeleteMode && (
                <td>
                  <input
                    type="checkbox"
                    checked={selectedConstants.includes(constant.id)}
                    onChange={() => handleConstantSelection(constant.id)}
                  />
                </td>
              )}
            </tr>
          ))}
          {isAddingConstant && (
            <tr>
              <td>
                <input
                  type="text"
                  value={newConstantName}
                  onChange={(e) => setNewConstantName(e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  value={newConstantValue}
                  onChange={(e) => setNewConstantValue(e.target.value)}
                />
              </td>
            </tr>
          )}
        </tbody>
      </table>
      <div>
        {!isAddingConstant && (
          <button
            className="btn btn-primary"
            onClick={() => setIsAddingConstant(true)}
          >
            Add Constant
          </button>
        )}
        {isAddingConstant && (
          <button className="btn btn-primary" onClick={handleAddConstant}>
            Add
          </button>
        )}
        <button
          className="btn btn-danger"
          onClick={() => setIsDeleteMode(!isDeleteMode)}
        >
          {isDeleteMode ? "Cancel" : "Delete Constant"}
        </button>
        {isDeleteMode && (
          <button
            className="btn btn-dark"
            onClick={handleDeleteSelectedConstants}
          >
            Delete Selected
          </button>
        )}
      </div>
    </div>
  );
}

export default ConstantsTable;
