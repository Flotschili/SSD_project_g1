import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export const fetchBreweries = async () => {
  const response = await axios.get(`${API_BASE_URL}/breweries`);
  return response.data;
};

export const fetchBreweryDetails = async (breweryId) => {
  const response = await axios.get(`${API_BASE_URL}/breweries/${breweryId}`);
  return response.data;
};

export const fetchBeerDetails = async (beerId) => {
  const response = await axios.get(`${API_BASE_URL}/beers/${beerId}`);
  return response.data;
};

export const updateBrewery = async (breweryId, breweryData) => {
  const response = await axios.put(`${API_BASE_URL}/breweries/${breweryId}`, breweryData);
  return response.data;
};

export const updateBeer = async (beerId, beerData) => {
  const response = await axios.put(`${API_BASE_URL}/beers/${beerId}`, beerData);
  return response.data;
};
