# Solution Key Generator

Scripts that build `Kinematics-Guided-Examples-Solution-Key.docx` — a clean, modern,
color-coded Word document with native Office Math (OMML) equations, aligned equal
signs, and boxed final answers.

## Files
- `engine.py` — low-level helpers: LaTeX→OMML conversion (via pandoc) and
  python-docx styling (shading, borders, colored callout boxes, tables).
- `content.py` — all authored content (7 guided examples + reference table).
- `build_doc.py` — assembles the document and writes the `.docx`.

## Requirements
- Python packages: `python-docx`, `lxml`
- `pandoc` on the system (used to translate LaTeX math into OMML). Update the
  `PANDOC` path near the top of `engine.py` if needed.

## Build
```
pip install python-docx lxml
python build_doc.py
```

## Notes
- Every equation is real editable Office Math (OMML), not an image.
- Multi-line derivations use LaTeX `aligned` blocks so they align at the `=` sign.
  Empty alignment cells are filled with a zero-width space so the equations render
  cleanly in Word, LibreOffice, and Google Docs alike.
