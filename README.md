# keyword-hunter

> A complete Nuclei keyword-search solution: includes a customizable `keyword-search.yaml` template (with `keywords.txt`) plus a Python wrapper that runs the scan, deduplicates by subdomain + keyword, and optionally colorizes the output.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📋 Table of Contents

- [🔍 Overview](#-overview)  
- [🚀 Installation](#-installation)  
- [⚙️ Usage](#️-usage)  
- [🛠 Template Details](#-template-details)  
- [🎨 Color Output](#-color-output)  
- [👥 Contributing](#-contributing)  
- [📄 License](#-license)  
- [🔗 Credits](#-credits)  

---

## 🔍 Overview

This repo bundles everything you need to run a keyword-based scan with [Nuclei](https://github.com/projectdiscovery/nuclei):

1. **`keyword-search.yaml`** + **`keywords.txt`**  
   - Define the HTTP paths, parameters or files you want to scan.  
   - Edit `keywords.txt` to add/remove keywords; the YAML template uses this list to generate checks.

2. **`keyword_hunter.py`**  
   - A lightweight Python 3 wrapper that:
     - Runs `nuclei -no-color -t keyword-search.yaml -l <targets>`
     - Captures all hits in real time
     - Deduplicates on **(subdomain, keyword)** so you see only the first occurrence of each
     - Optionally highlights URLs in **cyan** and keywords in **yellow**
     - Can save the full raw scan log for later inspection  

---

## 🚀 Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/keyword-hunter.git
   cd keyword-hunter
   ```
2. **Install prerequisites**
+ Python 3.6+
+ Nuclei v3.4+ (make sure nuclei is in your $PATH)
3. **Make the script executable**
   ```bash
     chmod +x keyword_hunter.py
   ```
## ⚙️ Usage
`./keyword_hunter.py -l <urls_file> [-o <raw_output.log>] [--color]` 

-   `-l <urls_file>`  
    Path to a newline-separated list of target URLs (same as `nuclei -l`).
    
-   `-o <raw_output.log>` _(optional)_  
    Save the full, unfiltered Nuclei output to a file.
    
-   `--color` _(optional)_  
    Highlight matched URLs in **cyan** and the `keywords="…"` segments in **yellow**.
    

**Example**:

`./keyword_hunter.py \
  -l ~/targets.txt \
  -o raw_nuclei.log \
  --color` 

This runs:

`nuclei -no-color -l ~/targets.txt -t keyword-search.yaml` 

…then filters, dedupes, and (optionally) colorizes the `[keyword-search]` hits.

----------

## 🛠 Template Details

-   **`keyword-search.yaml`**  
    Your Nuclei template. It reads `keywords.txt` to generate HTTP paths or checks for each keyword.
    
-   **`keywords.txt`**  
    A simple newline-separated list of terms (e.g. `login`, `dashboard`, `admin`).  
    Edit this file to customize which keywords your scans look for.
    

Feel free to add or remove keywords, or adjust the YAML logic to fit your targets.

----------

## 🎨 Color Output

If you use the `--color` flag, output lines are embellished with ANSI escapes:

-   **URLs** appear in **cyan**
    
-   **`keywords="…"`** segments appear in **yellow**
    

This makes it easy to visually scan results in your terminal.

----------

## 👥 Contributing

1.  **Fork** this repo
    
2.  **Create a branch** (`git checkout -b feature/my-improvement`)
    
3.  **Make your changes** (e.g. add options, support new templates)
    
4.  **Submit a Pull Request**—I’ll review and merge!
    

Please include tests or examples when adding new functionality.

----------

## 🔗 Credits

**Powered by 0_oNoProblem**  
Template & tooling by 0_oNoProblem. Feel free to drop me a star!
