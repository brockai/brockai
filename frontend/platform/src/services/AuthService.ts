import axios, { AxiosResponse, AxiosError } from 'axios';

const BASE_URL = 'http://localhost:9000';

type ResponseData = {
  
};

type ErrorData = {
  
};

export const authService = {

  login: async (dataToSend: any): Promise<AxiosResponse<ResponseData> | AxiosError<ErrorData>> => {
    debugger
    try {
      const response = await axios.post<ResponseData>(`http://localhost:9000/auth/login`, dataToSend);
      debugger
      return response;
    } catch (error) {
      debugger
      return error as AxiosError<ErrorData>;
    }
  },

  signup: async (dataToSend: any): Promise<AxiosResponse<ResponseData> | AxiosError<ErrorData>> => {
    try {
      const response = await axios.post<ResponseData>(`${BASE_URL}/auth/signup`, dataToSend);
      return response;
    } catch (error) {
      return error as AxiosError<ErrorData>;
    }
  },

  authenticated: async (dataToSend: any): Promise<AxiosResponse<ResponseData> | AxiosError<ErrorData>> => {
    try {
      const response = await axios.get<ResponseData>(`${BASE_URL}`, dataToSend);
      return response;
    } catch (error) {
      return error as AxiosError<ErrorData>;
    }
  },

};