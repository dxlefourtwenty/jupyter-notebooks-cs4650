#!/usr/bin/env python3

from common import evaluate_pipeline, load_dataset, print_summary, write_summary


def main() -> None:
    frame = load_dataset()
    accident_only = frame.loc[frame["class"] > 0].copy()
    target = accident_only["class"].replace({1: 0, 2: 1})

    summary = evaluate_pipeline(
        frame=accident_only,
        target=target,
        task_name="type1_vs_type2",
        labels=["Type 1", "Type 2"],
        include_firm=True,
    )

    write_summary("question1_summary.json", [summary])
    print_summary(summary)


if __name__ == "__main__":
    main()
