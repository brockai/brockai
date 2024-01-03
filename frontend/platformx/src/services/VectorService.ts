import opensearchInstance from '../interceptor/OpensearchInstance';

const opensearchApi: any = process.env.REACT_APP_OPENSEARCH_API || 'localhost:9200';

const Vectors = opensearchInstance;

export const fetchData = async (endpoint:string) => {
  try {
    const response = await opensearchInstance.get(opensearchApi + endpoint);
    if (response.status === 200) {
      const data = response.data.split('\n').map((row: any) => row.split(' ')[2]).filter(Boolean);
      return data;
    }
  } catch (error) {
    console.error('Error fetching indices:', error);
  }
};

export const fetchStats = async (indexIds:any) => {
  try {
    const response = await opensearchInstance.get(opensearchApi + indexIds +'/_stats');
    if (response.status === 200) {
      const data = response.data;
      return data;
    }
  } catch (error) {
    console.error('Error fetching indices:', error);
  }
};

export const createIndex = async (tenantId:any, indexMappings:any) => {
  try {
    const response = await opensearchInstance.put(opensearchApi + tenantId, indexMappings);
    if (response.status === 200) {
      return response;
    }
  } catch (error) {
    console.error('Error creating index:', error);
    return;
  }
};

export default Vectors;
