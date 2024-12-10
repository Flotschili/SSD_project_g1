import React, { useEffect, useState } from 'react';
import { fetchBreweryDetails, updateBrewery } from '../services/api';
import { useParams, useNavigate } from 'react-router-dom';
import { Button, TextField, Table, TableBody, TableCell, TableHead, TableRow, CircularProgress } from '@mui/material';

const BreweryDetail = () => {
  const { id } = useParams();
  const [brewery, setBrewery] = useState({ name: '', location: '', beers: [] });
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadBrewery = async () => {
      try {
        const data = await fetchBreweryDetails(id);
        setBrewery(data);
      } catch (error) {
        console.error('Error loading brewery details:', error);
      } finally {
        setLoading(false);
      }
    };
    loadBrewery();
  }, [id]);

  const handleSave = async () => {
    try {
      await updateBrewery(id, brewery);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating brewery:', error);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </div>
    );
  }

  return (
    <div>
      {isEditing ? (
        <TextField
          label="Name"
          value={brewery.name}
          onChange={(e) => setBrewery({ ...brewery, name: e.target.value })}
        />
      ) : (
        <h1>{brewery.name}</h1>
      )}
      <h2>{brewery.location}</h2>
      <Button onClick={() => setIsEditing(!isEditing)}>{isEditing ? 'Cancel' : 'Edit'}</Button>
      {isEditing && <Button onClick={handleSave}>Save</Button>}

      <h3>Beers</h3>
      {!brewery.beers?.length ? (
        <p>No beers available for this brewery.</p>
      ) : (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Alcohol %</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {brewery.beers.map((beer) => (
              <TableRow key={beer.id} onClick={() => navigate(`/beer/${beer.id}`)}>
                <TableCell>{beer.name}</TableCell>
                <TableCell>{beer.alcohol}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
};

export default BreweryDetail;
