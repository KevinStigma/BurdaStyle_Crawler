# coding: utf-8
import urllib2
import urllib
import httplib
import os
import re

def requestforPageHtml(url):
	req = urllib2.Request(url)   
	req.add_header('User-Agent','Chrome')
	try: 
		myResponse = urllib2.urlopen(req)
		myPage = myResponse.read()
		print 'get page successfully!'
		print url
	except urllib2.HTTPError, e:
		print 'The server couldn\'t fulfill the request.'
		print 'Error code: ',e.code
		print url
		return 'F'
	except urllib2.URLError,e:
		print 'We failed to reach a server.'
		print 'Reason: ',e.reason
		print url
		return 'F'
	except httplib.IncompleteRead, e:
		print 'IncompleteRead !'
		print url
		return 'I'
	else:
		return myPage
		
def retrieveforImage(img_url,local_save_path):
	try:
		urllib.urlretrieve(img_url,local_save_path)
		return True
	except IOError:
		print 'Can''t deal with this url.'
		return False
		
def saveImagefromUrl(img_url,local_save_path):
	is_re=False
	while is_re==False:
		is_re=retrieveforImage(img_url,local_save_path)

def getPageHtml(url):
	page_html=requestforPageHtml(url)
	while page_html=='F' or page_html=='I':
		page_html=requestforPageHtml(url)
	return page_html
	
def getPageRange(page_html):
	pags=re.findall(r'<ul class="pagination">.*?</ul>',page_html,re.S)
	if len(pags)==0:
		return 1
	pags=re.findall(r'<a.*?</a>',pags[0],re.S)
	nums=re.findall(r'\d+',pags[-2],re.S)
	nums=nums[-1]
	max_page=int(nums)
	return max_page
	
def getPageHeading(page_html):
	contents=re.search(r'<div id="page-heading" class="simple pattern pattern_store">.*?<span',page_html,re.S).group()
	contents=re.search(r'<h2>.*?<',contents,re.S).group()
	contents=re.search(r'>.*?<',contents,re.S).group()
	heading_txt=re.search(r'\w.*\w',contents).group()
	heading_txt=heading_txt.replace('\\',' ')
	heading_txt=heading_txt.replace('/',' ')
	heading_txt=heading_txt.replace(':',' ')
	return heading_txt
	
def getContentImgList(content_page_html):
	re_rules='<ul class="pattern-thumbs">.*?</div>'
	contents = re.findall(re_rules,content_page_html,re.S)
	img_txts=re.findall(r'<a href=".*?>',contents[0])
	img_urls=[]
	for parsed_text in img_txts:
		url=re.search('".*?"',parsed_text).group()
		url=url[1:-1]
		if url[-3:]=='png':
			continue
		img_urls.append(url)
	return img_urls
	
def getSubPageUrl(base_url,id):
	path_segs=base_url.split('&')
	path_segs.insert(2,'page='+str(id))
	sign='&'
	page_url=sign.join(path_segs)
	return page_url
	
def getSubPageContentsUrls(page_html):
	myItems = re.findall(r'<h3><a href=.*?>',page_html,re.S)
	count=0
	for item in myItems:
		tmp_str=re.findall(r'(".*?")',item)
		myItems[count]='http://www.burdastyle.com'+tmp_str[0][1:-1]
		count=count+1
	return myItems
	
def getDirsInDir(path):
	dirs=[];
	for parents,dirnames,filenames in os.walk(path):
		for dirname in dirnames:
			dirs.append(dirname)
	return dirs
	
def extractPatternContents(root_url):
	myPage=getPageHtml(root_url)
	max_page_id=getPageRange(myPage)
	
	print max_page_id
	path_segs=root_url.split('&')
	if len(path_segs)!=3:
		print 'Error in url''s type!'
		os.system('pause')
	
	image_list=[]
	page_list=[]
	heading_list=[]
	for page_id in range(1,max_page_id+1):
		page_url=getSubPageUrl(root_url,page_id)
		myPage=getPageHtml(page_url)
		myItems=getSubPageContentsUrls(myPage)
		for item in myItems:
			pageContent=getPageHtml(item)
			heading_txt=getPageHeading(pageContent)
			heading_list.append(heading_txt)
			img_urls=getContentImgList(pageContent)
			image_list.append(img_urls)
			page_list.append(item)
	return [image_list,page_list,heading_list]
	
all_patterns={'Blouses_w':2,'Capes_w':3,'Cardigans_w':4,'Coats_w':5,'Costumes_w':6,'Dresses_w':7,'Jackets&Blazers_w':8,
'Jumpsuits_w':9,'Lingerie&Loungewear_w':10,'Workout Wear_w':101,'Maternity_w':11,'Pants_w':12,'Shirts_w':13,
'Shorts_w':14,'Skirts_w':15,'Swimwear_w':16,'Tanks_w':17,'Tops_w':18,'Vests_w':19,'Wedding_w':20,'Other_w':21,
'Coats_m':23,'Costumes_m':24,'Jackets&Blazers_m':25,'Pants_m':26,'Shirts_m':27,'Tops_m':28,'Shorts_m':29,'Vests_m':31}
	
base_url='http://www.burdastyle.com/pattern_store/patterns?creator=6&most_recent=1&pattern_garment_type='
root_path='D:/burdastyle_data/'
f_type=open(root_path+'finished_types1.txt','w')
for pattern in all_patterns:
	print pattern
	entry_url=base_url+str(pattern_types[pattern])
	[image_list,page_list,heading_list]=extractPatternContents(entry_url)
	
	dir_path=root_path+pattern
	if not os.path.isdir(dir_path):
		os.mkdir(dir_path)
	dir_path=dir_path+'/'
	
	fid=open(dir_path+pattern+'.txt','w')
	ind=0
	for url in page_list:
		fid.write(heading_list[ind]+'\n')
		fid.write(page_list[ind]+'\n')
		fid.write(str(len(image_list[ind]))+'\n')
		for img_url in image_list[ind]:
			fid.write(img_url+'\n')
		ind=ind+1
	fid.close()
	
	ind=0
	print 'Downloading images...'
	for heading in heading_list:
		heading_dir=dir_path+heading
		print heading_dir
		
		create_folder=False
		while create_folder==False:
			if not os.path.isdir(heading_dir):
				os.mkdir(heading_dir)
				create_folder=True
			else:
				heading_dir=heading_dir+"(1)"
		#donwload the images for each page
		n=1
		for img_url in image_list[ind]:
			local_save_path=heading_dir+'/'+heading+'_'+str(n)+'.jpg'
			saveImagefromUrl(img_url,local_save_path)
			n=n+1
		ind=ind+1
	f_type.write(pattern+'\n')
	
f_type.close()

