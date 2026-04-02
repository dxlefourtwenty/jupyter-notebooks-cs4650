# Question 1: Are accident types 1 and 2 distinguishable?

I tested this by keeping only the accident rows and asking the model to tell `Type 1` from `Type 2`.

The result was not very strong. The holdout accuracy was about `53.3%`, and the balanced accuracy was about `50.7%`. That is only a little better than guessing, so the model is not doing a good job separating the two accident types.

So my answer is that the two accident types do not look clearly different in this dataset. Because of that, I think it makes more sense to group them together as just `Accident` for the rest of the homework.
