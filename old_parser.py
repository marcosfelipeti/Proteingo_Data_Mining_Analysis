import csv
import numpy as np
from random import *

interaction = "10000"
non_interaction = "Non-NC"

random_interactions_id = []

ids, pdb = [], []
p1_resname, p1_atname = [], []
p2_resname, p2_atname = [], []
distance, p, d = [], [], []

#get the distance
id_d_random, pdb_random = [],[]
p1_resname_random, p1_atname_random = [],[]
p2_resname_random, p2_atname_random = [],[]
distance_random, p_random, d_random = [],[],[]


#charge
charge_at1, charge_at2 = [], []

#get polarity
polarity_res1, polarity_res2 = [], []

#get number of covalent bonds
number_at1, number_at2 = [], []

#get amino acid types
res_type1, res_type2 = [], []

#correct Non-contacts
correct_nc = [43,244,253,264,285,336,637,708,768,890,902,926,997,1032,1051,1148,1160,523,609,288,122,196,208,254,313,546,693,754,772,800,828,917,1015,1062,1095,378,747,174,769,776,674,1116,1154,1159,523,60,288,597,571,145,606,691,76,443,210,775,338,449,856,316,474,605,20,427,351,798,988,86,962,888,699,56,530,29,277,719,10,567,437,1014,50,152,753,242,478,927,709,149,57,198,249,1001,70,17,541,144,259,230,713,822,131,620,642,232,380,834,153,626,805,873,531,986,304,482,220,179,556,920,842,801,491,641,612,733,903,587,1007,397,358,676,323,493,262,460,734,906,135,302,211,1018,364,545,505,615,432,835,658,136,763,85,1019,687,281,746]

def read_file():
	with open ('is_hb.csv') as csvfile:
		reader = csv.DictReader(csvfile)

		for row in reader:
			print row


#--------------------------------------------------------------------------------#

def getcontact_dist():
	with open('pc.csv') as csvfile:
		reader = csv.DictReader(csvfile)

		for row in reader:
			for i in random_interactions_id:
				if i == int(row['id_interaction_pair_atom']):
					#print i, row['pdb'], row['p1_resname'],row['p1_atname'] 
					id_d_random.append(i)
					pdb_random.append(pdb[ids.index(i)])
					p1_resname_random.append(p1_resname[ids.index(i)])
					p1_atname_random.append(p1_atname[ids.index(i)])
					p2_resname_random.append(p2_resname[ids.index(i)])
					p2_atname_random.append(p2_atname[ids.index(i)])
					distance_random.append(float(distance[ids.index(i)]))
					p_random.append(non_interaction)
					d_random.append(d[ids.index(i)])
#--------------------------------------------------------------------------------#

def getcharge():
	with open('charge.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		resis, atms, charges = [],[],[]
		
		for row in reader:
			resis.append(row['Residue'])
			atms.append(row['atom'])
			charges.append(float(row['charge']))	

	for index1, data in enumerate(id_d_random):
		for index, c in enumerate(charges):
			if p1_resname_random[index1]==resis[index] and p1_atname_random[index1]==atms[index]:
				charge_at1.append(charges[index])
			if p2_resname_random[index1]==resis[index] and p2_atname_random[index1]==atms[index]:
				charge_at2.append(charges[index])


	#print id_d[0],p1_resname[0],p2_atname[0],charge_at1[0],p2_resname[0],p2_atname[0], charge_at2[0]
	#print id_d[1],p1_resname[1],p2_atname[1],charge_at1[1],p2_resname[1],p2_atname[1], charge_at2[1]
#--------------------------------------------------------------------------------#

def getpolarity():
	with open('polarity.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		r, po = [], []
		
		for row in reader:
			r.append(row['res'])
			po.append(row['polarity'])


	for res1, res2 in zip(p1_resname_random, p2_resname_random):
		for index, data in enumerate(po):
			if res1 == r[index]:
				polarity_res1.append(po[index])
			if res2 == r[index]:
				polarity_res2.append(po[index])

#--------------------------------------------------------------------------------#

def getcovalentbonds():
	with open("covalent.txt") as f:
		content = f.read().splitlines()	

	for r, a, r1, a1 in zip(p1_resname_random, p1_atname_random, p2_resname_random, p2_atname_random):
		occurrences1 = 0
		occurrences2 = 0
		for i, c in enumerate(content):
			aux = c.split(",")

			if r == aux[1]:
				idx1 = i+1
				aux1 = content[idx1].split(",")
		 		while aux1[0] == "BOND" or aux1[0] == "DOUBLE":
		 			occurrences1 += aux1.count(a)
		 			idx1 = idx1+1
		 			if 0 <= idx1 < len(content):
		 				aux1 = content[idx1].split(",")
		 			else:
		 				break

		 	if r1 == aux[1]:
				idx2 = i+1
				aux2 = content[idx2].split(",")
		 		while aux2[0] == "BOND" or aux2[0] == "DOUBLE":
		 			occurrences2 += aux2.count(a1)
		 			idx2 = idx2+1
		 			if 0 <= idx2 < len(content):
		 				aux2 = content[idx2].split(",")
		 			else:
		 				break
		number_at1.append(str(occurrences1))
		number_at2.append(str(occurrences2))
#--------------------------------------------------------------------------------#

def getaminoacidtype():
	with open('amino_acid_types.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		r, ty = [], []
		
		for row in reader:
			r.append(row['res'])
			ty.append(row['type'])


	for res1, res2 in zip(p1_resname_random, p2_resname_random):
		for index, data in enumerate(ty):
			if res1 == r[index]:
				res_type1.append(ty[index])
			if res2 == r[index]:
				res_type2.append(ty[index])


#--------------------------------------------------------------------------------#

def savef(s):

	zipped = zip(id_d_random, 
		p1_resname_random, polarity_res1, res_type1, 
		p1_atname_random, charge_at1, number_at1,
	    p2_resname_random, polarity_res2, res_type2,
	    p2_atname_random, charge_at2, number_at2, distance_random, p_random)

	np.savetxt(s, zipped, header="id,p1_resname,polarity_res1,res_type1,"+
		"p1_atname,charge_at1,valence_at1,"+
		"p2_resname,polarity_res2,res_type2,"+
		"p2_atname,charge_at2,valence_at2,"+
		"distance,interaction", 
		fmt='%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s', comments='')


#---------------------------------------------------------------------------------#
s = 'hb.csv'

read_file()
#getcontact_dist()
#getcharge()
#getpolarity()
#getcovalentbonds()
#getaminoacidtype()
#savef(s)

print 'Data saved to file '+s			
#---------------------------------------------------------------------------#	
		