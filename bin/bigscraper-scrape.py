#!/usr/bin/python3

# Neoscrape
# New scraping test that finds game pages directly through web browsing, no metadata.xml required. Insanity.

"""
General Process

1. Get the platform name using convert.json/convert_flip.json
2. Get the platform id of the system using abbr_id.json
3. !!Download the 1st page (https://gamesdb.launchbox-app.com/platforms/games/[id]). Get the number of pages.!! No more

4. Run through the current page to try to find the name of the game entry. If so, step 6.
5. If not found, go to the next page, unless there are no more pages, then repeat step 4.

6. If a game is found, visit its link, and scrape the website for details, then images. You will also have a database id.
7. Copy text data to the scrape_cache under scrape_cache/[system]/[name].
8. Get the name of each image, then download it under img_cache/[system]/[image_name].

9. If no games are found, let the user know.

"""

def invalid(code):
	print("Issue Found:")
	if (code == 0):
		print("The file specified does not exist.")
	if (code == 1):
		print("Incorrect number of arguments:")
	if (code == 2):
		print("Invalid System. Please specify a valid system name or abbreviation. (run bigscraper help systems for more)")

	print("Run bigscraper.py scrape help for additional help")
	sys.exit()

# Color output
uc = "\033[0m"
def color(r, g, b, background=False):
	return "\033[{};2;{};{};{}m".format(48 if background else 38, r, g, b)

#
# Begin the actual program
#

# Invalid Checks
if not(os.path.isfile(sys.argv[3])):
	invalid(0)

if (len(sys.argv) != 4):
	invalid(1)

if (toabbr(sys.argv[2]) == "NOABBR"):
	invalid(2)



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

### STEP 1/2
sysid = toid(toabbr(sys.argv[2]))


### STEPS 4/5
# Initialize some variables
file_title = formulate(os.path.basename(sys.argv[3][0:sys.argv[3].rfind(".")]))
currentPage = 1
found = False

# Get 1st page
print("Getting Page " + color(243, 157, 57) + str(currentPage) + uc)
page = requests.get("https://gamesdb.launchbox-app.com/platforms/games/" + sysid + "|" + str(currentPage))
pagetree = html.fromstring(page.content)

# This xpath checks if any games exist on the page
page_gis = pagetree.xpath('//a[@class="list-item"]')

while (len(page_gis) != 0):
	print("Searching Page " + color(243, 157, 57) + str(currentPage) + uc)

	# Scan through each text item
	game_titles = pagetree.xpath("//div[@class='col-sm-10']/h3[1]/text()")
	f_game_titles = list()
	for t in game_titles:
		f_game_titles.append(formulate(t))

	if (file_title in f_game_titles):
		print(color(240, 112, 3) + "Game Found." + uc)
		found = True
		break
	else:
		currentPage += 1

		print("Getting Page " + color(243, 157, 57) + str(currentPage) + uc)
		page = requests.get("https://gamesdb.launchbox-app.com/platforms/games/" + sysid + "|" + str(currentPage))
		pagetree = html.fromstring(page.content)
		page_gis = pagetree.xpath('//a[@class="list-item"]')

if (found):
	# Get the game details link from the list of links and titles
	game_index = f_game_titles.index(file_title)
	details_link = pagetree.xpath('//a[@class="list-item"]/@href')[game_index]
	full_dl = "https://gamesdb.launchbox-app.com" + details_link

	### STEP 6
	ddi = {}
	ddi["File"] = sys.argv[3]

	print("Getting " + color(10, 165, 253) + "Details" + uc + " Page")
	details_page = requests.get(full_dl)
	details = html.fromstring(details_page.content)

	# Step 6 Part 1
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

	print(color(10, 165, 253) + "Details" + uc + " Compilation Complete.")

	# Step 6 Part 2
	dbid = full_dl.rsplit('/', 1)[-1]
	images_link = "https://gamesdb.launchbox-app.com/games/images/" + dbid

	print("Getting " + color(0, 135, 175) + "Images" + uc + " Page")
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

	print(color(0, 135, 175) + "Images" + uc + " Compilation Complete.")


	### STEP 7
	ddi_json = json.dumps(ddi, indent = 4)

	open(wd + "scrape_cache/" + toabbr(sys.argv[2]) + "/" + formulate(ddi["Name"][0]) + ".json", "w").write(ddi_json)

	print(color(24, 176, 30) + "Process Complete." + uc)
else:
	print(color(255, 75, 75) + "Game Not Found." + uc)
	print(color(24, 176, 30) + "Process Complete." + uc)



