import ParamsTable from "../components/ParamsTable";
import "../styles/workertable.css";

export function ParamPage() {
  return (
    <div className="container">
      <h1 className="text-center display-3 py-4">Parameters</h1>
      <ParamsTable/>
    </div>
  );
}
