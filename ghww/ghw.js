// (c) Ralph Doncaster 2022

"use strict";

// get first element by name
function gFEBN(name) {
    return document.getElementsByName(name)[0];
}

// get postal code & weather station for given AAN JSON data from thedatazone.ca
function getLocationData(d) {
    gFEBN("aanData").value = JSON.stringify(d);
    const SA = d["address_num"] + " " + d["address_street"] + " " + d["address_suffix"];
    gFEBN("street").value = SA;
    const WKID4326 = d["x_coord"] + "," + d["y_coord"];
    const f = new FormData(document.getElementById("aanq"));
    console.log(document.getElementById("aanq"));
    //for (const [key, val] of f) {
    //    console.log(key + ": " + val);
    //}

    var q = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?&f=json&SingleLine=" + SA + "&location=" + WKID4326 + "&maxLocations=1";
    console.log(q);
    fetch(q)
        .then(response => response.json())
        //.then(data => Id_addr.innerHTML += "<br>" + JSON.stringify(data));
        .then(data => {
            console.log(JSON.stringify(data));
            // postal code is after the 3rd comma in address
            gFEBN("postal").value = data["candidates"][0]["address"].split(",")[3].trim();
            });

    q =  "https://maps-cartes.services.geo.ca/server_serveur/rest/services/NRCan/Carte_climatique_HOT2000_Climate_Map_EN/MapServer/1/query?geometry=" + WKID4326 + "&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelWithin&f=json";
    console.log(q);
    fetch(q)
        .then(response => response.json())
        .then(data => gFEBN("weather").value = data["features"][0]["attributes"]["Name"]); 
}

// get NS assessment account (AAN) data
function findAAN(aan) {
    fetch("https://www.thedatazone.ca/resource/a859-xvcs.json?aan=" + aan)
        .then(response => response.json())
        .then(data => getLocationData(data[0]));
}

