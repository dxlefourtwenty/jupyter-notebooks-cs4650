#!/usr/bin/env python3

from common import evaluate_pipeline, load_dataset, print_summary, write_summary


def main() -> None:
    frame = load_dataset()

    three_class = evaluate_pipeline(
        frame=frame,
        target=frame["class"],
        task_name="three_class",
        labels=["No Accident", "Type 1", "Type 2"],
        include_firm=True,
    )

    binary = evaluate_pipeline(
        frame=frame,
        target=(frame["class"] > 0).astype(int),
        task_name="binary_accident",
        labels=["No Accident", "Accident"],
        include_firm=True,
    )

    write_summary("question2_summary.json", [three_class, binary])
    print_summary(three_class)
    print_summary(binary)


if __name__ == "__main__":
    main()
