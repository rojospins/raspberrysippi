import xml.etree.ElementTree as ET
from io import BytesIO
from tkinter import font
import requests
import tkinter as tk
from PIL import Image, ImageTk
import datetime

apikey = "6df1de37-39e1-497e-ae4c-48bd03fc5a46"

request = requests.get("https://www.rmv.de/hapi/location.name?accessId=6df1de37-39e1-497e-ae4c-48bd03fc5a46&input"
                       "=3015919")

responseEscholl = requests.get(
    'https://www.rmv.de/hapi/DepartureBoard?accessId=6df1de37-39e1-497e-ae4c-48bd03fc5a46&extId=3015919&maxJourneys=5')
contentEscholl = responseEscholl.text

responseHeinrich = requests.get(
    'https://www.rmv.de/hapi/DepartureBoard?accessId=6df1de37-39e1-497e-ae4c-48bd03fc5a46&extId=3024301&maxJourneys=5')
contentHeinrich = responseHeinrich.text

# print(contentEscholl)

# Parse the XML data
rootEscholl = ET.fromstring(contentEscholl)
rootHeinrich = ET.fromstring(contentHeinrich)


def fetch_Heinrich():
    # Add your API request logic here to get the XML data
    # For example, using the requests' library:
    response = requests.get \
        ("https://www.rmv.de/hapi/DepartureBoard?accessId=6df1de37-39e1-497e-ae4c-48bd03fc5a46&extId=3024301&maxJourneys=5")
    if response.status_code == 200:
        return ET.fromstring(response.content)
    else:
        return None


def fetch_Escholl():
    response = requests.get(
        "https://www.rmv.de/hapi/DepartureBoard?accessId=6df1de37-39e1-497e-ae4c-48bd03fc5a46&extId=3015919&maxJourneys=5")
    if response.status_code == 200:
        return ET.fromstring(response.content)
    else:
        return None


def display_schedule():
    listbox.delete(0, tk.END)

    # Fetch new schedule data
    root_Heinrich = fetch_Heinrich()
    root_Escholl = fetch_Escholl()

    if root_Heinrich is not None:
        # array for departures
        departures = []
        # Iterate through each 'Departure' element
        for departure in root_Heinrich.findall(".//{http://hacon.de/hafas/proxy/hafas-proxy}Departure"):
            tram_name = departure.attrib.get("name")
            stop_name = departure.attrib.get("stop")
            departure_time = departure.attrib.get("time")
            direction = departure.attrib.get("direction")

            # Remove unnecessary info
            tram_name = tram_name.replace("Tram", "").strip()
            stop_name = stop_name.replace("Darmstadt", "").strip()
            direction = direction.replace("Darmstadt", "").strip()
            direction = direction.replace("-", "").strip()

            departures.append(
                f" Linie {tram_name}, {stop_name}, Departure Time: {departure_time}, Direction: {direction}")

        for departure in departures:
            listbox.insert(tk.END, departure)

    if root_Escholl is not None:
        # array for departures
        departures = []
        # Iterate through each 'Departure' element
        for departure in root_Escholl.findall(".//{http://hacon.de/hafas/proxy/hafas-proxy}Departure"):
            tram_name = departure.attrib.get("name")
            stop_name = departure.attrib.get("stop")
            departure_time = departure.attrib.get("time")
            direction = departure.attrib.get("direction")

            # Remove unnecessary info
            tram_name = tram_name.replace("Tram", "").strip()
            stop_name = stop_name.replace("Darmstadt-", "").strip()
            stop_name = stop_name.replace("Darmstadt", "").strip()
            direction = direction.replace("Am Hinkelstein", "").strip()
            direction = direction.replace("-Alsbach", "").strip()
            direction = direction.replace("Darmstadt-", "").strip()
            direction = direction.replace(" -", "").strip()


            departures.append(
                f" Linie {tram_name}, {stop_name}, Departure Time: {departure_time}, Direction: {direction}")

        for departure in departures:
            listbox.insert(tk.END, departure)

        # Schedule the next update
    root.after(60000, display_schedule)


def fetch_weatherDarmstadt():
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "Darmstadt",
        "appid": "0f47efa99e006490635c49682eadc29c",
        "units": "metric",  # You can change this to "imperial" for Fahrenheit

    }
    try:
        response = requests.get(base_url, params=params)
        weather_data = response.json()

        if response.status_code == 200:
            temperature = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            id = weather_data["weather"][0]["icon"]

            icon_url = f"https://openweathermap.org/img/wn/{id}@2x.png"

            # Download the icon image
            icon_response = requests.get(icon_url)
            icon_image = Image.open(BytesIO(icon_response.content))

            returned_weather = f" {description}, Temp: {temperature}°C"
            return returned_weather
        else:
            return f"Failed to fetch weather data (Error {response.status_code})"
    except requests.RequestException as e:
        return f"Failed to fetch weather data: {str(e)}"


