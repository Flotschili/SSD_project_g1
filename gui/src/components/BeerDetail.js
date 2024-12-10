import React, { useEffect, useState } from 'react';
import { fetchBeerDetails, updateBeer } from '../services/api';
import { useParams } from 'react-router-dom';
import { Button, TextField } from '@mui/material';

const BeerDetail = () => {
  const { id } = useParams();
  const [beer, setBeer] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const loadBeer = async () => {
      const data = await fetchBeerDetails(id);
      setBeer(data);
    };
    loadBeer();
  }, [id]);

  const handleSave = async () => {
    await updateBeer(id, beer);
    setIsEditing(false);
  };

  return beer ? (
    <div>
      {isEditing ? (
        <TextField
          label="Name"
          value={beer.name}
          onChange={(e) => setBeer({ ...beer, name: e.target.value })}
        />
      ) : (
        <h1>{beer.name}</h1>
      )}
      <h2>{beer.alcohol}%</h2>
      <Button onClick={() => setIsEditing(!isEditing)}>{isEditing ? 'Cancel' : 'Edit'}</Button>
      {isEditing && <Button onClick={handleSave}>Save</Button>}
    </div>
  ) : (
    <p>Loading...</p>
  );
};

export default BeerDetail;
