import dotenv from 'dotenv';
dotenv.config();

import express from 'express';
import cors from 'cors';
import routerOpensearch from './routes/opensearchRouter.mjs';
const app = express();

app.use(express.json());
app.options('*', cors());
app.use(cors());
app.use(routerOpensearch);
 
app.listen(9000, () => console.log('brockai api listening on port 9000!'));