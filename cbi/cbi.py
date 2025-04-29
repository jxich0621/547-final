#! /usr/bin/env python3

from collections import defaultdict
import itertools
import json
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple
from cbi.data_format import (
    CBILog,
    ObservationStatus,
    Predicate,
    PredicateInfo,
    PredicateType,
    Report,
)


def collect_observations(log: CBILog) -> Dict[Predicate, ObservationStatus]:
    """
    Traverse the CBILog and collect observation status for each predicate.

    NOTE: If you find a `Predicate(line=3, column=5, pred_type="BranchTrue")`
    in the log, then you have observed it as True,
    further it also means you've observed is complement:
    `Predicate(line=3, column=5, pred_type="BranchFalse")` as False.

    :param log: the log
    :return: a dictionary of predicates and their observation status.
    """
    observations: Dict[Predicate, ObservationStatus] = defaultdict(
        lambda: ObservationStatus.NEVER
    )

    """
    TODO: Add your code here

    Hint: The PredicateType.alternatives will come in handy.
    """

    for entry in log:
        value = entry.value
        line = entry.line
        column = entry.column

        all_alternatives = PredicateType.alternatives(value)

        for alternative in all_alternatives:
            pred_type = alternative[0]
            obs_status = alternative[1]

            pred = Predicate(line=line, column=column, value=pred_type)
            observations[pred] = ObservationStatus.merge(observations[pred], obs_status)
        
    return observations


def collect_all_predicates(logs: Tuple[Iterable[CBILog],int]) -> Set[Predicate]:
    """
    Collect all predicates from the logs.

    :param logs: Collection of CBILogs
    :return: Set of all predicates found across all logs.
    """
    predicates = set()

    # TODO: Add your code here

    for log,_ in logs:
        for entry in log:

            if entry.is_branch:
                pred1 = Predicate(line=entry.line, column=entry.column, value=PredicateType.BRANCH_FALSE)
                pred2 = Predicate(line=entry.line, column=entry.column, value=PredicateType.BRANCH_TRUE)
                predicates.add(pred1)
                predicates.add(pred2)
            
            if entry.is_return:
                pred1 = Predicate(line=entry.line, column=entry.column, value=PredicateType.RETURN_POSITIVE)
                pred2 = Predicate(line=entry.line, column=entry.column, value=PredicateType.RETURN_NEGATIVE)
                pred3 = Predicate(line=entry.line, column=entry.column, value=PredicateType.RETURN_ZERO)
                predicates.add(pred1)
                predicates.add(pred2)
                predicates.add(pred3)

    return predicates


def cbi(success_logs_and_return_codes: List[Tuple[CBILog,int]], failure_logs_and_return_codes: List[Tuple[CBILog,int]]) -> Report:
    """
    Compute the CBI report.

    :param success_logs: logs of successful runs
    :param failure_logs: logs of failing runs
    :return: the report
    """

    all_predicates = collect_all_predicates(itertools.chain(success_logs_and_return_codes, failure_logs_and_return_codes))

    predicate_infos: Dict[Predicate, PredicateInfo] = {
        pred: PredicateInfo(pred) for pred in all_predicates
    }

    for success_log, _ in success_logs_and_return_codes:
        observations = collect_observations(success_log)
        for pred, obs_status in observations.items():
            if obs_status != ObservationStatus.NEVER:
                predicate_infos[pred].num_observed_in_success += 1

            if obs_status == ObservationStatus.ONLY_TRUE:
                predicate_infos[pred].num_true_in_success += 1

    for failure_log, failure_return_code in failure_logs_and_return_codes:
        observations = collect_observations(failure_log)
        for pred, obs_status in observations.items():
            if obs_status != ObservationStatus.NEVER:
                predicate_infos[pred].num_observed_in_failure += 1

                if failure_return_code == 2: # Div by zero
                    predicate_infos[pred].num_observed_in_failure_div_zero += 1
                elif failure_return_code == 3: # Null pointer dereference
                    predicate_infos[pred].num_observed_in_failure_null_ptr += 1
                elif failure_return_code == 4: # Assertion failure
                    predicate_infos[pred].num_observed_in_failure_assertion += 1

            if obs_status == ObservationStatus.ONLY_TRUE:
                predicate_infos[pred].num_true_in_failure += 1

                if failure_return_code == 2: # Div by zero
                    predicate_infos[pred].num_true_in_failure_div_zero += 1
                elif failure_return_code == 3: # Null pointer dereference
                    predicate_infos[pred].num_true_in_failure_null_ptr += 1
                elif failure_return_code == 4: # Assertion failure
                    predicate_infos[pred].num_true_in_failure_assertion += 1

    # TODO: Add your code here to compute the information for each predicate.

    # Finally, create a report and return it.
    report = Report(predicate_info_list=list(predicate_infos.values()))
    return report

def plot_top_k_increase_from_report_all_types(report_path: str, basename:str, k: int = 5, output_dir: str = "plots"):
    """
    Generate 4 plots:
        - Overall Increase
        - Increase for Division-by-Zero failures
        - Increase for Null Pointer Dereference failures
        - Increase for Assertion failures

    :param report_path: Path to the .json report generated by CBI
    :param k: Top k predicates to show
    :param output_dir: Directory where all plots will be saved
    """
    with open(report_path, "r") as f:
        report = json.load(f)

    predicate_info_list = report["predicate_info_list"]

    # For each kind, prepare (label, score) list
    all_scores = []
    div_zero_scores = []
    null_ptr_scores = []
    assertion_scores = []

    for info in predicate_info_list:
        label = f"Line {info['predicate']['line']:03}, Col {info['predicate']['column']:03}, {info['predicate']['pred_type']}"
        all_scores.append((label, info["increase"]))
        div_zero_scores.append((label, info["increase_div_zero"]))
        null_ptr_scores.append((label, info["increase_null_ptr"]))
        assertion_scores.append((label, info["increase_assertion"]))

    # Sort and pick top-k
    def get_top_k(scores):
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        return [(label, score) for label, score in sorted_scores if score > 0][:k]

    categories = [
        ("overall", all_scores),
        ("div_zero", div_zero_scores),
        ("null_ptr", null_ptr_scores),
        ("assertion", assertion_scores)
    ]

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, scores in categories:
        top_k = get_top_k(scores)
        if not top_k:
            print(f"No valid predicates for {name}, skipping plot.")
            continue

        labels, values = zip(*top_k)

        plt.figure(figsize=(12, 6))
        bars = plt.barh(range(len(labels)), values, tick_label=labels)
        plt.xlabel("Increase")
        plt.title(f"Top {k} Predicates by {name.capitalize()} Increase")
        plt.gca().invert_yaxis()
        plt.grid(axis="x", linestyle="--", alpha=0.7)

        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width + 0.005, bar.get_y() + bar.get_height()/2, f"{width:.3f}", va="center")

        plt.tight_layout()
        save_path = output_dir / f"{basename}_top_{name}_increase.png"
        plt.savefig(save_path)
        plt.close()