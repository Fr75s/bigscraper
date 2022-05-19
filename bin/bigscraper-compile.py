#!/usr/bin/python3

# compile.py
# Compiles scraped data into formats used by other software

dmy_convert = {
	"January": "01",
	"February": "02",
	"March": "03",
	"April": "04",
	"May": "05",
	"June": "06",
	"July": "07",
	"August": "08",
	"September": "09",
	"October": "10",
	"November": "11",
	"December": "12"
}


def invalid(code):
	print("Issue Found:")
	if (code == 0):
		print("Invalid System. Please specify a valid system name or abbreviation. (run bigscraper help systems for more)")
	if (code == 1):
		print("Invalid Export Type. Please specify a valid export type. Run bigscraper help exports for more information.")
	if (code == 2):
		print("Output folder specified does not exist.")
	if (code == 3):
		print("Incorrect Parameters.")
	if (code == 4):
		print("Either scrape_cache or image_cache doesn't exist or each is empty. Scrape games to create them.")

	print("Run bigscraper.py compile help for additional help")
	sys.exit()

def listin(compares, l):
	for c in compares:
		if c in l:
			return True
	return False

# Color output
uc = "\033[0m"
def color(r, g, b, background=False):
	return "\033[{};2;{};{};{}m".format(48 if background else 38, r, g, b)


# Checks
if (len(sys.argv) != 4 and len(sys.argv) != 5):
	invalid(3)

if (toabbr(sys.argv[2]) == "NOABBR"):
	invalid(0)

if not(formulate(sys.argv[3]) in ("PEGASUS", "PEGASUS_FRONTEND")):
	invalid(1)

cache_path = os.path.expanduser("~") + "/Documents/bigscraper/cache/"

if not(os.path.isdir(cache_path + "scrape_cache") and os.path.isdir(cache_path + "img_cache")):
	invalid(4)

if (len(sys.argv) == 5 and not(os.path.isdir(sys.argv[4]))):
	invalid(2)

a = toabbr(sys.argv[2])

if not(os.path.isdir(cache_path + "scrape_cache/" + a) and os.path.isdir(cache_path + "img_cache/" + a)):
	invalid(4)

if len(os.listdir(cache_path + "scrape_cache/" + a)) == 0 or len(os.listdir(cache_path + "img_cache/" + a)) == 0:
	invalid(4)


# Begin Compilation
out_path = os.path.expanduser("~") + "/Documents/bigscraper/output/" + a + "/"
if (len(sys.argv) == 4):
	if not(os.path.isdir(os.path.expanduser("~") + "/Documents/bigscraper/")):
		os.mkdir(os.path.expanduser("~") + "/Documents/bigscraper/")

	if not(os.path.isdir(os.path.expanduser("~") + "/Documents/bigscraper/output/")):
		os.mkdir(os.path.expanduser("~") + "/Documents/bigscraper/output/")

	if not(os.path.isdir(os.path.expanduser("~") + "/Documents/bigscraper/output/" + a + "/")):
		os.mkdir(os.path.expanduser("~") + "/Documents/bigscraper/output/" + a + "/")
else:
	out_path = sys.argv[4]
	if not(out_path[-1] == "/"):
		out_path += "/"

if not(os.path.isdir(out_path)):
	os.mkdir(out_path)

if not(os.path.isdir(out_path + "/media")):
	os.mkdir(out_path + "/media")


scrape_path = cache_path + "scrape_cache/" + a + "/"
image_path = cache_path + "img_cache/" + a + "/"


