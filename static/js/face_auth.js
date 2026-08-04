// Face authentication using face-api.js
// Loads models from CDN, captures face descriptor, and sends to server.

(function () {
  "use strict";

  const MODEL_URL = "https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.13/model";
  const SCRIPT_URL = "https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.13/dist/face-api.js";

  let faceApiLoaded = false;
  let faceApiLoading = null;
  let stream = null;
  let scanning = false;
  let captureMode = null; // "login" or "register"

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      const s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error("Failed to load " + src)); };
      document.head.appendChild(s);
    });
  }

  function loadFaceApi() {
    if (faceApiLoaded) return Promise.resolve();
    if (faceApiLoading) return faceApiLoading;
    faceApiLoading = loadScript(SCRIPT_URL).then(function () {
      return Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
        faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
        faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
      ]);
    }).then(function () {
      faceApiLoaded = true;
    });
    return faceApiLoading;
  }

  function setStatus(msg, type) {
    const el = document.getElementById("faceStatus");
    if (!el) return;
    el.textContent = msg;
    el.className = "se-face-status" + (type ? " se-face-status--" + type : "");
  }

  function startCamera() {
    const video = document.getElementById("faceVideo");
    const placeholder = document.getElementById("facePlaceholder");
    const btnStart = document.getElementById("btnStartFace");
    const btnScan = document.getElementById("btnScanFace");

    if (!video) return;

    setStatus("Loading face models...", "loading");

    loadFaceApi().then(function () {
      return navigator.mediaDevices.getUserMedia({ video: { width: 320, height: 240 } });
    }).then(function (s) {
      stream = s;
      video.srcObject = s;
      if (placeholder) placeholder.style.display = "none";
      if (btnStart) btnStart.disabled = true;
      if (btnScan) btnScan.disabled = false;
      setStatus("Camera ready. Position your face in the frame.", "ready");
    }).catch(function (err) {
      setStatus("Error: " + (err.message || "Could not access camera."), "error");
    });
  }

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach(function (t) { t.stop(); });
      stream = null;
    }
  }

  function drawDetection(video, detection) {
    const canvas = document.getElementById("faceCanvas");
    if (!canvas) return;
    const dims = faceapi.matchDimensions(canvas, video, true);
    const resized = faceapi.resizeResults(detection, dims);
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resized);
    faceapi.draw.drawFaceLandmarks(canvas, resized);
  }

  function captureDescriptor() {
    const video = document.getElementById("faceVideo");
    if (!video || !stream) {
      setStatus("Camera not started.", "error");
      return Promise.resolve(null);
    }
    return faceapi
      .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions({ inputSize: 320, scoreThreshold: 0.5 }))
      .withFaceLandmarks()
      .withFaceDescriptor()
      .then(function (detection) {
        if (!detection) return null;
        drawDetection(video, detection);
        return Array.from(detection.descriptor);
      });
  }

  function scanLogin() {
    if (scanning) return;
    scanning = true;
    const btnScan = document.getElementById("btnScanFace");
    if (btnScan) btnScan.disabled = true;
    setStatus("Scanning face...", "loading");

    captureDescriptor().then(function (descriptor) {
      if (!descriptor) {
        setStatus("No face detected. Please position your face in the frame and try again.", "error");
        scanning = false;
        if (btnScan) btnScan.disabled = false;
        return;
      }
      setStatus("Verifying...", "loading");
      return fetch("/face-auth/login/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": window.SE ? window.SE.getCSRF() : "",
        },
        body: JSON.stringify({ descriptor: descriptor }),
      });
    }).then(function (resp) {
      if (!resp) return null;
      return resp.json();
    }).then(function (data) {
      if (data && data.ok) {
        setStatus("Face recognized! Redirecting...", "success");
        window.location.href = data.redirect || "/dashboard/";
      } else {
        setStatus(data && data.error ? data.error : "Face not recognized.", "error");
        scanning = false;
        const btnScan = document.getElementById("btnScanFace");
        if (btnScan) btnScan.disabled = false;
      }
    }).catch(function () {
      setStatus("Connection error. Please try again.", "error");
      scanning = false;
      const btnScan = document.getElementById("btnScanFace");
      if (btnScan) btnScan.disabled = false;
    });
  }

  function scanRegister() {
    if (scanning) return;
    scanning = true;
    const btnScan = document.getElementById("btnScanFace");
    if (btnScan) btnScan.disabled = true;
    setStatus("Scanning face...", "loading");

    captureDescriptor().then(function (descriptor) {
      if (!descriptor) {
        setStatus("No face detected. Please position your face in the frame and try again.", "error");
        scanning = false;
        if (btnScan) btnScan.disabled = false;
        return;
      }
      setStatus("Saving face data...", "loading");
      return fetch("/face-auth/register/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": window.SE ? window.SE.getCSRF() : "",
        },
        body: JSON.stringify({ descriptor: descriptor }),
      });
    }).then(function (resp) {
      if (!resp) return null;
      return resp.json();
    }).then(function (data) {
      if (data && data.ok) {
        setStatus("Face captured! You can now log in with your face.", "success");
        setTimeout(function () { window.location.href = "/accounts/login/"; }, 2000);
      } else {
        setStatus(data && data.error ? data.error : "Failed to save face data.", "error");
        scanning = false;
        if (btnScan) btnScan.disabled = false;
      }
    }).catch(function () {
      setStatus("Connection error. Please try again.", "error");
      scanning = false;
      if (btnScan) btnScan.disabled = false;
    });
  }

  // Tab switching
  function initTabs() {
    const tabs = document.querySelectorAll(".se-auth-tab");
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        const target = tab.getAttribute("data-tab");
        tabs.forEach(function (t) { t.classList.remove("active"); });
        tab.classList.add("active");
        document.querySelectorAll(".se-auth-panel").forEach(function (p) {
          p.classList.remove("active");
        });
        const panel = document.getElementById("panel-" + target);
        if (panel) panel.classList.add("active");

        if (target === "face") {
          captureMode = panel && panel.querySelector("#btnScanFace") &&
            panel.querySelector("#btnScanFace").textContent.indexOf("Capture") !== -1 ? "register" : "login";
        } else {
          stopCamera();
        }
      });
    });
  }

  // Register form: after successful submit, switch to face capture
  function initRegisterForm() {
    const form = document.getElementById("registerForm");
    if (!form) return;
    form.addEventListener("submit", function () {
      // Let the form submit normally; server will redirect back with ?face=1
    });
    // Check URL param to auto-switch to face tab
    const params = new URLSearchParams(window.location.search);
    if (params.get("face") === "1") {
      const tab = document.getElementById("tabFaceCapture");
      if (tab) tab.click();
    }
  }

  function init() {
    initTabs();
    initRegisterForm();

    const btnStart = document.getElementById("btnStartFace");
    const btnScan = document.getElementById("btnScanFace");
    if (btnStart) btnStart.addEventListener("click", startCamera);
    if (btnScan) {
      btnScan.addEventListener("click", function () {
        // Determine mode based on which panel is active
        const facePanel = document.getElementById("panel-face");
        if (!facePanel || !facePanel.classList.contains("active")) return;
        const btnText = btnScan.textContent || "";
        if (btnText.indexOf("Capture") !== -1) {
          scanRegister();
        } else {
          scanLogin();
        }
      });
    }

    // Auto-start camera when face tab is activated
    const faceTabs = document.querySelectorAll('.se-auth-tab[data-tab="face"]');
    faceTabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        setTimeout(startCamera, 300);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Cleanup on page leave
  window.addEventListener("beforeunload", stopCamera);
})();
