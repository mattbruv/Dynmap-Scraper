import itertools
import os
import re
import sys
import math
from PIL import Image

# returns (name, x, z) coordinates from filename
def coordsFromFilename(filename):
    m = re.search('([-]?\d+)_([-]?\d+)\.png', filename)
    return (filename, int(m.group(1)), int(m.group(2)))

if __name__ == '__main__':

    folder = sys.argv[1]
    sources = os.listdir(folder)
    data = []

    for imgName in sources:
        coords = coordsFromFilename(imgName)
        data.append(coords)
    
    sortedList = sorted(data, key=lambda el: (el[2], -el[1]), reverse=True)
    group = itertools.groupby(sortedList, lambda x: x[2])
    # i have to make this copy because list() consumes the group and idgaf how to do this properly
    wtfPython = itertools.groupby(sortedList, lambda x: x[2])

    xIndex = 0
    yIndex = 0
    chunkSize = len(list(wtfPython)) * 128
    imageSize = (chunkSize, chunkSize)
    outputImage = Image.new("RGB", imageSize)

    for row, column in group:
        yOffset = (yIndex * 128)
        for x in column:
            # if the new width is greater than current, resize image
            xOffset = (xIndex * 128)
            # Copy the image chunk into its new spot in large image
            tempImg = Image.open(folder + "/" + x[0])
            outputImage.paste(tempImg, (xOffset, yOffset, (xOffset + 128), (yOffset + 128)))
            xIndex += 1
        yIndex += 1
        xIndex = 0
    print("Image size is {}".format(outputImage.size))

    outPath = "compiled/"

    if not os.path.exists(outPath):
        os.mkdir(outPath)

    outputImage.save(outPath + folder + ".png")