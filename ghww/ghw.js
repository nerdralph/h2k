// (c) Ralph Doncaster 2022

const TAXREGISTRY = {
    "NS": "https://www.thedatazone.ca/resource/a859-xvcs.json?aan=", 
    "YYC": "https://data.calgary.ca/resource/simh-5fhj.json?roll_number="
}

// fetch JSON query & perform action on response data
function fetchJd(query, action) {
    console.log(query);
    fetch(query)
        .then(response => response.json())
        .then(data => {console.log(JSON.stringify(data)); action(data);});
}

function setPostal(address) {
    q = "https://ws1.postescanada-canadapost.ca/Capture/Interactive/Find/v1.00/json3ex.ws?Key=AX81-HA65-HM33-RA59&Text=" + address + "&Countries=CAN"; 
    fetchJd(q, d => aanq.elements._Postal.value = d.Items[0].Text.slice(-7));
}

function getCookie(name) {
    return document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`))?.at(2);
}

function nsAAN(d) {
    // data collection form elements
    const fe = aanq.elements;
    fe._YearBuilt.value = d.year_built || "1923";
    fe._Street.value = d.address_num + " " + d.address_street + " " + d.address_suffix;
    fe._City.value = d.address_city;
    fe._Province.value = "NOVA SCOTIA";
    setWeather(d.x_coord + "," + d.y_coord);
    setPostal(fe._Street.value + d.address_city + "NS");
}

function yycRoll(d) {
    // data collection form elements
    const fe = aanq.elements;
    fe._YearBuilt.value = d.year_of_construction;
    fe._Street.value = d.address;
    fe._Province.value = "ALBERTA";
    setWeather(d.longitude + "," + d.latitude);
}

const ROLLFN = {
    "NS": nsAAN,
    "YYC": yycRoll
}

// set weather station
// WKID4326 = gps longitude, gps latitude
function setWeather(WKID4326) {
    // data collection form elements
    const fe = aanq.elements;

//    var q = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?&f=json&SingleLine=" + address + "&location=" + WKID4326 + "&maxLocations=1";
//    fetchJd(q, d => [fe._Street.value, fe._City.value, fe._Province.value , fe._Postal.value]
//                     = d.candidates[0].address.split(", "));

    q =  "https://maps-cartes.services.geo.ca/server_serveur/rest/services/NRCan/Carte_climatique_HOT2000_Climate_Map_EN/MapServer/1/query?geometry=" + WKID4326 + "&geometryType=esriGeometryPoint&inSR=4326&f=json";
    fetchJd(q, d => fe.weather.value = d.features[0].attributes.Name);
}

// get property data for roll number
function findAAN(aan) {
    const region = location.hash.slice(1) || "NS";
    fetchJd(TAXREGISTRY[region] + aan, d => ROLLFN[region](d[0]));
}

function setFID(fid) {
    document.cookie = `_FileID=${fid};SameSite=Strict`;
    document.title = fid;
}

// increment FileID
function nextFile() {
    var fid = getCookie("_FileID");
    if (!fid) return "";
    // last 5 digits is house indicator: ERS Tech Procedures 2.9
    fid = fid.substr(0,5) + `${+fid.substr(5) + 1}`.padStart(5, "0"); 
    return fid;
}

// global form init
// window.onload = () => aanq.elements._FileID.value = location.search.slice(1);
window.onload = () => aanq.elements._FileID.value = nextFile();

