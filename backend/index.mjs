import express from 'express';

import cors from 'cors';
import platformRouter from './routes/index.mjs';
const app = express();

app.use(express.json());
app.options('*', cors());
app.use(cors());
app.use('/api', platformRouter);
 
app.listen(9000, () => console.log('brockai api listening on port 9000!'));