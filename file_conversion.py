import pdfplumber

class FileConverter:
    def pdf_to_md(self, path:str):
        HEADINGS = [
            "Technical Skills",
            "Projects",
            "Internship",
            "Extracurricular",
            "Education"
        ]

        with pdfplumber.open(path) as pdf:
            markdown_lines = []

            for page in pdf.pages:
                lines = page.extract_text().split("\n")

                for line in lines:
                    stripped = line.strip()

                    if stripped in HEADINGS:
                        markdown_lines.append(f"\n## {stripped}\n")

                    elif stripped.startswith("•") or stripped.startswith("-"):
                        markdown_lines.append(f"- {stripped.lstrip('•').strip()}")
                    else:
                        markdown_lines.append(stripped)

        markdown_text = "\n".join(markdown_lines)

        with open("old_resume.md", "w", encoding="utf-8") as f:
            f.write(markdown_text)

        print("Conversion done! See old_resume.md")
