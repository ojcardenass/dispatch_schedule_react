import { useEffect, useState } from "react";
import { getAllWorkerExp, deleteWorker } from "../api/workers.api";
import EditableTextWorkers from "./EditableTextWorkers";
import "../styles/workertable.css";

export function WorkerExpList() {
  const [workers, setWorkers] = useState([]);
  const [selectedWorkers, setSelectedWorkers] = useState([]);
  const [isDeleteMode, setIsDeleteMode] = useState(false);

  const loadWorkers = async () => {
    const res = await getAllWorkerExp();
    console.log(res);
    setWorkers(res.data);
  };

  useEffect(() => {
    loadWorkers();
  }, []);

  const handleWorkerSelection = (workerId) => {
    if (selectedWorkers.includes(workerId)) {
      setSelectedWorkers(selectedWorkers.filter((id) => id !== workerId));
    } else {
      setSelectedWorkers([...selectedWorkers, workerId]);
    }
  };

  const handleDeleteSelectedWorkers = async () => {
    // Se llama la API para eliminar el worker
    for (const workerId of selectedWorkers) {
      await deleteWorker(workerId);
    }
    // Se recargan los workers y se reinician las variables
    loadWorkers();
    setSelectedWorkers([]);
    setIsDeleteMode(false);
  };

  return (
    <div className="row">
      <div className="col-md-4 py-1">{/* //Notifications */}</div>

      <div className="col-md-6">
        <h1 className="text-center display-3 py-4">Workers List</h1>
        <button
          className="btn btn-danger"
          onClick={() => setIsDeleteMode(!isDeleteMode)}
        >
          {isDeleteMode ? "Cancel" : "Delete Worker"}
        </button>
        {isDeleteMode && (
          <button
            className="btn btn-secondary"
            onClick={handleDeleteSelectedWorkers}
          >
            Delete Selected
          </button>
        )}
        <div>
          <table className="table table-striped table-bordered table-hover">
            <thead>
              <tr>
                <th>Name</th>
                <th>Weight</th>
                <th>Roles</th>
                {isDeleteMode && <th>Delete</th>}
              </tr>
            </thead>
            <tbody className="text-center" style={{ verticalAlign: "middle" }}>
              {workers.map((worker, index) => (
                <tr key={index}>
                  <td>
                    <EditableTextWorkers
                      initialText={worker.name}
                      type="text"
                      field="name"
                      workerId={worker.id}
                    />
                  </td>
                  <td>
                    <EditableTextWorkers
                      initialText={worker.weight}
                      type="number"
                      field="weight"
                      workerId={worker.id}
                    />
                  </td>
                  <td>
                    <table className="table table-bordered">
                      <thead>
                        <tr>
                          <th>Role Name</th>
                          <th>Experience</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(worker.roles_exp).map(
                          ([roleName, experience], roleIndex) => {
                            const [role] = roleName.split("_");
                            return (
                              <tr key={roleIndex}>
                                <td>{role}</td>
                                <td>
                                  <EditableTextWorkers
                                    initialText={experience}
                                    type="number"
                                    field={roleName}
                                    workerId={worker.id}
                                  />
                                </td>
                              </tr>
                            );
                          }
                        )}
                      </tbody>
                    </table>
                  </td>
                  {isDeleteMode && (
                    <td>
                      <input
                        type="checkbox"
                        checked={selectedWorkers.includes(worker.id)}
                        onChange={() => handleWorkerSelection(worker.id)}
                      />
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
