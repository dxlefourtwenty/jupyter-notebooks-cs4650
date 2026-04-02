# What `common.py` Is Doing

I made `common.py` to hold the parts of the code that every question needed.

Instead of rewriting the same setup four different times, I put the shared steps in one file. That includes loading the data, building the logistic regression model, testing it, and saving the graphs and summary files.

So the point of `common.py` is just to keep the question files shorter and easier to read. Each question file can focus on its own part of the homework, while `common.py` handles the repeated setup in the background.

