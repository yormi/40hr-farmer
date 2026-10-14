/**
 * Fit call sheet: estimated propane cost to heat a greenhouse between two dates.
 * Same model as playbook/propagation/propane_weekly_cost.py, 3 years of history.
 *
 * =PROPANE_COST("G1S 2P1", DATE(2027,2,1), DATE(2027,11,1), 100, 30, "double", 0.85)
 *
 * @param {string} postalCode Postal code, zip code or address.
 * @param {Date} heatingStart First day of heating (transplant).
 * @param {Date} heatingEnd Last day of heating (crop out).
 * @param {number} lengthFeet Greenhouse floor length, ft.
 * @param {number} widthFeet Greenhouse floor width, ft.
 * @param {string} covering "single" or "double" poly.
 * @param {number} pricePerLitre Propane price, $/L.
 * @return Estimated propane cost, $.
 * @customfunction
 */
function PROPANE_COST(postalCode, heatingStart, heatingEnd, lengthFeet, widthFeet, covering, pricePerLitre) {
  const floorSquareMetres = lengthFeet * widthFeet * 0.0929;
  const dailyKwhPerSquareMetre = dailyHeatDemandByDayOfYear(postalCode, covering);
  let totalKwh = 0;
  for (let day = new Date(heatingStart); day <= heatingEnd; day.setDate(day.getDate() + 1)) {
    totalKwh += dailyKwhPerSquareMetre[monthDayKey(day)] * floorSquareMetres;
  }
  const litres = totalKwh / (PROPANE_KWH_PER_LITRE * HEATER_EFFICIENCY);
  return Math.round(litres * pricePerLitre);
}

const DAY_SETPOINT = 24;
const NIGHT_SETPOINT = 20;
const HEATER_EFFICIENCY = 0.8;
const HISTORY_YEARS = 3;
const ENVELOPE_PER_FLOOR = 1.5;
const U_VALUES = { single: 6.2, double: 4.2 }; // W/m²·°C
const TRANSMITTANCE = { single: 0.85, double: 0.75 }; // solar gain fraction
const PROPANE_KWH_PER_LITRE = 6.9;

/** Mean kWh per floor m² for each month-day, averaged over HISTORY_YEARS. Cached 6 h. */
function dailyHeatDemandByDayOfYear(postalCode, covering) {
  const coveringKey = String(covering).toLowerCase();
  if (!(coveringKey in U_VALUES)) throw new Error('covering must be "single" or "double"');
  const cache = CacheService.getScriptCache();
  const cacheKey = `propane:${postalCode}:${coveringKey}`;
  const cached = cache.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const location = geocode(postalCode);
  const hourly = hourlyWeather(location.latitude, location.longitude);
  const totals = {};
  const yearsSeen = {};
  hourly.time.forEach((stamp, index) => {
    const temperature = hourly.temperature_2m[index];
    if (temperature === null) return;
    const setpoint = hourly.is_day[index] ? DAY_SETPOINT : NIGHT_SETPOINT;
    const loss = U_VALUES[coveringKey] * ENVELOPE_PER_FLOOR * (setpoint - temperature);
    const gain = TRANSMITTANCE[coveringKey] * (hourly.shortwave_radiation[index] || 0);
    const key = stamp.slice(5, 10);
    totals[key] = (totals[key] || 0) + Math.max(0, loss - gain) / 1000;
    (yearsSeen[key] = yearsSeen[key] || {})[stamp.slice(0, 4)] = true;
  });
  const demand = {};
  Object.keys(totals).forEach((key) => {
    demand[key] = totals[key] / Object.keys(yearsSeen[key]).length;
  });
  cache.put(cacheKey, JSON.stringify(demand), 21600);
  return demand;
}

function geocode(postalCode) {
  const response = Maps.newGeocoder().geocode(String(postalCode));
  if (response.status !== 'OK') throw new Error(`Location not found: ${postalCode}`);
  const location = response.results[0].geometry.location;
  return { latitude: location.lat, longitude: location.lng };
}

function hourlyWeather(latitude, longitude) {
  const end = new Date();
  end.setDate(end.getDate() - 7);
  const start = new Date(end);
  start.setFullYear(end.getFullYear() - HISTORY_YEARS);
  const isoDate = (date) => Utilities.formatDate(date, 'UTC', 'yyyy-MM-dd');
  const url = 'https://archive-api.open-meteo.com/v1/archive' +
    `?latitude=${latitude}&longitude=${longitude}` +
    `&start_date=${isoDate(start)}&end_date=${isoDate(end)}` +
    '&hourly=temperature_2m,is_day,shortwave_radiation&timezone=auto';
  return JSON.parse(UrlFetchApp.fetch(url).getContentText()).hourly;
}

function monthDayKey(date) {
  const key = Utilities.formatDate(date, Session.getScriptTimeZone(), 'MM-dd');
  return key === '02-29' ? '02-28' : key;
}
