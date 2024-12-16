from tkinter import PhotoImage

url = []
image = {}

def loadTkImage(uri):
    global image
    global url
    if uri not in url:
        photo = PhotoImage(file=uri, format="png").subsample(3,3)
        image[uri] =photo 
        print(image)
    url.append(uri)
    return image.get(uri)
    