// Live location tracking page.
(function () {
  const mapEl = document.getElementById("map");
  const coordText = document.getElementById("coordText");
  const shareBtn = document.getElementById("shareBtn");
  let map = null, marker = null, watchId = null, shareUrl = null;

  if (!navigator.geolocation) { coordText.textContent = "Geolocation not supported."; return; }

  navigator.geolocation.getCurrentPosition(initMap, function () {
    mapEl.innerHTML = "<small class='text-muted p-3 d-block'>Location permission denied.</small>";
  }, { enableHighAccuracy: true });

  function initMap(pos) {
    const lat = pos.coords.latitude, lng = pos.coords.longitude;
    coordText.textContent = lat.toFixed(5) + ", " + lng.toFixed(5);
    if (typeof google !== "undefined" && google.maps) {
      map = new google.maps.Map(mapEl, { zoom: 15, center: { lat: lat, lng: lng } });
      marker = new google.maps.Marker({ position: { lat: lat, lng: lng }, map: map, title: "You are here" });
    } else {
      mapEl.innerHTML = "<small class='text-muted p-3 d-block'>Map unavailable (no API key configured).</small>";
    }
    SE.postJSON("/location/update/", { latitude: lat, longitude: lng, accuracy: pos.coords.accuracy }).catch(function () {});
    shareUrl = "https://www.google.com/maps?q=" + lat + "," + lng;
    watchId = navigator.geolocation.watchPosition(updateMap, function () {}, { enableHighAccuracy: true });
  }

  function updateMap(pos) {
    const lat = pos.coords.latitude, lng = pos.coords.longitude;
    coordText.textContent = lat.toFixed(5) + ", " + lng.toFixed(5);
    if (map && marker) { marker.setPosition({ lat: lat, lng: lng }); map.panTo({ lat: lat, lng: lng }); }
    SE.postJSON("/location/update/", { latitude: lat, longitude: lng, accuracy: pos.coords.accuracy }).catch(function () {});
    shareUrl = "https://www.google.com/maps?q=" + lat + "," + lng;
  }

  shareBtn.addEventListener("click", function () {
    if (!shareUrl) { SE.toast("Location not available yet.", "error"); return; }
    if (navigator.share) { navigator.share({ title: "My Live Location", url: shareUrl }).catch(function () {}); }
    else { navigator.clipboard.writeText(shareUrl).then(function () { SE.toast("Tracking link copied to clipboard.", "success"); }); }
  });
})();
