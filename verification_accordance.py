import os
def getDirsInDir(path):
	dirs=[];
	for parents,dirnames,filenames in os.walk(path):
		for dirname in dirnames:
			dirs.append(dirname)
	return dirs

all_patterns={'Blouses_w':2,'Capes_w':3,'Cardigans_w':4,'Coats_w':5,'Costumes_w':6,'Dresses_w':7,'Jackets&Blazers_w':8,
'Jumpsuits_w':9,'Lingerie&Loungewear_w':10,'Workout Wear_w':101,'Maternity_w':11,'Pants_w':12,
'Shorts_w':14,'Swimwear_w':16,'Tanks_w':17,'Tops_w':18,'Vests_w':19,'Other_w':21,
'Coats_m':23,'Costumes_m':24,'Jackets&Blazers_m':25,'Pants_m':26,'Shirts_m':27,'Tops_m':28,'Shorts_m':29,'Vests_m':31}

root_path='D:/burdastyle_data/'
for pattern in all_patterns:
	print pattern
	dir_path=root_path+pattern+'/'
	fid=open(dir_path+pattern+'.txt','r')
	heading_list=[]
	heading=fid.readline()
	while heading!='':
		heading=heading[:-1]
		heading_list.append(heading)
		tmp=fid.readline()
		tmp=fid.readline()
		img_n=int(tmp)
		imgs=[]
		for i in range(img_n):
			img_url=fid.readline()[:-1]
		heading=fid.readline()
	fid.close()
	item_count=len(heading_list)
	dirs=getDirsInDir(dir_path)
	print len(dirs)
	print item_count
	if len(dirs)!=item_count:
		print 'Disaccordance error'
		os.system('pause')
	else:
		print 'pass'