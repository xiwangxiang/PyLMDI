This project is based on the Git repo as follows:

# PyLMDI: An open source toolbox for LMDI decomposition analysis in Python

```
https://github.com/xiwang2718/PyLMDI
```



## Quick User Guide
This version of PyLMDI has been adjusted to be easier to use and understand. It is a work in progress for APERC staff, and any additions are welcome. 
It is expected that this project will remains easy to use and understand so as to encourage its use rather than seem too academic. 

You can easily understand the use of this project by viewing the files in /saved_runs/. 

The inputs need to be similar to what has currently been used, but this is expected to be simple to copy. 
Specifically you will want to create an xlsx with a sheet for energy, per structural category (eg. bus, heavy truck, car are structural variables of transport) per year, and a similar sheet for energy. When we incorporate the ability to calculate emissions outputs, we will also need an emissions data sheet of the same structure. 

There is the capcaity to create graphs from the outputs using plotly, and this capacity should be further developed to allow for new and intenresting ways to analyse the output. 


## Useful Links
Guide to LMDI as shared from Finns google drive account https://drive.google.com/file/d/1wCd-S55JVrHoQwRV7w9qZSVxTlfiqGa8/view?usp=sharing

## Intended updates:
-LMDI analysis of emissions and using emissions intensity as an extra driver.
