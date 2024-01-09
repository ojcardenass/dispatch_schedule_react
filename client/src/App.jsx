import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./styles/styles.css"

import { Navigation } from "./components/Navigation";
import * as Pages from './pages';

const {WorkerPage,WorkerFormPage,RolePage,RoleFormPage,ParamPage,ParamFormPage,ConstantPage,ConstantFormPage,ModelPage,SchedulePage,Home} = Pages


function App() {
  return (
    <BrowserRouter>
      <Navigation/>
      <Routes>
        
        <Route path="/" element={<Home/>} />
        <Route path="/workers/list" element={<WorkerPage />} />
        <Route path="/workers/create" element={<WorkerFormPage />} />
        <Route path="/roles" element={<RolePage />} />
        <Route path="/params" element={<ParamPage />} />
        <Route path="/schedule" element={<SchedulePage />} />
        <Route path="/model" element={<ModelPage />} />
        <Route path="/constants" element={<ConstantPage />} />
      </Routes>
    </BrowserRouter>

  );
}

export default App;