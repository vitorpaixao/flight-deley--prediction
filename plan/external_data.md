# External Data Research for Flight Delay Prediction

This document catalogs public external datasets that could improve delay prediction models built on the 2015 US domestic flights dataset (`flights.csv`, ~5.8M rows).

---

## 1. Weather Data

### 1.1 Iowa Mesonet ASOS (Recommended)

- **URL:** https://mesonet.agron.iastate.edu/request/download.phtml
- **Format:** CSV (custom query builder)
- **Key fields:** `station`, `valid` (timestamp), `tmpf` (temp °F), `dwpf` (dewpoint), `relh` (humidity), `drct` (wind direction), `sknt` (wind speed knots), `p01i` (1-hour precip inches), `vsby` (visibility miles), `skyc1`–`skyc3` (sky cover), `presentwx` (present weather codes: RA, SN, FG, TS, etc.)
- **Coverage:** Hourly observations from ASOS stations co-located at most US airports
- **Join strategy:** Map `ORIGIN_AIRPORT` (IATA code) → ASOS station ID (typically K + IATA, e.g., `ORD` → `KORD`). Match on date (`YEAR`, `MONTH`, `DAY`) and round `SCHEDULED_DEPARTURE` to nearest hour.
- **Cost:** Free
- **Why recommended:** Hourly granularity at the airport itself; simple CSV download; no API key needed; covers all major US airports.

### 1.2 NOAA Integrated Surface Database (ISD)

- **URL:** https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database
- **Format:** Fixed-width text or CSV (via `isdlite`)
- **Key fields:** `TEMP`, `DEW_POINT`, `WIND_SPEED`, `WIND_DIR`, `VISIBILITY`, `CEILING_HEIGHT`, `PRECIPITATION`
- **Join strategy:** Map airport IATA → USAF/WBAN station ID via station history file. Join on date+hour as above.
- **Cost:** Free
- **Notes:** More comprehensive than ASOS but requires station ID mapping. ISD-Lite is a simplified subset good for bulk analysis.

### 1.3 GHCN-Daily

- **URL:** https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily
- **Format:** CSV
- **Key fields:** `TMAX`, `TMIN`, `PRCP`, `SNOW`, `SNWD` (snow depth), `AWND` (avg wind)
- **Join strategy:** Map airport → nearest GHCN station (many airports have co-located stations). Join on `YEAR`, `MONTH`, `DAY`.
- **Cost:** Free
- **Notes:** Daily granularity only — less precise than ASOS but simpler to work with. Good for snowfall and temperature extremes.

### 1.4 Open-Meteo Historical Weather API

- **URL:** https://open-meteo.com/en/docs/historical-weather-api
- **Format:** JSON API
- **Key fields:** `temperature_2m`, `precipitation`, `windspeed_10m`, `visibility`, `weathercode`
- **Join strategy:** Query by airport lat/lon and date. Match on `YEAR`, `MONTH`, `DAY` and hour.
- **Cost:** Free (up to 10,000 requests/day, non-commercial)
- **Notes:** Convenient API but rate-limited. Good for filling gaps or quick prototyping.

### 1.5 Meteostat

- **URL:** https://meteostat.net/en/
- **Format:** JSON API / Python library (`meteostat`)
- **Key fields:** `temp`, `dwpt`, `rhum`, `prcp`, `snow`, `wdir`, `wspd`, `pres`, `coco` (weather condition code)
- **Join strategy:** Query by nearest weather station to airport coordinates. Join on date+hour.
- **Cost:** Free
- **Notes:** Python library makes integration easy. Hourly and daily endpoints available.

---

## 2. Holidays & Travel Seasons

### 2.1 US Federal Holidays (2015)

| Holiday | Date | Expected Impact |
|---|---|---|
| New Year's Day | Thu, Jan 1 | High — post-holiday return travel |
| Martin Luther King Jr. Day | Mon, Jan 19 | Moderate — long weekend |
| Presidents' Day | Mon, Feb 16 | Moderate — long weekend + ski travel |
| Memorial Day | Mon, May 25 | High — summer travel kickoff |
| Independence Day | Sat, Jul 4 | High — peak summer travel |
| Labor Day | Mon, Sep 7 | High — end of summer travel |
| Columbus Day | Mon, Oct 12 | Low–moderate |
| Veterans Day | Wed, Nov 11 | Low–moderate |
| Thanksgiving | Thu, Nov 26 | Very high — busiest travel period |
| Christmas | Fri, Dec 25 | Very high — holiday travel season |