def display_weather():
    returned_weather = fetch_weatherDarmstadt()
    weather_label.config(text=returned_weather)

    # Schedule the next weather update after 60000 milliseconds (1 minute)
    root.after(60000, display_weather)


def display_icons():
    returned_description = fetch_weatherDarmstadt()

    # Dictionary mapping weather conditions to their respective image paths
    path_cloudy = Image.open(
        r"C:\Users\Robbie\Dropbox\Mein PC (DESKTOP-TLDN6B0)\Desktop\weatherIcons\partialcloudy.png")
    thumbnail_cloudy = (100, 100)  # Set the desired thumbnail size
    path_cloudy.thumbnail(thumbnail_cloudy)
    # Update the label with the new image
    path_rain = Image.open(r"C:\Users\Robbie\Dropbox\Mein PC (DESKTOP-TLDN6B0)\Desktop\weatherIcons\rainy.jpg")
    path_rain.thumbnail(thumbnail_cloudy)

    path_snow = Image.open(r"C:\Users\Robbie\Dropbox\Mein PC (DESKTOP-TLDN6B0)\Desktop\weatherIcons\snow.png")
    path_snow.thumbnail(thumbnail_cloudy)

    path_cloudynight = Image.open(r"C:\Users\Robbie\Dropbox\Mein PC (DESKTOP-TLDN6B0)\Desktop\weatherIcons\cloudynight2.png")
    path_cloudynight.thumbnail(thumbnail_cloudy)

    image_cloudy = ImageTk.PhotoImage(path_cloudy)
    image_rain = ImageTk.PhotoImage(path_rain)
    image_snow = ImageTk.PhotoImage(path_snow)
    image_cloudynight = ImageTk.PhotoImage(path_cloudynight)

    # Get the current time
    current_time = datetime.datetime.now().time()

    # Define the time range for daytime (adjust as needed)
    daytime_start = datetime.time(6, 0)
    daytime_end = datetime.time(20, 0)

    if "cloud" in returned_description and daytime_start <= current_time <= daytime_end:
        icon_Label.config(image=image_cloudy)
        icon_Label.image = image_cloudy
    elif "rain" in returned_description and daytime_start <= current_time <= daytime_end:
        icon_Label.config(image=image_rain)
        icon_Label.image = image_rain
    elif "snow" in returned_description:
        icon_Label.config(image=image_snow)
        icon_Label.image = image_snow
    elif "cloud" in returned_description and not daytime_start <= current_time <= daytime_end:
        icon_Label.config(image=image_cloudynight)
        icon_Label.image = image_cloudynight
    else:
        # Handle the case where the weather condition is not recognized
        print("Weather condition not recognized!")

    # Schedule the function to run again after 60000 milliseconds (60 seconds)
    root.after(60000, display_icons)



# Create a Tkinter window
root = tk.Tk()
root.title("Train Schedule")
root.geometry("800x400")

# train icon
icon_trainpath = "C:/Users/Robbie/Dropbox/Mein PC (DESKTOP-TLDN6B0)/Downloads/trainICO.ico"
root.iconbitmap(icon_trainpath)

# Creating a frame to contain the widgets
frame = tk.Frame(root, bg="#3c4359")
frame.pack(expand=True, fill="both")

# Set custom font for the listbox
custom_font = font.Font(family="Arial", size=16)

# Creating a listbox
listbox = tk.Listbox(frame, width=80, height=int(10.5), font=custom_font, bg="#3c4359", fg="white")
listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# weather and temperature monitor
custom_weatherfont = font.Font(family="Javanese Text", size=25)

weather_label = tk.Label(frame, text="", font=custom_weatherfont, bg="#3c4359", fg="white", anchor="w")
weather_label.grid(row=1, column=0, pady=5, padx=10)

pillow_image = Image.open(r"C:\Users\Robbie\Dropbox\Mein PC (DESKTOP-TLDN6B0)\Desktop\weatherIcons\cloudySunnyRain.png")
thumbnail_size = (100, 100)  # Set the desired thumbnail size
pillow_image.thumbnail(thumbnail_size)
tk_image = ImageTk.PhotoImage(pillow_image)

# icon label
icon_Label = tk.Label(frame, image="", bg="#3c4359", anchor="w")
# icon_Label.grid(row=2, column=0, columnspan=2, pady=0, padx=10)

# Configure grid weights to make the Listbox expandable
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Call the display_schedule function initially to display the schedule
display_schedule()
display_weather()
# display_icons()

# Run the Tkinter event loop
root.mainloop()
