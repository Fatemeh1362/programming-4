# Feedback on your portfolio

Nice many commits, which are distributed nicely over time (the month of July and the beginning of August). The commit messages are quite informative, but there are quite a few deletes. However, it seems that the final excercise doesn't have its own directory. I am also missing a `.gitignore`-file.

Judging from your README, you are currenlty only concerned about the last assignment. However, I will also grade the other weeks, which have their own seperate README's. You should, however, make more use of the typographical possibilities that markdown is offering in order to make you readme's a bit more readable. You should also be more careful in your spelling, as there are currently too many mistakes in your text (I have changed a few of them, so you can see what I mean).

## Week 1

Nice enough implementation. Just don't add `_class` to filenames that contain classes. You should refrain from putting computational intent inside some naming formalism, and in Python you can also have multiple classes in one file (so what would you call that?).

Please have a look at the comments in the individual classes.

## Week 2

Nice and thorough readme (though you really should think about typography: now it looks like one big mind blur). Nice that you are explicit in the excercise's goal. A bit sad that you put your answers (and some more 🤷) in a notebook; I don't think that would be my choice of technology in this case (but as it's mostly markdown, I guess one could argue...). 

Your answers are nice (with a little help from our friend chatGPT I imagine). You could have provided some more statistical data about the code base, e.g. the average number of lines per method, the number of classes etc. You could also have provided some images: though you *do* have some plantuml-text, I don't see any rendering of it in your portfolio. Also it seems to be only a sequence diagram; addition of a class diagram would have been nice.

## Week 3

Nice that the readme of the first part is actually larger than the elaboration itself 😉. Good that you have done some refactoring on the code base, even though it could not be ran due to lack of website. This is, of course, a simple warm up excercise.

I don't quite see how the second part is supposed to run or be read. You state that you don't have an API-key, but in the excercise you are asked to obtain one. Also, there seems to be a few realisations of the same problem in your notebook. I don't think this has been actually run.


## Final assignment

I have to search a bit on how to run this application. Also why are you using a notebook for this excercise? I don't think that that is the technique of choice in this particular instance. Ans as you are basically using only one cell, that can (should) just be put in a separate python-file. And why is the file called '_modified'? Modified with regard to what? That is not something that should be reflected in the name of the file – we have version control for that purpose.

In your notebook you are making use of a json-file on your own file system (which I obviously don't have access to). There are also references to your own FS in the `application.json`. You use this to download the data-file (`sensor.csv`); I'll just make a new file, based on your notebook, to try to run your code...

After fifteen minutes trying, I must confess I failed in my noble quest. I actually don't understand how you want this application to run. Please have a look at my version of `main.py`, and my comments in the individual classes.
