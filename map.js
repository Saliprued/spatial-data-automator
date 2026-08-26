const map = L.map("map", { zoomControl: false }).setView([31.2, -99.4], 6);

L.control.zoom({ position: "bottomright" }).addTo(map);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
  maxZoom: 18,
}).addTo(map);

const typeColors = {
  "Refinery": "#d15d4f",
  "Storage Terminal": "#8266b4",
  "Compressor Station": "#2d7f88",
  "Pump Station": "#d39436",
  "Well Pad": "#4e8e62",
};

const statusOpacity = {
  "Active": 0.9,
  "Maintenance": 0.55,
  "Inactive": 0.28,
};

const escapeHtml = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

function markerStyle(feature) {
  const properties = feature.properties ?? {};
  const color = typeColors[properties.Facility_Type] ?? "#456c72";
  return {
    radius: 6,
    color: "#ffffff",
    weight: 1.5,
    fillColor: color,
    fillOpacity: statusOpacity[properties.Status] ?? 0.75,
  };
}

function popupContent(properties = {}) {
  return `
    <div class="facility-popup">
      <strong>${escapeHtml(properties.Location_Name)}</strong>
      <span>${escapeHtml(properties.Facility_Type)}</span>
      <dl>
        <dt>Operator</dt><dd>${escapeHtml(properties.Operator)}</dd>
        <dt>Status</dt><dd>${escapeHtml(properties.Status)}</dd>
        <dt>Facility ID</dt><dd>${escapeHtml(properties.Facility_ID)}</dd>
      </dl>
    </div>`;
}

function buildLegend(features) {
  const presentTypes = [...new Set(features.map(
    (feature) => feature.properties?.Facility_Type
  ))].filter(Boolean).sort();

  document.querySelector("#legend").innerHTML = `
    <strong>Facility type</strong>
    ${presentTypes.map((type) => `
      <span><i style="--marker-color:${typeColors[type] ?? "#456c72"}"></i>${escapeHtml(type)}</span>
    `).join("")}`;
}

fetch("./texas_energy_infrastructure.geojson")
  .then((response) => {
    if (!response.ok) {
      throw new Error(`GeoJSON request failed with status ${response.status}`);
    }
    return response.json();
  })
  .then((data) => {
    const features = Array.isArray(data.features) ? data.features : [];
    const facilityLayer = L.geoJSON(data, {
      pointToLayer: (feature, latlng) => L.circleMarker(latlng, markerStyle(feature)),
      onEachFeature: (feature, layer) => layer.bindPopup(popupContent(feature.properties)),
    }).addTo(map);

    if (features.length && facilityLayer.getBounds().isValid()) {
      map.fitBounds(facilityLayer.getBounds(), { padding: [32, 32], maxZoom: 7 });
    }

    document.querySelector("#facility-count").textContent = `${features.length} mapped facilities`;
    document.querySelector("#map-status").textContent = "Generated from the repository CSV";
    buildLegend(features);
  })
  .catch((error) => {
    console.error(error);
    document.querySelector("#facility-count").textContent = "Map unavailable";
    document.querySelector("#map-status").textContent = "The GeoJSON file could not be loaded.";
  });

