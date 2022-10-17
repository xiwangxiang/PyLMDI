## Quick User Guide
This version of PyLMDI has been adjusted to be much easier to use and understand. It is a work in progress for APERC staff but it can be used by anyone.

It is expected that this project will remain easy to use and understand so as to encourage its use rather than seem too academic. 

You can easily understand the use of this project by viewing the files in /saved_runs/ which make use of the library. 

The inputs need to be similar to what has currently been used, but this is expected to be simple to copy. 
An example of the data structure for the activity data is copied below (energy data structure is the same but with a column for energy rather than passenger_km):

	Year	Vehicle_type	Drive	passenger_km
	2017	2w	bev	118.350075
	2017	2w	g	826.808000
	2017	bus	bev	289.587211
	2017	bus	cng	468.013538
	2017	bus	d	1333.56073

For more info take a look at the saved_runs code and how the input data was structured and manipulated to make it work.

There is the capcaity to create graphs from the outputs using plotly and the functions in plot_output.py.

## About the method
Unfortunately I cannot directly give you the paper for which the method is based on. In the documentation are some screenshots of the formulae as created by me. The names of the papers are:
 - Multilevel index decomposition analysis: Approaches and application (X.Y.Xu, B.W.Ang)
 - LMDI decomposition approach: A guide for implementation (X.Y.Xu, B.W.Ang)

## Quick notes
Please note that the hierarchical method in LMDI_functions.py doesn't work for more than 2 structural variables. I plan to fix this but for now I don't have enough time. 