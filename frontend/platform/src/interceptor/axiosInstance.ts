import axios, { InternalAxiosRequestConfig, AxiosResponse } from 'axios';
import Cookies from 'js-cookie';

export const axiosInstance = axios.create({
  baseURL: 'http://localhost:9000', // Replace with your API base URL
});

axiosInstance.interceptors.request.use(config => {
    config.auth = {
      username: 'admin',
      password: 'admin',
    };
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
