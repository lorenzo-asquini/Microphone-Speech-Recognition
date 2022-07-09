# Microphone-Speech-Recognition
> Use Google Speech-to-Text to recognise audio from your microphone, saving the result in a .txt file and the original audio in a .wav file

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [License](#license)


## General Information
This projects allows you to freely transform the audio captured by your microphone into text.\
It uses Google Speech-to-Text to have a high quality speech recognition.\
The original audio can be saved directly to a .wav file and the output text is easily saved to a .txt file


## Technologies Used
- Javascript - version ES9
- Html - version 5
- Css - version 2.1
- Python - version 3.8.7


## Features
- Recognise the speech captured by your microphone and save the result into a .txt file
- Optionally save the audio you are recognising into a .wav file
- Recognise any language supported by Google Speech-to-Text technology
- It's free!


## Setup
- [Google Chrome](https://www.google.com/chrome) must be installed on your machine
- The following python libraries are needed for the program to fully function: 
  ```
  selenium
  webdriver-manager
  os
  shutil
  time
  pyaudio
  wave
  atexit
  ```
- Add any language you want using IETF BCP 47 language tags in [micRecognition.html](micRecognition/micRecognition.html):
  ```html
  <select name="language" id="language">
      <option value="it-IT">Italian</option>
      <option value="en-US">English</option>
      <option value="es-ES">Spanish</option>
  </select>
  ```
- An internet connection is required


## Usage
- Run the [python script](micRecognition.py)
- A Chrome page will open. Insert the output filename, select the language and decide if you want to record the audio of what you are recognising
- Click 'Confirm' and then 'Start'. Press 'Stop' to pause the recognition whenever you want, 'Start' again to resume
- Use the button 'FAST QUIT' on the right to exit quickly. Closing the web page will result in a long closing time


## Project Status
The project is complete


## License
The source code for the site is licensed under the [MIT license](LICENSE)
