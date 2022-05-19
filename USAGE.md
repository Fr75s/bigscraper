# Usage

## Table of Contents

- [Quickstart](#quickstart)
- [Help Commands](#help-commands)

## Quickstart

Using bigscraper to scrape games is very easy. This will be a quick overview for scraping. In this example, we will scrape a folder of GameCube games and output them to Pegasus, doing so in Linux.

Let's get started. Here's what our example GameCube games folder looks like.

```
~/Games/GC
|
|	Luigi's Mansion.iso
|	Dance Dance Revolution - Mario Mix.nkit.gcz
|	Super Mario Sunshine (USA).nkit.iso
|	Super Monkey Ball 2 (USA).nkit.iso
```

First, we will find out the abbreviation for the gamecube. Bigscraper accepts both full names and abbreviations, though abbreviations will shorten the commands. To do this, run the following in a terminal:

```
bigscraper help systems | grep "GameCube"
```

Here, `bigscraper help systems` lists the abbreviations and names for all systems. Normally, you would need to look through this to find the name of your system. Instead, we pipe the output (`|`) to the `grep "GameCube"` command, which finds the words "GameCube" in the output for us. This yields the following result.

```
	gc (Nintendo Gamecube)
```

The text on the left (gc) is our system abbreviation. Now we are ready to scrape games.

To scrape an entire folder, we use the command `bigscraper bulk`. For our example, the command will go as follows:

```
bigscraper bulk gc ~/Games/GC
```

In this command, you can see that the 3rd item is our system, gc, and the 4th item is the folder that contains our games. Running this command, you will see the progress done downloading metadata for each game in the ~/Games/GC folder.

Once that is done, we have collected our metadata. To output this metadata to Pegasus, we will use the following command:

```
bigscraper compile gc pegasus
```

This command "compiles" the data which we collected into the Pegasus Frontend format (metadata.pegasus.txt). By default, this outputs to the `~/Documents/bigscraper/[system]` folder, where `[system]` is the same as the system abbreviation, or item 3 in the command.

Once this command has run, you can find the metadata.pegasus.txt file and a media folder in the output folder. You can move these to the GameCube games folder, or leave them as is. Now, you have a file you can use in Pegasus Frontend.

## Help Commands

Bigscraper comes with several help commands that details syntax, systems and more. In these commands, "help" can be replaced by "-h", "-?" or "--help" with any capitalization.

To get a list of subcommands, run the following.

```
bigscraper help
```

To get help for subcommands, run the following, replacing `[subcommand]` with the proper subcommand.

```
bigscraper [subcommand] help
```

Additionally, you can see what systems and export formats are supported. This can be done through running either of the following.

Systems: `bigscraper help systems`
Export Formats: `bigscraper help exports` or `bigscraper help platforms`
