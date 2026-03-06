from decimal import Decimal
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem


def find_repo_root(path=Path.cwd()):
    if (path / "pyproject.toml").exists():
        return path
    return find_repo_root(path.parent)


def get_canonical_smiles_from_smiles(smiles: str) -> str:
    """
    Takes a SMILES string and returns its canonical SMILES string.

    Args:
        smiles: A SMILES string.

    Returns:
        The canonical SMILES string.

    Raises:
        ValueError: If the input SMILES string is invalid.
    """
    try:
        mol = Chem.MolFromSmiles(smiles)

        if mol is None:
            raise ValueError(f"Invalid SMILES string: '{smiles}'")

        canonical_smiles = Chem.MolToSmiles(mol)
        return canonical_smiles

    except Exception as e:
        raise ValueError(f"An unexpected error occurred while processing SMILES '{smiles}': {e}") from e


INEQUALITY_STR_INVERSION_MAP = {
    "=": "=",
    "~": "~",
    ">": "<",
    ">=": "<=",
    ">>": "<<",
    "<": ">",
    "<=": ">=",
    "<<": ">>",
}

def invert_inequality(inequality):
    if isinstance(inequality, str):
        if inequality in INEQUALITY_STR_INVERSION_MAP:
            return INEQUALITY_STR_INVERSION_MAP[inequality]
    if inequality is None or np.isnan(inequality):
        return inequality
    raise ValueError

def standard_val_to_neglog10(
    val: float
) -> float:
    return -np.log10(val * 1e-9)


def calc_neglog10_val(
    row: pd.Series
) -> float:
    if row["standard_units"] != "nM":
        return np.nan
    if not (isinstance(row["standard_value"], float) or isinstance(row["standard_value"], Decimal)):
        return np.nan
    return np.round(
        standard_val_to_neglog10(float(row["standard_value"])),
        2
        )