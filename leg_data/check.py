import os

images = os.listdir("./images")
videos = os.listdir("./videos")

imgs = []
for image in images:
    new = image.replace(".jpeg", "")
    imgs.append(new)
    
    
vids = []
for video in videos:
    new = video.replace(".mp4","")
    vids.append(new)

temp = []
for vid in vids:
    if vid not in imgs:
        print(vid)
        temp.append(vid)
        
print(vid)