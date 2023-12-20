import { AxiosResponse } from 'axios';
import axiosInstance from '../interceptor/axiosInstance';

const httpService = {
  get: async <T>(url: string): Promise<T> => {
    try {
      const response: AxiosResponse<T> = await axiosInstance.get<T>(url);
      return response.data;
    } catch (error:any) {
      throw new Error(error.message);
    }
  },

  post: async <T, U>(url: string, data: T): Promise<U> => {
    try {
      const response: AxiosResponse<U> = await axiosInstance.post<U>(url, data);
      return response.data;
    } catch (error:any) {
      throw new Error(error.message);
    }
  },
  
};

export default httpService;
