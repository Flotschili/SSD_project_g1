import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { TextField, Button, Container } from '@mui/material';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { Beer } from '../models/Beer';

// Define the Yup validation schema
const beerSchema = yup.object({
  id: yup.number().required(), // Add validation for id if necessary
  name: yup.string().required('Name is required'),
  alcoholPercent: yup.number().required('Alcohol percent is required'),
  description: yup.string().required('Description is required'),
  brewery: yup.string().required('Brewery is required'),
});

const BeerEdit = () => {
  const { control, handleSubmit, setValue } = useForm<Beer>({
    resolver: yupResolver(beerSchema),
  });

  const onSubmit = (data: Beer) => {
    console.log(data);
  };

  return (
    <Container>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Controller
          name="name"
          control={control}
          render={({ field }) => <TextField {...field} label="Name" />}
        />
        <Controller
          name="alcoholPercent"
          control={control}
          render={({ field }) => <TextField {...field} label="Alcohol Percentage" />}
        />
        <Controller
          name="description"
          control={control}
          render={({ field }) => <TextField {...field} label="Description" />}
        />
        <Controller
          name="brewery"
          control={control}
          render={({ field }) => <TextField {...field} label="Brewery" />}
        />
        <Button type="submit">Save</Button>
      </form>
    </Container>
  );
};

export default BeerEdit;
