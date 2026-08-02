let watchId = null;
let intervalId = null;

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const status = document.getElementById('locStatus');

startBtn.addEventListener('click', ()=>{
  if (navigator.geolocation){
    status.textContent = 'Obtaining location...';
    watchId = navigator.geolocation.watchPosition(sendPos, err=>{ status.textContent='Unable to get position'; }, {enableHighAccuracy:true});
  } else { status.textContent='Geolocation not supported'; }
});

stopBtn.addEventListener('click', ()=>{
  if (watchId) navigator.geolocation.clearWatch(watchId);
  status.textContent = 'Stopped';
});

function sendPos(pos){
  const lat = pos.coords.latitude;
  const lon = pos.coords.longitude;
  fetch('/location/save/', {
    method: 'POST',
    headers: {'X-CSRFToken': getCookie('csrftoken'), 'Content-Type':'application/x-www-form-urlencoded'},
    body: `lat=${lat}&lon=${lon}`
  }).then(r=>r.json()).then(j=>{
    if(j.status==='ok') status.textContent = `Sent: ${lat}, ${lon}`;
  }).catch(()=> status.textContent = 'Error sending');
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
