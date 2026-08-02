// voice.js - handles listening for registered voice command and triggering SOS
(function(){
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

  async function fetchPhrase(){
    try{
      const res = await fetch(window.VOICE_CONFIG.getCommandUrl, {credentials: 'same-origin'});
      const j = await res.json();
      return (j && j.phrase) ? j.phrase.trim() : '';
    }catch(e){
      return '';
    }
  }

  function startRecognition(targetPhrase){
    if (!targetPhrase) return;
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)){
      console.log('Speech recognition not supported');
      return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.onresult = function(event){
      for (let i=event.resultIndex; i<event.results.length; ++i){
        const transcript = event.results[i][0].transcript.trim();
        console.log('Heard:', transcript);
        if (transcript.toLowerCase() === targetPhrase.toLowerCase()){
          console.log('Voice command matched. Triggering SOS.');
          // trigger SOS via POST
          fetch(window.VOICE_CONFIG.triggerSosUrl, {
            method: 'POST',
            headers: {
              'X-CSRFToken': getCookie('csrftoken'),
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'message=Voice+Command+Triggered'
          }).then(r=>r.json()).then(j=>{
            // redirect to SOS page with query param for confirmation
            window.location.href = window.VOICE_CONFIG.sosPageUrl + '?voice=1';
          }).catch(err=>{
            alert('Failed to trigger SOS via voice command.');
          });
          recognition.stop();
          return;
        }
      }
    };
    recognition.onerror = function(e){
      console.log('Recognition error', e);
      // try restarting after a pause
      setTimeout(()=>recognition.start(), 1000);
    };
    recognition.onend = function(){
      // restart to keep listening
      setTimeout(()=>recognition.start(), 500);
    };
    recognition.start();
    console.log('Voice recognition started for phrase:', targetPhrase);
  }

  async function init(){
    if (!window.VOICE_CONFIG || !window.VOICE_CONFIG.listen) return;
    const phrase = await fetchPhrase();
    if (phrase) startRecognition(phrase);
  }

  // If loaded as module, init immediately
  init();
})();
