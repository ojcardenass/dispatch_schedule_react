import React, { useState, ChangeEvent } from "react";
import { getAllParams, getAllRoles, updateParam } from "../api/workers.api";

const EditableTextParams = ({ initialText, type, field, ParamId }) => {
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
    const data = { id: ParamId, [field]: text };

    // Obtener todos los parametros
    getAllParams().then(async (params) => {
      // Encontrar el nombre del parametro asociado al ParamId que se esta editando
      const targetParam = params.data.find((param) => param.id === ParamId);

      if (!targetParam) {
        // Error para cuando no se encuentre un parametro
        console.log("ParamId not found");
        return;
      }

      // Obtener el nombre del parametro que coincide
      const paramNameToMatch = targetParam.parameter;

      // Filtrar todos los parametros que coinciden con el mismo nombre asociado al ParamId
      const paramsToUpdate = params.data.filter((param) => {
        return param.parameter === paramNameToMatch;
      });

      // Si el campo es parametro solo se actualiza el nombre del parametro
      if (field === "parameter") {
        await Promise.all(
          paramsToUpdate.forEach(async (param) => {
            const dataParam = { id: param.id, [field]: text };
            // Llamado a la API para actualizar el nombre del parametro
            await updateParam(dataParam);
          })
        );
      }
      // De lo contrario se actualiza el valor
      else {
        await updateParam(data);
      }
    });
    setIsEditing(false); // Desactivar el modo edicion
  };

  // Calcular el tamaño del input en base al texto que contiene
  const textLength = text.toString().length;

  return (
      <div onDoubleClick={handleDoubleClick}>
        {isEditing ? (
          <input
            type={type}
            value={text}
            style={{ width: `${textLength * 9}px`, minWidth: "40px" }}
            onChange={handleChangeAndSize}
            onBlur={handleBlur}
          />
        ) : (
          <span>{text}</span>
        )}
      </div>
  );
};

export default EditableTextParams;
