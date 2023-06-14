# Hermite-Interpolation
Implementation of function interpolation using the Hermite polynomial, in the Python programming language (the dearpygui library was used to create the interface).

Simple instructions for use:

The implementation of this interpolation method consists of several sub-algorithms, the overall 
speed of the algorithm is O(n * m) (where n is the number of points at which interpolation 
takes place, and m is the order of the polynomial).

To use the program, it is enough to run gui.py, after which the user will be asked for 
information about the data on which he wants to perform interpolation (the main thing 
is to follow the instructions that will appear during the execution of the program). 
As a result, the user will receive a graph with interpolation at the specified points.
