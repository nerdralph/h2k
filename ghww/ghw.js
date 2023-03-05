// (c) Ralph Doncaster 2022

const TAXREGISTRY = {
    "NS": "https://www.thedatazone.ca/resource/a859-xvcs.json?aan=", 
    "YYC": "https://data.calgary.ca/resource/simh-5fhj.json?roll_number="
}

function nsAAN(d) {
    getHouseData( d.address_num + " " + d.address_street, d.x_coord + "," + d.y_coord);
}

function yycRoll(d) {
    getHouseData(d.address, d.longitude + "," + d.latitude);
}

const ROLLFN = {
    "NS": nsAAN,
    "YYC": yycRoll
}

// get postal code & weather station
// address = house number & street
// WKID4326 = gps longitude, gps latitude
function getHouseData(address, WKID4326) {
    const ae = aanq.elements;
    // ae.aanData.value = JSON.stringify(d);

    var q = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?&f=json&SingleLine=" + address + "&location=" + WKID4326 + "&maxLocations=1";
    console.log(q);
    fetch(q)
        .then(response => response.json())
        .then(data => {
            console.log(JSON.stringify(data));
            // argcis address = street, town, prov, postal
            [ae._Street.value, ae._City.value, ae._Province.value , ae._Postal.value] = 
                data.candidates[0].address.split(", ");
            });

    q =  "https://maps-cartes.services.geo.ca/server_serveur/rest/services/NRCan/Carte_climatique_HOT2000_Climate_Map_EN/MapServer/1/query?geometry=" + WKID4326 + "&geometryType=esriGeometryPoint&inSR=4326&f=json";
    console.log(q);
    fetch(q)
        .then(response => response.json())
        .then(data => ae.weather.value = data.features[0].attributes.Name); 
}

// get property data for roll number
function findAAN(aan) {
    const region = location.hash.substr(1);
    fetch(TAXREGISTRY[region] + aan)
        .then(response => response.json())
        .then(data => ROLLFN[region](data[0]));
    //    .then(data => getLocationData(data[0]));
}

