"""
import_manager.py

Coordinates the complete PDF import process.
"""

from pdf_importer.config import VERBOSE

from pdf_importer.pdf_reader import PDFReader
from pdf_importer.data_mapper import DataMapper
from pdf_importer.validators import Validator
from pdf_importer.database_writer import DatabaseWriter

from pdf_generator.schema_reader import SchemaReader


class ImportManager:

    def __init__(self):
        """
        Initializes all components required for the import process.
        """

        # Read the database schema once
        self.schema = SchemaReader().read_schema()

        # Initialize components
        self.reader = PDFReader()
        self.mapper = DataMapper()
        self.validator = Validator(self.schema)
        self.writer = DatabaseWriter()

    # --------------------------------------------------

    def import_pdf(self, pdf_path):
        """
        Imports a completed PDF into the database.

        Parameters
        ----------
        pdf_path : str
            Path to the completed PDF.
        """

        if VERBOSE:
            print("\nReading PDF...")

        raw_data = self.reader.read(pdf_path)

        if VERBOSE:
            print("OK")

        # --------------------------------------------------

        if VERBOSE:
            print("Mapping fields...")

        mapped_data = self.mapper.map(raw_data)

        if VERBOSE:
            print("OK")

        # --------------------------------------------------

        if VERBOSE:
            print("Validating values...")

        validated_data = self.validator.validate(mapped_data)

        if VERBOSE:
            print("OK")

        # --------------------------------------------------

        if VERBOSE:
            print("Writing to database...")

        self.writer.write(validated_data)

        if VERBOSE:
            print("OK")
            print("\nImport completed successfully.")