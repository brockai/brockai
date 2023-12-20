import { lazy } from 'react';

const Home = lazy(() => import('../pages/Home'));
const Account = lazy(() => import('../pages/Account'));
const SignIn = lazy(() => import('../pages/Authentication/SignIn'));
const SignUp = lazy(() => import('../pages/Authentication/SignUp'));

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
  {
    path: '/signin',
    title: 'SignIn',
    component: SignIn,
  },
  {
    path: '/signup',
    title: 'SignUp',
    component: SignUp,
  },
];

const routes = [...coreRoutes];
export default routes;
