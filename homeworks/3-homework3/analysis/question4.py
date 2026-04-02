#!/usr/bin/env python3

from common import evaluate_pipeline, load_dataset, print_summary, write_summary


def main() -> None:
    frame = load_dataset()

    with_firm = evaluate_pipeline(
        frame=frame,
        target=(frame["class"] > 0).astype(int),
        task_name="binary_accident",
        labels=["No Accident", "Accident"],
        include_firm=True,
    )

    without_firm_frame = frame.drop(columns=["FIRM"]).copy()
    without_firm = evaluate_pipeline(
        frame=without_firm_frame,
        target=(frame["class"] > 0).astype(int),
        task_name="binary_without_firm",
        labels=["No Accident", "Accident"],
        include_firm=False,
    )

    write_summary("question4_summary.json", [with_firm, without_firm])
    print_summary(with_firm)
    print_summary(without_firm)


if __name__ == "__main__":
    main()
