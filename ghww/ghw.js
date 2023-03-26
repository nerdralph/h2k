// (c) Ralph Doncaster 2022

const TAXREGISTRY = {
    "NS": "https://www.thedatazone.ca/resource/a859-xvcs.json?aan=", 
    "YYC": "https://data.calgary.ca/resource/simh-5fhj.json?roll_number="
}

function nsAAN(d) {
    aanq.elements._YearBuilt.value = d.year_built;
    getHouseData( d.address_num + " " + d.address_street, d.x_coord + "," + d.y_coord);
}

function yycRoll(d) {
    aanq.elements._YearBuilt.value = d.year_of_construction;
    getHouseData(d.address, d.longitude + "," + d.latitude);
}

const ROLLFN = {
    "NS": nsAAN,
    "YYC": yycRoll
}

// fetch JSON query & perform action on response data
function fetchJd(query, action) {
    console.log(query);
    fetch(query)
        .then(response => response.json())
        .then(data => {console.log(JSON.stringify(data)); action(data);});
}

// get address, postal code & weather station
// address = house number & street
// WKID4326 = gps longitude, gps latitude
function getHouseData(address, WKID4326) {
    const fe = aanq.elements;

    var q = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?&f=json&SingleLine=" + address + "&location=" + WKID4326 + "&maxLocations=1";
    fetchJd(q, d => [fe._Street.value, fe._City.value, fe._Province.value , fe._Postal.value]
                     = d.candidates[0].address.split(", "));

    q =  "https://maps-cartes.services.geo.ca/server_serveur/rest/services/NRCan/Carte_climatique_HOT2000_Climate_Map_EN/MapServer/1/query?geometry=" + WKID4326 + "&geometryType=esriGeometryPoint&inSR=4326&f=json";
    fetchJd(q, d => fe.weather.value = d.features[0].attributes.Name);
}

// get property data for roll number
function findAAN(aan) {
    const region = location.hash.substr(1);
    fetchJd(TAXREGISTRY[region] + aan, d => ROLLFN[region](d[0]));
}

// global form init
window.onload = () => aanq.elements._FileID.value = location.search.slice(1);

