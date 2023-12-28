import express from 'express';
// const VerifyToken = require('../../helper');

// import { embeddings, bearerToken } from '../controllers/opensearch.mjs';
const router = express.Router()
 
router.get('/', (req, res) => {
  // Logic to handle GET request for products
  res.send('Get all products');
});

// router.get('/embeddings', embeddings);
// router.get('/token', bearerToken)

export default router;