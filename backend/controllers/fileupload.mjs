import { createClient } from 'scp2';
import { loadEnv } from './config.mjs';
import multer from 'multer';
import { Spaces } from 'spaces-sdk';
import { v4 as uuidv4 } from 'uuid';

loadEnv();

const spaces = new Spaces({
  endpoint: process.env.endpoint,
  accessKeyId: process.env.accessKeyId,
  secretAccessKey: process.env.secretAccessKey,
  space: process.env.spaceName,
});



const fileupload = async(req, res) => {

  
}

export default fileupload;
