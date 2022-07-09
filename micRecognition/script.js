//Import APIs
var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition   //Controller of the recognition
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent  //Necessary to get the result from the recognition

var recognitionDefined = false;  //status variables
var recognitionStarted = false;
var recognitionEnded = false;

var previousPartsResult = "";  //The API allows only 5 minutes of continuous recognition. Previous recognised segments are stored here
var resetFunctionID;

var wakeLockObj = null;  //Do not make the pc sleep during recognition (allow doing manually)

var outputFileName = ""  //placeholders
var recordAudio = false;

var numberOfRecognitions = 0;  //necessary to check if there is a new recognition
var confirmationClick = 1;  //Necessary to avoid using alert to warn for a new recognition (problems with selenium)

var recognition = new SpeechRecognition();  //Language is set below
recognition.continuous = true;  //Continue to listen also with a pause
recognition.interimResults = true;  //Return also partial result to save in temp file
recognition.maxAlternatives = 1;  //Return only an alternative

var fastQuitRequest = false;  //Communicate to the python script to exit

function showCommands(){

    outputFileName = document.getElementById("outputFileName").value;  //filename where to save the recognition

    if(outputFileName == ""){  //check if the inserted name is empty
        document.getElementById("errorDefinition").innerHTML = "Error. Invalid name";
        return;
    }

    recordAudio = document.getElementById("recordingCheck").checked;

    confirmationClick++;

    if(recognitionDefined){  //ask if the user wants to start a new recognition
        if(confirmationClick < 2){
            document.getElementById("errorDefinition").innerHTML = 'You already defined a recognition. Do you want to define another? (Results from the previous one will be saved at the current state). Click again to confirm';
            return;
        }else{
            if(recognitionStarted){  //Stop the last recognition when confirming a new recognition
                stopRecognition();
            }
            document.getElementById("results").innerHTML = "";  //No danger of overwiting with nothing because at this point recognitionStarted will be always false (no action in the python script)
        }
    }else{
        recognitionDefined = true;  //First time confirming
    }

    document.getElementById("errorDefinition").innerHTML = "";  //No errors. Remove error message

    if(recordAudio){
        document.getElementById("isRecording").innerHTML = "Recording is ON"
    }else{
        document.getElementById("isRecording").innerHTML = "Recording is OFF"
    }

    confirmationClick = 0;

    recognition.lang = document.getElementById("language").value;  //BCP 47 Language Codes.

    displayRecognitionCommands();  //in helper.js
}

function fastQuit(){
    fastQuitRequest = true;
    if(recognitionStarted){
        stopRecognition();
    }
}

function startRecognition(){
    recognitionStarted = true;
    recognitionEnded = false;

    numberOfRecognitions++;  //A new file will be created by the python script
    previousPartsResult = "";

    try {
        activateWakeLock();  //If low on battery does not work
    }catch(err){
        console.error("Low battery");
    }

    recognition.start();  //Start recognition

    resetFunctionID = setInterval(resetRecognition, 4*60*1000);  //Reset the recognition every 4 minutes to be safe

    document.getElementById("startBtn").disabled = true;
    document.getElementById("stopBtn").disabled = false;
}

function stopRecognition(){
    recognitionStarted = false;
    recognitionEnded = true;

    clearInterval(resetFunctionID);

    wakeLockObj.release();//Free the screen from beeing awake
    wakeLockObj = null;

    recognition.stop();  //Stop recognition

    document.getElementById("startBtn").disabled = false;
    document.getElementById("stopBtn").disabled = true;
}

recognition.onresult = function(event) {  //The event returns a SpeechRecognitionResultList with SpeechRecognitionResult objects
  // The first [0] returns the SpeechRecognitionResult the first result picked. Every time there is a pause, it creates a new object in the list
  // The second [0] returns the SpeechRecognitionAlternative at position 0 (leave at 0 because alternatives are 1)

  var resultsStr = "";
  for(var i = 0; i < event.results.length; i++){  //It returns a different result for every pause
      resultsStr += event.results[i][0].transcript;
  }
  document.getElementById("results").innerHTML = previousPartsResult+" "+resultsStr;
}

//onnomatch and onerror removed because not important

function resetRecognition(){  //Add the current segment result and reset recognition
    recognition.stop();
}
recognition.onend = function(event){  //Linked to the recognition reset. Waits the ending of the recognition to restart
    if(recognitionStarted){
        previousPartsResult = document.getElementById("results").innerHTML;
        recognition.start();
    }
}

async function activateWakeLock() {
    wakeLockObj = await navigator.wakeLock.request('screen');
}
