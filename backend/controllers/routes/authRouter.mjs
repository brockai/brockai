import express from 'express';
import { addUserToKeycloak, loginToKeycloak } from '../controllers/authController.mjs';
import dotenv from 'dotenv';
dotenv.config();

const router = express.Router();

router.post('/login', (req, res) => {
  loginToKeycloak(req, res);
});

router.post('/signup',  (req, res) => {
  addUserToKeycloak(req, res);
});

export default router;