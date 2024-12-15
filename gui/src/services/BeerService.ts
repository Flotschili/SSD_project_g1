import { Beer } from "../models/Beer";
import axiosInstance from "./axiosConfig"; // Import the configured Axios instance

const BEER_API_URL = "/beers/";

class BeerService {
  async getBeers() {
    const response = await axiosInstance.get(BEER_API_URL);

    return response.data;
  }

  async getBeer(id: number) {
    const response = await axiosInstance.get(`${BEER_API_URL}${id}/`);

    return response.data;
  }

  async createBeer(beerData: Beer) {
    const response = await axiosInstance.post(BEER_API_URL, beerData);

    return response.data;
  }

  async updateBeer(id: number, beerData: Beer) {
    const response = await axiosInstance.put(`${BEER_API_URL}${id}/`, beerData);

    return response.data;
  }

  async deleteBeer(id: number) {
    const response = await axiosInstance.delete(`${BEER_API_URL}${id}/`);

    return response.data;
  }
}

export default new BeerService();
