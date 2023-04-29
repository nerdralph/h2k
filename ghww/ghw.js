// (c) Ralph Doncaster 2022

const TAXREGISTRY = {
    "NS": "https://www.thedatazone.ca/resource/a859-xvcs.json?aan=", 
    "YYC": "https://data.calgary.ca/resource/simh-5fhj.json?roll_number="
}

function getCookie(name) {
    return document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`))?.at(2);
}

function nsAAN(d) {
    aanq.elements._YearBuilt.value = d.year_built || "1923";
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

