
// --- DOM References ---
const slider = document.getElementById("myRange");
const output = document.getElementById("valueOutput");
const gridButton = document.getElementById("grid-on-off");
const gridStatus = document.getElementById("grid-status");
const gridOutput = document.getElementById("grid-output");
const gridBila2 = document.getElementById("bila2");
const loadBila4 = document.getElementById("bila4");
const solarSlider = document.getElementById("solar-slider");
const solarOutput = document.getElementById("solar-output");
const solarBila1 = document.getElementById("bila1");
const batteryValue = document.getElementById("battery-value");
const batteryChargeAnimation = document.getElementById("bila3-charge");
const batteryDischargeAnimation = document.getElementById("bila3-discharge");

// --- Get CSRF token from cookie ---
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie("csrftoken");

// --- Access Django variables ---
const urls = window.DJANGO_URLS;
const data = window.DJANGO_DATA;

// Initialize from Django context (on page load) 
if (data) {
    gridStatus.textContent = data.gridText;
    gridStatus.style.color = data.gridColor;
    gridOutput.textContent = data.gridNumber;
    gridBila2.style.display = data.gridAnimation;

    solarBila1.style.display = data.solarAnimation;
    solarSlider.textContent = data.solarSliderValue;

    loadBila4.style.display = data.loadAnimation;

    batteryChargeAnimation.style.display = data.batteryChargeOnOff;
    batteryDischargeAnimation.style.display = data.batteryDischargeOnOff;
}

// this is for grid it saves to db then checks for any changes
gridButton.addEventListener("click", () => saveGridToDatabase());
fetchGrid();
// this is for the house load saves to db then checks for changes
slider.addEventListener("change", () => saveLoadToDatabase());
fetchLoad();
// this is for max solar production saves to db and then checks fro changes
solarSlider.addEventListener("change", () => saveSolarMaxProductionToDatabase());
fetchSolar();



const openPopup = document.getElementById('openPopup');
const closePopup = document.getElementById('closePopup');
const popupOverlay = document.getElementById('popupOverlay');

openPopup.addEventListener('click', () => {
    popupOverlay.style.display = 'flex';
});

closePopup.addEventListener('click', () => {
    popupOverlay.style.display = 'none';
});

// Optional: Close when clicking outside popup
popupOverlay.addEventListener('click', (e) => {
    if (e.target === popupOverlay) {
    popupOverlay.style.display = 'none';
    }
});

// Functions

// ---- Save Load to DB ----
function saveLoadToDatabase() {
    fetch(urls.load_status, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ value: slider.value }),
    })
        .then((res) => res.json())
        .then((data) => {
            output.textContent = data.value;
            slider.value = data.value;
        })
        .catch(console.error);
}

// ---- Fetch Load ----
function fetchLoad() {
    fetch(urls.get_slider_value)
        .then(res => res.json())
        .then(data => {
            output.textContent = data.value;
            slider.value = data.value;
            loadBila4.style.display = data.value === 0 ? "none" : "flex";
            batteryCharge();
            setTimeout(fetchLoad, 1000);
        })
        .catch(() => setTimeout(fetchLoad, 2000));
}

// ---- Save Grid to DB ----
function saveGridToDatabase() {
    fetch(urls.gridStatus, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    }).catch(console.error);
}

// ---- Fetch Grid ----
function fetchGrid() {
    fetch(urls.grid_update)
        .then((res) => res.json())
        .then((data) => {
            if (data.grid === true) {
                gridStatus.textContent = "On grid";
                gridStatus.style.color = "#6dd07f";
                gridOutput.textContent = "20";
                gridBila2.style.display = "flex";
            } else {
                gridStatus.textContent = "Off grid";
                gridStatus.style.color = "red";
                gridOutput.textContent = "0";
                gridBila2.style.display = "none";
            }
            setTimeout(fetchGrid, 1000);
        })
        .catch(() => setTimeout(fetchGrid, 2000));
}

// ---- Save Solar Production ----
function saveSolarMaxProductionToDatabase() {
    fetch(urls.save_solar, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ solarValue: solarSlider.value }),
    })
        .then((res) => res.json())
        .then((data) => {
            solarOutput.textContent = data.solarValue;
            solarSlider.value = data.solarValue;
        })
        .catch(console.error);
}

// ---- Fetch Solar ----
function fetchSolar() {
    fetch(urls.update_solar)
        .then((res) => res.json())
        .then((data) => {
            solarOutput.textContent = data.solar;
            solarSlider.value = data.solar;
            solarBila1.style.display = data.solar === 0 ? "none" : "flex";
            batteryCharge();
            setTimeout(fetchSolar, 1000);
        })
        .catch(() => setTimeout(fetchSolar, 2000));
}

const battery_procent = document.getElementById("battery-procent");
// ---- Fetch Battery Charge ----
function batteryCharge() {
    fetch(urls.battery_charge)
        .then((res) => res.json())
        .then((data) => {
            batteryValue.textContent = data.bateryChargeValue;
            battery_procent.textContent = data.batteryPercent;
            if (data.bateryChargeValue > 0) {
                batteryChargeAnimation.style.display = "flex";
                batteryDischargeAnimation.style.display = "none";
            } else if (data.bateryChargeValue < 0) {
                batteryChargeAnimation.style.display = "none";
                batteryDischargeAnimation.style.display = "flex";
            } else {
                batteryChargeAnimation.style.display = "none";
                batteryDischargeAnimation.style.display = "none";
            }
        })
        .catch(() => setTimeout(batteryCharge, 2000));
}
