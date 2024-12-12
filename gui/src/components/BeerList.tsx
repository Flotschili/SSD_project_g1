import React, { useEffect, useState } from 'react';
import { Beer } from '../models/Beer';
import { BeerService } from '../services/BeerService';
import { useNavigate } from 'react-router-dom';
import { Table, TableBody, TableCell, TableHead, TableRow, TableSortLabel, Container } from '@mui/material';

const BeerList: React.FC = () => {
  const [beers, setBeers] = useState<Beer[]>([]);
  const [sortBy, setSortBy] = useState<'name' | 'alcoholPercent'>('name');
  const [sortAsc, setSortAsc] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    BeerService.getBeers().then(setBeers);
  }, []);

  const handleSort = (field: 'name' | 'alcoholPercent') => {
    setSortAsc(sortBy === field ? !sortAsc : true);
    setSortBy(field);
  };

  const sortedBeers = [...beers].sort((a, b) => {
    const order = sortAsc ? 1 : -1;
    return a[sortBy] > b[sortBy] ? order : -order;
  });

  return (
    <Container>
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
            <TableCell>Brewery</TableCell>
            <TableCell>
              <TableSortLabel
                active={sortBy === 'alcoholPercent'}
                direction={sortAsc ? 'asc' : 'desc'}
                onClick={() => handleSort('alcoholPercent')}
              >
                Alcohol (%)
              </TableSortLabel>
            </TableCell>
            <TableCell>Description</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {sortedBeers.map((beer) => (
            <TableRow
              key={beer.id}
              hover
              onClick={() => navigate(`/beers/${beer.id}`)}
              style={{ cursor: 'pointer' }}
            >
              <TableCell>{beer.name}</TableCell>
              <TableCell>{beer.brewery}</TableCell>
              <TableCell>{beer.alcoholPercent}</TableCell>
              <TableCell>{beer.description}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Container>
  );
};

export default BeerList;