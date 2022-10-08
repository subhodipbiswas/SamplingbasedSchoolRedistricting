# Sampling-based techniques for designing school boundaries


This is the GitHub repository corresponding to the paper [Sampling-based techniques for designing school boundaries](https://arxiv.org/abs/2206.03703).

## Installation

The code is written in Python3.8 and the experiments were run on a machine using Ubuntu 18.04 LTS. You can follow the commands below for setting up your project.

### Setting up virtual environment
Assuming your default Python3 version is 3.8, set up a virtual environment
```
pip install virtualenv
virtualenv -p python3 venv
```

### Activate the environment
Always make sure to activate it before running any python script of this project
```
source venv/bin/activate
```

## Package installation
Install the required packages contained in the file requirements.txt. This is a one-time thing, make sure the virtual environment is activated before performing this step.
```
pip install -r requirements.txt
```

Note that some geospatial packages in Python require dependencies like [GDAL](https://gdal.org/) to be already installed.  
You might also want to uninstall some unnecessary packages by doing the following:

```
pip uninstall pygeos
```

**NOTE:** They `gerrychain/` folder is based on the [GerryChain](https://github.com/mggg/GerryChain) package which was partly modified for solving the school redistricting problem. As such, we do not guarantee the correctness of the package. You may want to contact the original authors of the package for any issues related to GerryChain.

## Folder Structure
  ```
  ./
  │
  ├── README.md - Overview of the code repository
  │
  ├── gerrychain/ - the GerryChain package, v0.2.19.
  │
  ├── fcps/
  │   ├── data/ - dataset corresponding to FCPS for school year 2020-21
  │   ├── solutions/ - the initial solutions that are input to the algorithms
  │   │        ├── existing/ - the solutions corresponding to the existing plan
  │   │        └── seeded/ - the solutions corresponding to randomly generated plans
  │   └── results - results of the simulation run on FCPS dataset used in the paper
  │
  ├── lcps/
  │   ├── data/ - dataset corresponding to LCPS for school year 2020-21
  │   ├── solutions/ - the initial solutions that are input to the algorithms
  │   │        ├── existing/ - the solutions corresponding to the existing plan
  │   │        └── seeded/ - the solutions corresponding to randomly generated plans
  │   └── results - results of the simulation run on LCPS dataset used in the paper
  │
  ├── get_inputs.py - processes the geospatial files in data/ stores them in datastructures
  │
  ├── functions.py - contains objective functions corresponding to school (re)districting problem
  │
  ├── make_sol.py - generates initial solutions for the algorithm to work on
  │
  ├── utils.py - contains utility functions for the algorithms to use
  │
  ├── MCMC.py - contains the code for the sampling-based techniques
  │  
  ├── run_mcmc.py - script that executes the techniques in the file MCMC.py
  │  
  └── requirements.txt - contains the libraries that need to be imported 
  ```

## Run the code

Create executables:
```
make runable
```

You can simulate all the experiments for the sampling techniques as:
```
make BAA
make BCAA
make AIO
```
**Note:** These simulations are reported for existing solutions. Should you want to run the simulations for randomly generated solutions, you need to modify the code in the `Makefile` by replacing ` -i 3` with ` -i 1` and rerunning the above commands.

We already have provided the results of our simulations in `lcps/results` and `fcps/results`. Feel free to rerun them in your own machine.

### Deactivate the environment
Deactivate it before exiting the project
```
deactivate
```

## Citation
If you use this data/code for your work, please consider citing the following article(s):
```
@article{biswas2022memetic,
author = {Biswas, Subhodip and Chen, Fanglan and Chen, Zhiqian and Lu, Chang-Tien and Ramakrishnan, Naren},
title = {Memetic Algorithms for Spatial Partitioning Problems},
year = {2022},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
issn = {2374-0353},
url = {https://doi.org/10.1145/3544779},
doi = {10.1145/3544779},
note = {Just Accepted},
journal = {ACM Trans. Spatial Algorithms Syst.},
month = {May},
keywords = {Redistricting, Metaheuristic, Spatial Optimization}
}



@article{biswas2022sampling,
  title={Sampling-based techniques for designing school boundaries},
  author={Biswas, Subhodip and Chen, Fanglan and Chen, Zhiqian and Lu, Chang-Tien and Ramakrishnan, Naren},
  journal={arXiv preprint arXiv:2206.03703},
  year={2022}
}



@phdthesis{biswas2022phd,
  title={Spatial Optimization Techniques for School Redistricting},
  author={Biswas, Subhodip},
  year={2022},
  school={Virginia Tech},
  url={http://hdl.handle.net/10919/110433}
}
```
## Help
Should you have queries, please reach out to me at subhodip@vt.edu

