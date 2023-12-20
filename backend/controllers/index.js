const { exec } = require('child_process');
const jwt = require('jsonwebtoken')
require('dotenv').config();

const BEARER_TOKEN_SECRET = process.env.BEARER_TOKEN_SECRET

const bearerToken = async(req, res) => {
  try {
    let token = jwt.sign({ id: .369 }, BEARER_TOKEN_SECRET, {expiresIn: 3600})
    res.status(200).json({ data: token })
  } catch(e) {
    res.sendStatus(500)
  }
}

const embeddings = async(req, res) => {
  try{
    const pythonProcess = exec('python services/create_embeddings.py', (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error}`);
        return;
      }
      console.log(`Python script output: ${stdout}`);
      if (stderr) {
        console.error(`Python script error: ${stderr}`);
      }
    });
    
    pythonProcess.stdin.write('input to python script'); // Send input to Python script if needed
    pythonProcess.stdin.end(); // Close stdin for the process
    
    res.status(200).json({"message": "embeddings are complete"});
  }catch(e){
    console.log(e.message);
    res.sendStatus(500);
  }
}

module.exports = {
  embeddings, bearerToken
};
