from argparse import ArgumentParser
import os
from pathlib import Path 

import yaml

import pandas as pd

from benchmark_data_leakage.utils import find_repo_root, get_canonical_smiles_from_smiles


TARGET_MAPPING_FEP_4 = {
    # Keys are folder names as in https://github.com/openforcefield/protein-ligand-benchmark/tree/0.2.1/data
    # Values are (gene_name, uniprot_id, chembl_target_id)
    # Note that gene_name is from ChEMBL, e.g. MAPK8 -> JNK1 and MAPK14 -> p38 alpha
    "2019-12-09_p38": ("MAPK14", "Q16539", "CHEMBL260"),
    "2019-09-23_jnk1": ("MAPK8", "P45983", "CHEMBL2276"),
    "2020-02-07_tyk2": ("TYK2", "P29597", "CHEMBL3553"),
    "2019-12-13_cdk2": ("CDK2", "P24941", "CHEMBL301"),
}


def extract_benchmark_data(root_path):
    data_dir = os.path.join(root_path, 'data')
    all_records = []

    # Iterate through each folder in the 'data' directory (each represents a gene)
    if not os.path.exists(data_dir):
        print(f"Error: {data_dir} not found.")
        return pd.DataFrame()

    for folder_name in os.listdir(data_dir):
        gene_path = os.path.join(data_dir, folder_name)

        # Check if it's a directory
        if not os.path.isdir(gene_path):
            continue

        # Target the specific ligands.yml file
        ligands_file = os.path.join(gene_path, '00_data', 'ligands.yml')

        if os.path.exists(ligands_file):
            with open(ligands_file, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if not data:
                        continue

                    for lig_id, info in data.items():
                        # Extract measurement details safely
                        meas = info.get('measurement', {})

                        record = {
                            'folder_name': folder_name,
                            'name': info.get('name'),
                            'smiles': info.get('smiles'),
                            'measurement_value': meas.get('value'),
                            'measurement_unit': meas.get('unit'),
                            'measurement_comment': meas.get('comment'),
                            'measurement_doi': meas.get('doi'),
                            'measurement_type': meas.get('type'),
                            'measurement_error': meas.get('error'),
                        }
                        all_records.append(record)
                except yaml.YAMLError as exc:
                    print(f"Error parsing {ligands_file}: {exc}")

    # Create the pandas DataFrame
    df = pd.DataFrame(all_records)

    # Reorder columns as requested
    cols = ['folder_name', 'name', 'smiles', 'measurement_comment', 'measurement_doi', 
            'measurement_type', 'measurement_error', 'measurement_unit', 'measurement_value']
    return df[cols]


def main(
        protein_ligand_benchmark_root: str,
        out_fp: Path,
        ):

    # Load benchmark data
    benchmark_df = extract_benchmark_data(protein_ligand_benchmark_root)
    print(f"benchmark_df data loaded {benchmark_df.shape}")

    # Process all data
    benchmark_df = benchmark_df.loc[
        benchmark_df["folder_name"].isin(TARGET_MAPPING_FEP_4.keys())
    ].copy()
    benchmark_df["gene_name"] = None
    benchmark_df["uniprot_id"] = None
    benchmark_df["chembl_target_id"] = None
    for id_, row in benchmark_df.iterrows():
        # Assign target info
        gene_name, uniprot_id, chembl_target_id = TARGET_MAPPING_FEP_4[row["folder_name"]]
        benchmark_df.loc[id_, "gene_name"] = gene_name
        benchmark_df.loc[id_, "uniprot_id"] = uniprot_id
        benchmark_df.loc[id_, "chembl_target_id"] = chembl_target_id
        # Canonicalise the smiles
        smiles = row["smiles"]
        canonical_smiles = get_canonical_smiles_from_smiles(smiles)
        benchmark_df.loc[id_, "smiles"] = canonical_smiles

    print(f"Data has been prepared {benchmark_df.shape}")
    out_fp.parent.mkdir(exist_ok=True, parents=True)
    print(f"Dumping data to {out_fp}")
    benchmark_df.to_csv(out_fp)

if __name__ == '__main__':
    parser = ArgumentParser()
    out_dir = find_repo_root() / "data" / "out"
    parser.add_argument(
        '--protein_ligand_benchmark_root',
        help="This should be the root of the https://github.com/openforcefield/protein-ligand-benchmark/tree/0.2.1 repo (on v0.2.1)",
        type=str,
        )
    parser.add_argument(
        '--out_fp',
        help="Where to save the output data",
        type=Path,
        default=out_dir / "FEPp_benchmark.csv",
    )

    args = parser.parse_args()
    main(
        protein_ligand_benchmark_root=args.protein_ligand_benchmark_root,
        out_fp=args.out_fp,
        )