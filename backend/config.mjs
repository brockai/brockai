// config.mjs
import { readFileSync } from 'fs';

export const loadEnv = () => {
  const env = readFileSync('.env', 'utf8')
    .toString()
    .split('\n')
    .filter(Boolean)
    .forEach((line) => {
      const [key, value] = line.split('=');
      process.env[key.trim()] = value.trim();
    });
};
