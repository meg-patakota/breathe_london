"""### About getClarityData 
<br/> https://www.globalcleanair.org/wp-content/blogs.dir/95/files/2021/05/BL-Pilot-Final-Technical-Report.pdf <br/>
<br/>
Sensors: Air pollution monitoring networks. Each pod contains several air quality sensors that provide near real-time local air quality information.
    (Sensors overall average every 1-15 minutes)
    Sensors collect information in 10-second intervals.
    PM sensors operated 30-seconds in each minute.
<br/>
<br/> To extract the clarityData, Site Code : Needs to be used as a parameter  <br/>
<ul> 
Species Data (Pollutant Measures):  
    <li>IPM25: PM2.5 (Particular Matter, light-scattering optical particle counter) </li>
    <li>INO2 : NO2 (Nitrogen dioxide) in (µg/m3) </li>
    </ul>
<ul> Pollution Levels:
    <li>ScaledValue: This value for each species indicates pollution levels </li>"""

### Hourly Data Extraction

API_URL = "https://api.breathelondon.org/api/getClarityData/{siteCode}/{species}/{startTime}/{endTime}/{averaging}?key={apiKey}"

def get_clarity_data(siteCode, species, startTime, endTime, averaging):
    try:
    # Format the API URL with required parameters
        formatted_startTime = startTime.replace(" ", "%20")
        formatted_endTime = endTime.replace(" ", "%20")
        url = API_URL.format(siteCode=siteCode, species=species, startTime=formatted_startTime, endTime=formatted_endTime, averaging=averaging, apiKey=API_KEY)
    
        response = requests.get(url)
    
        # Check if request was successful
        if response.status_code == 200:
            sensors = response.json()
            sensors = pd.DataFrame.from_dict(sensors)
            return sensors
        else:
            print(f"Error with status code: {response.status_code}")
            print(response.text)
            return None
    
    except ValueError:
        print("Received an unexpected response:")
        print(response.text)
        return None