import express from 'express';
import { loadEnv } from '../config.mjs';
import multer  from 'multer';
import AWS from 'aws-sdk';
import { v4 as uuidv4 } from 'uuid';

const router = express.Router();
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

loadEnv();

let space = new AWS.S3({
  endpoint: "nyc3.digitaloceanspaces.com",
  useAccelerateEndpoint: false,
  //Create a credential using DO Spaces API key (https://cloud.digitalocean.com/account/api/tokens)
  credentials: new AWS.Credentials(process.env.accessKeyId, process.env.secretAccessKey, null)
});

const BucketName = "brockai";

router.post('/upload', function (file0, response, next) {
  console.log(file0)
  // upload(file0, response, function (error) {
  //   if (error) {
  //     console.log(error);
  //     return response.redirect("/error");
  //   }
  //   console.log('File uploaded successfully.');
  //   response.redirect("/success");
  // });
});


router.get('/:fileName', function (req, res, next) {
  let downloadParameters = {
    Bucket: BucketName,
    Key: req.params.fileName
  };

  space.getObject(downloadParameters, function(error, data) {
    if (error){
      console.error(error);
      res.sendStatus(500);
      return;
    }
    res.contentType(data.ContentType);
    res.end(data.Body, 'binary');
  });
});

export default router;

// const spacesEndpoint = new aws.Endpoint('nyc3.digitaloceanspaces.com');

// 

// router.post('/upload', (req, res) => {
//   console.log(req.files)
//   upload(req, res, (err) => {
//     console.log(req)
//     if (err) {
//       console.error(err);
//       return res.status(500).json({ error: 'Error uploading file' });
//     }
//     console.log('no err');
//     res.json({ message: 'File uploaded successfully' });
//   });
// });



// const s3 = new aws.S3({
//   endpoint: process.env.endpoint,
//   accessKeyId: process.env.accessKeyId,
//   secretAccessKey: process.env.secretAccessKey,
// });


// const s3 = new aws.S3({
//   endpoint: spacesEndpoint
// });

// Change bucket property to your Space name
// const upload = multer({
//   storage: multerS3({
//     s3: s3,
//     bucket: process.env.spacesEndpoint,
//     acl: 'public-read',
//     key: function (request, file, cb) {
//       console.log(file);
//       cb(null, file.originalname);
//     }
//   })
// }).array('upload', 1);

// router.post('/upload', async (req, res) => {
//   try {
//     await upload.single('file')(req, res);
//     res.json({ message: 'File uploaded successfully' });
//   } catch (error) {
//     console.error(error);
//     res.status(500).json({ error: 'Error uploading file' });
//   }
// });

// router.post('/upload', upload.single('files', 5), async (req, res) => {
//     try {
//       const uploadedFiles = req.files;
//   console.log(uploadedFiles)
//   //     for (const file of uploadedFiles) {
//   //       const fileName = Date.now().toString() + '-' + file.originalname;
//   //       await spaces.putObject({
//   //         Bucket: process.env.spaceName, 
//   //         Key: fileName,
//   //         Body: file.buffer,
//   //       });
//   //     }
  
//       res.json({ message: 'Files uploaded successfully!' });
//     } catch (error) {
//       console.error('Error uploading files:', error);
//       res.status(500).json({ error: 'Internal server error' });
//     }
//   });

// const storage = multerS3({
//   s3: s3,
//   bucket: process.env.spacesEndpoint,
//   acl: 'private',
//   key: function (req, file, cb) {
//     cb(null, Date.now().toString() + '-' + file.originalname);
//   },
// });

// const upload = multer({
//   storage: storage,
// }).single('file');