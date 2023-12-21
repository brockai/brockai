import { AxiosResponse } from 'axios';
import axiosInstance from '../interceptor/axiosInstance';
interface OpenSearchData {
  name: string;
}

const OPENSEARCH_URL = 'https://opensearch.brockai.com/';

const httpService = {
  checkHealthOpenSearch: async (): Promise<AxiosResponse<OpenSearchData[]>> => {
    try {
      const response: AxiosResponse<OpenSearchData[]> = await axiosInstance.get(OPENSEARCH_URL);
      return response;
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
