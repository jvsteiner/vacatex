from flask import Flask, request, send_file, jsonify
from pathlib import Path
import subprocess
import tempfile
import os

app = Flask(__name__)


@app.route("/compile", methods=["POST"])
def compile_latex():
    data = request.get_json()

    if not data or "fragment" not in data:
        return jsonify({"error": "LaTeX fragment is required"}), 400

    fragment = data["fragment"]
    preamble = data.get("preamble", "")

    latex_document = f"""
    \\documentclass{{standalone}}
    {preamble}
    \\begin{{document}}
    {fragment}
    \\end{{document}}
    """

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)
        tex_file = tempdir_path / "document.tex"
        pdf_file = tempdir_path / "document.pdf"
        svg_file = tempdir_path / "document.svg"

        # Write the LaTeX document to a .tex file
        with tex_file.open("w") as f:
            f.write(latex_document)

        try:
            # Compile the LaTeX document to PDF
            subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-output-directory",
                    tempdir,
                    str(tex_file),
                ],
                check=True,
            )

            # Convert the PDF to SVG using pdf2svg or a similar tool
            subprocess.run(["pdf2svg", str(pdf_file), str(svg_file)], check=True)

            return send_file(svg_file, mimetype="image/svg+xml")

        except subprocess.CalledProcessError as e:
            # Return the error details to the client if anything goes wrong
            return jsonify({"error": str(e), "output": e.output.decode()}), 500


if __name__ == "__main__":
    app.run(debug=True)
