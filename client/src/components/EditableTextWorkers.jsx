import React, { useState, ChangeEvent } from "react";
import { getAllRoles, updateRoleExp, updateWorker } from "../api/workers.api";

const EditableTextWorkers = ({ initialText, type, field, workerId }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [text, setText] = useState(initialText);

  const handleDoubleClick = () => {
    setIsEditing(true);
  };

  const handleChange = (event) => {
    setText(event.target.value);
  };

  const handleChangeAndSize = (event) => {
    const target = event.target;
    target.style.width = "60px";
    target.style.width = `${target.scrollWidth}px`;
    setText(event.target.value);
    handleChange(event);
  };

  const handleBlur = () => {
    const data = { id: workerId, [field]: text };

    getAllRoles().then((roles) => {
      // Se separa el nombre y el id del campo
      const [fieldName, experienceId] = field.split("_");
      const isItemInData = roles.data.some((role) => role.name === fieldName);

      if (isItemInData) {
        // Se guardan el id y la experiencia modificada
        const experience_data = { id: experienceId, experience: data[field] };
        // Llamar a la api para actualizar el valor de la experiencia
        updateRoleExp(experience_data)
          .then(() => {
            setIsEditing(false); // Desactivar el modo edicion
          })
          .catch((error) => {
            console.error("Error updating worker:", error);
          });
      }
      // Llamar a la api para actualizar el valor del trabajador
      updateWorker(data)
        .then(() => {
          setIsEditing(false); // Desactivar el modo edicion
        })
        .catch((error) => {
          console.error("Error updating worker:", error);
        });
    });
  };

  // Calcular el tamaño del input en base al texto que contiene
  const textLength = text.toString().length;

  return (
    <div onDoubleClick={handleDoubleClick}>
      {isEditing ? (
        <input
          type={type}
          value={text}
          style={{ width: `${textLength * 9}px`, minWidth: "60px" }}
          onChange={handleChangeAndSize}
          onBlur={handleBlur}
        />
      ) : (
        <span>{text}</span>
      )}
    </div>
  );
};

export default EditableTextWorkers;
