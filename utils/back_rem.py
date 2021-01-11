"""
Background Remover
==================
Function to remove backgrounds which fit user input criteria from pictures
- Saves files as .png
- Can be modified to remove black or white backgrounds
- Can also be modified to remove picture and leave white background
- Version 1.1
"""

from PIL import Image
from numpy import array
import sys
import glob

# import required methods from libraries

folder1=sys.argv[1]

def backRem (inputFile):
    
    try:
        # print(inputFile)
        image = Image.open(inputFile)
        image = image.convert('RGBA')
        # opens image and converts to Red, Green, Blue, Alpha interpretation
        
    except:
        print ("Unable to load file. Please check to make sure file exists and is spelled correctly.")
        # errors if the input is not an image file    
           
    data = array(image)
    # converts the image into four interconnected arrays of RGBA values ranging from 0 to 255
    
    [red, green, blue, alpha] = data.T
    # splits the four layers of the array into separate single layered arrays
    
    redValue = 240
    greenValue = 240
    blueValue = 240
    alphaValue = 240
    # asks the user for values to mask the background with
        
    try:
        redValue = int(redValue)
        greenValue = int(greenValue)
        blueValue = int(blueValue)
        alphaValue = int(alphaValue)
        # checks to see whether user input for mask values are type int
        
    except:
        print ("Please input values between 0 and 255 for mask.")
        # errors if the values are not integers between 0 and 255
    
    mask = (red >= redValue) & (green >= greenValue) & (blue >= blueValue) & (alpha >= alphaValue)
    # creates a mask for pixels that fit user defined parameters
    
    data[mask.T] = (0, 0, 0, 0)
    # alters pixels included in the mask to be transparent
    
    image = Image.fromarray(data)
    # converts four interconnected arrays back into image interpretation
    
    outputFile = inputFile[0:len(inputFile)-4] + ".png"
    image.save(outputFile)
    # creates a new file name based on the input and saves the edited image under that name
    
    
    # prints confirmation of successful conversion for user


for filename in glob.glob(folder1+'/*.png'):
    backRem(filename)
# function call
print ("Conversion Complete")