import axios, { AxiosResponse } from 'axios';
import axiosInstance from '../interceptor/axiosInstance';

const OPENSEARCH_URL = 'https://opensearch.brockai.com';

interface OpenSearchCredentials {
  name: string;
  password: string;
}

const openSearchService = {
  getUser: async (credentials:OpenSearchCredentials): Promise<AxiosResponse<OpenSearchCredentials[]>> => {
    console.log(credentials)
    try {
      console.log(`OPENSEARCH_URL/_plugins/_security/api/internalusers/${credentials.name}`)
      debugger
      const response: AxiosResponse<OpenSearchCredentials[]> = await axiosInstance.get(`OPENSEARCH_URL/plugins/_security/api/internalusers/${credentials.name}`);
      console.log(response)
      debugger
      return response;
    } catch (error:any) {
      console.log(error)
      debugger
      throw new Error(error.message);
    }
    debugger
  },

  // post: async <T, U>(url: string, data: T): Promise<U> => {
  //   try {
  //     const response: AxiosResponse<U> = await axiosInstance.post<U>(url, data);
  //     return response.data;
  //   } catch (error:any) {
  //     throw new Error(error.message);
  //   }
  // },
  
};

export default openSearchService;

// export const checkHealth = async (): Promise<AxiosResponse<any>> => {
//   try {
//     const response = await axios.get(`${OPENSEARCH_URL}`);
//     console.log(response)
//     return response;
//   } catch (error) {
//     throw new Error(`Error fetching data from Elasticsearch: ${error}`);
//   }
// };

// export const getUser = async (name:any): Promise<AxiosResponse<any>> => {
//   try {
//     const response = await .get(`${OPENSEARCH_URL}_plugins/_security/api/internalusers/${name}`);
//     console.log(response)
//     return response;
//   } catch (error) {
//     throw new Error(`Error fetching data from Elasticsearch: ${error}`);
//   }
// };

// export default checkHealth;
