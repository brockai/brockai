import axios, { InternalAxiosRequestConfig, AxiosResponse } from 'axios';
import Cookies from 'js-cookie';

export const axiosInstance = axios.create({
  baseURL: 'https://opensearch.brockai.com', 
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
