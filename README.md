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

If you want any help please feel free to reach out to me

## Quick notes
I have become aware of the paper 'The misinterpretation of structure effects of the LMDI and an alternative index decomposition' which can be access for free from here https://pubmed.ncbi.nlm.nih.gov/35518914/ which details: 'In particular, structure effects calculated with the LMDI cannot be interpreted as the sole effect of changes between energy-efficient and inefficient sectors"
 - I plan to look into how i can implement the MESE Decomposition method in this library however i haven't the time yet. 
