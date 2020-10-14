// Setup empty JS object to act as endpoint for all routes
projectData = {};

// Require Express to run server and routes
const express = require('express');
// Start up an instance of app
const app = express();
/* Middleware*/
const bodyParser = require('body-parser');
//Here we are configuring express to use body-parser as middle-ware.
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Cors for cross origin allowance
const cors = require('cors');
app.use(cors());
// Initialize the main project folder
app.use(express.static('website'));


// Setup Server
/*Set Target port*/
const port = 8000;
/* Boot up the server*/
const server = app.listen(port, listening);
function listening() {
    // console.log(server);
    console.log(`Running Server on localhost: ${port}`);
};

// set the server routes to handle data exchange requests (GET, and POST)
app.get('/getWeatherReport', getWeatherReport);

function getWeatherReport(request, response) {
    //console.log(request);
    console.log("Sending projectData in body:" + JSON.stringify(projectData));
    response.send(projectData);
}

app.post('/setWeatherReport', setWeatherReport);

function setWeatherReport(request, response) {
    //console.log("data before:" + JSON.stringify(data));
    //data.push(requset.body);
    //console.log("setWeatherReport:" + JSON.stringify(request.body));
    projectData.temperature = request.body.temperature;
    projectData.date = request.body.date;
    projectData.userResponse = request.body.userResponse;
    console.log("Current projectData after posting:" + JSON.stringify(projectData));
    //response.send('Posted Successfully');
}