from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os
import cv2

gmap_key = ""
static_folder = "20190315"
target_folder = "20190315/"

#-----------------------------------------
#https://github.com/rochacbruno/Flask-GoogleMaps
gps_data = target_folder + "defects.log"

f = open(gps_data, 'r')

gpsList = []
for gps_line in f:
    print(gps_line)
    date_time, gps_data, obj_detect, defect_img_path = gps_line.split("|")
    lat,lng = gps_data.split(',')
    defect_img_path = defect_img_path.replace("\n","")
    #get detceted classes
    str_classes = ""
    d_classes = []
    d_class = ""
    txt_classes = ""
    objs = obj_detect.split(',')
    for d_obj in objs:
        if(len(d_obj)>0):
            d_classes = d_obj.split(':')
            #txt_classes = ""
            for ii, class_name in enumerate(d_classes):
                if(ii>0):
                    txt_classes += ','+class_name
                else:
                    txt_classes += class_name

    if(len(d_classes)>0):
        d_class = d_classes[0][:3]
        print("TEST:", d_class)
        if(d_class=='D12'):
            icon_path = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        elif(d_class=='D20'):
            icon_path = 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'
        elif(d_class=='D40'):
            icon_path = 'http://maps.google.com/mapfiles/ms/icons/orange-dot.png'
        elif(d_class=='D50'):
            icon_path = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
        elif(d_class=='D51'):
            icon_path = 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png'
        else:
            icon_path = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'

    org_img = target_folder+'originals/'+defect_img_path
    preview_img = target_folder+'previews/'+defect_img_path
    url_link = "javascript: openwindow('" + org_img + "')"
    #filename = os.path.basename(defect_img_path)
    gpsList.append({'icon':icon_path,\
        'lat':float(lat), 'lng':float(lng), 'infobox':'<b>'+txt_classes+'</b><BR><a href="'+url_link+'"><img src="'+preview_img+'" width=480'+' /></a>' })

print(gpsList[0])

app = Flask(__name__, template_folder=".", static_url_path="/"+static_folder, static_folder=static_folder)
app.config['GOOGLEMAPS_KEY'] = gmap_key
GoogleMaps(app)

@app.route("/")
def mapview():
    # creating a map in the view
    sndmap = Map(
        identifier="sndmap",
        lat=float(lat),
        lng=float(lng),
        markers=gpsList,
        zoom = 16,
        style="height:1200px;width:850px;margin:0;"
    )
    return render_template('map01.html', sndmap=sndmap)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)
