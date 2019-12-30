import requests, json

# Begin by getting the Google Maps API key. You can get this by going to: https://developers.google.com/maps/gmp-get-started
f = open("maps_api_key.txt", "r")
apiKey = f.read()
f.close

# Convert the input location to coordinates, using the geocode Maps API.
def Get_Coordinates(apiKey, address):
 
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
           .format(address.replace(' ','+'), apiKey))
    try:
        response = requests.get(url)
        resp_json_payload = response.json()
        lat = resp_json_payload['results'][0]['geometry']['location']['lat'] # Dig down into the JSON objects to find the lat
        lng = resp_json_payload['results'][0]['geometry']['location']['lng'] # Then the lng (long)
    except:
        print('ERROR: {}'.format(address))
        lat = 0
        lng = 0
    return lat, lng


# Use the UK Police public API to pull data on location using lat lng coordinates and a year. Loop for all 12 months of the year.
def Get_Crimes(latt, long, year):

    url = "https://data.police.uk/api/crimes-at-location?date={year}&lat={lat}&lng={lon}"

    location = (latt,long)

    

    i = crimes = totcrimes = 0 # Init a bunch of empty variables.
    
    
    while i < 12:
        i+=1
        
        chkdate = year + "-" + str(i) # Add the month to the year.

        data = requests.get(url.format(year=chkdate,lat=location[0],lon=location[1]))

        crimes = len(json.loads(data.content.decode())) # Crimes for that month
        totcrimes += len(json.loads(data.content.decode())) # Crimes for the year

        print (str(chkdate) + " - Crimes: " + str(crimes) + ". Total crimes so far: " + str(totcrimes))

print("############################")
print("Welcome to the UK crime statistics checker...")

address = "Westminister"
year = str(2018)
#address = input("Please enter a UK address or location: # ")
#year = input("Please enter which year you want statistics for: # ")

lat, lng = Get_Coordinates(apiKey, address)

print('\n{} Coordinates:\nLatitude:  {}°\nLongitude: {}°'.format(address,lat, lng))
print("------------------\n")
print("Crime Statistics:")
print(Get_Crimes(lat,lng, year))

