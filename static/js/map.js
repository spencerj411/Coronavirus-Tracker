const minZoom = 3;

// initialize Leaflet
var map = L.map('map').setView({lon: 0, lat: 40}, minZoom);

// grab map tiles from mapbox and add to map
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + SECRET_KEY, {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    minZoom: minZoom,
    maxZoom: 15, 
    id: 'mapbox/light-v10', // 'spencerj411/ck778nrf5159n1it2rzendcfn'
    tileSize: 512,
    zoomOffset: -1,
    accessToken: SECRET_KEY
}).addTo(map);

// show the scale bar on the lower left corner
L.control.scale().addTo(map);

// values for cirlceMarker setting
const circleColour = '#f03';
const defaultBorderWeight = 2;

const pulseOffset = 3.5; // how far the pulsing circle is from the main circle

// variable by_province is from index.html (views-> template -> js)
for (const [location, labels] of Object.entries(JSON.parse(by_province))) {
    let longLat = {lon: parseFloat(labels['longitude']), lat: parseFloat(labels['latitude'])}; // location of where there's coronavirus
    
    let radius = Math.min(1.5 + Math.sqrt(labels['confirmed_num_cases']), 20);                

    let circle = L.circleMarker(longLat, {
        radius: radius,
        color: circleColour,
        fillColor: circleColour,
        fillOpacity: 0.2
    });
    let pulsingCircle = L.circleMarker(longLat, {
        radius: radius + pulseOffset,
        color: circleColour,
        weight: 5,
        className: 'pulse',
        opacity: 0.2
    }).addTo(map);

    let confirmedLabel = labels['confirmed_num_cases'] + ' ' + 'confirmed cases';
    let deathsLabel = labels['deaths_num_cases'] + ' ' + 'deaths';

    circle.bindPopup('<b>' + location + '</b>' + '<br>' + confirmedLabel + '<br>' + deathsLabel, {'offset': L.point(0, -10)}).addTo(map);
    
    // circle event handlers
    circle.on('mouseover', function(){
        circle.setStyle({ color: 'white', weight: 10 });
        this.openPopup();
    });

    circle.on('mouseout', function(){
        circle.setStyle({ color: circleColour, weight:  defaultBorderWeight});
        this.closePopup();
    });
}
