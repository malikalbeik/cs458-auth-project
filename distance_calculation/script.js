var storedLatitude = localStorage.getItem("latitude");
var storedLongitude = localStorage.getItem("longitude");

function getLocation() {
    if (storedLatitude && storedLongitude) {
        // If location is already stored, proceed to show sea distance page
        calculateSeaDistance(storedLatitude, storedLongitude);
        document.getElementById("seaDistancePage").style.display = "block";
        document.getElementById("sunDistancePage").style.display = "none";
        document.getElementById("nextBtn").style.display = "inline-block";
    } else {
        // Ask for permission to get location
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function (position) {
                    showPosition(position);
                    // Store the obtained location
                    localStorage.setItem("latitude", position.coords.latitude);
                    localStorage.setItem("longitude", position.coords.longitude);
                },
                showError
            );
        } else {
            document.getElementById("seaDistance").innerHTML =
                "Geolocation is not supported by this browser.";
        }
    }
}

function showPosition(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    calculateSeaDistance(latitude, longitude);
    document.getElementById("seaDistancePage").style.display = "block";
    document.getElementById("sunDistancePage").style.display = "none";
    document.getElementById("nextBtn").style.display = "inline-block";
}

function calculateSeaDistance(latitude, longitude) {
    var seaCoordinates = [
        { name: "Black Sea", latitude: 41.2, longitude: 29.1 },
        { name: "Marmara Sea", latitude: 40.8, longitude: 28.9 },
        { name: "Caspian Sea", latitude: 40.3, longitude: 50.3 },
        { name: "Mediterranean Sea", latitude: 35.0, longitude: 18.0 },
        { name: "Red Sea", latitude: 20.0, longitude: 38.0 },
        { name: "Adriatic Sea", latitude: 42.5, longitude: 17.5 },
        { name: "Aegean Sea", latitude: 37.5, longitude: 25.0 },
        { name: "Baltic Sea", latitude: 55.0, longitude: 20.0 },
        { name: "North Sea", latitude: 57.0, longitude: 3.0 },
        { name: "Arabian Sea", latitude: 10.0, longitude: 65.0 },
        { name: "Andaman Sea", latitude: 12.0, longitude: 97.0 },
        { name: "South China Sea", latitude: 12.0, longitude: 115.0 },
        { name: "East China Sea", latitude: 30.0, longitude: 123.0 },
        { name: "Philippine Sea", latitude: 15.0, longitude: 130.0 },
        { name: "Coral Sea", latitude: -18.0, longitude: 150.0 },
        { name: "Tasman Sea", latitude: -40.0, longitude: 160.0 },
        { name: "Bering Sea", latitude: 58.0, longitude: -175.0 },
    ];

    var minDistance = Number.MAX_VALUE;
    var nearestSea = "";

    seaCoordinates.forEach(function (sea) {
        var distance = calculateDistance(
            storedLatitude,
            storedLongitude,
            sea.latitude,
            sea.longitude
        );
        if (distance < minDistance) {
            minDistance = distance;
            nearestSea = sea.name;
        }
    });

    document.getElementById("seaDistance").innerHTML =
        "Distance to nearest sea (" +
        nearestSea +
        "): " +
        minDistance.toFixed(2) +
        " km";
}

function calculateDistance(lat1, lon1, lat2, lon2) {
    var R = 6371;
    var dLat = deg2rad(lat2 - lat1);
    var dLon = deg2rad(lon2 - lon1);
    var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) *
        Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = R * c;
    return d;
}

function deg2rad(deg) {
    return deg * (Math.PI / 180);
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            document.getElementById("seaDistance").innerHTML =
                "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            document.getElementById("seaDistance").innerHTML =
                "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            document.getElementById("seaDistance").innerHTML =
                "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            document.getElementById("seaDistance").innerHTML =
                "An unknown error occurred.";
            break;
    }
}

function calculateSunDistanceWithInput() {
    var latitude = parseFloat(document.getElementById("latitude").value);
    var longitude = parseFloat(document.getElementById("longitude").value);

    if (isNaN(latitude) || isNaN(longitude)) {
        alert("Please enter valid coordinates.");
        return;
    }

    var sunDistance = calculateDistanceToSun(latitude, longitude);
    document.getElementById("inputSunDistance").innerHTML =
        "Distance to Sun's core (Input Coordinates): " + sunDistance.toFixed(2) + " km";
}

function calculateDistanceToSun(latitude, longitude) {
    var AU = 149597870.7; // Astronomical Unit in kilometers
    var ecc = 0.0167086; // Eccentricity of Earth's orbit
    var d2r = Math.PI / 180; // Degrees to radians conversion

    // Current date
    var date = new Date();

    // Calculate number of days since perihelion (January 3, 2001)
    var jan3_2001 = new Date(2001, 0, 3);
    var days_since_perihelion = (date - jan3_2001) / (1000 * 60 * 60 * 24);

    // Mean anomaly
    var M = (357.5291 + 0.98560028 * days_since_perihelion) % 360;

    // Equation of center
    var C =
        1.9148 * Math.sin(M * d2r) +
        0.02 * Math.sin(2 * M * d2r) +
        0.0003 * Math.sin(3 * M * d2r);

    // Ecliptic longitude
    var lambda = (M + 102.9372 + C + 180) % 360;

    // Distance to the Sun (in AU)
    var r =
        (1.000001018 * (1 - ecc * ecc)) /
        (1 + ecc * Math.cos((lambda - 180) * d2r));

    // Convert AU to kilometers
    var distance = r * AU;

    var factor = (Math.abs(latitude) + Math.abs(longitude)) / 100000
    var locationFactor = factor + 1;
    distance *= locationFactor;

    return distance;
}

function getLocationForSunDistance() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            showSunDistancePosition,
            showError
        );
    } else {
        document.getElementById("inputSunDistance").innerHTML =
            "Geolocation is not supported by this browser.";
    }
}

function showSunDistancePosition(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    calculateSunDistanceWithCoords(latitude, longitude);
}

function calculateSunDistanceWithCoords(latitude, longitude) {
    var sunDistance = calculateDistanceToSun(latitude, longitude);
    document.getElementById("currentLocationSunDistance").innerHTML =
        "Distance to Sun's core (Current Location): " + sunDistance.toFixed(2) + " km";
}

function showSunDistancePage() {
    document.getElementById("seaDistancePage").style.display = "none";
    document.getElementById("sunDistancePage").style.display = "block";
}

setInterval(updateSunDistances, 1000);

function updateSunDistances() {
    var latitude = parseFloat(document.getElementById("latitude").value);
    var longitude = parseFloat(document.getElementById("longitude").value);

    if (!isNaN(latitude) && !isNaN(longitude) && (latitude >= -90) && (latitude <= 90) && (longitude >= -180) && (longitude <= 180)) {
        document.getElementById("error").innerHTML = " ";
        calculateSunDistanceWithInput();
    }
    else {
        document.getElementById("error").innerHTML = "Distance to Sun's core (Input Coordinates): Invalid Input";
        document.getElementById("inputSunDistance").innerHTML = " ";
    }


    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                showSunDistancePosition(position);
                calculateSunDistanceWithCoords(position.coords.latitude, position.coords.longitude);
            },
            showError
        );
    }
}
