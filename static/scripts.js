//
// The javascript file has the main loop where it calls the data from the server
// then we take it and make it into a pretty table, yay
//


let thedata;
function theLOOP(){
    fetch("/LC")
    .then((response) => response.json())
    .then((data) => {
        if (data && data != thedata){
            thedata = data;
            console.log(thedata);
            updateTable(thedata);
        }

    });
};

let intervalId;
intervalId = setInterval(theLOOP, 200);
let loopActive = true;
//main loop button
document.querySelector("#mainloop").addEventListener("click", function() {
    if (loopActive) {
      clearInterval(intervalId);
      console.log("maintestloop off");
      loopActive = false;
      document.getElementById("mainloop").innerHTML = "Toggle live loop (OFF)";
    } else {
      intervalId = setInterval(theLOOP, 200);
      console.log("maintestloop on");
      loopActive = true;
      document.getElementById("mainloop").innerHTML = "Toggle live loop (ON)";
    }
});


document.querySelector("#offlinetest").addEventListener("click", async function() {
  try {
    const response = await fetch("/offlinedatatest");
    const offlinedata = await response.json();
    console.log(offlinedata);
    updateTable(offlinedata);
    updateTablebeta(offlinedata);
  } catch (error) {
    console.error(error);
  }
});

/////////////////////////////////
//Table Creation
/////////////////////////////////
function getDefaultHeaders(data){
  const balanceBuffHeaders = [];
  for (const teamOrBench in data) {
    const championObject = data[teamOrBench];
    for (const championName in championObject) {
      const balanceBuffObject = championObject[championName]['Balance Buff'];
      if (typeof balanceBuffObject === 'object') {
        for (const header in balanceBuffObject) {
          if (!balanceBuffHeaders.includes(header)) {
            balanceBuffHeaders.push(header);
          }
        }
      }
    }
  }
  return balanceBuffHeaders
}

function getLegibleHeaders(data) {

  const headerMappings = {
    "dmg_dealt": "Damage Dealt",
    "dmg_taken": "Damage Taken"
    //"ability_haste": "Ability Haste",
    //"tenacity": "Tenacity",
    //"energy_regen": "Energy Regen",
    //"healing" : "Healing",
    //"shielding" : "Shielding"
    //"mana_regen" :
    //"attack_speed" : 
    //"movement_speed" :
  };
  defaultheaders = getDefaultHeaders(data)

  const legibleBalanceBuffHeaders = defaultheaders.map(header => {
    return headerMappings[header] || header.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
  });
  return legibleBalanceBuffHeaders;
}


function getLheader(data){
  const balanceBuffHeaders = [];
  for (const teamOrBench in data) {
    const championObject = data[teamOrBench];
    for (const championName in championObject) {
      const balanceBuffObject = championObject[championName]['Balance Buff'];
      if (typeof balanceBuffObject === 'object') {
        for (const header in balanceBuffObject) {
          if (!balanceBuffHeaders.includes(header)) {
            balanceBuffHeaders.push(header);
          }
        }
      }
    }
  }
  const headerMappings = {
    "dmg_dealt": "Damage Dealt",
    "dmg_taken": "Damage Taken"
    //"ability_haste": "Ability Haste",
    //"tenacity": "Tenacity",
    //"energy_regen": "Energy Regen",
    //"healing" : "Healing",
    //"shielding" : "Shielding"
    //"mana_regen" :
    //"attack_speed" : 
    //"movement_speed" :
  };
  const legibleBalanceBuffHeaders = balanceBuffHeaders.map(header => {
    return headerMappings[header] || header.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
  });
  return legibleBalanceBuffHeaders;
}



function updateTable(data) {
  const table1 = document.getElementById("table1");
  const tbody1 = table1.querySelector("tbody");
  const thead1 = table1.querySelector("thead");
  thead1.innerHTML = "";

  const table2 = document.getElementById("table2");
  const tbody2 = table2.querySelector("tbody");
  const thead2 = table2.querySelector("thead");
  thead2.innerHTML = "";

  const DefaultHeaders = getDefaultHeaders(data);
  const LegibleHeaders = getLegibleHeaders(data);
  const headers = getLheader(data);


  const headerRow = document.createElement("tr");

  const championHeader = document.createElement("th");
  championHeader.innerText = "Champion";
  headerRow.appendChild(championHeader);
  
  headers.forEach((header) => {
    const headerCell = document.createElement("th");
    headerCell.innerText = headers[header] || header;
    headerRow.appendChild(headerCell);
  });
  
  const winRateHeader = document.createElement("th");
  winRateHeader.innerText = "Win Rate";
  headerRow.appendChild(winRateHeader);
  
  thead1.appendChild(headerRow.cloneNode(true));
  thead2.appendChild(headerRow.cloneNode(true));

  tbody1.innerHTML = "";
  tbody2.innerHTML = "";

  Object.entries(data).forEach(([group, champions]) => {
    Object.entries(champions).forEach(([champion, stats]) => {
      const row = document.createElement("tr");
      row.insertCell().innerHTML = `<img src="${stats.Icon}" alt="${champion}"/>`;
  
      const buffs = stats["Balance Buff"];
      DefaultHeaders.forEach((header) => {
        row.insertCell().innerText = buffs[header] ?? "";
      });
  
      row.insertCell().innerText = stats["win rate"];
  
      if (group === "team") {
        tbody1.appendChild(row);
      } else if (group === "bench") {
        tbody2.appendChild(row);
      }
    });
  });
}



function updateTablebeta(data) {
  const table = document.getElementById("betatable");
  const tbody = table.querySelector("tbody");
  tbody.innerHTML = "";

  Object.entries(data).forEach(([group, champions]) => {
    Object.entries(champions).forEach(([champion, stats]) => {
      const row = document.createElement("tr");
      row.insertCell().innerText = champion;

      const buffs = stats["Balance Buff"];
      row.insertCell().innerText = buffs["ability_haste"] ?? "";
      row.insertCell().innerText = buffs["dmg_dealt"] ?? "";
      row.insertCell().innerText = buffs["dmg_taken"] ?? "";
      row.insertCell().innerText = buffs["tenacity"] ?? "";
      row.insertCell().innerText = buffs["energy_regen"] ?? "";

      row.insertCell().innerText = stats["win rate"];
      tbody.appendChild(row);
    });
  });
}


//////////////////////////////////////////
//testing makes me happy
//////////////////////////////////////////

function devmode() {
  const hiddenElements = document.querySelectorAll('.hidden');
  hiddenElements.forEach(element => {
    element.classList.remove('hidden');
  });
}

function updateNumber() {
  fetch('/updatenumber')
      .then(response => response.json())
      .then(data => {
          const numEl = document.getElementById('dumbbox');
          if (numEl) {
            numEl.innerHTML = data.number;
          }
      });
};

setInterval(updateNumber,1000);

document.querySelector('#test').addEventListener("click", function() {
  console.log("hi");
})
