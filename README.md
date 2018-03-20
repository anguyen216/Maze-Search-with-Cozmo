# Maze-Search-with-Cozmo
This is done as a final project for CMP202 (at Chatham University) - introduction to programming (with Python). 

The program allows Cozmo Robot to autonomically navigate through an "unknown" maze and find a way out using depth-first search algorithm.

### Acknowledgement and Note
- Other contributor: Jordan Schultz-McArdle 
- Three methods are written by Dr. Rosenthal (guidance faculty for this project) - matneighbors(), getnavidirection() and navigate_path().
- Due to limited time of the project and limited knowledge of Cozmo's vision (Cozmo does not have object sensor, only camera), we did not use Cozmo's vision to detect the maze's wall. Instead, we input the location of walls of the "unknown" maze in walls() method.
- This program runs with the previous version of the SDK (before Cozmo SDK update in December 2017). The update may have changed the turn and drive function which will affect this program, may need to be changed accordingly to the new update.

### Prerequisite
In order to run the program, user will need a Cozmo robot, a compatible mobile devices, Cozmo free app, a computer that has Cozmo SDK.

### Installing
nstructions to install Cozmo SDK and how to run SDK files can be found in this [link](http://cozmosdk.anki.com/docs/install-macos.html)

### Running
after installing SDK, to run the program in this folder, simply type into terminal
`./FinalMaze.py` 

The program runs with default starting location of A1 and South as facing direction. To change these values, change these values in line 176

### Troubleshooting
If you try to run the file and got the message "Permission denied".

Follow the following steps to get the file running
- Download Cozmo sdk example file
- Duplicate one of the example file. 
- Copy and paste this program into the duplicated example file
- Run the duplicated example file with the content of this program
