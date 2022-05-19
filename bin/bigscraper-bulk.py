#!/usr/bin/python3

# bulk
# Scraping an entire folder.

"""
General Process

1. Get the platform name using convert.json/convert_flip.json
2. Get the platform id of the system using abbr_id.json

3. Download the next page, and see if there are any matches. If so, download the pages for the game's sites and put their info similarly to neoscrape.py.
4. If there are no more games to be found in the page, move on
5. If there are more pages, repeat step 3, otherwise stop.

"""

def title(f):
	return formulate(f[0:f.rfind(".")])

def invalid(code):
	print("Issue Found:")
	if (code == 0):
		print("The folder specified does not exist.")
	if (code == 1):
		print("Incorrect number of arguments:")
	if (code == 2):
		print("Invalid System. Please specify a valid system name or abbreviation. (run bigscraper help systems for more)")

	print("Run bigscraper.py scrape -h for additional help")
	sys.exit()

# Color output
uc = "\033[0m"
def color(r, g, b, background=False):
	return "\033[{};2;{};{};{}m".format(48 if background else 38, r, g, b)


# Invalid Checks
if not(os.path.isdir(sys.argv[3])):
	invalid(0)

if (len(sys.argv) != 4):
	invalid(1)

if (toabbr(sys.argv[2]) == "NOABBR"):
	invalid(2)

# Folder Creation
if not(os.path.isdir(os.path.expanduser("~") + "/Documents/bigscraper/")):
	os.mkdir(os.path.expanduser("~") + "/Documents/bigscraper/")

if not(os.path.isdir(os.path.expanduser("~") + "/Documents/bigscraper/cache/")):
	os.mkdir(os.path.expanduser("~") + "/Documents/bigscraper/cache/")

wd = os.path.expanduser("~") + "/Documents/bigscraper/cache/"

if not(os.path.isdir(wd + "scrape_cache")):
	print("Making Folder " + color(10, 165, 253) + wd + "scrape_cache" + uc)
	os.mkdir(wd + "scrape_cache")

if not(os.path.isdir(wd + "img_cache")):
	print("Making Folder " + color(10, 165, 253) + wd + "img_cache" + uc)
	os.mkdir(wd + "img_cache")

if not(os.path.isdir(wd + "scrape_cache/" + toabbr(sys.argv[2]))):
	print("Making Folder " + color(10, 165, 253) + wd + "scrape_cache/" + toabbr(sys.argv[2]) + uc)
	os.mkdir(wd + "scrape_cache/" + toabbr(sys.argv[2]))

if not(os.path.isdir(wd + "img_cache/" + toabbr(sys.argv[2]))):
	print("Making Folder " + color(10, 165, 253) + wd + "img_cache/" + toabbr(sys.argv[2]) + uc)
	os.mkdir(wd + "img_cache/" + toabbr(sys.argv[2]))


gamepath = sys.argv[3]
if not(gamepath[-1] == "/"):
	gamepath += "/"


# Start Getting Game List Pages
currentPage = 1

gameslist = []
for f in os.listdir(gamepath):
	if not(os.path.splitext(os.path.basename(f))[1] in nongame_extensions):
		if not(os.path.isdir(gamepath + f)):
			gameslist.append(f)

print("Scanning for " + color(240, 112, 3) + str(len(gameslist)) + uc + " games")

sysid = toid(toabbr(sys.argv[2]))



# Get 1st page
print("Getting Page " + color(243, 157, 57) + str(currentPage) + uc)
page = requests.get("https://gamesdb.launchbox-app.com/platforms/games/" + sysid + "|" + str(currentPage))
pagetree = html.fromstring(page.content)
# This xpath checks if any games exist on the page
page_gis = pagetree.xpath('//a[@class="list-item"]')

gamesFound = 0
while (len(page_gis) != 0):
	print("Searching Page " + color(243, 157, 57) + str(currentPage) + uc)

	# Scan through each text item
	game_titles = pagetree.xpath("//div[@class='col-sm-10']/h3[1]/text()")
	f_game_titles = list()
	for t in game_titles:
		f_game_titles.append(formulate(t))

	for g in gameslist:
		if (title(g) in f_game_titles):
			gamesFound += 1
			print("Game " + color(243, 157, 57) + str(gamesFound) + uc + " of " + color(240, 112, 3) + str(len(gameslist)) + uc + " found: " + title(g))

			print("Getting " + color(10, 165, 253) + "Details" + uc)
			game_index = f_game_titles.index(title(g))
			details_link = pagetree.xpath('//a[@class="list-item"]/@href')[game_index]
			full_dl = "https://gamesdb.launchbox-app.com" + details_link

			details_page = requests.get(full_dl)
			details = html.fromstring(details_page.content)

			ddi = {}
			ddi["File"] = gamepath + g

			info = details.xpath('//td[@class="row-header"]/text()')
			for i in info:
				if i in ("Name", "Platform", "Release Date", "Game Type", "ESRB", "Max Players", "Cooperative"):
					ddi[i] = details.xpath('//td[@class="row-header" and text()="' + i + '"]/../td[2]/span[1]/text()')
				if i in ("Developers", "Publishers", "Genres", "Wikipedia", "Video Link"):
					ddi[i] = details.xpath('//td[@class="row-header" and text()="' + i + '"]/../td[2]/span[1]/a/text()')
				if i in ("Overview"):
					ddi[i] = details.xpath('//div[@class="view"]/text()')
				if i in ("Rating"):
					ddi[i] = details.xpath('//span[@id="communityRating"]/text()')

			# Step 6 Part 2
			print("Getting " + color(0, 135, 175) + "Images" + uc + " for " + title(g))
			dbid = full_dl.rsplit('/', 1)[-1]
			images_link = "https://gamesdb.launchbox-app.com/games/images/" + dbid

			images_page = requests.get(images_link)
			images = html.fromstring(images_page.content)

			image_links = images.xpath('//a[contains(@href, "https://images.launchbox-app.com")]/@href')
			image_titles = images.xpath('//a[contains(@href, "https://images.launchbox-app.com")]/@data-title')

			index = 0
			for link in image_links:
				corres_title = image_titles[index]
				extension = os.path.splitext(link)[1]

				### STEP 8
				print("Downloading Image " + color(243, 157, 57) + str(index + 1) + uc + " of " + color(240, 112, 3) + str(len(image_links)) + uc)

				image = requests.get(link)
				open(wd + "img_cache/" + toabbr(sys.argv[2]) + "/" + corres_title + extension, "wb").write(image.content)

				index += 1

			ddi["Images"] = (image_titles if len(image_titles) > 0 else ["NULL"])
			ddi_json = json.dumps(ddi, indent = 4)

			open(wd + "scrape_cache/" + toabbr(sys.argv[2]) + "/" + formulate(ddi["Name"][0]) + ".json", "w").write(ddi_json)

			print(color(1, 141, 129) + "Metadata Successfully Gathered" + uc + " for " + title(g))

	currentPage += 1
	page = requests.get("https://gamesdb.launchbox-app.com/platforms/games/" + sysid + "|" + str(currentPage))
	pagetree = html.fromstring(page.content)
	page_gis = pagetree.xpath('//a[@class="list-item"]')

print(color(10, 165, 253) + "Last Page Reached." + uc)
print(color(24, 176, 30) + "Process Complete." + uc)








