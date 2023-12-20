const express = require('express') 
// const VerifyToken = require('../../helper');

const { embeddings, bearerToken } = require('../controllers/index')
const router = express.Router()
 
router.get('/embeddings', embeddings);
router.get('/token', bearerToken)

module.exports = router;