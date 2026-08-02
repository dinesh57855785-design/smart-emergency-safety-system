// admin_dashboard.js
async function jfetch(url){
  const r = await fetch(url, {credentials: 'same-origin'});
  return r.json();
}

async function init(){
  // daily
  const daily = await jfetch('/dashboard/api/daily_sos/');
  const dLabels = daily.map(d=>d.date);
  const dData = daily.map(d=>d.count);
  const ctxD = document.getElementById('dailySosChart').getContext('2d');
  new Chart(ctxD, {type:'line', data:{labels:dLabels, datasets:[{label:'Daily SOS', data:dData, backgroundColor:'rgba(255,99,132,0.2)', borderColor:'rgba(255,99,132,1)', fill:true}]}});

  const monthly = await jfetch('/dashboard/api/monthly_sos/');
  const mLabels = monthly.map(d=>d.month);
  const mData = monthly.map(d=>d.count);
  const ctxM = document.getElementById('monthlySosChart').getContext('2d');
  new Chart(ctxM, {type:'bar', data:{labels:mLabels, datasets:[{label:'Monthly SOS', data:mData, backgroundColor:'rgba(54,162,235,0.2)', borderColor:'rgba(54,162,235,1)'}]}});

  const etypes = await jfetch('/dashboard/api/emergency_types/');
  const eLabels = etypes.map(d=>d.message || 'Unknown');
  const eData = etypes.map(d=>d.count);
  const ctxE = document.getElementById('etypeChart').getContext('2d');
  new Chart(ctxE, {type:'doughnut', data:{labels:eLabels, datasets:[{data:eData, backgroundColor:['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF']}]}});

  const users = await jfetch('/dashboard/api/user_registrations/');
  const uLabels = users.map(d=>d.date);
  const uData = users.map(d=>d.count);
  const ctxU = document.getElementById('userRegChart').getContext('2d');
  new Chart(ctxU, {type:'line', data:{labels:uLabels, datasets:[{label:'User Registrations', data:uData, backgroundColor:'rgba(153,102,255,0.2)', borderColor:'rgba(153,102,255,1)', fill:true}]}});
}

window.addEventListener('DOMContentLoaded', init);
