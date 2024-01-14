import express from 'express';
import { loadEnv } from '../config.mjs';
import multer from 'multer';
import AWS from 'aws-sdk';
import { v4 as uuidv4 } from 'uuid';

loadEnv();

const spaces = new AWS.S3({
    endpoint: process.env.endpoint,
    accessKeyId: process.env.accessKeyId,
    secretAccessKey: process.env.secretAccessKey,
});

const router = express.Router();
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

router.post('/upload', upload.array('files', 5), async (req, res) => {
    try {
      const uploadedFiles = req.files;
  
      for (const file of uploadedFiles) {
        const fileName = Date.now().toString() + '-' + file.originalname;
        await spaces.putObject({
          Bucket: process.env.spaceNam, 
          Key: fileName,
          Body: file.buffer,
        });
      }
  
      res.json({ message: 'Files uploaded successfully!' });
    } catch (error) {
      console.error('Error uploading files:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

export default router;