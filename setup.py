from setuptools import setup

setup(
	name = "bigscraper-cli",
	version = "1.0",
	description = "Metadata scrpaing tool for Launchbox",
	keywords = "scraper launchbox metadata",
	author = "Fr75s",

	scripts = [
		"bin/bigscraper",
		"bin/bigscraper-bulk.py",
		"bin/bigscraper-compile.py",
		"bin/bigscraper-data.py",
		"bin/bigscraper-scrape.py"
	],

	install_requires = [
		"lxml",
		"requests"
	]
)
