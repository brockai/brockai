import express from 'express';
// import { KeycloakAdminClient } from 'keycloak-admin';
const KeycloakAdminClient = require('keycloak-admin');

import dotenv from 'dotenv';
dotenv.config();

// keycloak.grantManager.obtainDirectly(username, password)
// .then((grant) => {
//   res.json(grant);
// })
// .catch((err) => {
//   res.status(400).json({ error: err });
// });

// const keycloak = new Keycloak({}, {
//   clientId: process.env.KEYCLOAK_CLIENT_ID || 'platform',
//   bearerOnly: true,
//   serverUrl: process.env.KEYCLOAK_URL+'/auth' || 'localhost:8080',
//   realm: process.env.KEYCLOAK_REALM || 'brockai',
// });

const keycloak = new KeycloakAdminClient({
  baseUrl: process.env.KEYCLOAK_URL + '/auth' || 'localhost:8080/auth',
  realmName: process.env.KEYCLOAK_REALM || 'brockai',
});

const authenticateAdmin = async () => {
  isAuth = await keycloak.auth({
    username: 'admin',
    password: 'admin',
    grantType: 'password',
    clientId: 'platform',
  });
  return isAuth;
};

const findUserByEmail = (users) => {
  const foundUser = users.find(user => user.email === req.body.email);
  return foundUser; // Returns the user object or undefined if not found
};

export async function loginToKeycloak(req, res) {
  try {

    const isAuth = await authenticateAdmin();

    if (isAuth) {
      const users = await keycloak.users.find({
        realm: 'brockai',
      });

      const user = findUserByEmail(users);

      if (user) {
        console.log('User found', user);
        return res.status(200).json(user);
      }
      else {
        res.sendStatus(401).json('User does not exist please sign up');
      }
      
    }
    else {
      res.sendStatus(401).json('System not available');
    }

  } catch (error) {
    console.error('Error adding user:', error);
    res.sendStatus(500).json(error);

  } finally {
    keycloak.stop();
  }

};


export async function addUserToKeycloak(req, res) {
  try {

    const isAuth = await authenticateAdmin();

    if (isAuth) {
      const userToAdd = {
        username: 'new_user',
        enabled: true,
        email: 'new_user@example.com',
        credentials: [
          { type: 'password', value: 'user_password', temporary: false }
        ]
      };

      // Add the user to Keycloak
      await keycloak.users.create({
        realm: 'your-realm',
        ...userToAdd,
      });

      console.log('User added successfully');
    }
  } catch (error) {
    console.error('Error adding user:', error);
  } finally {
    // Close the Keycloak admin client connection
    keycloak.stop();
  }
};


// export default authControllers;
