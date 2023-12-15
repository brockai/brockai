const express = require('express') 
// const VerifyToken = require('../../helper');

const { embeddings } = require('../controllers/index')
const router = express.Router()
 
router.get('/embeddings', embeddings);

module.exports = router;