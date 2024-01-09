import { useEffect, useState } from "react";
import {
  getAllParams,
  createParam,
  deleteParam,
  getAllRoles,
} from "../api/workers.api";
import EditableTextParams from "../components/EditableTextParams";
import RoleTable from "./RoleTable";

function ParamsTable() {
  const [params, setParams] = useState([]);
  const [roles, setRoles] = useState([]);
  const [selectedParams, setSelectedParams] = useState([]);
  const [isDeleteMode, setIsDeleteMode] = useState(false);
  const [isAddingParam, setIsAddingParam] = useState(false);
  const [newParamName, setNewParamName] = useState("");
  const [newParamValues, setNewParamValues] = useState({});

  const groupDataByParameter = (data) => {
    const groupedData = {};

    data.forEach((item) => {
      const parameter = item.parameter;

      if (!groupedData[parameter]) {
        // If the parameter key doesn't exist, create an array for it.
        groupedData[parameter] = [];
      }

      // Push the item into the corresponding parameter group.
      groupedData[parameter].push(item);
    });

    return groupedData;
  };

  const loadParams = async () => {
    const res = await getAllParams();
    // console.log(res);

    const data = groupDataByParameter(res.data);
    setParams(data);
  };

  useEffect(() => {
    loadParams();
    loadRoles();
  }, []);

  const loadRoles = async () => {
    const res = await getAllRoles();
    setRoles(res.data);
  };

  // useEffect(() => {
  //   loadRoles();
  // }, []);

  const handleParamSelection = (paramId) => {
    if (selectedParams.includes(paramId)) {
      setSelectedParams(selectedParams.filter((id) => id !== paramId));
    } else {
      setSelectedParams([...selectedParams, paramId]);
    }
  };

  const handleDeleteSelectedParams = async () => {
    // Se elimina el role seleccionado de la base de datos
    for (const paramId of selectedParams) {
      await deleteRole(paramId);
    }
    // Se recargan los roles y se reinician variables
    loadParams();
    setSelectedParams([]);
    setIsDeleteMode(false);
  };

  const handleAddParam = async () => {
    // Se llama la API para crear un rol
    const newParams = roles.map((role, index) => ({
      parameter: newParamName,
      value: newParamValues[role.id] || "",
      role: role.id,
    }));

    for (const newParam of newParams) {
      await createParam(newParam);
    }

    //Se recargan los Params y se reinician variables
    loadParams();
    setIsAddingParam(false);
    setNewParamName("");
    setNewParamValues({});
  };

  return (
    <div className="child text-center">
      <table className="table table-striped table-bordered table-hover">
        <thead>
          <tr>
            <th>Name</th>
            <th>Values</th>
          </tr>
        </thead>
        <tbody className="text-center" style={{ verticalAlign: "middle" }}>
          {Object.keys(params).map((parameter) => (
            <tr key={parameter}>
              <td>
              <EditableTextParams
                initialText={parameter}
                type="text"
                field="parameter"
                ParamId={params[parameter][0].id}
              />
              </td>
              <td>
                <RoleTable
                  headers={["Role Name", "Values"]}
                  data={params[parameter]}
                  dataColumns={["role_name", "value"]}
                  isDeleteMode={isDeleteMode}
                  selectedItems={selectedParams}
                  handleSelection={handleParamSelection}
                  editableCell={"value"}
                />
              </td>
            </tr>
          ))}
          {isAddingParam && (
            <tr>
              <td>
                <input
                  type="text"
                  value={newParamName}
                  style={{ width: "105px" }}
                  onChange={(e) => setNewParamName(e.target.value)}
                />
              </td>
              <td>
                <table className="table table-bordered">
                  <thead>
                    <tr>
                      <th>Role Name</th>
                      <th>Values</th>
                    </tr>
                  </thead>
                  <tbody>
                    {roles.map((role, index) => (
                      <tr key={index}>
                        <td>{role.name}</td>
                        <td>
                          <input
                            type="number"
                            value={newParamValues[role.id] || ""}
                            style={{ width: "60px" }}
                            min={0}
                            onChange={(e) =>
                              setNewParamValues({
                                ...newParamValues,
                                [role.id]: e.target.value,
                              })
                            }
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </td>
            </tr>
          )}
        </tbody>
      </table>
      <div className="button-container">
        {!isAddingParam && (
          <button
            className="btn btn-primary"
            onClick={() => setIsAddingParam(true)}
          >
            Add Param
          </button>
        )}
        {isAddingParam && (
          <button className="btn btn-primary" onClick={handleAddParam}>
            Add
          </button>
        )}
        <button
          className="btn btn-danger"
          onClick={() => setIsDeleteMode(!isDeleteMode)}
        >
          {isDeleteMode ? "Cancel" : "Delete Param"}
        </button>
        {isDeleteMode && (
          <button className="btn btn-dark" onClick={handleDeleteSelectedParams}>
            Delete Selected
          </button>
        )}
      </div>
    </div>
  );
}

export default ParamsTable;
