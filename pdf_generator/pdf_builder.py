"""
pdf_builder.py
==============

Main engine responsible for generating the fillable PDF from the
database schema.

Workflow

SchemaReader
      │
      ▼
FieldMetadata
      │
      ▼
FieldMapper (fallback)
      │
      ▼
PDFBuilder
"""

from pathlib import Path

from reportlab.pdfgen import canvas
from sqlalchemy import table

from config import (
    OUTPUT_FOLDER,
    PDF_NAME,
    PAGE_SIZE,
    LEFT_MARGIN,
    TOP_MARGIN,
    FIELD_WIDTH,
    FIELD_HEIGHT,
    ROW_SPACING,
)

from schema_reader import SchemaReader
from field_mapper import FieldMapper
from styles import PDFStyles

from field_metadata import (
    FieldMetadata,
    DEFAULT_TEMPLATE,
)

from field_metadata.constants import (
    ControlType,
)


class PDFBuilder:
    """
    Generates a fillable PDF from a MySQL schema.
    """

    TITLE = "OAT Clinical Registry"

    SECTION_SPACING = 25
    TABLE_SPACING = 30
    PAGE_BOTTOM_MARGIN = 80

    LABEL_OFFSET_Y = 5
    FIELD_OFFSET_X = 180

    SECTION_WIDTH = 450

    def __init__(self):

        self.reader = SchemaReader()

        self.mapper = FieldMapper()

        self.metadata = FieldMetadata()

        self.pdf = None
        self.styles = None

        self.page_width = 0
        self.page_height = 0

        self.x = LEFT_MARGIN
        self.y = 0

    # ==========================================================
    # DOCUMENT INITIALIZATION
    # ==========================================================

    def initialize_document(self):
        """
        Creates the PDF document and initializes the drawing context.
        """

        Path(OUTPUT_FOLDER).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.pdf = canvas.Canvas(
            str(Path(OUTPUT_FOLDER) / PDF_NAME),
            pagesize=PAGE_SIZE,
        )

        self.styles = PDFStyles(self.pdf)

        self.page_width, self.page_height = PAGE_SIZE

        self.x = LEFT_MARGIN
        self.y = self.page_height - TOP_MARGIN

    def draw_header(self):
        """
        Draws the page title.
        """

        self.styles.draw_title(
            self.TITLE,
            self.x,
            self.y,
        )

        self.y -= 40

    # ==========================================================
    # PAGE MANAGEMENT
    # ==========================================================

    def new_page(self):
        """
        Starts a new page.
        """

        self.pdf.showPage()

        self.styles = PDFStyles(self.pdf)

        self.y = self.page_height - TOP_MARGIN

        self.draw_header()

    def check_page_break(self, required_height=0):
        """
        Starts a new page if there is not enough vertical space.
        """

        if self.y - required_height < self.PAGE_BOTTOM_MARGIN:
            self.new_page()

    # ==========================================================
    # METADATA
    # ==========================================================

    def get_template(self, table_name, column):
        """
        Returns the FieldTemplate associated with a column.

        Priority:

            metadata.py
                  ↓
            field_mapper.py
                  ↓
            DEFAULT_TEMPLATE
        """

        template = self.metadata.get(
            table_name,
            column.name,
        )

        if template != DEFAULT_TEMPLATE:
            return template

        return self.mapper.infer_from_column(
            column
        )

    # ==========================================================
    # LABELS
    # ==========================================================

    @staticmethod
    def humanize(name):
        """
        Converts database names into readable labels.

        Example:

            patient_id
                ↓
            Patient ID

            neck_circumference_cm
                ↓
            Neck Circumference (cm)
        """

        label = name.replace("_", " ")

        label = label.replace(" Id", " ID")
        label = label.replace(" Cbct", " CBCT")
        label = label.replace(" Ahi", " AHI")
        label = label.replace(" Sao2", " SaO2")
        label = label.replace(" Bmi", " BMI")
        label = label.replace(" Rom", " ROM")
        label = label.replace(" Cpap", " CPAP")

        label = label.title()

        replacements = {
            "Id": "ID",
            "Cbct": "CBCT",
            "Ahi": "AHI",
            "Ai": "AI",
            "Bmi": "BMI",
            "Rom": "ROM",
            "Sao2": "SaO2",
            "Ct90": "CT90",
            "Cpap": "CPAP",
        }

        words = []

        for word in label.split():

            words.append(
                replacements.get(
                    word,
                    word,
                )
            )

        label = " ".join(words)

        label = label.replace(" Cm", " (cm)")
        label = label.replace(" Kg", " (kg)")

        return label

    # ==========================================================
    # LAYOUT
    # ==========================================================

    def draw_section(self, table_name):
        """
        Draws a section header for a database table.
        """

        self.check_page_break(40)

        self.styles.draw_section(
            self.humanize(table_name),
            self.x,
            self.y,
            self.SECTION_WIDTH,
        )

        self.y -= self.SECTION_SPACING

    def draw_label(self, label):
        """
        Draws a field label.
        """

        self.styles.draw_label(
            label,
            self.x,
            self.y + self.LABEL_OFFSET_Y,
        )

    # ==========================================================
    # FIELD DIMENSIONS
    # ==========================================================

    def get_field_height(self, template):
        """
        Returns the field height depending on the template.
        """

        if template.multiline:
            return FIELD_HEIGHT * 4

        return FIELD_HEIGHT

    def get_required_height(self, template):
        """
        Calculates the vertical space required by a field.
        """

        height = self.get_field_height(template)

        return height + ROW_SPACING

    def get_field_x(self):
        """
        Returns the X coordinate where the input field starts.
        """

        return self.x + self.FIELD_OFFSET_X

    def move_next_row(self, template):
        """
        Moves the cursor to the next row.
        """

        self.y -= self.get_required_height(template)

    # ==========================================================
    # TEMPLATE HELPERS
    # ==========================================================

    @staticmethod
    def is_text_field(template):

        return template.control == ControlType.TEXT

    @staticmethod
    def is_textarea(template):

        return (
            template.control == ControlType.TEXT
            and template.multiline
        )

    @staticmethod
    def is_checkbox(template):

        return template.control == ControlType.CHECKBOX

    @staticmethod
    def is_radio(template):

        return template.control == ControlType.RADIO

    @staticmethod
    def is_dropdown(template):

        return template.control == ControlType.DROPDOWN

    @staticmethod
    def is_listbox(template):

        return template.control == ControlType.LISTBOX

    @staticmethod
    def is_date(template):

        return template.control == ControlType.DATE

    @staticmethod
    def is_number(template):

        return template.data_type in (
            "integer",
            "float",
            "decimal",
        )

    # ==========================================================
    # PDF FIELD NAMES
    # ==========================================================

    @staticmethod
    def build_field_name(table_name, column_name):
        """
        Creates a unique PDF field name.
        """

        return f"{table_name}.{column_name}"

    # ==========================================================
    # BUILD
    # ==========================================================

    def build(self):
        """
        Generates the complete fillable PDF.
        """

        schema = self.reader.read_schema()

        self.initialize_document()

        self.draw_header()

        for table in schema.values():

            self.draw_table(table)

        self.pdf.save()

        print(
            f"PDF generated successfully: "
            f"{Path(OUTPUT_FOLDER) / PDF_NAME}"
        )
    # ==========================================================
    # TABLES
    # ==========================================================

    def draw_table(self, table):
        """
        Draws all fields belonging to one database table.
        """

        if not table.columns:
            return

        self.check_page_break(50)

        self.draw_section(table.name)

        for column in table.columns.values():

            self.draw_column(
                table.name,
                column,
            )

        self.y -= self.TABLE_SPACING

    # ==========================================================
    # COLUMNS
    # ==========================================================

    def draw_column(
        self,
        table_name,
        column,
    ):
        """
        Draws one database column.
        """

        template = self.get_template(
            table_name,
            column,
        )

        print(
            f"{table_name}.{column.name} -> "
            f"control={template.control}, "
            f"options={template.options}"
        )

        required_height = self.get_required_height(
            template
        )

        self.check_page_break(
            required_height,
        )

        label = (
            template.label
            or self.humanize(column.name)
        )

        self.draw_label(label)

        field_name = self.build_field_name(
            table_name,
            column.name,
        )

        self.draw_field(
            field_name=field_name,
            column=column,
            template=template,
        )

        self.move_next_row(
            template,
        )

    # ==========================================================
    # FIELD RENDERING
    # ==========================================================

    def draw_field(
        self,
        field_name,
        column,
        template,
    ):
        """
        Draws a PDF field depending on its ControlType.
        """

        if self.is_checkbox(template):
            return self.draw_checkbox(
                field_name,
                column,
                template,
            )

        if self.is_radio(template):
            return self.draw_radio_group(
                field_name,
                column,
                template,
            )

        if self.is_dropdown(template):
            return self.draw_dropdown(
                field_name,
                column,
                template,
            )

        if self.is_listbox(template):
            return self.draw_listbox(
                field_name,
                column,
                template,
            )

        if self.is_textarea(template):
            return self.draw_textarea(
                field_name,
                column,
                template,
            )

        return self.draw_textfield(
            field_name,
            column,
            template,
        )

    # ==========================================================
    # TEXT FIELD
    # ==========================================================

    def draw_textfield(
        self,
        field_name,
        column,
        template,
    ):
        """
        Draws a standard AcroForm text field.
        """

        self.pdf.acroForm.textfield(
            name=field_name,
            x=self.get_field_x(),
            y=self.y,
            width=self.get_width(column, template),
            height=FIELD_HEIGHT,
            borderStyle="solid",
            forceBorder=True,
            value=self.get_default_value(column, template),
            tooltip=self.get_tooltip(column, template),
        )

    # ==========================================================
    # MULTILINE FIELD
    # ==========================================================

    def draw_textarea(
        self,
        field_name,
        column,
        template,
    ):
        """
        Draws a multiline text field.
        """

        self.pdf.acroForm.textfield(
            name=field_name,
            x=self.get_field_x(),
            y=self.y,
            width=self.get_width(column, template),
            height=self.get_field_height(template),
            borderStyle="solid",
            forceBorder=True,
            value=self.get_default_value(column, template),
            tooltip=self.get_tooltip(column, template),
            fieldFlags="multiline",
        )

    # ==========================================================
    # CHECKBOX
    # ==========================================================

    def draw_checkbox(
        self,
        field_name,
        column,
        template,
    ):
        """
        Draws a checkbox.
        """

        self.pdf.acroForm.checkbox(
            name=field_name,
            x=self.get_field_x(),
            y=self.y,
            buttonStyle="check",
            checked=bool(self.get_default(template)),
            tooltip=self.get_tooltip(column, template)
        )

    # ==========================================================
    # RADIO GROUP
    # ==========================================================

    def draw_radio_group(
        self,
        field_name,
        column,
        template,
    ):
        """
        Draws a horizontal radio button group.
        """

        x = self.get_field_x()

        options = self.get_options(column, template)

        spacing = 70

        for index, option in enumerate(options):

            radio_x = x + index * spacing

            self.pdf.acroForm.radio(
                name=field_name,
                value=str(option),
                selected=(
                    template.default == option
                ),
                x=radio_x,
                y=self.y,
                buttonStyle="circle",
            )

            self.pdf.drawString(
                radio_x + 15,
                self.y + 2,
                str(option),
            )

    # ==========================================================
    # DROPDOWN
    # ==========================================================

    def draw_dropdown(
        self,
        field_name,
        column,
        template,
    ):
        """
        Draws a dropdown field.

        If the installed ReportLab version does not support
        AcroForm choice fields, a normal textfield is created
        as a fallback.
        """

        if not hasattr(self.pdf.acroForm, "choice"):

            return self.draw_textfield(
                field_name,
                column,
                template,
            )

        options = self.get_options(
            column,
            template,
        )

        self.pdf.acroForm.choice(
            name=field_name,
            tooltip=self.get_tooltip(column, template),
            value=self.get_default_value(column, template),
            options=self.normalize_options(options),
            x=self.get_field_x(),
            y=self.y,
            width=self.get_width(column, template),
            height=FIELD_HEIGHT,
            borderStyle="solid",
            forceBorder=True,
        )

    # ==========================================================
    # LISTBOX
    # ==========================================================

    def draw_listbox(
        self,
        field_name,
        column,
        template,
    ):
        """
        Draws a listbox.

        Falls back to a normal textfield if the installed
        ReportLab version does not expose choice().
        """

        if not hasattr(self.pdf.acroForm, "choice"):

            return self.draw_textfield(
                field_name,
                column,
                template,
            )

        options = self.get_options(
        column,
        template,
        )

        self.pdf.acroForm.choice(
            name=field_name,
            tooltip=self.get_tooltip(column, template),
            value=self.get_default_value(column, template),
            options=self.normalize_options(options),
            x=self.get_field_x(),
            y=self.y,
            width=self.get_width(column, template),
            height=max(
                self.get_height(template),
                FIELD_HEIGHT * 4,
            ),
            borderStyle="solid",
            forceBorder=True,
            fieldFlags="multiSelect",
        )

    # ==========================================================
    # COMMON HELPERS
    # ==========================================================

    @staticmethod
    def normalize_options(options):
        """
        Converts any iterable of options into a list of strings.
        """

        if not options:
            return []

        return [
            str(option)
            for option in options
        ]

    @staticmethod
    def normalize_default(value):
        """
        Returns a valid default value for AcroForm fields.
        """

        if value is None:
            return ""

        return str(value)

        # ==========================================================
    # TEMPLATE ACCESS HELPERS
    # ==========================================================

    @staticmethod
    def get_width(column, template):
        """
        Returns the most appropriate width for a field.
        """

        if template.width:
            return template.width

        sql_type = (column.sql_type or "").upper()

        if sql_type == "DATE":
            return 80

        if sql_type == "TIME":
            return 70

        if sql_type == "DATETIME":
            return 120

        if sql_type in (
            "INT",
            "INTEGER",
            "BIGINT",
            "SMALLINT",
            "MEDIUMINT",
            "TINYINT",
        ):
            return 60

        if sql_type in (
            "DECIMAL",
            "NUMERIC",
            "FLOAT",
            "DOUBLE",
            "REAL",
        ):
            return 80

        if column.max_length:

            if column.max_length <= 10:
                return 80

            if column.max_length <= 30:
                return 120

            if column.max_length <= 100:
                return 180

        return FIELD_WIDTH

    @staticmethod
    def get_tooltip(column, template):
        """
        Returns the tooltip displayed in the PDF.
        """

        if template.tooltip:
            return template.tooltip

        tooltip = column.sql_type

        if column.max_length:
            tooltip += f" ({column.max_length})"

        if not column.nullable:
            tooltip += " - Required"

        return tooltip

    @staticmethod
    def get_default_value(column, template):
        """
        Returns the initial value of the field.
        """

        if template.default is not None:
            return template.default

        sql_type = (column.sql_type or "").upper()

        if sql_type == "DATE":
            return "dd/mm/yyyy"

        if sql_type == "TIME":
            return "hh:mm"

        if sql_type == "DATETIME":
            return "dd/mm/yyyy hh:mm"

        return ""

    @staticmethod
    def get_options(column, template):
        """
        Returns the available options for dropdowns, listboxes and radios.
        """

        if template.options:
            return template.options

        if column.enum_values:
            return column.enum_values

        return []

    @staticmethod
    def get_height(template):
        """
        Returns the height defined by the template or the calculated height.
        """

        if template.height:
            return template.height

        if template.multiline:
            return FIELD_HEIGHT * 4

        return FIELD_HEIGHT

    @staticmethod
    def get_default(template):
        """
        Returns the normalized default value.
        """

        if template.default is None:
            return ""

        return str(template.default)


    @staticmethod
    def is_visible(template):
        """
        Indicates whether the field should be rendered.
        """

        return template.visible

    @staticmethod
    def is_required(template):
        """
        Indicates whether the field is mandatory.
        """

        return template.required

    @staticmethod
    def is_read_only(template):
        """
        Indicates whether the field is read-only.
        """

        return template.read_only

    @staticmethod
    def has_options(template):
        """
        Indicates whether the field contains selectable options.
        """

        return bool(template.options)