from typing import Optional, Union

import psycopg2


class ChEMBLRequester:

    def __init__(
            self,
            host,
            user,
            password,
            dbname,
            ):

        self.conn = psycopg2.connect(
            dbname=dbname,
            host=host,
            user=user,
            password=password,
        )

        self.cur = self.conn.cursor()
        self.dbname = dbname

    def get_uniprot_id_component_data(self):
        GET_DATA_QUERY = """
        select cs.accession,
            cs.description,
            cs.organism,
            cs."sequence"
        from component_sequences cs
        where cs.component_type = 'PROTEIN'
        """
        COL_ORDER = [
            "uniprot_id",
            "description",
            "organism",
            "sequence",
        ]
        self.cur.execute(
            GET_DATA_QUERY,
        )
        rows = self.cur.fetchall()
        results = []
        for row in rows:
            results.append({k: v for k, v in zip(COL_ORDER, row)})

        return results

    def get_chembl_id_to_smiles(
            self,
    ) -> list[tuple[str, str]]:
        GET_SMILES_QUERY = """
        select md.chembl_id, cs.canonical_smiles
        from molecule_dictionary md
        join compound_structures cs on md.molregno = cs.molregno
        """
        self.cur.execute(
            GET_SMILES_QUERY,
        )
        rows = self.cur.fetchall()
        return rows
    
    def get_single_protein_targets(
        self,
    ) -> list[dict[str, str]]:
        GET_SINGLE_PROTEIN_TARGETS_QUERY = """
        SELECT 
            td.chembl_id AS chembl_target_id,
            td.pref_name,
            cs.organism,
            cs.accession,
            cs2.component_synonym AS gene_name
        FROM target_dictionary td
        JOIN target_components tc ON td.tid = tc.tid
        JOIN component_sequences cs ON tc.component_id = cs.component_id
        JOIN component_synonyms cs2 ON cs2.component_id = cs.component_id
        WHERE td.target_type = 'SINGLE PROTEIN'
            AND cs.component_type = 'PROTEIN'
            AND cs2.syn_type = 'GENE_SYMBOL'
        """
        COL_ORDER = ["chembl_target_id", "target_name", "organism", "uniprot_id", "gene_name"]
        self.cur.execute(
            GET_SINGLE_PROTEIN_TARGETS_QUERY,
        )
        rows = self.cur.fetchall()
        results = []
        for row in rows:
            row_dict = {k: v for k, v in zip(COL_ORDER, row)}
            results.append(row_dict)
        return results
    
    def get_all_single_protein_activity_data(
            self,
            target_chembl_ids: Optional[list[str]] = None,
    ) -> list[dict[str, Union[str, float, None]]]:
        GET_ALL_SINGLE_PROTEIN_ACTIVITY_DATA_QUERY = """
        SELECT
            td.chembl_id AS target_id,
            a2.chembl_id AS assay_id,
            md.chembl_id AS ligand_id,
            a.standard_type AS measurement_type,
            a.standard_relation AS measurement_relation,
            a.pchembl_value,
            a.activity_comment,
            cp.mw_freebase AS molecular_weight,
            d.year AS assay_year,
            a.data_validity_comment,
            a.potential_duplicate,
            a.standard_value,
            a.standard_units
        FROM activities a
        JOIN assays a2 ON a2.assay_id = a.assay_id
        JOIN molecule_dictionary md ON md.molregno = a.molregno
        JOIN compound_properties cp ON a.molregno = cp.molregno
        JOIN target_dictionary td ON a2.tid = td.tid
        JOIN docs d ON a2.doc_id = d.doc_id
        WHERE td.target_type = 'SINGLE PROTEIN'
            AND a2.assay_type = 'B'
            AND a2.relationship_type IN ('D', 'H')
            AND (a.data_validity_comment IS NULL OR a.data_validity_comment = 'Manually validated')
        """
        params = None
        if target_chembl_ids is not None:
            GET_ALL_SINGLE_PROTEIN_ACTIVITY_DATA_QUERY += """
            AND td.chembl_id IN %s
            """
            params = (tuple(target_chembl_ids),)

        COL_ORDER = [
            "chembl_target_id", "chembl_assay_id", "chembl_ligand_id", "measurement_type",
            "measurement_relation", "pchembl_value", "activity_comment",
            "molecular_weight", "assay_year",
            "data_validity_comment", "potential_duplicate",
            "standard_value", "standard_units"
        ]
        self.cur.execute(
            GET_ALL_SINGLE_PROTEIN_ACTIVITY_DATA_QUERY,
            params,
        )
        rows = self.cur.fetchall()
        results = []
        for row in rows:
            row_dict = {k: v for k, v in zip(COL_ORDER, row)}
            results.append(row_dict)
        return results