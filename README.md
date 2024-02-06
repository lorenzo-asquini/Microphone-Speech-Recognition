# Microphone-Speech-Recognition
> Use Google's Speech-to-Text to recognize audio from your microphone, saving the result in a `.txt` file and the original audio in a `.wav` file.

## Table of Contents
* [General Info](#general-information)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [License](#license)


## General Information
This project allows you to freely transform the audio captured by your microphone into text. It makes use of Google's Speech-to-Text to have high-quality speech recognition. The original audio can be saved directly to a `.wav` file, and the output text is easily saved to a `.txt` file.


## Features
- Recognise the speech captured by your microphone and save the result into a `.txt` file.
- Optionally save the audio you are recognizing into a `.wav` file.
- Recognise any language supported by Google's Speech-to-Text technology.
- It's free!


## Setup
- [Google Chrome](https://www.google.com/chrome) must be installed on your machine.
- Install the required libraries specified in [requirements.txt](requirements.txt). Python version 3.7.9 was used.
- Add any language you want using IETF BCP 47 language tags in [micRecognition.html](micRecognition/micRecognition.html):
  ```html
  <select name="language" id="language">
      <option value="it-IT">Italian</option>
      <option value="en-US">English</option>
      <option value="es-ES">Spanish</option>
  </select>
  ```
- An internet connection is required.


## Usage
- Run the [main python script](micRecognition.py).
- A Chrome page will open. Insert the output filename, select the language, and decide if you want to record the audio of what you are recognizing.
- Click 'Confirm' and then 'Start'. Press 'Stop' to pause the recognition whenever you want, and 'Start' again to resume.
- Use the button 'FAST QUIT' on the right to exit quickly. Closing directly the web page will result in a longer closing times.


## License
The source code for the site is licensed under the [MIT license](LICENSE).
