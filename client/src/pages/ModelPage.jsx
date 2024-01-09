import React, { useState } from 'react';
import { Button, Alert } from 'react-bootstrap';
import { runOptimization } from "../api/workers.api";


export function ModelPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleRunOptimization = () => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    // Replace these with your actual model_params and solver_opt data
    const modelParams = {};
    const solverOpt = {};
    const data = {modelParams, solverOpt}

    // Call the API function with model_params and solver_opt
    runOptimization(data)
      .then((response) => {
        setResult(response.data.result);
      })
      .catch((err) => {
        setError('Error running optimization: ' + err.message);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  return (
    <div>
      <h1 className="text-center display-3 py-3">Schedule Model</h1>

      <Button variant="primary" onClick={handleRunOptimization} disabled={isLoading}>
        Run Optimization
      </Button>

      {isLoading && <p>Loading...</p>}
      {result && <p>Optimization Result: {result}</p>}
      {error && <Alert variant="danger">{error}</Alert>}
    </div>
  );

}