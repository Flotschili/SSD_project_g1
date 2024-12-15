// FILE: BeerList.tsx
import React, { useEffect, useState } from 'react';
import { Beer } from '../models/Beer';
import BeerService from '../services/BeerService';
import { Table, TableBody, TableCell, TableHead, TableRow, TableSortLabel, Container, Button } from '@mui/material';
import BeerForm from './BeerForm';

const BeerList: React.FC = () => {
  const [beers, setBeers] = useState<Beer[]>([]);
  const [sortBy, setSortBy] = useState<'name' | 'alcohol_content'>('name');
  const [sortAsc, setSortAsc] = useState(true);
  const [open, setOpen] = useState(false);
  const [selectedBeer, setSelectedBeer] = useState<Beer | null>(null);

  useEffect(() => {
    BeerService.getBeers().then(setBeers);
  }, []);

  const handleSort = (field: 'name' | 'alcohol_content') => {
    setSortAsc(sortBy === field ? !sortAsc : true);
    setSortBy(field);
  };

  const sortedBeers = [...beers].sort((a, b) => {
    const order = sortAsc ? 1 : -1;
    return a[sortBy] > b[sortBy] ? order : -order;
  });

  const handleOpen = (beer: Beer | null) => {
    setSelectedBeer(beer);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedBeer(null);
  };

  const handleSave = () => {
    BeerService.getBeers().then(setBeers);
  };

  return (
    <Container >
      <Button variant="contained" color="primary" onClick={() => handleOpen(null)}>
        Add Beer
      </Button>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>
              <TableSortLabel
                active={sortBy === 'name'}
                direction={sortAsc ? 'asc' : 'desc'}
                onClick={() => handleSort('name')}
              >
                Name
              </TableSortLabel>
            </TableCell>
            <TableCell>Beer Type</TableCell>
            <TableCell>Brewery</TableCell>
            <TableCell>
              <TableSortLabel
                active={sortBy === 'alcohol_content'}
                direction={sortAsc ? 'asc' : 'desc'}
                onClick={() => handleSort('alcohol_content')}
              >
                Alcohol Percent
              </TableSortLabel>
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {sortedBeers.map((beer) => (
            <TableRow key={beer.id} onClick={() => handleOpen(beer)}>
              <TableCell>{beer.name}</TableCell>
              <TableCell>{beer.beer_type}</TableCell>
              <TableCell>{beer.brewery}</TableCell>
              <TableCell>{beer.alcohol_content}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <BeerForm open={open} onClose={handleClose} beer={selectedBeer} onSave={handleSave} />
    </Container>
  );
};

export default BeerList;