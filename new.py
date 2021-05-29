import sqlite3
import pandas as pd



# database init + cursor
snp_conn = sqlite3.connect("snp.db")
c = snp_conn.cursor()

# making db for genstudio
c.execute('''
CREATE TABLE genstudio (
ID INTEGER PRIMARY KEY,
SNP_Name TEXT,
SNP_Index INTEGER,
SNP_Aux INTEGER,
Sample_ID TEXT,
SNP TEXT,
Allele1_Top TEXT,
Allele2_Top TEXT,
Allele1_Forward TEXT,
Allele2_Forward TEXT,
Allele1_AB TEXT,
Allele2_AB TEXT,
Chr INTEGER,
Position INTEGER);
''')

# metadata.db creating
c.execute('''
CREATE TABLE metadata (
ID INTEGER PRIMARY KEY,
dna_chip_id TEXT,
breed TEXT,
sex TEXT
FOREIGN KEY (dna_chip_id) REFERENCES genstudio (Sample_ID) ON DELETE CASCADE);
''')

# stats table
c.execute('''CREATE TABLE stats (
sample_id INTEGER,
SNP_Index INTEGER
GC_Score REAL,
GT_Score REAL,
Theta REAL,
R REAL,
B_Allele_Freq REAL,
Log_R_Ratio REAL
FOREIGN KEY (sample_id) REFERENCES metadata (sample_id) ON DELETE CASCADE,
FOREIGN KEY (SNP_Index) REFERENCES genstudio (SNP_Index) ON DELETE CASCADE));
''')

# open files
genstudio = pd.read_csv("genstudio.csv")
metadata = pd.read_csv("metadata.csv")


### filling
genstudio.to_sql('genstudio', con=snp_conn, if_exists='append', index = False)
metadata.to_sql('metadata', con=meta_conn, if_exists='append', index = False)
snp_conn.commit()
conn.close()
