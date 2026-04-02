# Question 3: Which features are significant, and which can be ignored?

For this part, I used the simpler `No Accident` versus `Accident` model since that worked better overall.

The features that stood out the most were `Length`, `AFZ`, `MFZ`, `End`, and `NFZ`. So shift length and some of the fatigue-related values seem to matter the most for this prediction.

Some other columns had only a small effect, and `MalAdj` can basically be ignored because it does not change at all in this dataset. A column that never changes cannot really help the model.

So my main takeaway is that the fatigue-related features do seem useful, while a few other columns do not add much.
