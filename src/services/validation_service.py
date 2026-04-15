import logging

from integrations.xml_reader import DSXMLReader
#from utils.file_utils import get_latest_file
from core.config import CSV_DIR, XML_DIR
from models.validation_result import ValidationResult


class ValidationService:

    def validate(self, csv_file: str, xml_file: str, hour_index: int, hour_label: str):
        """
        Core validation logic:
        - compares CSV vs XML values
        - returns structured result
        """

        csv_value, direction = self._get_csv_data(csv_file, hour_index)

        xml_reader = DSXMLReader(xml_file)
        xml_value = xml_reader.get_quantity_for_hour(hour_index, direction)

        is_valid = csv_value == xml_value

        result = ValidationResult(
            hour_label=hour_label,
            csv_value=csv_value,
            xml_value=xml_value,
            direction=direction,
            is_valid=is_valid
        )

        logging.info(str(result))

        return result

    def _get_csv_data(self, csv_file: str, hour_index: int):
        """
        Extract CSV value + direction flow
        """

        import pandas as pd

        df = pd.read_csv(csv_file)

        csv_value = int(float(str(df.iloc[hour_index, 3]).replace(",", "")))
        direction = str(df.iloc[hour_index, 4])

        return csv_value, direction