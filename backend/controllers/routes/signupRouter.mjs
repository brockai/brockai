import express from 'express';
import createClient from 'keycloak-admin';

import dotenv from 'dotenv';
dotenv.config();

const router = express.Router();

const keycloakAdmin = createClient
// const keycloakAdmin = createClient({
//   baseUrl: process.env.KEYCLOAK_URL+'/admin',
//   realmName: process.env.KEYCLOAK_REALM || 'brockai',
// });


async function createKeycloakUser(username, email, password) {
  try {
    await keycloakAdmin.auth({
      username: process.env.KEYCLOAK_ADMIN_USERNAME,
      password: process.env.KEYCLOAK_ADMIN_PASSWORD,
      grantType: 'password',
      clientId: process.env.KEYCLOAK_CLIENT_ID,
    });

    const user = await keycloakAdmin.users.create({
      realm: keycloakConfig.realmName,
      username: username,
      email: email,
      enabled: true,
      credentials: [
        {
          type: 'password',
          value: password,
        },
      ],
    });

    return user;
  } catch (error) {
    console.error('Error creating Keycloak user:', error);
    throw error;
  }
}

router.post('/', async (req, res) => {
  const { username, email, password } = req.body;

  try {
    const newUser = await createKeycloakUser(username, email, password);
    res.status(201).json(newUser);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create user' });
  }
});

export default router;


