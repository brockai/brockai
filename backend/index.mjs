import express from 'express';
import session from 'express-session';
import Keycloak from 'keycloak-connect';

import dotenv from 'dotenv';
dotenv.config();

import cors from 'cors';
import vectorRouter from './routes/index.mjs';
const app = express();

app.use(
  session({
    secret: process.env.BEARER_TOKEN_SECRET,
    resave: false,
    saveUninitialized: true,
  })
);

app.use(express.json());
app.options('*', cors());
app.use(cors());
// app.use('/api',vectorRouter);
 
app.listen(9000, () => console.log('brockai api listening on port 9000!'));