if (formulate(sys.argv[3]) in ("PEGASUS", "PEGASUS_FRONTEND", "PEGASUS_FE")):
	#
	# Compile to Pegasus Frontend
	# metadata.pegasus.txt
	#
	print("Compiling to " + color(255, 75, 75) + "Pegasus Frontend" + uc)

	if (os.path.isfile(out_path + "/metadata.pegasus.txt")):
		os.remove(out_path + "/metadata.pegasus.txt")

	outfile = open(out_path + "/metadata.pegasus.txt", "a")

	out = []

	out.append("collection: " + convert_rev[a])
	out.append("\nshortname: " + a)
	out.append("\ncommand: INSERT_COMMAND_HERE")
	out.append("\n")

	gameIndex = 0
	for datafile in os.listdir(scrape_path):
		full = scrape_path + datafile
		data = json.load(open(full, "r"))

		gameIndex += 1
		print("Game " + color(243, 157, 57) + str(gameIndex) + uc + " of " + color(240, 112, 3) + str(len(os.listdir(scrape_path))) + uc + ": " + data["Name"][0])


		out.append("\ngame: " + data["Name"][0])
		out.append("\nfile: " + data["File"])
		out.append("\nrating: " + (str(float(data["Rating"][0]) / 5.0) if "Rating" in data else "0.0"))
		out.append("\ndescription: " + (data["Overview"][0] if "Overview" in data else "-"))
		out.append("\nsummary: " + (data["Overview"][0] if "Overview" in data else "-"))

		if ("Developers" in data):
			for d in data["Developers"]:
				out.append("\ndevelopers: " + d)
		if ("Publishers" in data):
			for d in data["Publishers"]:
				out.append("\npulishers: " + d)
		if ("Genres" in data):
			for d in data["Genres"]:
				out.append("\ngenres: " + d)

		out.append("\nplayers: " + (data["Max Players"][0] if "Max Players" in data else "1"))

		#dateform = (data["Release Date"][0].split(" ") if "Release Date" in data else ["January", "1,", "1970"])
		dateform = ["January", "1,", "1970"]
		if ("Release Date" in data):
			if (len(data["Release Date"][0]) > 4):
				dateform = data["Release Date"][0].split(" ")

				date_month = dmy_convert[dateform[0]]
				date_day = dateform[1].split(",")[0]
				if (int(date_day) < 10):
					date_day = "0" + date_day

				out.append("\nrelease: " + dateform[2] + "-" + date_month + "-" + date_day)
				out.append("\nreleaseYear: " + dateform[2])
				out.append("\nreleaseMonth: " + date_month)
				out.append("\nreleaseDay: " + date_day)
			else:
				dateform = data["Release Date"][0]
				out.append("\nreleaseYear: " + dateform)

		img_boxFront = ""
		boxFrontExists = False
		if not(os.path.isdir(out_path + "/media/covers")):
			os.mkdir(out_path + "/media/covers")
		if listin(["Box - Front"], str(data["Images"])):
			for img in reversed(data["Images"]):
				if listin(["Box - Front"], img):
					for imgfile in os.listdir(cache_path + "img_cache/" + a):
						if (img in imgfile and listin(("North America", "United States", "World"), imgfile)):
							boxFrontExists = True
							shutil.copyfile(cache_path + "img_cache/" + a + "/" + imgfile, out_path + "/media/covers/" + formulate(data["Name"][0]) + ".png")
		if (boxFrontExists):
			out.append("\nassets.boxFront: media/covers/" + formulate(data["Name"][0]) + ".png")


		img_boxBack = ""
		boxBackExists = False
		if not(os.path.isdir(out_path + "/media/backcovers")):
			os.mkdir(out_path + "/media/backcovers")
		if listin(["Box - Back"], str(data["Images"])):
			for img in reversed(data["Images"]):
				if listin(["Box - Back"], img):
					for imgfile in os.listdir(cache_path + "img_cache/" + a):
						if (img in imgfile and listin(("North America", "United States", "World"), imgfile)):
							boxBackExists = True
							shutil.copyfile(cache_path + "img_cache/" + a + "/" + imgfile, out_path + "/media/backcovers/" + formulate(data["Name"][0]) + ".png")
		if (boxBackExists):
			out.append("\nassets.boxBack: media/backcovers/" + formulate(data["Name"][0]) + ".png")


		img_logo = ""
		logoExists = False
		if not(os.path.isdir(out_path + "/media/logos")):
			os.mkdir(out_path + "/media/logos")
		if listin(["Clear Logo"], str(data["Images"])):
			for img in reversed(data["Images"]):
				if listin(["Clear Logo"], img):
					for imgfile in os.listdir(cache_path + "img_cache/" + a):
						if (img in imgfile and listin(("North America", "United States", "World"), imgfile)):
							logoExists = True
							shutil.copyfile(cache_path + "img_cache/" + a + "/" + imgfile, out_path + "/media/logos/" + formulate(data["Name"][0]) + ".png")
		if (logoExists):
			out.append("\nassets.logo: media/logos/" + formulate(data["Name"][0]) + ".png")
			out.append("\nassets.wheel: media/logos/" + formulate(data["Name"][0]) + ".png")


		img_physical = ""
		physicalExists = False
		if not(os.path.isdir(out_path + "/media/physical")):
			os.mkdir(out_path + "/media/physical")
		if listin(["Cart - Front", "Disc"], str(data["Images"])):
			for img in reversed(data["Images"]):
				if listin(["Cart - Front", "Disc"], img):
					for imgfile in os.listdir(cache_path + "img_cache/" + a):
						if (img in imgfile and listin(("North America", "United States", "World"), imgfile)):
							physicalExists = True
							shutil.copyfile(cache_path + "img_cache/" + a + "/" + imgfile, out_path + "/media/physical/" + formulate(data["Name"][0]) + ".png")
		if (physicalExists):
			out.append("\nassets.cartridge: media/physical/" + formulate(data["Name"][0]) + ".png")


		img_background = ""
		backgroundExists = False
		if not(os.path.isdir(out_path + "/media/background")):
			os.mkdir(out_path + "/media/background")
		if ("Background" in str(data["Images"])):
			for img in reversed(data["Images"]):
				if ("Background" in img):
					for imgfile in os.listdir(cache_path + "img_cache/" + a):
						if (img in imgfile):
							backgroundExists = True
							shutil.copyfile(cache_path + "img_cache/" + a + "/" + imgfile, out_path + "/media/background/" + formulate(data["Name"][0]) + ".png")
		if (backgroundExists):
			out.append("\nassets.background: media/background/" + formulate(data["Name"][0]) + ".png")


		img_titlescreen = ""
		titlescreenExists = False
		if not(os.path.isdir(out_path + "/media/titlescreen")):
			os.mkdir(out_path + "/media/titlescreen")
		if ("Screenshot - Game Title" in str(data["Images"])):
			for img in reversed(data["Images"]):
				if ("Screenshot - Game Title" in img):
					for imgfile in os.listdir(cache_path + "img_cache/" + a):
						if (img in imgfile):
							titlescreenExists = True
							shutil.copyfile(cache_path + "img_cache/" + a + "/" + imgfile, out_path + "/media/titlescreen/" + formulate(data["Name"][0]) + ".png")
		if (titlescreenExists):
			out.append("\nassets.titlescreen: media/titlescreen/" + formulate(data["Name"][0]) + ".png")


		img_gameplay = ""
		gameplayExists = False
		if not(os.path.isdir(out_path + "/media/gameplay")):
			os.mkdir(out_path + "/media/gameplay")
		if ("Screenshot - Gameplay" in str(data["Images"])):
			for img in reversed(data["Images"]):
				if ("Screenshot - Gameplay" in img):
					for imgfile in os.listdir(cache_path + "img_cache/" + a):
						if (img in imgfile):
							gameplayExists = True
							shutil.copyfile(cache_path + "img_cache/" + a + "/" + imgfile, out_path + "/media/gameplay/" + formulate(data["Name"][0]) + ".png")
		if (gameplayExists):
			out.append("\nassets.screenshot: media/gameplay/" + formulate(data["Name"][0]) + ".png")
		elif (titlescreenExists):
			out.append("\nassets.screenshot: media/titlescreen/" + formulate(data["Name"][0]) + ".png")

		out.append("\n\n")

	outfile.writelines(out)
	outfile.close()

	print("\nOutput written to " + color(10, 165, 253) + out_path + uc)
	print(color(24, 176, 30) + "Process Complete." + uc)










