#!/usr/bin/env python3
"""
keyword_hunter.py — dedupe nuclei keyword-search results by subdomain+keyword
Powered by 0_oNoProblem
"""

import subprocess
import sys
import argparse
import re
from urllib.parse import urlparse
from pathlib import Path

# ANSI color codes
CYAN   = "\033[36m"
YELLOW = "\033[33m"
RESET  = "\033[0m"

def extract_host(url):
    return urlparse(url).netloc

def extract_keyword(line):
    m = re.search(r'keywords="([^"]+)"', line)
    return m.group(1) if m else None

def colorize_line(line: str) -> str:
    # color URLs cyan
    line = re.sub(r'(https?://\S+)', f"{CYAN}\\1{RESET}", line)
    # color keywords="..." yellow
    line = re.sub(r'(keywords="[^"]+")', f"{YELLOW}\\1{RESET}", line)
    return line

def run_nuclei(urls_file, template_path, raw_output_path=None, use_color=False):
    print(f"{CYAN}→ Powered by 0_oNoProblem{RESET}", file=sys.stderr)
    cmd = [
        "nuclei",
        "-no-color",
        "-l", urls_file,
        "-t", template_path
    ]
    raw_out = open(raw_output_path, "w") if raw_output_path else None
    seen = set()

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        for raw_line in proc.stdout:
            if raw_out:
                raw_out.write(raw_line)
            line = raw_line.strip()
            if "[keyword-search]" not in line:
                continue

            # extract URL
            url_m = re.search(r'https?://\S+', line)
            if not url_m:
                continue
            url = url_m.group(0)
            host = extract_host(url)
            if not host:
                continue

            kw = extract_keyword(line) or ""
            key = f"{host}|{kw}"
            if key not in seen:
                seen.add(key)
                out = colorize_line(line) if use_color else line
                print(out)
        proc.wait()
    finally:
        if raw_out:
            raw_out.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Dedupe nuclei keyword-search by subdomain+kw\nPowered by 0_oNoProblem",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-l", required=True, help="Input URLs list")
    parser.add_argument("-o", help="Save raw nuclei output here")
    parser.add_argument("-c", "--color", action="store_true",
                        help="Enable colored output")
    args = parser.parse_args()

    tpl = Path(__file__).parent / "keyword-search.yaml"
    if not tpl.exists():
        print(f"Error: {tpl} not found", file=sys.stderr)
        sys.exit(1)

    run_nuclei(args.l, str(tpl), raw_output_path=args.o, use_color=args.color)
