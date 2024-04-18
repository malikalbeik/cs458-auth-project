// page.tsx
'use client'

import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'

export default function Home() {
  const { data: session } = useSession({
    required: true,
    onUnauthenticated() {
      redirect('/api/auth/signin?callbackUrl=/')
    }
  })

  // Raw HTML content from index.html
  const htmlContent = `
  <!DOCTYPE html>
  <html lang="en">
  
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Distance Calculator</title>
      <style>
          body {
              font-family: Arial, sans-serif;
              margin: 0;
              padding: 0;
              background-color: #f4f4f4;
          }
  
          .container {
              max-width: 800px;
              margin: 0 auto;
              padding: 20px;
          }
  
          input[type="text"],
          input[type="password"],
          input[type="number"] {
              width: 100%;
              padding: 10px;
              margin: 10px 0;
              border: 1px solid #ccc;
              border-radius: 5px;
              box-sizing: border-box;
          }
  
          button {
              padding: 10px 20px;
              background-color: #4CAF50;
              color: white;
              border: none;
              border-radius: 5px;
              cursor: pointer;
          }
  
          button:hover {
              background-color: #45a049;
          }
      </style>
  </head>
  
  <body>
      <div class="container">
          <div id="loginPage">
              <h2>Login</h2>
              <input type="text" id="username" placeholder="Username">
              <input type="password" id="password" placeholder="Password">
              <button onclick="authenticate()">Login</button>
          </div>
          <div id="seaDistancePage" style="display:none;">
              <h2>Sea Distance</h2>
              <p id="seaDistance">Getting your location...</p>
              <button onclick="getLocation()">Get Location</button>
              <button id="nextBtn" onclick="showSunDistancePage()" style="display:none;">Next</button>
          </div>
          <div id="sunDistancePage" style="display:none;">
              <h2>Sun Distance</h2>
              <button onclick="getLocationForSunDistance()">Use My Location</button>
              <p>Or enter coordinates:</p>
              <input type="number" id="latitude" placeholder="Latitude">
              <input type="number" id="longitude" placeholder="Longitude">
              <button onclick="calculateSunDistanceWithInput()">Calculate Distance</button>
              <p id="sunDistance"> </p>
          </div>
      </div>
  
      <script>
          function authenticate() {
              var username = document.getElementById('username').value;
              var password = document.getElementById('password').value;
              if (username === 'user' && password === 'password') {
                  document.getElementById('loginPage').style.display = 'none';
                  document.getElementById('seaDistancePage').style.display = 'block';
              } else {
                  alert('Invalid credentials');
              }
          }
  
          function getLocation() {
              if (navigator.geolocation) {
                  navigator.geolocation.getCurrentPosition(showPosition, showError);
              } else {
                  document.getElementById('seaDistance').innerHTML = "Geolocation is not supported by this browser.";
              }
          }
  
          function showPosition(position) {
              var latitude = position.coords.latitude;
              var longitude = position.coords.longitude;
              calculateSeaDistance(latitude, longitude);
              document.getElementById('seaDistancePage').style.display = 'block';
              document.getElementById('sunDistancePage').style.display = 'none';
              document.getElementById('nextBtn').style.display = 'inline-block';
          }
  
          function calculateSeaDistance(latitude, longitude) {
              var seaCoordinates = [
                  { name: 'Black Sea', latitude: 41.2, longitude: 29.1 },
                  { name: 'Marmara Sea', latitude: 40.8, longitude: 28.9 },
                  { name: 'Caspian Sea', latitude: 40.3, longitude: 50.3 },
                  { name: 'Mediterranean Sea', latitude: 35.0, longitude: 18.0 },
                  { name: 'Red Sea', latitude: 20.0, longitude: 38.0 },
                  { name: 'Adriatic Sea', latitude: 42.5, longitude: 17.5 },
                  { name: 'Aegean Sea', latitude: 37.5, longitude: 25.0 },
                  { name: 'Baltic Sea', latitude: 55.0, longitude: 20.0 },
                  { name: 'North Sea', latitude: 57.0, longitude: 3.0 },
                  { name: 'Arabian Sea', latitude: 10.0, longitude: 65.0 },
                  { name: 'Andaman Sea', latitude: 12.0, longitude: 97.0 },
                  { name: 'South China Sea', latitude: 12.0, longitude: 115.0 },
                  { name: 'East China Sea', latitude: 30.0, longitude: 123.0 },
                  { name: 'Philippine Sea', latitude: 15.0, longitude: 130.0 },
                  { name: 'Coral Sea', latitude: -18.0, longitude: 150.0 },
                  { name: 'Tasman Sea', latitude: -40.0, longitude: 160.0 },
                  { name: 'Bering Sea', latitude: 58.0, longitude: -175.0 },
              ];
  
              var minDistance = Number.MAX_VALUE;
              var nearestSea = '';
  
              seaCoordinates.forEach(function (sea) {
                  var distance = calculateDistance(latitude, longitude, sea.latitude, sea.longitude);
                  if (distance < minDistance) {
                      minDistance = distance;
                      nearestSea = sea.name;
                  }
              });
  
              document.getElementById('seaDistance').innerHTML = "Distance to nearest sea (" + nearestSea + "): " + minDistance.toFixed(2) + " km";
          }
  
          function calculateDistance(lat1, lon1, lat2, lon2) {
              var R = 6371;
              var dLat = deg2rad(lat2 - lat1);
              var dLon = deg2rad(lon2 - lon1);
              var a =
                  Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                  Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
                  Math.sin(dLon / 2) * Math.sin(dLon / 2)
                  ;
              var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
              var d = R * c;
              return d;
          }
  
          function deg2rad(deg) {
              return deg * (Math.PI / 180)
          }
  
          function showError(error) {
              switch (error.code) {
                  case error.PERMISSION_DENIED:
                      document.getElementById('seaDistance').innerHTML = "User denied the request for Geolocation.";
                      break;
                  case error.POSITION_UNAVAILABLE:
                      document.getElementById('seaDistance').innerHTML = "Location information is unavailable.";
                      break;
                  case error.TIMEOUT:
                      document.getElementById('seaDistance').innerHTML = "The request to get user location timed out.";
                      break;
                  case error.UNKNOWN_ERROR:
                      document.getElementById('seaDistance').innerHTML = "An unknown error occurred.";
                      break;
              }
          }
  
          function calculateSunDistanceWithInput() {
              var latitude = parseFloat(document.getElementById('latitude').value);
              var longitude = parseFloat(document.getElementById('longitude').value);
  
              if (isNaN(latitude) || isNaN(longitude)) {
                  alert("Please enter valid coordinates.");
                  return;
              }
  
              var sunDistance = calculateDistanceToSun(latitude, longitude);
              document.getElementById('sunDistance').innerHTML = "Distance to Sun's core: " + sunDistance.toFixed(2) + " km";
          }
  
          function calculateDistanceToSun(latitude, longitude) {
              var AU = 149597870.7; // Astronomical Unit in kilometers
              var ecc = 0.0167086; // Eccentricity of Earth's orbit
              var obl_ecl = 23.4397; // Obliquity of the ecliptic in degrees
              var d2r = Math.PI / 180; // Degrees to radians conversion
  
              // Current date
              var date = new Date();
  
              // Calculate number of days since perihelion (January 3, 2001)
              var jan3_2001 = new Date(2001, 0, 3);
              var days_since_perihelion = (date - jan3_2001) / (1000 * 60 * 60 * 24);
  
              // Mean anomaly
              var M = (357.5291 + 0.98560028 * days_since_perihelion) % 360;
  
              // Equation of center
              var C = (1.9148 * Math.sin(M * d2r)) + (0.0200 * Math.sin(2 * M * d2r)) + (0.0003 * Math.sin(3 * M * d2r));
  
              // Ecliptic longitude
              var lambda = (M + 102.9372 + C + 180) % 360;
  
              // Distance to the Sun (in AU)
              var r = (1.000001018 * (1 - ecc * ecc)) / (1 + ecc * Math.cos((lambda - 180) * d2r));
  
              // Convert AU to kilometers
              var distance = r * AU;
  
              return distance;
          }
  
          function getLocationForSunDistance() {
              if (navigator.geolocation) {
                  navigator.geolocation.getCurrentPosition(showSunDistancePosition, showError);
              } else {
                  document.getElementById('sunDistance').innerHTML = "Geolocation is not supported by this browser.";
              }
          }
  
          function showSunDistancePosition(position) {
              var latitude = position.coords.latitude;
              var longitude = position.coords.longitude;
              calculateSunDistanceWithCoords(latitude, longitude);
          }
  
          function calculateSunDistanceWithCoords(latitude, longitude) {
              var sunDistance = calculateDistanceToSun(latitude, longitude);
              document.getElementById('sunDistance').innerHTML = "Distance to Sun's core: " + sunDistance.toFixed(2) + " km";
          }
  
          function showSunDistancePage() {
              document.getElementById('seaDistancePage').style.display = 'none';
              document.getElementById('sunDistancePage').style.display = 'block';
          }
      </script>
  </body>
  
  </html>
  `;

  if (session?.user) {
    return (
      <main>
        {/* Render the raw HTML content */}
        <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      </main>
    );
  }
}

