// reports.js - fetch data and render charts on the reports dashboard
async function jsonFetch(url){
  const res = await fetch(url, {credentials: 'same-origin'});
  return res.json();
}

async function init(){
  // daily
  const daily = await jsonFetch('/reports/api/daily/');
  const dailyLabels = daily.map(d=>d.date);
  const dailyData = daily.map(d=>d.count);
  const ctxDaily = document.getElementById('dailyChart').getContext('2d');
  new Chart(ctxDaily, {type:'line', data:{labels:dailyLabels, datasets:[{label:'Emergencies',data:dailyData,backgroundColor:'rgba(255,99,132,0.2)',borderColor:'rgba(255,99,132,1)',fill:true}]}});

  const weekly = await jsonFetch('/reports/api/weekly/');
  const weekLabels = weekly.map(d=>d.week);
  const weekData = weekly.map(d=>d.count);
  const ctxWeek = document.getElementById('weeklyChart').getContext('2d');
  new Chart(ctxWeek, {type:'bar', data:{labels:weekLabels, datasets:[{label:'Weekly',data:weekData,backgroundColor:'rgba(54,162,235,0.2)',borderColor:'rgba(54,162,235,1)'}]}});

  const monthly = await jsonFetch('/reports/api/monthly/');
  const mLabels = monthly.map(d=>d.month);
  const mData = monthly.map(d=>d.count);
  const ctxM = document.getElementById('monthlyChart').getContext('2d');
  new Chart(ctxM, {type:'bar', data:{labels:mLabels, datasets:[{label:'Monthly',data:mData,backgroundColor:'rgba(75,192,192,0.2)',borderColor:'rgba(75,192,192,1)'}]}});

  const users = await jsonFetch('/reports/api/user_activity/');
  const uLabels = users.map(d=>d.user);
  const uData = users.map(d=>d.count);
  const ctxU = document.getElementById('userChart').getContext('2d');
  new Chart(ctxU, {type:'bar', data:{labels:uLabels, datasets:[{label:'User Activity',data:uData,backgroundColor:'rgba(153,102,255,0.2)',borderColor:'rgba(153,102,255,1)'}]}});

  const etypes = await jsonFetch('/reports/api/emergency_types/');
  const eLabels = etypes.map(d=>d.message || 'Unknown');
  const eData = etypes.map(d=>d.count);
  const ctxE = document.getElementById('etypeChart').getContext('2d');
  new Chart(ctxE, {type:'pie', data:{labels:eLabels, datasets:[{data:eData, backgroundColor:['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF']}]}});

  const pstats = await jsonFetch('/reports/api/police_stats/');
  const pLabels = pstats.map(d=>d.status);
  const pData = pstats.map(d=>d.count);
  const ctxP = document.getElementById('policeChart').getContext('2d');
  new Chart(ctxP, {type:'doughnut', data:{labels:pLabels, datasets:[{data:pData, backgroundColor:['#4BC0C0','#FF6384','#36A2EB','#FFCE56']}]}});

  const sms = await jsonFetch('/reports/api/sms_stats/');
  const sLabels = sms.map(d=>d.status);
  const sData = sms.map(d=>d.count);
  const ctxS = document.getElementById('smsChart').getContext('2d');
  new Chart(ctxS, {type:'doughnut', data:{labels:sLabels, datasets:[{data:sData, backgroundColor:['#FF9F40','#FF6384','#36A2EB']}]}});

  // recent emergencies
  const recent = await jsonFetch('/reports/api/recent/');
  const recentList = document.getElementById('recentList');
  if (recent && recent.length){
    const ul = document.createElement('ul'); ul.className='list-group';
    recent.forEach(r=>{
      const li = document.createElement('li'); li.className='list-group-item';
      li.textContent = `${r.id} - ${r.user} - ${r.created_at} - ${r.message || ''}`;
      ul.appendChild(li);
    });
    recentList.appendChild(ul);
  } else {
    recentList.textContent = 'No recent emergencies';
  }
}

window.addEventListener('DOMContentLoaded', init);
