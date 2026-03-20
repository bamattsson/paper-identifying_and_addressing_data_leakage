## Reproduction

### 0. Setup

**Option A: conda**
```bash
conda env create -f environment.yml
conda activate benchmark-data-leakage
pip install -e .
```

**Option B: uv**

> **Note:** `mmseqs2` is not on PyPI and must be installed separately first, e.g. via conda (`conda install -c bioconda mmseqs2`) or a [prebuilt binary](https://github.com/soedinglab/MMseqs2).

```bash
uv sync
```

### 1. Preprocessing
Two external dependencies are required:
- A local PostgreSQL ChEMBL database (v36 was used; earlier versions should work)
- A local cloned version of [protein-ligand-benchmark v0.2.1](https://github.com/openforcefield/protein-ligand-benchmark/tree/0.2.1)

Then run the notebooks `notebooks/01_*`.

### 2. Analysis
Run `notebooks/02_leakage_analysis.ipynb` to reproduce the leakage table and MAPK8 figure.