import express from 'express';

import cors from 'cors';
import fileRouter from './routes/file.mjs';

const app = express();
app.options('*', cors());
app.use(cors());
app.use(express.json());

app.use('/api', fileRouter);
 
app.listen(9000, () => console.log('brockai api listening on port 9000!'));