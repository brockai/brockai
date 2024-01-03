import axios from 'axios';

const opensearchApi: any = process.env.REACT_APP_OPENSEARCH_API || 'localhost:9200';

const opensearchInstance = axios.create({
  baseURL: opensearchApi,
  timeout: 5000,
});

const username = 'admin';
const password = 'admin';
const basicAuth = 'Basic ' + btoa(username + ':' + password);


opensearchInstance.interceptors.request.use(
  (config) => {
    const fetchedToken = localStorage.getItem('accessToken');
    if (fetchedToken) {
      config.headers.Authorization = basicAuth;
      
      // config.headers.Authorization = `Bearer ${fetchedToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor: Handle response data or errors
opensearchInstance.interceptors.response.use(
  (response) => {
    // Handle successful responses
    return response;
  },
  (error) => {
    // Handle error responses
    return Promise.reject(error);
  }
);

export default opensearchInstance;
