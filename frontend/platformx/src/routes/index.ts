import { lazy } from 'react';

const Home = lazy(() => import('../pages/Home'));
const Account = lazy(() => import('../pages/Account'));

const coreRoutes = [
  {
    path: '/',
    title: 'Home',
    component: Home,
  },
  {
    path: '/account',
    title: 'Account Settings',
    component: Account,
  },
];

const routes = [...coreRoutes];
export default routes;
