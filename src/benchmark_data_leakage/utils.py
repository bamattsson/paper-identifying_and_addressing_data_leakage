from pathlib import Path

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