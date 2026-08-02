// Shared helpers for the Smart Emergency System frontend.
window.SE = {
  getCSRF: function () {
    const m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : "";
  },
  postJSON: function (url, data) {
    return fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": this.getCSRF(),
      },
      body: JSON.stringify(data || {}),
    }).then(function (r) {
      if (!r.ok) throw new Error("Request failed: " + r.status);
      return r.json();
    });
  },
  postForm: function (url, formData) {
    return fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: { "X-CSRFToken": this.getCSRF() },
      body: formData,
    }).then(function (r) {
      if (!r.ok) throw new Error("Request failed: " + r.status);
      return r.json();
    });
  },
  toast: function (msg, type) {
    const cls = type === "error" ? "alert-danger" : type === "success" ? "alert-success" : "alert-info";
    const el = document.createElement("div");
    el.className = "alert " + cls + " alert-dismissible fade show";
    el.role = "alert";
    el.innerHTML = msg + '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
    const target = document.querySelector(".container") || document.body;
    target.prepend(el);
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 5000);
  },
  isOnline: function () { return navigator.onLine; },
};

window.addEventListener("online", function () {
  if (window.SE && window.SE.onOnline) window.SE.onOnline();
});
window.addEventListener("offline", function () {
  window.SE && window.SE.toast("You are offline. Emergency video will be recorded locally.", "error");
});
