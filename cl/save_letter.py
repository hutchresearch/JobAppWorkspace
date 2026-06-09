#!/usr/bin/env python3
"""
Compile cover_letter_template.tex and save as companyname_cover_letter.pdf in oldletters/

Usage: python save_letter.py <company_name>
"""

import subprocess
import re
import os
import sys
import shutil

def find_pdflatex():
    pdflatex = shutil.which("pdflatex")
    if pdflatex:
        return pdflatex
    miktex_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"),
        r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe",
    ]
    for path in miktex_paths:
        if os.path.exists(path):
            return path
    return None

def sanitize_filename(name):
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s]+", "_", name)
    return name

def main():
    if len(sys.argv) < 2:
        print("Usage: python save_letter.py <company_name>")
        return

    company = " ".join(sys.argv[1:])
    safe_name = sanitize_filename(company)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    tex_file = os.path.join(script_dir, "cover_letter_template.tex")
    oldletters_dir = os.path.join(script_dir, "oldletters")
    os.makedirs(oldletters_dir, exist_ok=True)
    output_pdf = os.path.join(oldletters_dir, f"{safe_name}_cover_letter.pdf")

    pdflatex = find_pdflatex()
    if not pdflatex:
        print("Error: pdflatex not found. Install MiKTeX.")
        return

    print(f"Compiling cover letter for: {company}")

    result = subprocess.run(
        [pdflatex, "-interaction=nonstopmode", "-output-directory", oldletters_dir, tex_file],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("LaTeX compilation failed!")
        print(result.stdout)
        return

    generated_pdf = os.path.join(oldletters_dir, "cover_letter_template.pdf")
    os.replace(generated_pdf, output_pdf)
    print(f"Saved: {output_pdf}")

    for ext in [".aux", ".log", ".out"]:
        aux_file = os.path.join(oldletters_dir, f"cover_letter_template{ext}")
        if os.path.exists(aux_file):
            os.remove(aux_file)

if __name__ == "__main__":
    main()
