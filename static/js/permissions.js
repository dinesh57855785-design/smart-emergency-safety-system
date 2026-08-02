// static/js/permissions.js
(function () {
  const overlay = document.getElementById('permissionOverlay');
  const cameraEl = document.getElementById('cameraStatus');
  const micEl = document.getElementById('microphoneStatus');
  const locEl = document.getElementById('locationStatus');
  const alertContainer = document.getElementById('permissionAlertContainer');

  let permissionsRequested = false;
  let permissionState = { camera: 'unknown', microphone: 'unknown', location: 'unknown' };

  function showOverlay(show) { if (!overlay) return; overlay.style.display = show ? 'flex' : 'none'; }
  function updateUI() {
    updateStatusElement(cameraEl, 'Camera', permissionState.camera);
    updateStatusElement(micEl, 'Microphone', permissionState.microphone);
    updateStatusElement(locEl, 'Location', permissionState.location);
    checkForDenied();
  }
  function updateStatusElement(el, label, state) {
    if (!el) return;
    const allowed = state === 'granted' || state === 'allowed';
    const text = allowed ? 'Allowed' : (state === 'denied' ? 'Denied' : 'Unknown');
    const color = allowed ? 'text-success' : (state === 'denied' ? 'text-danger' : 'text-muted');
    el.innerHTML = `${label}: <span class="${color}">${text}</span>`;
  }
  function showPermissionAlert() {
    if (!alertContainer) return;
    alertContainer.innerHTML = `
      <div class="alert alert-warning" role="alert">
        One or more permissions were denied. To allow live video and location features, enable Camera, Microphone and Location for this site in your browser settings:<br/>
        <ul>
          <li>Chrome: Click the lock icon in the address bar → Site settings → Allow camera/microphone/location</li>
          <li>Firefox: Page Info (padlock) → Permissions → Allow camera/microphone/location</li>
          <li>Safari: Preferences → Websites → Camera/Microphone/Location</li>
        </ul>
        After changing browser permissions, reload this page.
      </div>`;
  }
  function checkForDenied() {
    if (!alertContainer) return;
    if (permissionState.camera === 'denied' || permissionState.microphone === 'denied' || permissionState.location === 'denied') {
      showPermissionAlert();
    } else { alertContainer.innerHTML = ''; }
  }

  async function requestCameraAndMic() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      permissionState.camera = 'allowed'; permissionState.microphone = 'allowed';
      try { stream.getTracks().forEach(t => t.stop()); } catch (e) { }
    } catch (err) {
      if (err && (err.name === 'NotAllowedError' || err.name === 'SecurityError' || err.name === 'PermissionDeniedError')) {
        permissionState.camera = 'denied'; permissionState.microphone = 'denied';
      } else {
        permissionState.camera = permissionState.camera === 'allowed' ? 'allowed' : 'denied';
        permissionState.microphone = permissionState.microphone === 'allowed' ? 'allowed' : 'denied';
      }
    }
    updateUI();
  }

  function requestLocation() {
    return new Promise((resolve) => {
      if (!navigator.geolocation) { permissionState.location = 'denied'; updateUI(); return resolve(); }
      navigator.geolocation.getCurrentPosition(
        function (pos) { permissionState.location = 'allowed'; updateUI(); resolve(pos); },
        function (err) { permissionState.location = (err && err.code === err.PERMISSION_DENIED) ? 'denied' : 'denied'; updateUI(); resolve(); },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
      );
    });
  }

  async function requestPermissionsOnce() {
    if (permissionsRequested) return;
    permissionsRequested = true;
    showOverlay(true);
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      await requestCameraAndMic();
    } else { permissionState.camera = 'denied'; permissionState.microphone = 'denied'; }
    await requestLocation();
    showOverlay(false);
    updateUI();
  }

  document.addEventListener('DOMContentLoaded', function () {
    try { requestPermissionsOnce(); } catch (e) { console.error('Permission request failed', e); showOverlay(false); }
  });

  window.SOS_PERMISSIONS = permissionState;
})();
