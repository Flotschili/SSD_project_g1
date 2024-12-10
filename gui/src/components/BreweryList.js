import React, { useEffect, useState } from 'react';
import { fetchBreweries } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { Table, TableBody, TableCell, TableHead, TableRow, TableSortLabel } from '@mui/material';

const BreweryList = () => {
  const [breweries, setBreweries] = useState([]);
  const [sortOrder, setSortOrder] = useState('asc');
  const [sortField, setSortField] = useState('name');
  const navigate = useNavigate();

  useEffect(() => {
    const loadBreweries = async () => {
      const data = await fetchBreweries();
      setBreweries(data);
    };
    loadBreweries();
  }, []);

  const handleSort = (field) => {
    const isAsc = sortField === field && sortOrder === 'asc';
    setSortOrder(isAsc ? 'desc' : 'asc');
    setSortField(field);
  };

  const sortedBreweries = [...breweries].sort((a, b) => {
    if (a[sortField] < b[sortField]) return sortOrder === 'asc' ? -1 : 1;
    if (a[sortField] > b[sortField]) return sortOrder === 'asc' ? 1 : -1;
    return 0;
  });

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>
            <TableSortLabel
              active={sortField === 'name'}
              direction={sortField === 'name' ? sortOrder : 'asc'}
              onClick={() => handleSort('name')}
            >
              Name
            </TableSortLabel>
          </TableCell>
          <TableCell>
            <TableSortLabel
              active={sortField === 'location'}
              direction={sortField === 'location' ? sortOrder : 'asc'}
              onClick={() => handleSort('location')}
            >
              Location
            </TableSortLabel>
          </TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {sortedBreweries.map((brewery) => (
          <TableRow key={brewery.id} onClick={() => navigate(`/brewery/${brewery.id}`)}>
            <TableCell>{brewery.name}</TableCell>
            <TableCell>{brewery.location}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default BreweryList;
