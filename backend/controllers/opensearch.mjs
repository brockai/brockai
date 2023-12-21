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

export default embeddings;
