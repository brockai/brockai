import { Suspense, lazy } from 'react';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { Nav } from './Nav'
import Landing from './pages/Landing';
import Loader from './common/Loader';
import routes from './routes';

const DefaultLayout = lazy(() => import('./layout/Layout'));

function App() {

  const { isLoading, error } = useAuth0();

  return isLoading ? (
    <Loader />
  ) : (
    <>
      <Toaster
        position="top-right"
        reverseOrder={false}
        containerClassName="overflow-auto"
      />
      <Router>
        <Nav />
        <Routes>
          <Route element={<DefaultLayout />}>
          </Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
