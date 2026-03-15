 // Initialize the map centered on Texas
const map = L.map('map').setView([31.9686, -99.9018], 6);

// Add the base map tiles (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Fetch and load your automated GeoJSON file
fetch('texas_energy_infrastructure.geojson')
    .then(response => response.json())
    .then(data => {
        //Add the GeoJSON data to the map with popups
        L.geoJSON(data, {
            onEachFeature: function (feature, layer) {
                // Create a popup for each facility
                let popupContent = `
                    <b>Facility:</b> ${feature.properties.Location_Name}<br>
                    <b>Type:</b> ${feature.properties.Facility_Type}<br>
                    <b>Operator:</b> ${feature.properties.Operator}<br>
                    <b>Status:</b> ${feature.properties.Status}
                `;
                layer.bindPopup(popupContent);
            }
        }).addTo(map);
    })
    .catch(error => console.error('Error loading the GeoJSON file:', error));