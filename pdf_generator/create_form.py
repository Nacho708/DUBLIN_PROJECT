"""
Entry point for generating the clinical PDF form.
"""

from pdf_builder import PDFBuilder


def main():

    print("=" * 60)
    print("Generating Clinical PDF Form...")
    print("=" * 60)

    builder = PDFBuilder()

    builder.build()

    print("\nPDF generated successfully.")


if __name__ == "__main__":

    main()