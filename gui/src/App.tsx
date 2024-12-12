import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import BeerList from './components/BeerList';
import BeerDetail from './components/BeerDetail';
import BeerEdit from './components/BeerEdit';

const App: React.FC = () => (
  <Router>
    <Header />
    <Routes>
      <Route path="/" element={<BeerList />} />
      <Route path="/beers/:id" element={<BeerDetail />} />
      <Route path="/beers/:id/edit" element={<BeerEdit />} />
    </Routes>
  </Router>
);

export default App;
