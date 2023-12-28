// import Keycloak from 'keycloak-js';

// const keycloakUrl = process.env.REACT_APP_KEYCLOAK_URL;
// const realm = process.env.REACT_APP_KEYCLOAK_REALM;
// const clientId = process.env.REACT_APP_KEYCLOAK_CLIENT_ID;

// const keycloakConfig = {
//   url: `${keycloakUrl}/auth`,
//   realm: `${realm}brockai`,
//   clientId: `${clientId}`,
// };

// const keycloak = new Keycloak(keycloakConfig);

// export const login = (username:, password:string) => {
//   return new Promise((resolve, reject) => {
//     keycloak
//       .init({ onLoad: 'login-required' })
//       .then((authenticated) => {
//         if (authenticated) {
//           keycloak
//             .login({ username:username, password:password })
//             .then(() => {
//               resolve(keycloak);
//             })
//             .catch(() => {
//               reject('Failed to authenticate');
//             });
//         } else {
//           reject('Authentication failed');
//         }
//       })
//       .catch(() => {
//         reject('Failed to initialize Keycloak');
//       });
//   });
// };

// export const logout = () => {
//   keycloak.logout();
// };

// export default keycloak;






// import Keycloak, { KeycloakInitOptions, KeycloakInstance }  from 'keycloak-js';

// class KeycloakService {
  
//   private keycloak: KeycloakInstance | null = null;

//   init = async (): Promise<void> => {
//     const keycloakUrl = process.env.REACT_APP_KEYCLOAK_URL;
//     const realm = process.env.REACT_APP_KEYCLOAK_REALM;
//     const clientId = process.env.REACT_APP_KEYCLOAK_CLIENT_ID;

//     const initOptions: KeycloakInitOptions = {
//       url: `${keycloakUrl}/auth`,
//       realm: `${realm}brockai`,
//       clientId: `${clientId}`,
//       onLoad: 'check-sso',
//     };

//     // this.keycloak = Keycloak(initOptions);

//     await this.keycloak.init(initOptions);
//   };

//   private initKeycloak() {
    

//     this.keycloak = new Keycloak({
      
//     });
//   }

//   login = async (username: string, password: string): Promise<void> => {
//     if (!this.keycloak) {
//       throw new Error('Keycloak is not initialized');
//     }

//     try {
//       await this.keycloak.login({
//         username,
//         password,
//       });
//     } catch (error) {
//       console.error('Login failed:', error);
//     }
//   };

//   public logout() {
//     if (this.keycloak) {
//       this.keycloak.logout();
//     }
//   }
// }

// export default new KeycloakService();
