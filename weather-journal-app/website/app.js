/* Global Variables */
const weatherServiceBaseUrl = 'https://api.openweathermap.org/data/2.5/weather?';
const zipPrefix = 'zip=';
const appIdPrefix = '&appid=';
const unitsArgument = '&units=metric';
const weatherAPIey = '36ca0427c9bc597e1c0a2a3a8e9798e7';

//add listener to Generate button
document.getElementById('generate').addEventListener('click', showTargetWeather);
/*
 * Interact with Weather webAPI, then save the latst retrieved data from user and API Call
 * At last Update the GUI accordingly
 */
function showTargetWeather(e) {
    // Create a new date instance dynamically with JS
    let d = new Date();
    let newDate = (d.getMonth() + 1) + '.' + d.getDate() + '.' + d.getFullYear();
    const zipCode = document.getElementById('zip').value;
    const userResponse = document.getElementById('feelings').value;

    getCurrentWeather(weatherServiceBaseUrl + zipPrefix + zipCode + unitsArgument + appIdPrefix + weatherAPIey)
        .then(function (data) {
            console.log('1st fn data:' + data)
            postWeatherReport('/setWeatherReport', { temperature: data.main.temp, date: newDate, userResponse: userResponse });
        })
        .then(function () {
            
            updateUI();
        });
}
//Element Variables


/* get the last saved data from the server*/
const getCurrentWeather = async (url = '') => {
    console.log('weatherRequest:' + url);
    const weatherResponse = await fetch(url);

    try {
        const weatherData = weatherResponse.json();
        console.log(weatherData);
        return weatherData;
    } catch (error) {
        //Basic error handling through printing it to the console
        console.log("error", error);
    }
}

/* save the retrieved data into projectData*/
const postWeatherReport = async (url = '', data = {}) => {
    console.log("data recieved for posting:" + JSON.stringify(data));
    const response = await fetch(url, {
        method: 'POST', 
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),       
    });

    try {
        const newData = await response.json();
        console.log(newData);
        return newData;
    } catch (error) {
        //Basic error handling through printing it to the console
        console.log("error", error);
    }
};

/* update the GUI with the new data retrieved from the Wep API and */
const updateUI = async () => {
    const request = await fetch('/getWeatherReport');
    try {
        const allData = await request.json();
        console.log(allData);
        document.getElementById('date').innerHTML = '⌛️'+allData.date;
        document.getElementById('temp').innerHTML = '🌡'+allData.temperature+"";
        document.getElementById('content').innerHTML = '👱🏽‍♂️'+allData.userResponse;
    } catch (error) {
        //Basic error handling through printing it to the console
        console.log("error", error);
    }
}



