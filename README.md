# 3DPiafCreation
Free and Open 3D Creation Software. Use the MultiCode file at https://github.com/PiafPowaz/MultiCode to create source files but isn't necessary.

# Python Dependencies

Pygame and Scipy

## Some Feature use

- OpenCV: to convert an image into a binary file.

- Pymesh from https: //github.com/taxpon/pymesh : to export the 3D Object as .obj and .stl 

# 1.4.1

- Lots of updates.

# 1.4.0

## New feature :

- Allow to export the 3D Object as .obj and .stl by using the key e and the console.

# 1.3.0

## New feature :

- Allow to change the name of used images by using the key TAB and the console.

- Allow to change the name of the saved file (without extension) by using the key s and the console.

- Allow to change the name of the loaded file (without extension) by using the key l and the console.

- With OpenCV, allow to convert a png image into a binary file using the key i and the console.

# 1.2.0

## New feature :

- Allow to use only imagex.txt and imagey.txt to create a 3D object. Using imagez.txt without using the two others might get an issue. I will try to fix it if it appears, add it to the To Do list.

- Zoom in the 3D object by pressing the key n and zoom out by pressing the key b. Replace keys to mouse scrolling could be nice. Added to the To Do list.

- Minimize the number of point by using the key o, that feature will remove point inside the 3D object and then allow to move it faster. This feature might take some time to execute.

- Save the 3D object as a .3DPiaf by using the key s. So after Minimize the number of point, the 3D object can be saved to avoid to minimize it each time it's loaded.

- Load the 3D object by using the key l.

# 1.1.0

- Allow to use imagex.txt, imagey.txt and imagez.txt to create a 3D object.

# To Do

- Use buttons as the QUIT one to convert image to binary, save, load, export the 3D object and the editor mod.

- Make an editor mode.

- Allow to save as a .png in the editor mode.

- Use an other color (grey ?) to remove 1, 2, 3 or more points at specific position in editor mode. (This one isn't easy to explain) 

- Fix issues which appears when using imagez.txt without using the two others. 

- Replace zoom keys by the mouse scrolling. 

- Convert any image file to binary without using OpenCV.

- Translate the python code into another programming language using if possible MultiCode.

- Center the rotation on the object's center.

- Translate all the French words into English ones.