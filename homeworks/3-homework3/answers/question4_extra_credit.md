# Question 4: What happens if `FIRM` is removed?

When I removed `FIRM` and ran the model again, the results barely changed.

With `FIRM`, the holdout accuracy was about `79.4%`. Without `FIRM`, it was about `79.3%`. The balanced accuracy also stayed almost the same.

So removing `FIRM` did not really hurt the model. That tells me the model is getting most of its useful information from the other features, not from the company ID column.
