const prompts = require('prompts');
prompts.override(require('yargs').argv);
const { spawn } = require('child_process');

const fs = require('fs');

const scriptPath = './scripts/select-it.sh';

async function selectMp3() {
  try {
    const mp3Files = fs.readdirSync('/mnt/c/Users/dmitr/Music/it', { withFileTypes: true })
      .filter(dirent => dirent.isFile() && dirent.name.endsWith('.mp3'))
      .map(dirent => dirent.name.replace('.mp3', '')); 

    const choices = mp3Files.map((file, index) => ({ title: file, value: `0${index + 1}` }));

    const response = await prompts({
      type: 'select',
      name: 'selectedFile',
      message: 'Select an MP3 file:',
      choices: choices,
    });

    console.log(`Selected: ${response.selectedFile}`);
    
    // Execute the bash script with the selected file number as an argument
    const child = spawn(scriptPath, [response.selectedFile]);

    child.stdout.on('data', (data) => {
      console.log(`Output from bash script: ${data.toString()}`);
    });

    child.stderr.on('data', (data) => {
      console.error(`Error from bash script: ${data.toString()}`);
    });

    child.on('close', (code) => {
      console.log(`Bash script exited with code: ${code}`);
    });

  } catch (err) {
    console.error("Error reading directory:", err);
  }
}

selectMp3();