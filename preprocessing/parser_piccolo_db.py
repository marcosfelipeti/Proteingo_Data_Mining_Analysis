import pandas as pd
import numpy as np
import csv

#Definitions:
#path,file names, and chunksize
basic_path = '/scratch/Second_analysis_proteingo/contacts_second_paper/'
basic_path_to_save = '/scratch/Second_analysis_proteingo/contacts_with_features/'
contacts_files = ['is_hb.csv', 'is_hydrophobe.csv', 'is_ionic.csv', 'is_arom.csv', 'is_no_contact.csv']  #not uploaded here due to huge size (~2.5GB)

chunksize = 10 ** 6

#--------------------------------------------------------------------------------------------------------------------------------------------
def main():
	for contact_file in contacts_files:
		file = basic_path + contact_file
		read_file(file, contact_file)

#--------------------------------------------------------------------------------------------------------------------------------------------		
def read_file(file, contact_file):	

	for chunk in pd.read_csv(file, chunksize=chunksize, header=None, 
		names=['pdb', 'chain_res1', 'chain_number1', 'res1', 'atom1', 
		'chain_res2', 'chain_number2', 'res2', 'atom2', 'distance'],
		keep_default_na=False):
		process_and_save_data(chunk, contact_file)

#--------------------------------------------------------------------------------------------------------------------------------------------
def process_and_save_data(chunk, contact_file):    	
	pdbs = chunk.pdb.astype(str).str.split('\n')
	residues1 = chunk.res1.str.split('\n')
	residues2 = chunk.res2.str.split('\n')
	atoms1 = chunk.atom1.str.split('\n')
	atoms2 = chunk.atom2.str.split('\n')
	chains_res1 = chunk.chain_res1.str.split('\n')
	chains_res2 = chunk.chain_res2.str.split('\n')
	chains_number_res1 = chunk.chain_number1.astype(str).str.split('\n')
	chains_number_res2 = chunk.chain_number2.astype(str).str.split('\n')
	distances = chunk.distance.astype(str).str.split('\n')

	with open(basic_path_to_save+contact_file, 'a') as myfile:
		print('Saving data to {0}'.format(contact_file))

		for pdb, res1, res2, atom1, atom2, chain_res1, chain_res2, chain_number1, chain_number2, distance in zip(pdbs,residues1, residues2, atoms1, atoms2, chains_res1, chains_res2, chains_number_res1, chains_number_res2, distances):
			polarity_res1, polarity_res2 = get_residue_polarity(res1[0], res2[0])
			type_residue1, type_residue2 = get_amino_acid_type(res1[0], res2[0])
			charge_at1, charge_at2 = get_atom_charges(res1[0], res2[0], atom1[0], atom2[0])
			covalent_bonds_number_at1, covalent_bonds_number_at2 = get_atoms_covalent_bonds_number(res1[0], res2[0], atom1[0], atom2[0])

			row = [pdb[0],
				chain_res1[0],
				chain_number1[0],
				res1[0], 
				polarity_res1, 
				type_residue1, 
				atom1[0], 
				charge_at1, 
				covalent_bonds_number_at1, 
				chain_res2[0],
				chain_number2[0],
				res2[0], 
				polarity_res2, 
				type_residue2, 
				atom2[0], 
				charge_at2, 
				covalent_bonds_number_at1,
				distance[0]]

			wr = csv.writer(myfile)
			wr.writerow(row)


#--------------------------------------------------------------------------------------------------------------------------------------------
def get_residue_polarity(res1, res2):

	polarity_res1, polarity_res2 = '', ''

	with open('../features/polarity.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if res1 == row['residue']:
				polarity_res1 = row['polarity']
			if res2 == row['residue']:
				polarity_res2 = row['polarity']	

	return polarity_res1, polarity_res2	

#--------------------------------------------------------------------------------------------------------------------------------------------
def get_amino_acid_type(res1, res2):

	type_residue1, type_residue2 = '', ''

	with open('../features/amino_acid_types.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if res1 == row['residue']:
				type_residue1 = row['type']
			if res2 == row['residue']:
				type_residue2 = row['type']

	return type_residue1, type_residue2			

#--------------------------------------------------------------------------------------------------------------------------------------------
def get_atom_charges(res1, res2, atom1, atom2):

	charge_at1, charge_at2 = '', ''

	with open('../features/charge.csv') as csvfile:
		reader = csv.DictReader(csvfile)	
		for row in reader:
			if(row['Residue'] == res1 and row['at_name'] == atom1):
				charge_at1 = row['charge']
			if(row['Residue'] == res2 and row['at_name'] == atom2):
				charge_at2 = row['charge']

	return charge_at1, charge_at2	

#--------------------------------------------------------------------------------------------------------------------------------------------
def get_atoms_covalent_bonds_number(res1, res2, atom1, atom2):

	with open("../features/covalent.txt") as reader:
		file_content = reader.read().splitlines()	

	covalent_bonds_number_at1, covalent_bonds_number_at2 = 0, 0

	for i, content in enumerate(file_content):
		line = content.split(",")

		if res1 == line[1]:
			covalent_bonds_number_at1 = walk_through_bonds_for_covalent_bonds(i, content, line, file_content, atom1)
		if res2 == line[1]:
			covalent_bonds_number_at2 = walk_through_bonds_for_covalent_bonds(i, content, line, file_content, atom2)

	return covalent_bonds_number_at1, covalent_bonds_number_at2		


def walk_through_bonds_for_covalent_bonds(i, content, line, file_content, atom):

	covalent_bonds_number_at = 0
	index_next_line = i+1
	next_line = file_content[index_next_line].split(",")

	while next_line[0] == "BOND" or next_line[0] == "DOUBLE":
		covalent_bonds_number_at += next_line.count(atom)
		index_next_line = index_next_line+1

		if 0 <= index_next_line < len(file_content):
			next_line = file_content[index_next_line].split(",")
		else:
			break

	return covalent_bonds_number_at					
#--------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

	main()