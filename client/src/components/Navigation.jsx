import { Link } from "react-router-dom"

import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

export function Navigation() {
  return (
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="/">Schedule app</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/">Home</Nav.Link>

            <NavDropdown title="Workers" id="basic-nav-dropdown">
              <NavDropdown.Item href="/workers/list">Worker List</NavDropdown.Item>
              <NavDropdown.Item href="/workers/create">Create Worker</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="Roles" id="basic-nav-dropdown">
              <NavDropdown.Item href="/roles">Roles</NavDropdown.Item>
              <NavDropdown.Item href="/params">Parameters</NavDropdown.Item>
            </NavDropdown>         
            <Nav.Link href="/schedule">Schedule</Nav.Link>
            <NavDropdown title="Model" id="basic-nav-dropdown">
              <NavDropdown.Item href="/model">Model</NavDropdown.Item>
              <NavDropdown.Item href="/constants">Constant List</NavDropdown.Item>
            </NavDropdown>         
            <Nav.Link href="/signin">Sign In</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}