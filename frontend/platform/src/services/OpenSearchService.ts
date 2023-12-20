export interface OpenSearchCredentials {
  email: string;
  password: string
}

const REACT_APP_OPENSEARCH_API:any = "https://localhost:9200/";
// const REACT_APP_OPENSEARCH_API:any = process.env.REACT_APP_OPENSEARCH_API;
// const REACT_APP_OPENSEARCH_USER:any = process.env.REACT_APP_OPENSEARCH_USER;
// const REACT_APP_OPENSEARCH_PASSWORD:any = process.env.REACT_APP_OPENSEARCH_PASSWORD;
// console.log(REACT_APP_OPENSEARCH_API)
const encodedCredentials = btoa(`admin:admin`);

// const encodedCredentials = btoa(`${REACT_APP_OPENSEARCH_USER}:${REACT_APP_OPENSEARCH_PASSWORD}`);

export const loginUser = async (userData: OpenSearchCredentials): Promise<void> => {
  console.log(userData, REACT_APP_OPENSEARCH_API+'_plugins/_security/api/internalusers/admin')
  debugger
  try {
    const response = await fetch(REACT_APP_OPENSEARCH_API+'_plugins/_security/api/internalusers/admin', {
      method: 'GET',
      headers: {
        Authorization: `Basic ${encodedCredentials}`,
        'Content-Type': 'application/json',
        
      },
    });
    debugger
    
    
    // if (!response.ok) {
    //   throw new Error('Failed to create user');
    // }
    const usersData = await response.json();
    return usersData;

  } catch (error) {
    debugger
    console.error('Error creating user:', error);
    throw new Error('Failed to create user');
  }
};

