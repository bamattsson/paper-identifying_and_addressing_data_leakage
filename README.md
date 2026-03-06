## Reproduction

### 0. Setup
```bash
conda env create -f environment.yml
conda activate benchmark-data-leakage
pip install -e .
```

### 1. Preprocessing
Two external dependencies are required:
- A local PostgreSQL ChEMBL database (v36 was used; earlier versions should work)
- A local cloned version of [protein-ligand-benchmark v0.2.1](https://github.com/openforcefield/protein-ligand-benchmark/tree/0.2.1)

Then run the notebooks `notebooks/01_*`.

### 2. Analysis
Run `notebooks/02_leakage_analysis.ipynb` to reproduce the leakage table and MAPK8 figure.