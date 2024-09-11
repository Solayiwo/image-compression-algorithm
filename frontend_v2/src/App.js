import React from 'react';
import './App.css';
// import Header from './components/header/header.component';
import Homepage from './pages/hompage/homepage';
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
} from "react-router-dom";


function App() {
  return (
    <BrowserRouter>
      <div>
        <Homepage />
      </div>
    </BrowserRouter>
  );
}

export default App;
