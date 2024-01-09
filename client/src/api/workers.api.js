import axios from "axios";

// URL Base de la api

const workersApi = axios.create({
  baseURL: "http://localhost:8000/",
});

// APIs para obtener datos

export const getAllWorkerExp = () => {
  return workersApi.get("workers/");
};

export const getAllRolesExp = () => {
  return workersApi.get("experience/");
};

export const getAllRoles = () => {
  return workersApi.get("roles/");
};

export const getAllConstants = () => {
  return workersApi.get("constants/");
};

export const getAllParams = () => {
  return workersApi.get("parameters/")
}

// APIs de creacion

export const createWorker = (data) => {
  const worker = { name: data.name, weight: data.weight };

  // Extraer los roles y experiencias del objeto data
  const rolesAndExperiences = data.roles.map((role) => ({
    role_id: role.role_id,
    role_name: role.role_name,
    experience: role.experience || 0,
  }));

  // Crear el trabajador
  return workersApi.post("workers/", worker).then((response) => {
    // obtener el id del trabajador creado
    const workerId = response.data.id;

    // Crear las experiencias del trabajador en cada rol
    const experiencePromises = rolesAndExperiences.map((roleExp) => {
      const experienceData = {
        worker: workerId,
        role: roleExp.role_id,
        experience: roleExp.experience,
      };
      // Crear la experiencia
      return workersApi.post("experience/", experienceData);
    });

    // Esperar a que todas las experiencias se hayan creado
    return Promise.all(experiencePromises);
  });
};

export const createRole = (data) => {
  return workersApi.post("roles/", data);
};

export const createConstant = (data) => {
  return workersApi.post("constants/", data);
};

export const createParam = (data) => {
  return workersApi.post("parameters/", data)
}

// APIs de modificacion

export const updateWorker = (data) => {
  return workersApi.patch(`workers/${data.id}/`, data);
};

export const updateRoleExp = (data) => {
  return workersApi.patch(`experience/${data.id}/`, data);
};

export const updateConstant = (data) => {
  return workersApi.patch(`constants/${data.id}/`, data);
};

export const updateParam = (data) => {
  return workersApi.patch(`parameters/${data.id}/`, data)
}

// APIs de eliminacion

export const deleteWorker = (data) => {
  return workersApi.delete(`workers/${data}/`);
};

export const deleteRole = (data) => {
  return workersApi.delete(`roles/${data}/`);
};

export const deleteConstant = (data) => {
  return workersApi.delete(`constants/${data}/`);
};

export const deleteParam = (data) => {
  return workersApi.delete(`parameters/${data.id}`)
}

// API para correr el modelo de optimizacion
export const runOptimization = (data) => {
  return workersApi.post("run/",data);
};