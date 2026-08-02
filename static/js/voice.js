// Voice message recording on the voice page.
(function () {
  const startRec = document.getElementById("startRec");
  const stopRec = document.getElementById("stopRec");
  const recTimer = document.getElementById("recTimer");
  const recWave = document.getElementById("recWave");
  const audioPreview = document.getElementById("audioPreview");
  let mediaRecorder = null, chunks = [], recInterval = null, recSeconds = 0;

  startRec.addEventListener("click", function () {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
      mediaRecorder = new MediaRecorder(stream);
      chunks = [];
      mediaRecorder.ondataavailable = function (e) { chunks.push(e.data); };
      mediaRecorder.onstop = function () {
        const blob = new Blob(chunks, { type: "audio/webm" });
        audioPreview.src = URL.createObjectURL(blob);
        audioPreview.style.display = "block";
        const fd = new FormData();
        fd.append("audio", blob, "voice.webm");
        fd.append("transcript", "Voice message");
        SE.postForm("/voice/register/", fd)
          .then(function () { SE.toast("Voice message saved.", "success"); })
          .catch(function () { SE.toast("Upload failed.", "error"); });
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
  });

  stopRec.addEventListener("click", function () {
    if (mediaRecorder && mediaRecorder.state !== "inactive") { mediaRecorder.stop(); }
    startRec.disabled = false; stopRec.disabled = true; recWave.style.display = "none";
    clearInterval(recInterval);
  });
})();
