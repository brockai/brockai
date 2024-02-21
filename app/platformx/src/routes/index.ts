import { lazy } from 'react';

const Landing = lazy(() => import('../pages/Landing'));
const Datasets = lazy(() => import('../pages/Datasets'));


const coreRoutes = [
  {
    path: '/',
    title: 'Landing',
    component: Landing,
  },
  {
    path: '/datasets',
    title: 'Datasets',
    component: Datasets
  },
];

const routes = [...coreRoutes];


export default routes;
