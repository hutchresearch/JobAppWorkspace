# JobAppWorkspace

A small, collaborative workspace for building resumes and cover letters in the lab.
Resumes are written as [RenderCV](https://github.com/rendercv/rendercv) YAML (→ Typst → PDF);
cover letters are LaTeX with a script to compile + archive per-company copies.

The idea: keep one tuned `design` block and a couple of helper scripts that everyone
shares, so you only ever edit your own content, not the formatting plumbing.

## What's here

```
JobAppWorkspace/
├── example/
│   └── Example_Resume.yaml      # dummy content + the shared, tuned design block — copy this to start
├── cl/
│   ├── cover_letter_template.tex  # LaTeX cover letter with [bracketed] placeholders
│   └── save_letter.py             # compile the .tex and archive it as <company>_cover_letter.pdf
├── requirements.txt               # Python deps (rendercv[full], pinned)
├── .gitignore                     # keeps personal files (your real resume, signature, archives) out of git
└── README.md
```

> **Keep personal stuff out of the repo.** Your real resume YAML, your `signature.png`,
> and the `oldletters/` / `oldresumes/` archives are gitignored on purpose. Don't force-add them.

## Setup

- **Python 3.x**
- **A LaTeX engine** for cover letters: [MiKTeX](https://miktex.org/) on Windows (gives you `pdflatex`).
  This is not a pip package, so install it separately.

Create a virtual environment and install the Python deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` pulls in `rendercv[full]` — the `full` extra bundles Typst, so you don't need a
separate Typst install. After this, re-apply the Education-gap patch (see "Known issue" below) since it
touches the installed package.

## Resume workflow

1. Copy the example to your own file:
   ```powershell
   Copy-Item example\Example_Resume.yaml Jane_Doe_Resume.yaml
   ```
2. Edit `cv:` (your content). Leave `design:` / `locale:` / `settings:` alone unless you know what you're changing.
3. Render. This one-liner renders **and** archives a copy under `oldresumes\<tag>\` so you keep a
   snapshot of each tailored version:
   ```powershell
   $company="standard"; rendercv render .\Jane_Doe_Resume.yaml; `
     New-Item -ItemType Directory -Force "oldresumes\$company"; `
     Copy-Item -Path "rendercv_output\*" -Destination "oldresumes\$company" -Recurse
   ```
   The PDF lands in `rendercv_output\`.

### Windows console gotcha (UTF-8)

RenderCV prints Unicode (e.g. `✓`) and the default Windows console (cp1252) can crash with
`UnicodeEncodeError`. If that happens, set UTF-8 for the session first:

```powershell
$env:PYTHONIOENCODING="utf-8"; $env:PYTHONUTF8="1"
```

## Cover letter workflow

1. Edit `cl/cover_letter_template.tex` — fill in the `[bracketed]` placeholders (your name/contact in the
   header, the company, the role, and the body).
2. **Signature loading:** drop your own `signature.png` into `cl/` (a scan/photo of your signature,
   transparent background works best). It's gitignored, so it stays on your machine. The template uses
   `\IfFileExists` — if there's no `signature.png`, it falls back to typing your name, so it always compiles.
3. Compile + archive a named copy:
   ```powershell
   python cl\save_letter.py "Acme Corp"
   ```
   Output: `cl\oldletters\acme_corp_cover_letter.pdf`. Aux files are cleaned up automatically.

## Known issue: extra margin below the Education section

The `engineeringresumes` theme renders an empty second-row block for education entries that have no
highlights, which shows up as a phantom gap below the Education section. RenderCV's templates live in
the **installed package** (not in this repo), so this is a local patch you re-apply after any
`pip install`/upgrade of rendercv.

Find the package dir:
```powershell
python -c "import rendercv,os;print(os.path.dirname(rendercv.__file__))"
```

Edit `renderer\templater\templates\typst\entries\EducationEntry.j2.typ` and change the second-row guard
from:
```jinja
{% if not design.entries.short_second_row %}
```
to:
```jinja
{% if not design.entries.short_second_row and entry.main_column.splitlines()[first_row_lines:]|length > 0 %}
```
This stops emitting the empty block so the phantom gap disappears. (Regular entries don't wrap the empty
block, so they're unaffected — only Education needs this.)

Verified on rendercv 2.6.

## Contributing

This is a shared lab workspace — improvements to the template, the scripts, or these docs are welcome.
Keep all personal data (real resumes, signatures, contact info) out of commits.
