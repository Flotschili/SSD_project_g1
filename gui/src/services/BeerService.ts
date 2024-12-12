import axios from 'axios';
import { Beer } from '../models/Beer';

const API_URL = 'https://your-backend-api.com/beers';

export const BeerService = {
  async getBeers(): Promise<Beer[]> {
    const response = await axios.get<Beer[]>(API_URL);
    return response.data;
  },

  async getBeer(id: number): Promise<Beer> {
    const response = await axios.get<Beer>(`${API_URL}/${id}`);
    return response.data;
  },

  async updateBeer(beer: Beer): Promise<void> {
    await axios.put(`${API_URL}/${beer.id}`, beer);
  },
};
