import { IncomingForm } from 'formidable';
import { createClient } from 'scp2';
import { loadEnv } from './config.mjs';
import { v4 as uuidv4 } from 'uuid';

loadEnv();

const fileupload = async(req, res) => {

  const form = new formidable.IncomingForm();

  form.parse(req, async (err, fields, files) => {
    if (err) {
      return res.status(500).json({ error: 'Error parsing form data' });
    }

    const file = files.file;

    if (!file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const { path: filePath, name: fileName } = file;

    try {
      const scpConfig = {
        host: process.env.DIGITAL_OCEAN_HOST,
        username: process.env.DIGITAL_OCEAN_USER,
        privateKey: process.env.DIGITAL_OCEAN_ACCESS_TOKEN,
        passphrase: '',
        path: process.env.DIGITAL_OCEAN_BLOB_PATH,
      };

      const client = new createClient(scpConfig);

      blobId = uuidv4();

      await client.upload(filePath, scpConfig.path+'/'+blobId+'/'+fileName);

      res.json({ message: 'File uploaded and transferred via SCP' });
    } catch (error) {
      console.error('Error transferring file:', error);
      res.status(500).json({ error: 'Error transferring file via SCP' });
    }
  });
}

export default fileupload;
