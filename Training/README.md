# Use this files to train the neural networks
Move this files to the main folder before using.
## app.py
This script's funtion is to gather data for the neural networks via camera. 
* Press 1 to enter the keypoint classifier mode.
* Press 2 to enter the point history classifier mode.
* Press 0 to go back to normal mode
#
After entering a mode, press any letter to save the keypoints data while doing the hand gesture you want.
## keypoint_classification.ipynb
Run this script on JupyterNotebook to train the model using the keypoint classifier data.
## point_history_classification.ipynb
Run this script on JupyterNotebook to train the model using the point history classifier data
#
All data and models will be stored in the model folder.
