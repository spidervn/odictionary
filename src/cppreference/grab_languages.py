
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


def grab_sub_page(page_url, deep_level):
	print (page_url)

	PAGE_MAINURL="https://en.cppreference.com"

	rq = requests.get(PAGE_MAINURL + page_url)
	data = rq.text
	soup = BeautifulSoup(data)

	myhtml = ""
	hd = soup.find(id="firstHeading")
	bc = soup.find(id="bodyContent")

	if deep_level == 2:
		myhtml += "<h2>" + hd.text + "<h2>"
	elif deep_level == 3:
		myhtml += "<h3>" + hd.text + "<h3>"
	else:
		myhtml += "<h4>" + hd.text + "<h4>"
	myhtml += "<div>"
	myhtml += str(bc)
	myhtml += "</div>"

	return myhtml

def grab_cppreference_language(url, outfile):
	# url =https://en.cppreference.com/w/cpp/language
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

	html = "<html>"
	html += "<head>"	
	html += "<title>" + soup.title.string + "</title>"
	html += "</head>"
	html += "<body>"
	html += "<h1>" + soup.title.string + "</h1>"
	page_count = 1
	fcontent = soup.find_all(id="mw-content-text")
	ftable = soup.find("table")

	html += "<div>"
	html += str(fcontent[0])
	html += "</div>"
	html += "</body>"

	list_title = ftable.find_all("a")

	for one_title in list_title:
		print(one_title)
		if one_title.parent.name == "b":
			html += grab_sub_page(one_title["href"], 2)
		else:
			html += grab_sub_page(one_title["href"], 3)

	f = open(outfile, "w+", encoding="utf-8")
	f.write(html)
	f.close()

	return html

grab_cppreference_language("https://en.cppreference.com/w/cpp/language", "a.html")	
