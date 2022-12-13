from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import cv2
import os
import requests

def zoom_at(img, zoom):
    """
    Simple image zooming without boundary checking.
    Centered at "coord", if given, else the image center.

    img: numpy.ndarray of shape (h,w,:)
    zoom: float
    coord: (float, float)
    """
    for i in img.shape:
        print(i)
    h, w, _ = [ zoom * i for i in img.shape ]
    cx, cy = w/2, h/2
    img = cv2.resize( img, (0, 0), fx=zoom, fy=zoom)
    img = img[ int(round(cy - h/zoom * .5)) : int(round(cy + h/zoom * .5)),
               int(round(cx - w/zoom * .5)) : int(round(cx + w/zoom * .5)),
               : ]  
    return img

city = input("Enter the city :")
res = requests.get("http://api.openweathermap.org/geo/1.0/direct?q="+city+"&limit=1&appid=fa9f9ad2c655517061ababd27eb10fad")
cityinfo = res.json()
lat,lon = cityinfo[0]["lat"],cityinfo[0]["lon"]
driver = webdriver.Chrome()
zoom=3
for i in range(10):
    urlstr = 'https://www.google.co.in/maps/@'+str(lat)+','+str(lon)+','+str(round(zoom,2))+'z/data=!3m1!1e3'
    driver.get(urlstr)
    sleep(2)
    fnamestr = str(i)+'0.png'
    sleep(5)
    driver.get_screenshot_as_file('images/'+fnamestr)
    zoom+=1
    start=1.1
    for j in range(10):
        fnamestr2 = str(i)+str(j)+'.png'
        pic = cv2.imread('images/'+fnamestr)
        cv2.imwrite('images/'+fnamestr2, zoom_at(pic, start))
        start+=.1
images = [img for img in os.listdir('images') if img.endswith(".png")]
imgs = list(range(100))
for image in images:
    i = image.split(".")[0]
    imgs[int(i)]=image
frame = cv2.imread(os.path.join('images', imgs[0]))
height, width, layers = frame.shape
video = cv2.VideoWriter('video/'+city+'.avi', 0, 60, (width,height))
ln = len(imgs)
for image in imgs:
    print(image)
    video.write(cv2.imread(os.path.join('images', image)))
cv2.destroyAllWindows()
video.release()

driver.quit()
print("end...") 