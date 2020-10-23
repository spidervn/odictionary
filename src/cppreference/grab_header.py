
from bs4 import BeautifulSoup
import requests

def get_count_page(page_summary):
	page_count = 1
	index = page_summary.find('of')
	if index >= 0:
		page_count = int(page_summary[(index+2):])
	return page_count

def get_goto_page_link(current_url, page_index):

	rq = requests.get(current_url)
	data = rq.text
	mysoup = BeautifulSoup(data)
	fpaginate = mysoup.find_all(id="pagination_top")

	link = ""
	page_str = str(page_index)

	fhrefs = fpaginate[0].find_all("a")

	for ahref in fhrefs:
		if ahref.text == page_str:
			link = ahref["href"]
	return link

def grab_a_page(page_url):
	rq = requests.get(page_url)
	data = rq.text
	soup = BeautifulSoup(data)

	f_div_posts = soup.find(id="postlist")
	f_li_posts = f_div_posts.find_all("li", class_="postbitlegacy")
	myhtml = ""

	print("LEN=", len(f_li_posts))

	for f_li_post in f_li_posts:

		username = ""
		member_type = ""
		userinfo_extra = ""
		posthead = ""
		content = ""

		f_div_posthead = f_li_post.find("div", class_="posthead")
		f_a_user = f_li_post.find("div", class_="username_container")
		f_member_type = f_li_post.find("span", class_="usertitle")
		f_userinfo_extra = f_li_post.find("dl", class_="userinfo_extra")
		f_content = f_li_post.find("div", class_="content")
		
		username = f_a_user.text
		member_type = f_member_type.text
		userinfo_extra = f_userinfo_extra.text
		posthead = f_div_posthead.text
		content = f_content.text

		# print("APost **************************")
		# print("-- PostDate:", posthead)
		# print("-- UserName:", username)
		# print("-- Extra Info:", userinfo_extra)
		# print("-- Content: ")
		# print("*******************************")
		# print(content)
		# print("")

		myhtml += "<h4>user: " + username + "</h4>"
		myhtml += "<p><strong>Post: " + posthead + "</strong></p>"
		myhtml += "<p><strong>member_type: " + member_type + "</strong></p>"
		myhtml += "<p><strong>user-info: " + userinfo_extra + "</strong></p>"
		myhtml + "<p>------------------------------------</p>"
		myhtml += "<div>" + f_content.prettify() + "</div>"
		myhtml += "<br/>"	

	return myhtml	



def grab_sub_page(page_url, deep_level, toc_id_now):
	PAGE_MAINURL="https://en.cppreference.com"
	url_full = PAGE_MAINURL + page_url
	print ("FULL URL ", url_full)

	rq = requests.get(url_full)
	data = rq.text
	soup = BeautifulSoup(data)

	myhtml = ""
	hd = soup.find(id="firstHeading")
	bc = soup.find(id="mw-content-text") # soup.find(id="bodyContent")
	div_navbar = bc.find("div", class_="t-navbar")
	table_toc = bc.find(id="toc")
	str_toc = "toc_" + str(toc_id_now+1)
	if div_navbar != None:
		div_navbar.clear()
	if table_toc != None:
		table_toc.clear()

	if deep_level == 1:
		myhtml += "<h1 id='" + str_toc  +"' class='color_blue'>" + hd.text + "</h1>"
	elif deep_level == 2:
		myhtml += "<h2 id='" + str_toc + "' class='color_l1blue'>" + hd.text + "</h2>"
	elif deep_level == 3:
		myhtml += "<h3 id='" + str_toc + "' class='color_l2blue'>" + hd.text + "</h3>"
	else:
		myhtml += "<h4 id='" + str_toc + "' class='color_l2blue'>" + hd.text + "</h4>"
	myhtml += "<div>"
	myhtml += str(bc)
	myhtml += "</div>"

	f = open("sub.html", "w+", encoding="utf-8")
	f.write(myhtml)
	f.close()

	return [ myhtml, hd.text, toc_id_now + 1]



def grab_cppreference_header(url, outfile):
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)
	toc_id_now = 1
	tocdict = {}
	tocdict[toc_id_now] = [ soup.title.string, 1]

	page_count = 1
	fcontent = soup.find(id="mw-content-text")
	ftables = fcontent.find_all("table")
	ftable = None

	for table1 in ftables:
		if 'class' in table1.attrs:
			print(type(table1))
			print("Classs=", type(table1.attrs))
		else:
			ftable = table1
			break
		# if table1['class'][0] != 't-nv-begin':
		# 	print("Found Table=", table1)
		# 	ftable = table1
		# 	break

	htmlbody = ""
	htmlbody += "<h1 id='toc_1' class='color_blue'>" + soup.title.string + "</h1>"
	htmlbody += "<div>"
	htmlbody += str(str(fcontent))
	htmlbody += "</div>"

	list_title = ftable.find_all("a")
	count = 0

	for one_title in list_title:
		print(one_title)
		if one_title.parent.name == "b":
			deep_level = 1

			grab_r = grab_sub_page(one_title["href"], deep_level, toc_id_now) 
			htmlbody += grab_r[0]
			toc_id_now = grab_r[2]
			tocdict[grab_r[2]] = [ grab_r[1], deep_level]
		
        else:
			deep_level = 2
			grab_r = grab_sub_page(one_title["href"], deep_level, toc_id_now)
			htmlbody += grab_r[0]
			toc_id_now = grab_r[2]
			tocdict[grab_r[2]] = [ grab_r[1], deep_level]

		count += 1
		if count > 4:
			# break
			pass
	tochtml = "<div>"
	for i in range(1,toc_id_now+1):
		if tocdict[i][1] == 1:
			tochtml += "<p><a href='#toc_" + str(i) + "'>" + tocdict[i][0] + "</a></p>"
		elif tocdict[i][1] == 2:
			tochtml += "<p><a href='#toc_" + str(i) + "'>&nbsp;&nbsp;&nbsp;&nbsp;" + tocdict[i][0] + "</a></p>"
		else:
			tochtml += "<p><a href='#toc_" + str(i) + "'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + tocdict[i][0] + "</a></p>"
	tochtml += "</div>"

	html = "<html>"
	html += "<head>"
	html += str(soup.head)
	# html +=  "<title>" + soup.title.string + "</title>"

	html += "<body>"
	html += """<style type="text/css">
		.color_blue {
			color: #0000FF;
		}

		.color_l1blue {
			color #0707FF;
		};

		.color_l2blue {
			color #AAAAFF;
		};
	</style>
	"""	
	html += tochtml
	html += htmlbody
	html += "</body>"

	f = open(outfile, "w+", encoding="utf-8")
	f.write(html)
	f.close()

	return html

grab_cppreference_header("https://en.cppreference.com/w/cpp/header", "header.html")	
#
# grab_sub_page()
# grab_sub_page("/w/cpp/header", 2);
#

#
# r  = requests.get("https://en.cppreference.com/w/cpp/header")
# data = r.text
# soup = BeautifulSoup(data)
#

# print(str(soup.head))

# bc = soup.find(id="bodyContent")
# print(bc)
# f = open("cc.html", "w+", encoding="utf-8")
# f.write(str(bc))
# f.close()
