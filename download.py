import math
import sys
import time
import urllib.request
import os
import yaml

def error(message):
    sys.exit("ERROR: {}\nAborting.".format(message))

imageNameFormat = "z_118_118.png"
imageNameFormat = "{view}{chunkX}_{chunkZ}.png"

def genImageName(view, chunkX, chunkZ):
    return imageNameFormat.format(
        view = viewToString(view),
        chunkX = chunkX,
        chunkZ = chunkZ
    )

def viewToString(view):
    if view == 0:
        return ""
    else:
        result = ""
        for x in range(0, view):
            result += "z"
        return (result + "_")

def getLowerContainingZone(chunkIndex, chunkInterval):
    while chunkIndex % chunkInterval != 0:
        chunkIndex -= 1
    return chunkIndex

def getUpperContainingZone(chunkIndex, chunkInterval):
    while chunkIndex % chunkInterval != 0:
        chunkIndex += 1
    return chunkIndex

if __name__ == '__main__':

    data = open("config.yaml", "r")
    config = yaml.load(data)

    # Init config variables
    domain = str(config['domain'])
    view = int(config['view'])
    x1 = int(config['bounds']['x1'])
    z1 = int(config['bounds']['z1'])
    x2 = int(config['bounds']['x2'])
    z2 = int(config['bounds']['z2'])
    chunkSize = int(config['chunkSize'])

    # Validate config settings and calculate image parameters
    if view < 0 or view > 7:
        error("Invalid view level given in config.")
    
    chunkInterval = 2 ** view

    def lowBound(chunkIndex):
        chunkIndex = chunkIndex // chunkSize
        return getLowerContainingZone(chunkIndex, chunkInterval)

    def upperBound(chunkIndex):
        chunkIndex = chunkIndex // chunkSize
        return getUpperContainingZone(chunkIndex, chunkInterval)

    chunkX1 = lowBound(x1)
    chunkZ1 = lowBound(z1)
    chunkX2 = upperBound(x2)
    chunkZ2 = upperBound(z2)

    print("View level {}: generating screenshots every {} chunks".format(view, chunkInterval))
    print("From chunk ({},{}) to ({},{})".format(
        chunkX1, chunkZ1, chunkX2, chunkZ2
    ))

    timestamp = int(time.time())
    outputPath = str(timestamp) + "/"
    numImages = 0

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    for x in range(chunkX1, (chunkX2 + chunkInterval), chunkInterval):
        for z in range(chunkZ1, (chunkZ2 + chunkInterval), chunkInterval):
            numImages += 1
            imageName = genImageName(view, x, z)
            imageURL = domain + imageName
            print("Downloading {}".format(imageURL))

            with urllib.request.urlopen(imageURL) as url:
                with open(outputPath + imageName, 'wb') as f:
                    f.write(url.read())
    
    print("Finished downloading {} images to {}".format(numImages, outputPath))