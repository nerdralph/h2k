// (c) Ralph Doncaster 2022, 2023

// get postal code & weather station for given AAN JSON data from thedatazone.ca
function getLocationData(d) {
    const ae = aanq.elements;
    ae.aanData.value = JSON.stringify(d);
    const SA = d.address_num + " " + d.address_street;
    const WKID4326 = d.x_coord + "," + d.y_coord;
    console.log(aanq);

    var q = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?&f=json&SingleLine=" + SA + "&location=" + WKID4326 + "&maxLocations=1";
    console.log(q);
    fetch(q)
        .then(response => response.json())
        .then(data => {
            console.log(JSON.stringify(data));
            // address = street, town, prov, postal
            [ae.street.value, ae.city.value, , ae.postal.value] = 
                data.candidates[0].address.split(", ");
            });

    q =  "https://maps-cartes.services.geo.ca/server_serveur/rest/services/NRCan/Carte_climatique_HOT2000_Climate_Map_EN/MapServer/1/query?geometry=" + WKID4326 + "&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelWithin&f=json";
    console.log(q);
    fetch(q)
        .then(response => response.json())
        .then(data => ae.weather.value = data.features[0].attributes.Name); 
}

// get NS assessment account (AAN) data
function findAAN(aan) {
    fetch("https://www.thedatazone.ca/resource/a859-xvcs.json?aan=" + aan)
        .then(response => response.json())
        .then(data => getLocationData(data[0]));
}

