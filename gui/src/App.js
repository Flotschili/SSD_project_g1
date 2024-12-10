import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BreweryList from './components/BreweryList';
import BreweryDetail from './components/BreweryDetail';
import BeerDetail from './components/BeerDetail';

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<BreweryList />} />
      <Route path="/brewery/:id" element={<BreweryDetail />} />
      <Route path="/beer/:id" element={<BeerDetail />} />
    </Routes>
  </Router>
);

export default App;
