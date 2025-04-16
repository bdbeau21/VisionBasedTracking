# Vision Based Object Tracking System

The Vision Based Object Tracking system enables real-time visual tracking of a red-colored object using a Luxonis OAK-D camera. The camera is connected to a host computer running a Python based script which processes the real time video, identifies the location of the red object and its horizontal position, and transmits a corresponding servo angle to an Arduino microcontroller. The Ardunio actuates a servo motor to follow the object’s movements and displays the servo angle on an OLED screen. This system demonstrates the basics of machine vision, mechatronics, and embedded firmware all combined together.

Inside this repo you will find a System Design Document that provids a blue print for this system, Python code for video processing and object detections, and Arduino firmware code actuates the servo motor and displays to the OLED Display

Link to video of project: https://drive.google.com/file/d/1zovjEjm7cXpkNMrJkgIR-7B5XOPgknOE/view?usp=share_link

Picture of system: [SystemDisplay.HEIC](https://github.com/bdbeau21/VisionBasedTracking/blob/main/SystemDisplay.HEIC)
