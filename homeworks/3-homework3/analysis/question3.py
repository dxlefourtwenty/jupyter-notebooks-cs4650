#!/usr/bin/env python3

from common import evaluate_pipeline, load_dataset, print_summary, write_summary


def main() -> None:
    frame = load_dataset()
    summary = evaluate_pipeline(
        frame=frame,
        target=(frame["class"] > 0).astype(int),
        task_name="binary_accident",
        labels=["No Accident", "Accident"],
        include_firm=True,
    )

    write_summary("question3_summary.json", [summary])
    print_summary(summary)


if __name__ == "__main__":
    main()
