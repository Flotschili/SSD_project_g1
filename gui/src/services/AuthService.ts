import axiosInstance from "./axiosConfig"; // Import the configured Axios instance

const AUTH_URL = 'http://localhost:8000/api/v1/auth/';
const VALIDATE_TOKEN_URL = 'http://localhost:8000/api/v1/auth/user/';

class AuthService {
  async login(username: string, password: string): Promise<void> {
    const response = await axiosInstance.post(AUTH_URL + 'login/', {
      username,
      password,
    });
    localStorage.setItem('token', response.data.key); // Store the token in localStorage
  }

  async logout(): Promise<void> {
    const response = await axiosInstance.post(AUTH_URL + 'logout/');

    if (response.status !== 200) {
      console.error('Error logging out:', response.data);
    }

    localStorage.removeItem('token'); // Remove the token from localStorage
  }

  async validateToken(): Promise<boolean> {
    try {
      const response = await axiosInstance.get(VALIDATE_TOKEN_URL);
      return response.status === 200 && response.data;
    } catch (error) {
      console.error('Error validating token:', error);
      return false;
    }
  }
}

export default new AuthService();