# Question 2: How accurately does the regressor classify the samples?

I looked at this two ways.

First, I tried the full 3-class version: `No Accident`, `Type 1`, and `Type 2`. That model had about `73.4%` holdout accuracy, but its balanced accuracy was only about `49.7%`. So even though the overall accuracy looks okay, it is not handling the accident classes very well.

Then I combined `Type 1` and `Type 2` into one `Accident` class. That worked much better. The holdout accuracy was about `79.4%`, and the balanced accuracy was about `76.1%`.

So overall, the model does a decent job when the problem is just `No Accident` versus `Accident`, but not a very good job when I force it to split accidents into two separate types. The confusion matrices back that up.
