#! /usr/bin/env python3

import json
import sys
import os

from dataclasses import asdict
from pathlib import Path

from cbi.cbi import cbi, plot_top_k_increase_from_report_all_types
from cbi.utils import get_logs_and_return_codes


def main() -> int:
    """
    Usage: cbi [target] [fuzzer-output-dir]
    """
    if len(sys.argv) < 3:
        print(
            f"Usage: cbi [target] [fuzzer-output-dir]",
            file=sys.stderr,
        )
        return 1
    target, fuzz_output_dir = sys.argv[1:]

    if not Path(target).exists():
        print(f"{target} not found", file=sys.stderr)
        return 1
    if not Path(fuzz_output_dir).exists():
        print(f"{fuzz_output_dir} not found", file=sys.stderr)
        return 1

    # Generate the cbi logs
    success_logs_and_return_codes, failure_logs_and_return_codes = get_logs_and_return_codes(target=target, fuzz_dir=Path(fuzz_output_dir))
    # Analyze the cbi logs and generate the report
    report = cbi(success_logs_and_return_codes=success_logs_and_return_codes, 
                 failure_logs_and_return_codes=failure_logs_and_return_codes)
    # Visualize the report
    print(report)
    # Save the report to a file
    
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    basename = Path(target).as_posix().replace("/", "_")
    report_path = report_dir / f"{basename}.json"

    with open(report_path, "w") as fp:
        json.dump(asdict(report), fp, indent=4)

    plot_top_k_increase_from_report_all_types(
        report_path=report_path,
        basename = basename,
        k=5,
        output_dir=report_dir,
    )

    return 0


if __name__ == "__main__":
    """
    Usage: cbi [target] [fuzzer-output-dir]
    """
    sys.exit(main())
