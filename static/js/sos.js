// SOS page logic: trigger, live tracking, video, voice message, voice command.
(function () {
  const btn = document.getElementById("sosBtn");
  const status = document.getElementById("sosStatus");
  const endBtn = document.getElementById("endSosBtn");
  const recordBtn = document.getElementById("recordVoiceBtn");
  const voiceRec = document.getElementById("voiceRecorder");
  const startRec = document.getElementById("startRec");
  const stopRec = document.getElementById("stopRec");
  const recTimer = document.getElementById("recTimer");
  const recWave = document.getElementById("recWave");
  const audioPreview = document.getElementById("audioPreview");
  const voiceCmdBtn = document.getElementById("voiceCmdBtn");
  const voiceCmdResult = document.getElementById("voiceCmdResult");
  const mapEl = document.getElementById("map");

  let mediaRecorder = null;
  let audioChunks = [];
  let recInterval = null;
  let recSeconds = 0;

  btn.addEventListener("click", triggerSOS);
  endBtn.addEventListener("click", endSOS);
  recordBtn.addEventListener("click", function () { voiceRec.style.display = "block"; });
  startRec.addEventListener("click", startRecording);
  stopRec.addEventListener("click", stopRecording);
  voiceCmdBtn.addEventListener("click", startVoiceCommand);

  function triggerSOS() {
    if (!navigator.geolocation) { SE.toast("Geolocation not supported on this device.", "error"); }
    btn.disabled = true;
    btn.textContent = "ACTIVATED";
    status.style.display = "block";

    navigator.geolocation.getCurrentPosition(
      function (pos) {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        initMap(lat, lng);
        document.getElementById("coordText").textContent = lat.toFixed(5) + ", " + lng.toFixed(5);
        SE.postJSON("/sos/trigger/", { latitude: lat, longitude: lng })
          .then(function (data) {
            SOS_DATA.eventId = data.event_id;
            SOS_DATA.videoRoomUrl = data.video_room_url;
            document.getElementById("locStatus").textContent = "Captured";
            document.getElementById("videoStatus").textContent = "Live";
            document.getElementById("smsStatus").textContent = data.sms_status || "sent";
            document.getElementById("policeStatus").textContent = data.police_status || "sent";
            if (data.video_room_url) {
              document.getElementById("videoLink").href = data.video_room_url;
              document.getElementById("videoLinkWrap").style.display = "block";
            }
            startTracking();
            openVideoRoom();
          })
          .catch(function (err) { SE.toast("SOS trigger failed: " + err.message, "error"); });
      },
      function (err) {
        SE.toast("Location permission denied. Triggering SOS without precise location.", "error");
        SE.postJSON("/sos/trigger/", {})
          .then(function (data) { SOS_DATA.eventId = data.event_id; SOS_DATA.videoRoomUrl = data.video_room_url; openVideoRoom(); })
          .catch(function (e) { SE.toast("SOS failed: " + e.message, "error"); });
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  }

  function initMap(lat, lng) {
    if (SOS_DATA.map) { SOS_DATA.marker.setPosition({ lat: lat, lng: lng }); return; }
    if (typeof google === "undefined" || !google.maps) { mapEl.innerHTML = "<small class='text-muted'>Map unavailable (no API key)</small>"; return; }
    SOS_DATA.map = new google.maps.Map(mapEl, { zoom: 15, center: { lat: lat, lng: lng } });
    SOS_DATA.marker = new google.maps.Marker({ position: { lat: lat, lng: lng }, map: SOS_DATA.map, title: "Your location" });
  }

  function startTracking() {
    SOS_DATA.trackingTimer = setInterval(function () {
      navigator.geolocation.getCurrentPosition(function (pos) {
        const lat = pos.coords.latitude, lng = pos.coords.longitude;
        if (SOS_DATA.map && SOS_DATA.marker) { SOS_DATA.marker.setPosition({ lat: lat, lng: lng }); SOS_DATA.map.panTo({ lat: lat, lng: lng }); }
        document.getElementById("coordText").textContent = lat.toFixed(5) + ", " + lng.toFixed(5);
        SE.postJSON("/sos/update-location/" + SOS_DATA.eventId + "/", { latitude: lat, longitude: lng }).catch(function () {});
      }, function () {}, { enableHighAccuracy: true, timeout: 10000 });
    }, 10000);
  }

  function openVideoRoom() {
    if (!SOS_DATA.videoRoomUrl) return;
    if (SE.isOnline()) {
      window.open(SOS_DATA.videoRoomUrl, "_blank");
    } else {
      SE.toast("Offline: camera will record locally and sync when online.", "error");
      startOfflineRecording();
    }
  }

  function startOfflineRecording() {
    navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(function (stream) {
      const mr = new MediaRecorder(stream);
      const chunks = [];
      mr.ondataavailable = function (e) { chunks.push(e.data); };
      mr.onstop = function () {
        const blob = new Blob(chunks, { type: "video/webm" });
        const fd = new FormData();
        fd.append("video", blob, "offline.webm");
        SE.postForm("/video/upload-offline/", fd).then(function () { SE.toast("Offline video synced.", "success"); }).catch(function () {});
      };
      mr.start();
      SE.toast("Recording emergency video locally...", "info");
      setTimeout(function () { if (mr.state !== "inactive") mr.stop(); }, 60000);
    }).catch(function () { SE.toast("Camera permission denied.", "error"); });
  }

  function endSOS() {
    if (!SOS_DATA.eventId) { SE.toast("No active emergency.", "error"); return; }
    if (SOS_DATA.trackingTimer) clearInterval(SOS_DATA.trackingTimer);
    fetch("/sos/end/" + SOS_DATA.eventId + "/", {
      method: "POST", credentials: "same-origin",
      headers: { "X-CSRFToken": SE.getCSRF() },
    }).then(function () {
      SE.toast("Emergency ended. Stay safe.", "success");
      btn.disabled = false; btn.textContent = "SOS"; status.style.display = "none";
    }).catch(function () { SE.toast("Could not end emergency.", "error"); });
  }

  // Voice message recording
  function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];
      mediaRecorder.ondataavailable = function (e) { audioChunks.push(e.data); };
      mediaRecorder.onstop = function () {
        const blob = new Blob(audioChunks, { type: "audio/webm" });
        audioPreview.src = URL.createObjectURL(blob);
        audioPreview.style.display = "block";
        const fd = new FormData();
        fd.append("audio", blob, "voice.webm");
        fd.append("transcript", "Emergency voice message");
        SE.postForm("/voice/register/", fd)
          .then(function () { SE.toast("Voice message saved and shared.", "success"); })
          .catch(function () { SE.toast("Voice upload failed.", "error"); });
        if (SOS_DATA.eventId) {
          SE.postForm("/sos/upload-voice/" + SOS_DATA.eventId + "/", fd).catch(function () {});
        }
      };
      mediaRecorder.start();
      startRec.disabled = true; stopRec.disabled = false; recWave.style.display = "inline-block";
      recSeconds = 0;
      recInterval = setInterval(function () {
        recSeconds++;
        const m = String(Math.floor(recSeconds / 60)).padStart(2, "0");
        const s = String(recSeconds % 60).padStart(2, "0");
        recTimer.textContent = m + ":" + s;
      }, 1000);
    }).catch(function () { SE.toast("Microphone permission denied.", "error"); });
  }

  function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") { mediaRecorder.stop(); }
    startRec.disabled = false; stopRec.disabled = true; recWave.style.display = "none";
    clearInterval(recInterval);
  }

  // Voice command recognition
  function startVoiceCommand() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { SE.toast("Voice recognition not supported in this browser.", "error"); return; }
    const rec = new SR();
    rec.lang = "en-US"; rec.continuous = false; rec.interimResults = false;
    rec.onresult = function (e) {
      const phrase = e.results[0][0].transcript.trim().toLowerCase();
      voiceCmdResult.textContent = 'Heard: "' + phrase + '"';
      SE.postJSON("/voice/command/", { phrase: phrase })
        .then(function (data) {
          if (data.trigger_sos) { SE.toast('Command "' + phrase + '" recognized. Activating SOS!', "success"); triggerSOS(); }
          else { voiceCmdResult.textContent += " — not an emergency command."; }
        })
        .catch(function () { SE.toast("Command check failed.", "error"); });
    };
    rec.onerror = function (e) { SE.toast("Voice recognition error: " + e.error, "error"); };
    rec.start();
    voiceCmdResult.textContent = "Listening...";
  }
})();
