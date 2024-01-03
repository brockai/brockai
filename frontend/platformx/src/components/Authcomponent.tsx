import React, { useEffect, useState } from 'react';
import {  createAuth0Client} from '@auth0/auth0-spa-js';

function AuthComponent() {
  const [auth0Client, setAuth0Client] = useState<any | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  useEffect(() => {
    const initAuth0 = async () => {
      const auth0 = await createAuth0Client({
        domain: 'auth0Config.domain',
        clientId: 'auth0Config.clientId',
      });
      setAuth0Client(auth0);

      if (window.location.search.includes('code=')) {
        try {
          await auth0.handleRedirectCallback();
          const token = await auth0.getTokenSilently();
          setAccessToken(token);
        } catch (error) {
          console.error('Authentication error:', error);
        }
      }
    };

    initAuth0();
  }, []);

  const login = async () => {
    if (auth0Client) {
      await auth0Client.loginWithRedirect();
    }
  };

  const logout = async () => {
    if (auth0Client) {
      await auth0Client.logout();
    }
  };

  return (
    <div>
      {accessToken ? (
        <>
          <p>Access Token: {accessToken}</p>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <button onClick={login}>Login</button>
      )}
    </div>
  );
}

export default AuthComponent;
