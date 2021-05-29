import sqlite3
import pandas as pd



# database init + cursor
snp_conn = sqlite3.connect("snp.db")
cursor = snp_conn.cursor()

# making db for genstudio
cursor.execute('''
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
cursor.execute('''
CREATE TABLE metadata (
ID INTEGER PRIMARY KEY,
dna_chip_id TEXT,
breed TEXT,
sex TEXT,
FOREIGN KEY (dna_chip_id) REFERENCES genstudio (Sample_ID) ON DELETE CASCADE);
''')

# stats table
cursor.execute('''CREATE TABLE stats (
sample_id INTEGER,
SNP_Index INTEGER,
GC_Score REAL,
GT_Score REAL,
Theta REAL,
R REAL,
B_Allele_Freq REAL,
Log_R_Ratio REAL,
FOREIGN KEY (sample_id) REFERENCES metadata (sample_id) ON DELETE CASCADE,
FOREIGN KEY (SNP_Index) REFERENCES genstudio (SNP_Index) ON DELETE CASCADE);
''')

# open files
genstudio = pd.read_csv("genstudio.csv")
metadata = pd.read_csv("metadata.csv")

genstudio = genstudio.drop('Unnamed: 0', axis=1)
metadata = metadata.drop('Unnamed: 0', axis=1)

genstudio.rename(columns = {'SNP Name':'SNP_Name',
 'SNP Index':'SNP_Index',
 'SNP Aux':'SNP_Aux',
 'Sample ID':'Sample_ID',
 'Allele1 - Top':'Allele1_Top',
 'Allele2 - Top':'Allele2_Top',
 'Allele1 - Forward':'Allele1_Forward',
 'Allele2 - Forward':'Allele2_Forward',
 'Allele1 - AB':'Allele1_AB',
 'Allele2 - AB':'Allele2_AB',
 'GC Score':'GC_Score',
 'GT Score':'GT_Score',
 'B Allele Freq':'B_Allele_Freq',
 'Log R Ratio':'Log_R_Ratio'}, inplace = True)
 
stats = genstudio[['SNP_Index','Sample_ID','GC_Score',
                   'GT_Score','B_Allele_Freq','R','Theta','Log_R_Ratio']]
                   
genstudio = genstudio.drop(['GC_Score', 'GT_Score','B_Allele_Freq','R','Theta','Log_R_Ratio'],axis=1)
                                
genstudio.to_csv('genstudio_mod.csv') 
metadata.to_csv('metadata.csv')
stats.to_csv('stats.csv')

genstudio_mod = pd.read_csv('genstudio_mod.csv')
genstudio_mod = genstudio_mod.drop('Unnamed: 0', axis=1)

### filling
genstudio_mod.to_sql('genstudio', con=snp_conn, if_exists='append', index = False)
metadata.to_sql('metadata', con=snp_conn, if_exists='append', index = False)
stats.to_sql('stats', con=snp_conn, if_exists='append', index = False)
snp_conn.commit()
# conn.close()

# trying
sql_delete_query = """Delete from genstudio where SNP_Name = '1_10723065'"""
sql_update_query = """Update metadata set sex = 'XY' where dna_chip_id = '202341831114R02C01'"""
sql_cascade_query = """Delete from link_table_cascade where sample_id = '1'"""
snp_conn.commit
snp_conn.close()
