import requests
import time

# EXAMPLE INPUT:  1600 Pennsylvania Ave NW, Washington DC

access_key = '0a48b7da7968d4199470d731ea13c5e4'
loop = 3

# While true:
while loop > 0:
    # Sleep for 3 seconds while
    time.sleep(3)
    # Open file prng-service.txt
    f1pointer = open("input.txt", "r+")
    # Read file
    command = f1pointer.read()
    # Erase the input.txt file
    f1pointer.seek(0)
    f1pointer.truncate(0)
    # Close file
    f1pointer.close()
    # If line in file is not empty
    if command != "":
        # build and send get request
        api_url = 'http://api.positionstack.com/v1/forward?access_key=' + access_key + "&query=" + command
        # send request/get response
        r = requests.get(url=api_url)
        # jsonify the response
        r = r.json()
        # get longitude and latitude
        longitude = r["data"][0]["longitude"]
        latitude = r["data"][0]["latitude"]
        # create coords string
        coord = str(latitude) + ", " + str(longitude)
        # Open output.txt
        f1pointer = open("output.txt", "w+")
        # write coordinates
        f1pointer.write(coord)
        # Close file
        f1pointer.close()


