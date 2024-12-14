import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Beer } from '../models/Beer';
import BeerService from '../services/BeerService';
import { Button, Container, Typography } from '@mui/material';

const BeerDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [beer, setBeer] = useState<Beer | null>(null);

  useEffect(() => {
    if (id) {
      BeerService.getBeer(Number(id)).then(setBeer);
    }
  }, [id]);

  if (!beer) return <Typography>Loading...</Typography>;

  return (
    <Container>
      <Typography variant="h4">{beer.name}</Typography>
      <Typography>Brewery: {beer.brewery}</Typography>
      <Typography>Alcohol: {beer.alcoholPercent}%</Typography>
      <Typography>{beer.description}</Typography>
      <Button variant="contained" onClick={() => navigate(`/beers/${beer.id}/edit`)}>
        Edit
      </Button>
    </Container>
  );
};

export default BeerDetail;