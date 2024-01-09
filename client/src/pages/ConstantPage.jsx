
import ConstantsTable from "../components/ConstantsTable";
import "../styles/workertable.css";

export function ConstantPage() {
 
  return (
    <div className="text-center col-md-6 container">
      <h1 className="text-center display-3 py-4">Constants List</h1>
      <ConstantsTable />
    </div>
  );
}
