/**
 * Fit call sheet: estimated propane cost to heat a greenhouse between two dates.
 * Same model as playbook/propagation/propane_weekly_cost.py, 3 years of history.
 *
 * =PROPANE_COST("G1S 2P1", DATE(2027,2,1), DATE(2027,11,1), 100, 30, "double", 3.20)
 *
 * @param {string} postalCode Postal code, zip code or address.
 * @param {Date} heatingStart First day of heating (transplant).
 * @param {Date} heatingEnd Last day of heating (crop out).
 * @param {number} lengthFeet Greenhouse floor length, ft.
 * @param {number} widthFeet Greenhouse floor width, ft.
 * @param {string} covering "single" or "double" poly.
 * @param {number} pricePerGallon Propane price, $/US gal.
 * @return Estimated propane cost, $.
 * @customfunction
 */
function PROPANE_COST(postalCode, heatingStart, heatingEnd, lengthFeet, widthFeet, covering, pricePerGallon) {
  const floorSquareMetres = lengthFeet * widthFeet * 0.0929;
  const dailyKwhPerSquareMetre = dailyHeatDemandByDayOfYear(postalCode, covering);
  let totalKwh = 0;
  for (let day = new Date(heatingStart); day <= heatingEnd; day.setDate(day.getDate() + 1)) {
    totalKwh += dailyKwhPerSquareMetre[monthDayKey(day)] * floorSquareMetres;
  }
  const gallons = totalKwh / (PROPANE_KWH_PER_LITRE * HEATER_EFFICIENCY) / LITRES_PER_US_GALLON;
  return Math.round(gallons * pricePerGallon);
}

const DAY_SETPOINT = 24;
const NIGHT_SETPOINT = 20;
const HEATER_EFFICIENCY = 0.8;
const HISTORY_YEARS = 3;
const ENVELOPE_PER_FLOOR = 1.5;
const U_VALUES = { single: 6.2, double: 4.2 }; // W/m²·°C
const TRANSMITTANCE = { single: 0.85, double: 0.75 }; // solar gain fraction
const PROPANE_KWH_PER_LITRE = 6.9;
const LITRES_PER_US_GALLON = 3.785;
const MISSING = -999;
const WATTS_PER_MEGAJOULE_HOUR = 1e6 / 3600; // MJ/m²/hr → W/m²

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
  Object.keys(hourly.T2M).forEach((stamp) => {
    const temperature = hourly.T2M[stamp];
    const radiation = Math.max(0, hourly.ALLSKY_SFC_SW_DWN[stamp]) * WATTS_PER_MEGAJOULE_HOUR;
    if (temperature === MISSING) return;
    const setpoint = radiation > 0 ? DAY_SETPOINT : NIGHT_SETPOINT;
    const loss = U_VALUES[coveringKey] * ENVELOPE_PER_FLOOR * (setpoint - temperature);
    const gain = TRANSMITTANCE[coveringKey] * radiation;
    const key = `${stamp.slice(4, 6)}-${stamp.slice(6, 8)}`;
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

/** NASA POWER hourly, last HISTORY_YEARS full calendar years, local solar time. */
function hourlyWeather(latitude, longitude) {
  const lastYear = new Date().getFullYear() - 1;
  const url = 'https://power.larc.nasa.gov/api/temporal/hourly/point' +
    '?parameters=T2M,ALLSKY_SFC_SW_DWN&community=AG&format=JSON&time-standard=LST' +
    `&latitude=${latitude}&longitude=${longitude}` +
    `&start=${lastYear - HISTORY_YEARS + 1}0101&end=${lastYear}1231`;
  return JSON.parse(UrlFetchApp.fetch(url).getContentText()).properties.parameter;
}

function monthDayKey(date) {
  const key = Utilities.formatDate(date, Session.getScriptTimeZone(), 'MM-dd');
  return key === '02-29' ? '02-28' : key;
}
