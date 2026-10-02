# 🌦️ India Weather Monitoring & Analytics Dashboard

> **A real-time weather analytics dashboard built with Looker Studio to monitor and analyze weather conditions across cities in India.**

## 📌 Project Overview

As part of my Data Analytics learning journey, I wanted to learn **Looker Studio** and understand how it can be used to build interactive, continuously updated dashboards.
Instead of learning the tool only through tutorials, I followed a **project-based learning approach** and built the **India Weather Monitoring & Analytics Dashboard**.
The dashboard brings together weather data from cities across India and transforms it into interactive visualizations, KPIs, geographic analysis, and analytical insights.

---

## 🎯 Project Objectives

* Learn and apply **Looker Studio** in a real-world analytics project
* Build an interactive weather monitoring dashboard
* Analyze weather patterns across Indian cities
* Create meaningful KPIs for quick insights
* Visualize geographic differences in weather conditions
* Explore relationships between weather variables
* Work with continuously updated data

---

## 🛠️ Tools & Technologies

| Tool               | Purpose                                      |
| ------------------ | -------------------------------------------- |
| **Python**         | Data collection and processing               |
| **Google Sheets**  | Data storage and connection to Looker Studio |
| **Looker Studio**  | Dashboard development and visualization      |
| **GitHub Actions** | Automated data updates                       |
| **Weather API**    | Real-time weather data source                |

---

## 📊 Dataset

The dashboard uses weather data collected for cities across India.

### Key fields include:

* City
* State
* Latitude
* Longitude
* Weather Time
* Timezone
* Temperature (°C)
* Feels Like Temperature (°C)
* Humidity (%)
* Precipitation (mm)
* Rainfall (mm)
* Weather Code
* Weather Condition
* Cloud Cover (%)
* Wind Speed (km/h)
* Wind Direction (°)
* Wind Gusts (km/h)
* Data Fetch Timestamp

The dataset is automatically updated so that the dashboard can reflect the latest available weather information.

---

# 📑 Dashboard Structure

The project contains **2 interactive dashboard pages** in Looker Studio.

## 📍 Page 1 — Weather Overview

The first page provides a high-level overview of weather conditions across India.

### Key Components

* 🌡️ Average Temperature
* 💧 Average Humidity
* 🌧️ Total Rainfall
* 🌬️ Average Wind Speed
* 🗺️ Geographic weather visualization
* Weather condition distribution
* City-level weather information
* Interactive filters

This page is designed for quickly understanding the current weather situation across different locations.

---

## 📈 Page 2 — Weather Analytics

The second page focuses on deeper analysis and relationships between weather variables.

### Key Visualizations

* **Temperature vs Humidity**
* **Rainfall by City**
* **Weather Conditions by Location**
* **Geographic/Bubble Map Analysis**
* City-level comparisons
* Weather metric comparisons

These visualizations help identify patterns and differences between cities.

---

# 🔍 Key Analytical Questions

The dashboard was designed around questions such as:

* Which cities recorded the highest rainfall?
* Which cities have the highest and lowest temperatures?
* How does temperature vary across India?
* What is the relationship between temperature and humidity?
* Which cities are experiencing different weather conditions?
* How does rainfall vary geographically?
* Which locations experience stronger winds?

---

# ⚙️ Data Pipeline

The project follows an automated data pipeline:

```text
Weather API
     ↓
Python Data Processing
     ↓
Google Sheets
     ↓
Looker Studio
     ↓
Interactive Dashboard
```

### Automation

**GitHub Actions** is used to automate the data update process.

The workflow periodically runs the Python script, retrieves updated weather information, and updates the Google Sheets data source connected to Looker Studio.

This allows the dashboard to function as a **continuously updated weather monitoring system** rather than a static dataset project.

---

# 📊 Dashboard Features

### Interactive Filters

Users can explore the dashboard by filtering weather information based on locations and other available dimensions.

### KPI Cards

Key metrics are presented using KPI cards for quick interpretation.

### Geographic Visualization

Maps and bubble charts are used to visualize weather conditions geographically across Indian cities.

### Analytical Charts

Different chart types are used to explore relationships and comparisons between weather variables.

---

# 💡 What I Learned

This project was primarily a **project-based learning experience for Looker Studio**.

Through this project, I learned how to:

* Connect Google Sheets with Looker Studio
* Build interactive dashboards
* Create KPI scorecards
* Configure chart dimensions and metrics
* Use different aggregation methods
* Build geographic visualizations
* Create bubble maps
* Analyze relationships using scatter charts
* Add filters and interactive controls
* Design a multi-page analytical report
* Connect automated data updates to a BI dashboard

More importantly, I learned that **building a project is one of the most effective ways to learn a new analytics tool.**

---

# 🚀 Future Improvements

Some potential improvements for future versions include:

* Add more cities and weather parameters
* Add historical weather trends
* Introduce date-based analysis
* Add weather alerts and thresholds
* Add forecasting capabilities
* Create more advanced regional comparisons
* Integrate additional weather APIs
* Expand the dashboard with historical vs. current weather analysis

---

# 📂 Project Structure

```text
India-Weather-Monitoring-Analytics/
│
├── weather_updater.py
├── weather_update.yml
├── data/
│   └── indian_cities.xlsx
│
├── README.md
└── screenshots/
    ├── weather_overview.png
    └── weather_patterns.png
```

---

# 📸 Dashboard Preview

### Page 1 — Weather Overview

https://github.com/YASHIKAANEJA/INDIA-WEATHER-ANALYTICS/blob/main/weather%20overview.png

### Page 2 — Weather Analytics

https://github.com/YASHIKAANEJA/INDIA-WEATHER-ANALYTICS/blob/main/weather%20patterns.png

---

# 🎓 Learning Journey

This project started with a simple goal:

> **I wanted to learn Looker Studio as a Data Analyst skill.**

Rather than stopping at tutorials, I decided to learn by building a complete project around a real-world use case.
The result was the **India Weather Monitoring & Analytics Dashboard** — combining automated data collection, Google Sheets, Looker Studio, data visualization, and analytics into one project.


