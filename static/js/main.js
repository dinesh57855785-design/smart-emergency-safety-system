/* main.js - simple placeholder with toast helper */
console.log('Smart Emergency System loaded');

function showToast(message, type='info', ttl=5000){
  const container = document.getElementById('toastContainer');
  if(!container) return;
  const toastId = 't'+Math.random().toString(36).substr(2,9);
  const toastEl = document.createElement('div');
  toastEl.className = `toast align-items-center text-bg-${type} border-0`;
  toastEl.setAttribute('role','alert');
  toastEl.setAttribute('aria-live','assertive');
  toastEl.setAttribute('aria-atomic','true');
  toastEl.id = toastId;
  toastEl.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">${message}</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  `;
  container.appendChild(toastEl);
  const bsToast = new bootstrap.Toast(toastEl, {delay: ttl});
  bsToast.show();
  toastEl.addEventListener('hidden.bs.toast', ()=>{ toastEl.remove(); });
}
