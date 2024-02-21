import { useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';
import Login from './components/Login';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import { Outlet } from 'react-router-dom';
import Brockailogo from './images/logo/brockailogo.png'

export function Nav() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const { isAuthenticated, user } = useAuth0<{
    name: string;
    nickname: string;
  }>();
  
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
     
      {isAuthenticated ? (
        <div className="dark:bg-boxdark-2 dark:text-bodydark">
          <div className="flex h-screen overflow-hidden">
            <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
            <div className="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
              <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
              <main>
                <div>
                  <span id="hello">Hello, {user?.name}, {user?.nickname}!</span>{' '}
                </div>
                <div className="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
                  <Outlet />
                </div>
              </main>
            </div>
          </div>
        </div>
      ) : (
        <div className="dark:bg-boxdark-2 dark:text-bodydark">
          <div className="flex h-screen overflow-hidden">
            <div className="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
              <Login />
              <main>
                <div className="min-h-screen flex items-center justify-center">
                  <img src={Brockailogo} alt="Logo" style={{ height: '150px' }} />
                </div>
              </main>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}