Corsi Block Tapping Task [last updated: January 23, 2018]

Authors:
--------
Maik Joshua Wigand(m.j.wigand@student.utwente.nl)[s1821652]
Nils Vockenberg (n.vockenberg@student.utwente.nl)[s1871404]
University of Twente

Tested for python versions 2.7 (corsi_src_27.py) and 3.6 (corsi_src_36.py) [Developed under 3.6 and ported to 2.7]

INSTALLATION
------------
- The following python libraries are required: 
	need to be installed manually if that has not already been done:
	-pygame
	-xlsxwriter
	-configparser
	-numpy
	usually come with a fresh python install (version 2.1+):
	-sys
	-time
	-random
	-tkinter

- To start either the 2.7 version or the 3.6 version using start_27.bat or start_36.bat respectively, First, the file ending ".batXXX" has to be changed to ".bat".
Furthermore, the python path needs to perhaps be adjusted in the batch file.

GENERAL USAGE NOTES
-------------------
- When using for the first time when saving trial results, the program will create a new file called data.xlsx in its directory. 
Upon later savings, the program will jut override the data file.

- Having the data.xlsx file open while trying to save will result in an error.

- Is is possible to change certain parameters using the config.ini file. 
	- some values can leaad to errors and should be thouroughly tested beforehand.
	- "corsi_block_number" should be set between 2 and 9

- The code is designed to be very easily customizable with dynamic text input and output methods.