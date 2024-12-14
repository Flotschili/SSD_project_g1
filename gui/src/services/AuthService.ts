import axiosInstance from "./axiosConfig"; // Import the configured Axios instance

const LOGIN_URL = 'http://localhost:8000/api/v1/auth/login/';
const VALIDATE_TOKEN_URL = 'http://localhost:8000/api/v1/auth/user/';

class AuthService {
  async login(username: string, password: string): Promise<void> {
    const response = await axiosInstance.post(LOGIN_URL, {
      username,
      password,
    });
    localStorage.setItem('token', response.data.key); // Store the token in localStorage
  }

  async validateToken(): Promise<boolean> {
    try {
      const response = await axiosInstance.get(VALIDATE_TOKEN_URL);
      console.log('Token validation response:', response.data);

      return response.status === 200 && response.data;
    } catch (error) {
      console.error('Error validating token:', error);
      return false;
    }
  }
}

export default new AuthService();