### 2.2 Travel Windows

- **Thanksgiving window:** Nov 22–29, 2015 (Sun before through Sun after)
- **Christmas/New Year window:** Dec 18, 2015 – Jan 3, 2016
- **Spring break:** Varies by region; typically mid-March through mid-April
- **Summer peak:** Jun 15 – Aug 15

### 2.3 Join Strategy

Create a binary feature `IS_HOLIDAY` and/or `DAYS_TO_NEAREST_HOLIDAY` derived from `YEAR`, `MONTH`, `DAY`. Also create `IS_TRAVEL_WINDOW` for the extended periods above. No external file needed — can be hard-coded as a Python dictionary or small CSV.

### 2.4 Source for Holiday Dates

- **URL:** https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/#url=2015
- **Format:** HTML (manual extraction or scrape)
- **Cost:** Free

---

## 3. Major Events (2015)

| Event | Dates | City | Affected Airports |
|---|---|---|---|
| CES (Consumer Electronics Show) | Jan 6–9 | Las Vegas, NV | LAS |
| Super Bowl XLIX | Feb 1 | Glendale, AZ | PHX |
| SXSW | Mar 13–22 | Austin, TX | AUS |
| NCAA Men's Final Four | Apr 4–6 | Indianapolis, IN | IND |
| Kentucky Derby | May 2 | Louisville, KY | SDF |
| NBA Finals (Warriors vs Cavaliers) | Jun 4–16 | Oakland/Cleveland | OAK, SFO, CLE |
| San Diego Comic-Con | Jul 9–12 | San Diego, CA | SAN |
| US Open (Tennis) | Aug 31 – Sep 13 | New York, NY | JFK, LGA, EWR |
| World Series (Royals vs Mets) | Oct 27 – Nov 1 | Kansas City/New York | MCI, JFK, LGA, EWR |
| Thanksgiving (Macy's Parade, etc.) | Nov 26 | Nationwide | All |

### Join Strategy

Create a lookup table of (date range, airport list) pairs. For each flight, flag `IS_MAJOR_EVENT = 1` if `ORIGIN_AIRPORT` or `DESTINATION_AIRPORT` is in the affected airport set and the flight date falls within the event window. Join on `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT`, `YEAR`, `MONTH`, `DAY`.

---

## 4. Severe Weather Events (2015)

### 4.1 Winter Storm Juno

- **Dates:** Jan 26–28, 2015
- **Region:** Northeast US (New York, Boston, New England)
- **Impact:** ~7,700 flight cancellations; NYC airports (JFK, LGA, EWR) closed; Boston (BOS) severely affected
- **Source:** https://en.wikipedia.org/wiki/January_2015_North_American_blizzard

### 4.2 Record Boston Snowfall

- **Period:** Jan–Feb 2015 (multiple storms)
- **Impact:** Boston received 110.6 inches of snow in winter 2014–15, breaking records. BOS experienced chronic delays and cancellations through February.
- **Affected airports:** BOS, PVD, BDL

### 4.3 February Northeast Storms

- **Dates:** Feb 2, Feb 8–9, Feb 14–15, Feb 21–22, 2015
- **Region:** Northeast
- **Impact:** Cumulative disruption across BOS, JFK, LGA, EWR, PHL, DCA, IAD, BWI

### 4.4 Hurricane Joaquin

- **Dates:** Sep 28 – Oct 3, 2015 (closest approach to US: Oct 1–3)
- **Region:** Bahamas, East Coast US (heavy rain even though it didn't make landfall)
- **Impact:** East Coast flooding caused moderate cancellations at MIA, FLL, CLT, JFK
- **Source:** https://en.wikipedia.org/wiki/Hurricane_Joaquin

### 4.5 December 2015 Storms

- **Dates:** Dec 26–28, 2015 (winter storm Goliath)
- **Region:** Southern Plains, Midwest, Northeast
- **Impact:** Tornadoes in TX, blizzards in NM/TX, flooding; ~2,000 flight cancellations
- **Affected airports:** DFW, DAL, ABQ, OKC, MCI

### Join Strategy

Create a severe weather event table with (start_date, end_date, affected_airports). Flag flights with `IS_SEVERE_WEATHER_EVENT`. Join on date and `ORIGIN_AIRPORT` / `DESTINATION_AIRPORT`.

---

## 5. Airport Metadata

### 5.1 OurAirports

- **URL:** https://ourairports.com/data/
- **Format:** CSV (`airports.csv`)
- **Key fields:** `ident` (ICAO), `iata_code`, `type` (large_airport, medium_airport, small_airport), `latitude_deg`, `longitude_deg`, `elevation_ft`, `municipality`, `iso_region`
- **Supplementary file:** `runways.csv` — `length_ft`, `width_ft`, `surface`, `lighted`
- **Join strategy:** Join on `iata_code` = `ORIGIN_AIRPORT` (or `DESTINATION_AIRPORT`)
- **Cost:** Free (public domain)
- **Notes:** Elevation and runway count can proxy for terrain difficulty and airport capacity.

### 5.2 OpenFlights

- **URL:** https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat
- **Format:** CSV (no header)
- **Key fields:** `Name`, `City`, `Country`, `IATA`, `ICAO`, `Latitude`, `Longitude`, `Altitude`, `Timezone` (UTC offset), `DST` (daylight saving rule), `Tz` (Olson timezone)
- **Join strategy:** Join on `IATA` = `ORIGIN_AIRPORT`
- **Cost:** Free (ODbL license)
- **Notes:** Timezone info is useful for converting `SCHEDULED_DEPARTURE` (local time) to UTC for proper temporal features.

### 5.3 FAA Hub Classification

- **URL:** https://www.faa.gov/airports/planning_capacity/categories
- **Format:** PDF / HTML table
- **Key fields:** Airport code, hub size (Large, Medium, Small, Non-hub)
- **Join strategy:** Map `ORIGIN_AIRPORT` → hub category
- **Cost:** Free
- **Notes:** Hub size is a strong proxy for congestion and delay propagation.

---

## 6. Air Traffic Volume

### 6.1 BTS T-100 Domestic Segment Data

- **URL:** https://www.transtats.bts.gov/Tables.asp?QO_VQ=EFI&QO_anzr=Nv4%20Pn44vr4%20Fgngvfgvpf%20%28Sbez%2041%20Genssvp%29-%20%20N77%20Pn44vr45&QO_fu146_anzr=Nv4%20Pn44vr4%20Fgngvfgvpf
- **Format:** CSV (downloadable via BTS query tool)
- **Key fields:** `ORIGIN`, `DEST`, `DEPARTURES_PERFORMED`, `PASSENGERS`, `SEATS`, `CARRIER`, `MONTH`, `YEAR`
- **Join strategy:** Aggregate to monthly departures per airport. Join on `ORIGIN_AIRPORT` = `ORIGIN`, `YEAR`, `MONTH`.
- **Cost:** Free
- **Notes:** Monthly granularity. Useful as a congestion proxy — airports with more departures tend to have more delays.

---

## 7. Economic / Fuel Data

### 7.1 EIA Jet Fuel Prices

- **URL:** https://www.eia.gov/dnav/pet/pet_pri_spt_s1_w.htm
- **Format:** CSV / XLS (weekly)
- **Key fields:** `Date`, `U.S. Gulf Coast Kerosene-Type Jet Fuel Spot Price ($/gal)`
- **Join strategy:** Match flight date to nearest weekly price. Join on `YEAR`, `MONTH`, `DAY` (round to week).
- **Cost:** Free
- **Notes:** Low priority. Fuel prices may affect airline scheduling decisions and route profitability, but indirect effect on delays.

### 7.2 FRED Economic Indicators

- **URL:** https://fred.stlouisfed.org/
- **Format:** CSV / JSON API
- **Key fields:** GDP growth, unemployment rate, consumer confidence
- **Join strategy:** Monthly or quarterly values joined on `YEAR`, `MONTH`.
- **Cost:** Free
- **Notes:** Low priority. Macroeconomic indicators have weak direct relationship with individual flight delays.

---

## 8. FAA System Data

### 8.1 FAA Ground Delay Programs (GDP) Archive

- **URL:** https://www.fly.faa.gov/Products/GDPArchive.html
- **Format:** HTML / text logs
- **Key fields:** Airport, program start/end times, average delay, reason (weather, volume, equipment)
- **Join strategy:** Map GDP events to `ORIGIN_AIRPORT` or `DESTINATION_AIRPORT` and date. Flag `IS_GDP_ACTIVE`.
- **Cost:** Free
- **Notes:** Directly captures ATC-imposed delays. Parsing required as format is semi-structured.

### 8.2 FAA OPSNET Delay Data

- **URL:** https://aspm.faa.gov/opsnet/sys/main.asp
- **Format:** CSV (query builder)
- **Key fields:** Airport, date, delay cause (weather, volume, equipment, runway, other), number of delays > 15 min
- **Join strategy:** Daily airport-level delay counts. Join on `ORIGIN_AIRPORT`, `YEAR`, `MONTH`, `DAY`.
- **Cost:** Free (requires FAA ASPM account, free registration)
- **Notes:** High value — provides the FAA's own delay attribution. Good for validating model predictions.

---

## Priority Matrix

Sources ranked by **(Predictive Value) × (Ease of Integration)**:

| Priority | Source | Predictive Value | Ease of Integration | Notes |
|---|---|---|---|---|
| **1 (Critical)** | Iowa Mesonet ASOS | ★★★★★ | ★★★★★ | Weather is the #1 delay cause; CSV download, easy join |
| **2 (High)** | Holidays / Travel Windows | ★★★★☆ | ★★★★★ | Simple to create; known demand spikes |
| **3 (High)** | OurAirports metadata | ★★★★☆ | ★★★★★ | Static join; elevation, runway count, airport type |
| **4 (High)** | Severe Weather Events | ★★★★★ | ★★★★☆ | Small lookup table; captures extreme disruptions |
| **5 (High)** | FAA Hub Classification | ★★★★☆ | ★★★★☆ | Small table; strong congestion proxy |
| **6 (Medium)** | BTS T-100 Traffic Volume | ★★★★☆ | ★★★☆☆ | Monthly granularity limits precision; BTS download |
| **7 (Medium)** | Major Events | ★★★☆☆ | ★★★★☆ | Small effect radius; manual table creation |
| **8 (Medium)** | OpenFlights (timezones) | ★★★☆☆ | ★★★★★ | Enables UTC conversion for time-of-day features |
| **9 (Medium)** | FAA OPSNET | ★★★★★ | ★★☆☆☆ | High value but needs FAA account + scraping |
| **10 (Medium)** | NOAA ISD / GHCN-Daily | ★★★★☆ | ★★★☆☆ | Alternatives to ASOS; more complex station mapping |
| **11 (Low)** | FAA GDP Archive | ★★★★☆ | ★★☆☆☆ | Semi-structured logs need parsing |
| **12 (Low)** | Open-Meteo / Meteostat | ★★★☆☆ | ★★★☆☆ | API rate limits for 5.8M rows; good for prototyping |
| **13 (Low)** | EIA Jet Fuel Prices | ★★☆☆☆ | ★★★★☆ | Indirect effect on delays |
| **14 (Low)** | FRED Economic Indicators | ★☆☆☆☆ | ★★★★☆ | Weak relationship to individual flight delays |

### Recommended Implementation Order

1. **Quick wins (no external download):** Holidays, travel windows, severe weather event flags — all can be hard-coded from this document.
2. **High-impact external data:** Iowa Mesonet ASOS weather + OurAirports metadata — two CSV downloads that cover the two most important external factors (weather and airport characteristics).
3. **If time permits:** BTS T-100 traffic volume, FAA hub classification, major events table.
