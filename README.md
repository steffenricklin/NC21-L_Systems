# Natural Computing: Final project

## Applying EA to L-Systems

### Setup

Unfortunately, we did not find the time to provide a requirements.txt with the packages you need to be able to import all the packages yet.
So it might be that you have to install a few packages via pip manually.

We may update this project today (10.06.2021) with a requirements.txt so you can easily see which packages are required.

### Running a simulation

To run a simulation run the `src/main.py file`.

#### Changing settings

To run a different experiment using different settings you can change in main.py:

##### 1. the values of the `parameters` dictionary.
The default is:
```python
parameters = {"angle": 22.5,
              "pop_size": 30,
              "iterations": 5,
              "nr_gens": 500,
              "tournament_size": 5,
              "p_mutation": 0.75,
              "fitness_func": 'convex'
}
```

   - possible value for `fitness_func` are: `convex` and `hu`. By default `convex` uses the Hu moments metric in a 
   alternating fashion.

##### 2. change the setting of the `goal` LSystem object.
The default is:
```python
goal = LSystem(axiom='A',
               rules={'B': 'BB', 'A': 'B[+AB-[A]--A][---A]'},
               angle=parameters["angle"],
               iterations=parameters["iterations"])
```

We will try to upload an updated main.py today (10.06.2021), so you may also run the file via the command line.



### Sample run

1. Run `src/main.py` with desired settings

2. Obtain results. Results are not save automatically but must be manually saved when shown at the end of the simulation.

Outputs are plots for the systems with the best fitness of the last generation and textual output of describing the systems 

Consol output of an example system:
```
turtle 0:
	- axiom:    D
	- t.-rules: {'D': 'D[BD--DA]', 'A': 'B-+DAD+B-', 'C': 'BADD', 'B': 'DB+B'}
	- fitness:  0.04905
```

Plot of the above example system 0:

![Plotted system 0](Results/500MixFitness/Figure_1.png)
