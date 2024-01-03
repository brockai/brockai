import { Suspense, lazy, useEffect, useState } from 'react';
import { createAuth0Client } from '@auth0/auth0-spa-js';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

import Home from './pages/Home';
import Loader from './common/Loader';
import routes from './routes';

const DefaultLayout = lazy(() => import('./layout/Layout'));

function App() {

  const [auth0Client, setAuth0Client] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setTimeout(() => setLoading(false), 1000);

    const initAuth0 = async () => {
      const auth0Domain: any = process.env.REACT_APP_AUTH0_DOMAIN;
      const auth0ClientId: any = process.env.REACT_APP_AUTH0_CLIENT_ID;
      
      const auth0 = await createAuth0Client({
        domain: auth0Domain,
        clientId: auth0ClientId,
      });
      setAuth0Client(auth0);

      if (window.location.search.includes('code=')) {
        try {
          // await auth0.handleRedirectCallback();
          const token = await auth0.getTokenSilently();
          const idToken = await auth0.getIdTokenClaims();
          
          if (idToken) {
            const tenantId = idToken['nickname'] || 'bclayton403';

            localStorage.setItem('accessToken', token);
            localStorage.setItem('tenantId', tenantId);
          }
        } catch (error) {
          console.error('Authentication error:', error);
        }
      }
    };

    initAuth0();
  }, []);

  return loading ? (
    <Loader />
  ) : (
    <>
      <Toaster
        position="top-right"
        reverseOrder={false}
        containerClassName="overflow-auto"
      />
      <Router>
        <Routes>
          <Route element={<DefaultLayout />}>
            <Route index element={<Home />} />
            {routes.map((routes, index) => {
              const { path, component: Component } = routes;
              return (
                <Route
                  key={index}
                  path={path}
                  element={
                    <Suspense fallback={<Loader />}>
                      <Component />
                    </Suspense>
                  }
                />
              );
            })}
          </Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
