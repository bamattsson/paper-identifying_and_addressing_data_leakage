### Set-up

Install the dependencies with this
```
conda env create -f environment.yml
conda activate benchmark-data-leakage
pip install -e .
```

Further dependencies that are needed:

#### 01_create_data_split.ipynb
A postgres ChEMBL database (v36 was used when generating the data, but most earlier versions should be fine)

#### 02_extract_FEPp4_data.ipynb
You need to clone https://github.com/openforcefield/protein-ligand-benchmark/tree/0.2.1 (v0.2.1 is required)