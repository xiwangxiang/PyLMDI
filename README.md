## About the Log Mean Divisia Index I method:
Index decomposition or factorisation analysis quantifies the impact of different driving forces on energy consumption. Understanding how each of the elements impact energy consumption is essential to determine which have the largest potential for savings and the areas that should be prioritised for the development of energy efficiency policies. 

The Log Mean Divisia Index I (LMDI I) methodology, meets three of the four criteria presented below, the most important of which is perfect decomposition (i.e. does not produce a residual term). However, it is considered relatively difficult to communicate to non-experts and is not suitable where there are zeros or negative numbers in the data set being analysed.

When choosing a decompostion method, the following factors should be considered:
 - The index methodology must be theoretically sound, i.e. an insignificant or no residual or interaction term and also must meet the index requirement of time reversibility. 
 - The index methodology must be applicable to all sectors and sub-sectors so that they can all be interpreted in the same way, making it possible to aggregate the sub-sectors results. 
 - The interpretation of the index must be straightforward (i.e. the results must be easy to understand). 
 - Data to calculate the different effects must be available.

## About this repo
This version of PyLMDI is a fork of a github library i found but adjusted to be easier to use and understand. It is a work in progress for APERC staff but it can be used and updated by anyone.

It is expected that this project will remain easy to use and understand so as to encourage its use rather than seem too academic. 

## Quick User Guide
You can easily understand the use of this project by viewing the files in /saved_runs/ which make use of the library. 

The inputs need to be similar to what has currently been used, but this is expected to be simple to copy. 

### Example activity data structure:

	Year	Vehicle_type	Drive	passenger_km
	2017	2w	bev	118.350075
	2017	2w	g	826.808000
	2017	bus	bev	289.587211
	2017	bus	cng	468.013538
	2017	bus	d	1333.56073

### Example energy data structure

	Year	Vehicle_type	Drive	energy
	2017	2w	bev	118.350075
	2017	2w	g	826.808000
	2017	bus	bev	289.587211
	2017	bus	cng	468.013538
	2017	bus	d	1333.56073


For more info take a look at the saved_runs code and how the input data was structured and manipulated to make it work.

There is the capcaity to create graphs from the outputs using plotly and the functions in plot_output.py. They are quite nice graphs but are probably quite fiddly if you aren't using them for similar analysis as I do with them. 

## About the method
Unfortunately I cannot directly give you the paper for which the method is based on. The names of the papers are:
 - Multilevel index decomposition analysis: Approaches and application (X.Y.Xu, B.W.Ang)
 - LMDI decomposition approach: A guide for implementation (X.Y.Xu, B.W.Ang)

If you want any help understanding the methods please feel free to reach out to me, they are pretty difficult to get your head around and i am keen to make sure somoene else doesn't have to struggle as much as i did!

## Quick notes
I have become aware of the paper 'The misinterpretation of structure effects of the LMDI and an alternative index decomposition' which can be access for free from here https://pubmed.ncbi.nlm.nih.gov/35518914/ which details: 'In particular, structure effects calculated with the LMDI cannot be interpreted as the sole effect of changes between energy-efficient and inefficient sectors"
 - I plan to look into how i can implement the MESE Decomposition method in this library however i haven't the time yet. 

## Setup
There are two options for environments. They depend if you want to use jupyter or just the command line to run the model. I prefer to use jupyter but i know that it takes a lot of space/set-up-time.

config/env_jupyter.yml
config/env_no_jupyter.yml
run: conda env create --prefix ./env_jupyter --file ./config/env_jupyter.yml

Then: conda activate ./env_jupyter

Note that installing those libraries in the yml files will result in a few other dependencies also being installed.
