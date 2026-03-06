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
            cs2.component_synonym as "gene_name",
            cs."sequence"
        from component_sequences cs
        join component_synonyms cs2 on cs2.component_id = cs.component_id
        where cs.component_type = 'PROTEIN'
            and cs2.syn_type = 'GENE_SYMBOL'
        """
        COL_ORDER = [
            "uniprot_id",
            "description",
            "organism",
            "gene_name",
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