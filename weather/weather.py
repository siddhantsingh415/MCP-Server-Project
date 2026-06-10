from typing import Any

import httpx

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

NWS_API_BASE = "https://api.weather.gov"

USER_AGENT = "weather-app/1.0"

async def makes_news_request(url: str) -> dict[str, Any] | None: 
    '''Make request to NWS API with proper error handling'''
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client: 
        try: 
            response = await client.get(url, headers = headers, timeout = 30.0)
            response.raise_for_status()
            return response.json()
        except Exception: 
            return None


def format_alert(feature: dict) -> str:
    ''' format to be readable '''
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
""" 

@mcp.tool()
async def get_alerts(state: str) -> str: 
    """
    
    Gets weather for given state

    args: 

    state: str 
    name of the state
    
    """

    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await makes_news_request()

    if not data or "features" not in data: 
        return "Unable to fetch alerts or no alerts found"
    
    if not data["features"]:
        return "No active alerts in this state"
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    
    get forecast for a location in lattitude and longitude

    args: 

    latitude: float
    latitude of location

    longitude: float
    longitude of location

    """

    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await makes_news_request(points_url)

    if not points_data:
        return "unable to fetch data at location"
    
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await makes_news_request(forecast_url)

    if not forecast_data: 
        return "unable to fetch forecast for this location"
    
    periods = forecast_data["properties"]["periods"]
    forecasts = []

    for period in periods[:5]:
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]} degrees {period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()