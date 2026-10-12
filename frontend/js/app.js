const API = "http://127.0.0.1:8001";
const $=id=>document.getElementById(id);
let latestTelemetry = null;
let lastRouteKey = "";


const el={
  dot:$("connectionDot"), conn:$("connectionText"), score:$("riskScore"),
  band:$("riskBand"), scenario:$("scenario"), zone:$("zone"),
  temp:$("temperature"), smoke:$("smoke"), gas:$("gas"), occupancy:$("occupancy"),
  factors:$("factors"), explanation:$("riskExplanation"),
  select:$("scenarioSelect"), button:$("scenarioButton"),
  routeStart:$("routeStartZone")
};

async function loadScenarios(){
  const r=await fetch(`${API}/api/simulation/scenarios`);
  const data=await r.json();
  el.select.innerHTML="";
  data.scenarios.forEach(s=>{
    const option=document.createElement("option");
    option.value=s; option.textContent=s;
    el.select.appendChild(option);
  });
  el.select.value=data.active;
}

async function activateScenario(){
  const response = await fetch(
    `${API}/api/simulation/scenario/${encodeURIComponent(el.select.value)}`,
    { method: "POST" }
  );

  const data = await response.json();

  if (!response.ok || !data.success) {
    throw new Error(data.detail || "Scenario activation failed.");
  }

  lastRouteKey = "";
  await calculateEvacuationRoute();
}

function updateTwin(zone){
  document.querySelectorAll(".zone-block").forEach(node=>{
    node.classList.toggle("active",node.dataset.zone===zone);
  });
}

async function calculateEvacuationRoute(){

  const status = $("routeStatus");
  const pathEl = $("routePath");
  const details = $("routeDetails");
  const button = $("routeButton");

  if(!latestTelemetry){
    status.textContent = "Waiting for live telemetry.";
    return;
  }

  button.disabled = true;
  status.classList.remove("route-unavailable", "route-available");
  pathEl.classList.remove("route-unavailable");
  status.textContent = "Calculating route...";
  pathEl.textContent = "";
  details.textContent = "";

  try{
    const params = new URLSearchParams({
      from_zone: el.routeStart.value
    });
    const response = await fetch(`${API}/api/evacuation/route?${params}`);
    const data = await response.json();
    if(!response.ok){
      throw new Error(data.detail || "Route request failed.");
    }

    document.querySelectorAll(".zone-block.exit").forEach(node => {
      node.classList.toggle(
        "blocked",
        (data.blocked_exits || []).includes(node.dataset.zone)
      );
    });

    // Clear previous route highlighting
    document.querySelectorAll(".zone-block").forEach(node => {
      node.classList.remove("route-step");
    });

    // Highlight every zone in the recommended route
    if (data.available && Array.isArray(data.route)) {
      data.route.forEach(zone => {
        document.querySelectorAll(".zone-block").forEach(node => {
          if (node.dataset.zone === zone && !node.classList.contains("blocked")) {
            node.classList.add("route-step");
          }
        });
      });
    }

    if(data.available){
      status.textContent = `Recommended destination: ${data.destination}`;
      status.classList.add("route-available");
      pathEl.textContent = data.route.join(" → ");
      details.textContent =
        `Scenario: ${data.scenario} | Starting zone: ${data.starting_zone} | Steps: ${data.steps}`;
    }else{
      status.textContent = "NO ROUTE AVAILABLE — all listed exits are unavailable.";
      status.classList.add("route-unavailable");
      pathEl.textContent = "Evacuation route could not be calculated.";
      pathEl.classList.add("route-unavailable");
      details.textContent =
        `Scenario: ${data.scenario} | Blocked exits: ${(data.blocked_exits || []).join(", ") || "None listed"}`;
    }
  }catch(error){
    status.textContent = "Could not calculate route.";
    status.classList.add("route-unavailable");
    pathEl.textContent = error.message;
    console.error("Evacuation route failed:", error);
  }finally{
    button.disabled = false;
  }
}

function updateUI(payload){
  const t = payload.telemetry, r = payload.risk;
  latestTelemetry = t;

  const routeKey = `${t.scenario}|${t.zone}`;
  if (routeKey !== lastRouteKey) {
    lastRouteKey = routeKey;
  }

  el.score.textContent = r.score;
  el.band.textContent = r.band;
  el.scenario.textContent = t.scenario;
  el.zone.textContent = t.zone;
  el.temp.textContent = t.temperature;
  el.smoke.textContent = t.smoke;
  el.gas.textContent = t.gas;
  el.occupancy.textContent = t.occupancy;

  el.explanation.textContent =
    `Risk score ${r.score}/100 (${r.band}) in ${r.zone}. Scenario: ${t.scenario}. Sensor state: ${t.status}.`;

  updateTwin(t.zone);

  if (r.score >= 80) {
    el.band.style.background = "#432020";
    el.band.style.color = "#ff9e9e";
  } else if (r.score >= 60) {
    el.band.style.background = "#3e3020";
    el.band.style.color = "#ffd18a";
  } else {
    el.band.style.background = "#163322";
    el.band.style.color = "#72df9a";
  }
}

function connect() {
  const ws = new WebSocket("ws://127.0.0.1:8001/ws/live");

  ws.onopen = () => {
    el.dot.style.background = "#52d273";
    el.conn.textContent = "LIVE";
  };

  ws.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      updateUI(payload);
    } catch (error) {
      console.error("Invalid WebSocket message:", error);
    }
  };

  ws.onerror = (error) => {
    console.error("WebSocket connection error:", error);
    el.dot.style.background = "#ff5f56";
    el.conn.textContent = "CONNECTION ERROR";
  };

  ws.onclose = () => {
    el.dot.style.background = "#f0ad4e";
    el.conn.textContent = "RECONNECTING";
    setTimeout(connect, 2000);
  };
}

$("routeButton").addEventListener("click", calculateEvacuationRoute);

el.button.addEventListener("click", async () => {
  try {
    el.button.disabled = true;
    await activateScenario();
  } catch (error) {
    console.error("Scenario activation failed:", error);
  } finally {
    el.button.disabled = false;
  }
});

(async () => {
  try {
    await loadScenarios();
    connect();
  } catch (error) {
    console.error("Dashboard initialization failed:", error);
    el.dot.style.background = "#ff5f56";
    el.conn.textContent = "BACKEND OFFLINE";
  }
})();
