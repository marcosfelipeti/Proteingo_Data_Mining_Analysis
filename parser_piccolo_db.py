import pandas as pd
import csv

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
	print (file)
	#print (chunk.head())
	get_atom_charges(chunk)

#--------------------------------------------------------------------------------------------------------------------------------------------
def get_atom_charges(chunk):

	residues1 = chunk.res1.str.split('\n')
	residues2 = chunk.res2.str.split('\n')
	atoms1 = chunk.atom1.str.split('\n')
	atoms2 = chunk.atom2.str.split('\n')

	with open('charge.csv') as csvfile:
		reader = csv.DictReader(csvfile)

		for r1, r2, a1, a2 in zip(residues1, residues2, atoms1, atoms2):
			res1, atom1, res2, atom2 = r1[0], a1[0], r2[0], a2[0]
		
			for row in reader:
				if(row['Residue'] == res1 and row['at_name'] == atom1):
					charge1 = row['charge']
				if(row['Residue'] == res2 and row['at_name'] == atom2):
					charge2 = row['charge']

			print(res1, atom1, charge1, res2, atom2, charge2)		

#--------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

	for i in contacts_files:
		file = basic_path + i
		read_file(file)
