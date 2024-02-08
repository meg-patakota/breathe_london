import os
import requests
import pandas as pd

class SensorDataManager:
    """
    A class to manage sensor data from the Breathe London API.

    Attributes:
        api_key (str): API key for authenticating requests to the Breathe London API.
        api_url (str): URL for the ListSensors endpoint of the Breathe London API.
    """

    def __init__(self, api_key: str, api_url: str = "https://api.breathelondon.org/api/ListSensors"):
        """
        Initializes the SensorDataManager with an API key and optionally a custom API URL.

        Parameters:
            api_key (str): API key for authenticating requests.
            api_url (str): URL for the ListSensors endpoint. Default is set to Breathe London's ListSensors API.
        """
        self.api_key = api_key
        self.api_url = api_url

    def get_sensors(self) -> pd.DataFrame:
        """
        Fetches sensor data from the API and returns a DataFrame containing the sensor information.

        Returns:
            A pandas DataFrame containing sensor data, or None if the request fails.
        """
        try:
            # Construct the URL with the API key as a query parameter
            url = f"{self.api_url}?key={self.api_key}"

            # Make the GET request
            response = requests.get(url)
            # Check for a successful response
            if response.status_code == 200:
                sensors = response.json()[0]
                return pd.DataFrame(sensors)
            else:
                # Handle potential errors
                print(f"Error {response.status_code}: {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def process_sensor_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes sensor data by removing empty or null values in SiteClassification and normalizing SiteName.

        Parameters:
            df (pd.DataFrame): DataFrame containing sensor data.

        Returns:
            A processed pandas DataFrame with the specified columns cleaned.
        """
        if df is not None:
            # Remove any empty strings or null values from SiteClassification
            df = df[~df['SiteClassification'].isin(['', None])]
            # Normalize SiteName
            df['SiteName'] = df['SiteName'].str.strip().str.lower()
            return df
        else:
            return None

if __name__ == "__main__":
    api_key = os.getenv('API_KEY')  # Ensure your API key is set in the environment variables
    if api_key:
        manager = SensorDataManager(api_key)
        df_summary = manager.get_sensors()
        if df_summary is not None:
            df_summary = manager.process_sensor_data(df_summary)
            # Display the head of the processed DataFrame
            print(df_summary.head())
        else:
            print("Failed to retrieve sensors.")
    else:
        print("API_KEY not found. Please set your API key in the environment variables.")
