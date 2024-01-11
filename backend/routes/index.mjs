import express from 'express';

import { fileUpload } from '../controllers/fileupload.mjs';
const router = express.Router();

app.post('/upload', fileUpload);

export default router;