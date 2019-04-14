
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

		myhtml += "<h3>Post: " + posthead + "</h3>"
		myhtml += "<p><strong>user: " + username + "</strong></p>"
		myhtml += "<p><strong>member_type: " + member_type + "</strong></p>"
		myhtml += "<p><strong>user-info: " + userinfo_extra + "</strong></p>"
		myhtml + "<p>------------------------------------</p>"
		myhtml += "<div>" + content + "</div>"
		myhtml += "<br/>"	

	return myhtml	

def grab_peg(url, outfile):
	# url = "https://www.pegym.com/forums/success-forum/117408-my-hanging-progression-log.html" # raw_input("Enter a website to extract the URL's from: ")
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

	html = "<html>"
	html += "<head>"	
	html += "<title>" + soup.title.string + "</title>"
	html += "</head>"
	html += "<body>"
	page_count = 1
	fpaginate = soup.find_all(id="pagination_top")
	page_link = url

	if len(fpaginate) > 0:
		f_span_summary = fpaginate[0].find_all("a", class_="popupctrl")
		if len(f_span_summary) > 0:
			page_count = get_count_page(f_span_summary[0].text)

	print("Pagecount", page_count)

	html += grab_a_page(page_link)
	for i in range(2,page_count+1):
		page_link = get_goto_page_link(page_link, i)
		print("PAGELIHNK=", page_link)
		html += grab_a_page(page_link)
	html += "</body>"

	f = open(outfile, "w+", encoding="utf-8")
	f.write(html)
	f.close()

	return html

# for link in soup.find_all('a'):
    #print(link.get('href'))
# print(soup.prettify())
# Find page count
# grab_a_page("https://www.pegym.com/forums/success-forum/117408-my-hanging-progression-log-2.html")
grab_peg("https://www.pegym.com/forums/success-forum/130248-my-first-6-months-my-gains.html", "a.html")
