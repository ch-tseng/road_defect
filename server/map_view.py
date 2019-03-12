from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os
import cv2

static_folder = "20190301"
target_folder = "20190301/"

#-----------------------------------------
gps_data = target_folder + "defects.log"

f = open(gps_data, 'r')

gpsList = []
for gps_line in f:
    print(gps_line)
    date_time, gps_data, obj_detect, defect_img_path = gps_line.split("|")
    lat,lng = gps_data.split(',')
    defect_img_path = defect_img_path.replace("\n","")

    org_img = target_folder+'originals/'+defect_img_path
    preview_img = target_folder+'previews/'+defect_img_path
    #filename = os.path.basename(defect_img_path)
    gpsList.append({'icon':'http://maps.google.com/mapfiles/ms/icons/green-dot.png',\
        'lat':float(lat), 'lng':float(lng), 'infobox':'<a href="'+org_img+'" target="_blank">\
        <img src="'+preview_img+'" height=60 width=90'+' /></a>' })

print(gpsList[0])

app = Flask(__name__, template_folder=".", static_url_path="/"+static_folder, static_folder=static_folder)
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
