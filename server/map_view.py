from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os
import cv2

gps_data = "20190301.defect"

f = open(gps_data, 'r')

gpsList = []
for gps_line in f:
    print(gps_line)
    date_time, gps_data, obj_detect, defect_img_path, icon_img_path = gps_line.split("|")
    lat,lng = gps_data.split(',')
    filename = os.path.basename(defect_img_path)
    icon_img_path = icon_img_path.replace("\n","")
    gpsList.append({'icon':'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'lat':float(lat), 'lng':float(lng), 'infobox':'<img src="'+icon_img_path+'" />' })

print(gpsList[0])

app = Flask(__name__, template_folder=".", static_url_path = "/ap_defect_icons", static_folder = "ap_defect_icons")
app.config['GOOGLEMAPS_KEY'] = "AIzaSyBPxuoRArkJBsCVa_e0DCEzo9UuPP-r_Bk"
GoogleMaps(app)

@app.route("/")
def mapview():
    # creating a map in the view
    sndmap = Map(
        identifier="sndmap",
        lat=24.7356,
        lng=120.9027,
        markers=gpsList
    )
    return render_template('map01.html', sndmap=sndmap)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)
