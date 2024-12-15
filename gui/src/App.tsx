import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import BeerList from './components/BeerList';
import LoginPage from './components/LoginPage';
import PrivateRoute from './routes/PrivateRoute'; // Import the PrivateRoute component

const App: React.FC = () => (
  <Router>
    <Header />
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<PrivateRoute element={<BeerList />} />} />
    </Routes>
  </Router>
);

export default App;