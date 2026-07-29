from pdf_importer.config import get_input_pdfs
from pdf_importer.import_manager import ImportManager


def main():

    manager = ImportManager()

    for pdf_path in get_input_pdfs():

        print(f"\nImporting {pdf_path.name}...")

        manager.import_pdf(pdf_path)


if __name__ == "__main__":
    main()