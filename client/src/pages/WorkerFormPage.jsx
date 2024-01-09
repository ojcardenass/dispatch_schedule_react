import { getAllRoles, createWorker } from "../api/workers.api";
import { useForm } from "react-hook-form";
import { useEffect, useState } from "react";

export function WorkerFormPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    getValues,
  } = useForm();
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    async function loadRoles() {
      const res = await getAllRoles();
      console.log(res);
      setRoles(res.data);
    }
    loadRoles();
  }, []);

  const onSubmit = handleSubmit(async (data) => {
    // Extraer roles y experiencias de los datos del formulario
    const roleData = roles.map((role) => ({
      role_id: role.id,
      role_name: role.name,
      experience: data[`exp${role.name}`] || 0,
    }));

    // Combinar los datos del trabajador con los roles y experiencias
    const workerData = {
      name: data.name,
      weight: data.weight,
      roles: roleData,
    };

    const res = await createWorker(workerData);
    console.log(res);
  });

  // Definir la experiencia inicial de cada rol
  useEffect(() => {
    roles.forEach((role) => {
      setValue(`exp${role.name}`, 0);
    });
  }, [roles, setValue]);

  return (
    <div className="text-center">
      <h1 className="text-center display-3 py-4">Create Worker</h1>
      <form onSubmit={onSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            id="name"
            type="text"
            placeholder="Write a name"
            {...register("name", { required: true })}
          />
        </div>

        <div>
          <label htmlFor="weight">Weight:</label>
          <input
            type="number"
            id="weight"
            placeholder="Write a weight"
            min={0}
            {...register("weight", { required: true })}
          />
        </div>

        {roles.map((role) => (
          <div key={role.id}>
            <label htmlFor={`exp${role.name}`}>Exp {role.name}:</label>
            <input
              id={`exp${role.name}`}
              type="number"
              placeholder={`Write ${role.name} experience`}
              min={0}
              max={10}
              {...register(`exp${role.name}`, { required: true })}
              style={{ width: "16%" }}
            />
          </div>
        ))}

        <button type="submit" className="btn btn-success">
          Save{" "}
        </button>
      </form>
    </div>
  );
}
