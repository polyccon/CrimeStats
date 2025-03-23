let map;

function updateCrimeData() {
    let center = map.getCenter();
    let lat = center.lat;
    let lng = center.lng;

    console.log(`Fetching crime data for: lat=${lat}, lng=${lng}`);

    // Fetch updated crime data based on the new center point
    fetch(`/heatmap?lat=${lat}&lng=${lng}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Error fetching crime data:", data.error);
                return;
            }

            console.log("Updating heatmap with new crime data:", data);

            // Remove previous heatmap (if any)
            document.getElementById("heatmap-layer")?.remove();

            // Add new heatmap as an image overlay
            let img = document.createElement("img");
            img.id = "heatmap-layer";
            img.src = data.map;
            img.style.position = "absolute";
            img.style.top = "0";
            img.style.left = "0";
            img.style.width = "100%";
            img.style.height = "100%";
            img.style.opacity = "0.7";  // Slight transparency

            document.getElementById("map").appendChild(img);
        })
        .catch(error => console.error("Error:", error));
}

window.onload = function () {
    map = L.map("map").setView([51.5074, -0.1278], 12);  // Default to London

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    // Fetch new crime data when the user moves the map
    map.on("moveend", updateCrimeData);

    // Load initial data
    updateCrimeData();
};
