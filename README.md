## Instructions for reproduction
### 0. Set-up

Install the dependencies with this
```
conda env create -f environment.yml
conda activate benchmark-data-leakage
pip install -e .
```

Further dependencies that are needed:

### 1. Preprocessing
- You need to be able to connect to a posgres ChEMBL database (v36 was used when generating the data, but most earlier versions should be fine)
- You need to clone https://github.com/openforcefield/protein-ligand-benchmark/tree/0.2.1 (v0.2.1 is required)
- Run the notebooks/01_*

### 2. Do analysis
- Run notebooks/02_leakage_analysis.ipynb to produce the table overview and graph for MAPK8