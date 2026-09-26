import os
import time
import requests
import pandas as pd
import gspread

from google.oauth2.service_account import Credentials


# ============================================================
# CONFIGURATION
# ============================================================

EXCEL_FILE = "indian_cities.xlsx"

# Your Google Sheet ID
# Example:
# https://docs.google.com/spreadsheets/d/1ABC123XYZ456/edit
# Sheet ID = 1ABC123XYZ456
SPREADSHEET_ID = os.environ.get("GOOGLE_SHEET_ID")

WORKSHEET_NAME = "Current_Weather"

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

BATCH_SIZE = 100


# ============================================================
# WEATHER CODE MAPPING
# ============================================================

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",

    45: "Fog",
    48: "Depositing rime fog",

    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",

    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",

    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",

    66: "Light freezing rain",
    67: "Heavy freezing rain",

    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",

    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",

    85: "Slight snow showers",
    86: "Heavy snow showers",

    95: "Thunderstorm",

    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


# ============================================================
# GOOGLE SHEETS AUTHENTICATION
# ============================================================

def connect_to_google_sheet():

    if not SPREADSHEET_ID:
        raise ValueError(
            "GOOGLE_SHEET_ID environment variable is missing."
        )

    credentials_path = "google_credentials.json"

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            "google_credentials.json was not found."
        )

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_file(
        credentials_path,
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    try:
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

    except gspread.WorksheetNotFound:

        worksheet = spreadsheet.add_worksheet(
            title=WORKSHEET_NAME,
            rows=1000,
            cols=30
        )

    return worksheet


# ============================================================
# READ EXCEL CITY MASTER
# ============================================================

def load_city_data():

    print("Reading Excel file...")

    df = pd.read_excel(EXCEL_FILE)

    # Clean column names
    df.columns = df.columns.str.strip()

    required_columns = [
        "City",
        "State",
        "Latitude",
        "Longitude"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in Excel: {missing_columns}"
        )

    # Keep only required columns
    df = df[required_columns].copy()

    # Convert coordinates
    df["Latitude"] = pd.to_numeric(
        df["Latitude"],
        errors="coerce"
    )

    df["Longitude"] = pd.to_numeric(
        df["Longitude"],
        errors="coerce"
    )

    # Remove invalid rows
    df = df.dropna(
        subset=[
            "City",
            "State",
            "Latitude",
            "Longitude"
        ]
    )

    # Remove invalid geographical coordinates
    df = df[
        (df["Latitude"] >= -90)
        & (df["Latitude"] <= 90)
        & (df["Longitude"] >= -180)
        & (df["Longitude"] <= 180)
    ]

    # Remove duplicate cities/coordinates
    df = df.drop_duplicates(
        subset=["City", "State", "Latitude", "Longitude"]
    )

    df = df.reset_index(drop=True)

    print(f"Cities loaded: {len(df)}")

    return df


# ============================================================
# FETCH WEATHER FROM OPEN-METEO
# ============================================================

def fetch_weather_batch(batch):

    latitudes = ",".join(
        batch["Latitude"].astype(str)
    )

    longitudes = ",".join(
        batch["Longitude"].astype(str)
    )

    params = {
        "latitude": latitudes,
        "longitude": longitudes,

        "current": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "weather_code",
            "cloud_cover",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
        ]),

        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
        "timezone": "auto",
    }

    response = requests.get(
        OPEN_METEO_URL,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    # Multiple coordinates return a list
    if isinstance(data, dict):
        data = [data]

    results = []

    for city_row, weather in zip(
        batch.itertuples(index=False),
        data
    ):

        current = weather.get("current", {})

        weather_code = current.get(
            "weather_code"
        )

        result = {
            "City": city_row.City,
            "State": city_row.State,

            "Latitude": city_row.Latitude,
            "Longitude": city_row.Longitude,

            "Weather_Time": current.get(
                "time"
            ),

            "Timezone": weather.get(
                "timezone"
            ),

            "Temperature_C": current.get(
                "temperature_2m"
            ),

            "Feels_Like_C": current.get(
                "apparent_temperature"
            ),

            "Humidity_Percent": current.get(
                "relative_humidity_2m"
            ),

            "Precipitation_mm": current.get(
                "precipitation"
            ),

            "Rain_mm": current.get(
                "rain"
            ),

            "Weather_Code": weather_code,

            "Weather_Condition": WEATHER_CODES.get(
                weather_code,
                "Unknown"
            ),

            "Cloud_Cover_Percent": current.get(
                "cloud_cover"
            ),

            "Wind_Speed_kmh": current.get(
                "wind_speed_10m"
            ),

            "Wind_Direction_deg": current.get(
                "wind_direction_10m"
            ),

            "Wind_Gusts_kmh": current.get(
                "wind_gusts_10m"
            ),

            "Fetched_At_UTC": pd.Timestamp.now(
                tz="UTC"
            ).strftime("%Y-%m-%d %H:%M:%S"),
        }

        results.append(result)

    return results


# ============================================================
# FETCH ALL WEATHER DATA
# ============================================================

def get_all_weather(city_df):

    all_results = []

    total_cities = len(city_df)

    for start in range(
        0,
        total_cities,
        BATCH_SIZE
    ):

        end = min(
            start + BATCH_SIZE,
            total_cities
        )

        batch = city_df.iloc[
            start:end
        ]

        print(
            f"Fetching cities "
            f"{start + 1}-{end} "
            f"of {total_cities}..."
        )

        try:

            batch_results = fetch_weather_batch(
                batch
            )

            all_results.extend(
                batch_results
            )

        except Exception as e:

            print(
                f"ERROR in batch "
                f"{start + 1}-{end}: {e}"
            )

            raise

    return pd.DataFrame(all_results)


# ============================================================
# UPDATE GOOGLE SHEETS
# ============================================================

def update_google_sheet(
    worksheet,
    weather_df
):

    print("Updating Google Sheet...")

    # Convert NaN to empty strings
    weather_df = weather_df.fillna("")

    # Convert dataframe to list
    values = [
        weather_df.columns.tolist()
    ] + weather_df.astype(str).values.tolist()

    # Clear old snapshot
    worksheet.clear()

    # Write new snapshot
    worksheet.update(
        values,
        "A1",
        raw=True
    )

    print(
        f"Google Sheet updated with "
        f"{len(weather_df)} cities."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    start_time = time.time()

    print("=" * 60)
    print("INDIA WEATHER AUTOMATION")
    print("=" * 60)

    try:

        # 1. Read Excel
        city_df = load_city_data()

        # 2. Fetch weather
        weather_df = get_all_weather(
            city_df
        )

        # 3. Save local backup
        weather_df.to_csv(
            "latest_weather_backup.csv",
            index=False
        )

        # 4. Connect Google Sheets
        worksheet = connect_to_google_sheet()

        # 5. Update Google Sheets
        update_google_sheet(
            worksheet,
            weather_df
        )

        elapsed = time.time() - start_time

        print("=" * 60)
        print("SUCCESS")
        print(
            f"Cities updated: {len(weather_df)}"
        )
        print(
            f"Execution time: {elapsed:.2f} seconds"
        )
        print("=" * 60)

    except Exception as e:

        print("=" * 60)
        print("AUTOMATION FAILED")
        print("=" * 60)

        print(str(e))

        raise


if __name__ == "__main__":
    main()