import { useEffect, useState } from "react";
import { getAllRoles, createRole, deleteRole } from "../api/workers.api";
import "../styles/workertable.css";

export function RolePage() {
  const [roles, setRoles] = useState([]);
  const [selectedRoles, setSelectedRoles] = useState([]);
  const [isDeleteMode, setIsDeleteMode] = useState(false);
  const [isAddingRole, setIsAddingRole] = useState(false);
  const [newRoleName, setNewRoleName] = useState("");

  const loadRoles = async () => {
    const res = await getAllRoles();
    console.log(res);
    setRoles(res.data);
  };

  useEffect(() => {
    loadRoles();
  }, []);

  const handleRoleSelection = (roleId) => {
    if (selectedRoles.includes(roleId)) {
      setSelectedRoles(selectedRoles.filter((id) => id !== roleId));
    } else {
      setSelectedRoles([...selectedRoles, roleId]);
    }
  };

  const handleDeleteSelectedRoles = async () => {
    // Se elimina el role seleccionado de la base de datos
    for (const roleId of selectedRoles) {
      await deleteRole(roleId);
    }
    // Se recargan los roles y se reinician variables
    loadRoles();
    setSelectedRoles([]);
    setIsDeleteMode(false);
  };

  const handleAddRole = async () => {
    // Se llama la API para crear un rol
    const newRole = {
      name: newRoleName,
    };

    await createRole(newRole);
    //Se recargan los roles y se reinician variables
    loadRoles();
    setIsAddingRole(false);
    setNewRoleName("");
  };

  return (
    <div className="text-center col-md-6 container">
      <h1 className="text-center display-3 py-4">Roles List</h1>
      <div className="child">
        <table className="table table-striped table-bordered table-hover">
          <thead>
            <tr>
              <th>Name</th>
              {isDeleteMode && <th>Delete</th>}
            </tr>
          </thead>
          <tbody className="text-center" style={{ verticalAlign: "middle" }}>
            {roles.map((role, index) => (
              <tr key={index}>
                <td>{role.name}</td>
                {isDeleteMode && (
                  <td>
                    <input
                      type="checkbox"
                      checked={selectedRoles.includes(role.id)}
                      onChange={() => handleRoleSelection(role.id)}
                    />
                  </td>
                )}
              </tr>
            ))}
            {isAddingRole && (
              <tr>
                <td>
                  <input
                    type="text"
                    value={newRoleName}
                    onChange={(e) => setNewRoleName(e.target.value)}
                  />
                </td>
              </tr>
            )}
          </tbody>
        </table>
        <div>
          {!isAddingRole && (
            <button
              className="btn btn-primary"
              onClick={() => setIsAddingRole(true)}
            >
              Add Role
            </button>
          )}
          {isAddingRole && (
            <button className="btn btn-primary" onClick={handleAddRole}>
              Add
            </button>
          )}
          <button
            className="btn btn-danger"
            onClick={() => setIsDeleteMode(!isDeleteMode)}
          >
            {isDeleteMode ? "Cancel" : "Delete Role"}
          </button>
          {isDeleteMode && (
            <button className="btn btn-dark" onClick={handleDeleteSelectedRoles}>
              Delete Selected
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
