# Identifying and Addressing Data Leakage in Binding Affinity Benchmarks

This repository contains code and data to reproduce the results in [the paper](https://www.biorxiv.org/content/10.64898/2026.06.29.735309v1). The analysis is split across two pipelines depending on which sections you want to reproduce.

---

## Quick guide

| Paper sections | What they cover | Where to go |
|---|---|---|
| Sections 3 & 4 (and first figure in Section 7) | Sequence similarity splits and property biases | [`chembl_analysis/README.md`](chembl_analysis/README.md) |
| Sections 5 & 6 | FEP+ 4 benchmark analysis and baselines | Continue reading below |
| Section 7 | Reproducing the Novelty-Tiered Affinity benchmark and the baseline model | Follow README in [`bamattsson/ntab`](https://github.com/bamattsson/ntab), for Mean(Max(Tanimoto similarity)) use commit 97ec529

---

## Reproducing sections 5 & 6

### 0. Prerequisites

**External dependencies:**

- A local PostgreSQL **ChEMBL 36** database. Connection details go in `chembl_db.yaml` (see `chembl_db.yaml.example`).
- A local clone of [protein-ligand-benchmark v0.2.1](https://github.com/openforcefield/protein-ligand-benchmark/tree/0.2.1). Set the path in `notebooks/01_extract_FEPp4_data.ipynb`.
- **MMseqs2** installed separately, e.g. via conda (`conda install -c bioconda mmseqs2`) or a [prebuilt binary](https://github.com/soedinglab/MMseqs2).

### 1. Install Python dependencies

**Option A — conda:**
```bash
conda env create -f environment.yml
conda activate benchmark-data-leakage
pip install -e .
```

**Option B — uv:**
```bash
uv sync
```

> **Note:** MMseqs2 is not on PyPI. If using uv, install MMseqs2 separately before proceeding.

### 2. Preprocessing

Run the two preprocessing notebooks:

```
notebooks/01_extract_FEPp4_data.ipynb   # Extracts FEP+ 4 test data, maps to ChEMBL IDs
                                        # Produces: data/out/FEPp_benchmark.csv

notebooks/01_create_data_split.ipynb    # Fetches sequences, creates train/val/test split
                                        # Requires a manual MMseqs2 run mid-notebook
                                        # Produces: data/out/FEP_data_split.csv
```

### 3. Analysis

Run the analysis notebooks:

```
notebooks/02_leakage_analysis.ipynb     # Leakage table and MAPK8 figure
notebooks/02_baseline_plots.ipynb       # Baseline performance plots
notebooks/02_tanimoto_threshold_plot.ipynb  # Data leakage dependence on the Tanimoto threshold
```

All figures are saved to `figures/`.
