import pandas as pd

#Definitions:
#path,file names, and chunksize
basic_path = '/scratch/Second_analysis_proteingo/contacts_second_paper/'
contacts_files = {'is_hb.csv', 'is_hydrophobe.csv', 'is_ionic.csv', 'is_arom.csv', 'is_no_contact.csv'}
chunksize = 10 ** 6

#--------------------------------------------------------------------------------------------------------------------------------------------

def read_file(file):
	for chunk in pd.read_csv(file, chunksize=chunksize, header=None, 
		names=['pdb', 'chain_res1', 'chain_number1', 'res1', 'atom1', 'chain_res2', 'chain_number2', 'res2', 'atom2', 'distance']):
		process(chunk)

#--------------------------------------------------------------------------------------------------------------------------------------------
def process(chunk):    	
	#print (file)
	#print (chunk.head())
	get_atom_charges(chunk)

#--------------------------------------------------------------------------------------------------------------------------------------------
def get_atom_charges(chunk):

	res1 = chunk['res1']
	res2 = chunk['res2']
	atom1 = chunk['atom1']
	atom2 = chunk['atom2']
	print(res1, atom1, res2, atom2)

	rows = pd.read_csv("charge.csv")
	
	for row in rows:
		if(row['Residue'] == res1 and row['at_name'] == atom1):
			charge1 = row['carge']
		if(row['Residue'] == res2 and row['at_name'] == atom2):
			charge2 = row['carge']

	print(res1, atom1, charge1, res2, atom2, charge2)		

#--------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

	for i in contacts_files:
		file = basic_path + i
		read_file(file)