import xml.etree.ElementTree as ET

NAMESPACE = {
    'ns': 'urn:iec62325.351:tc57wg16:451-2:scheduledocument:5:1'
}


class DSXMLReader:
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.time_series = self.root.findall('ns:TimeSeries', NAMESPACE)

    def _get_series(self, direction: str):
        """
        Returns correct TimeSeries based on direction
        """
        if direction == "FRGB":
            return self.time_series[0]
        elif direction == "GBFR":
            return self.time_series[1]
        else:
            raise ValueError("Invalid direction (FRGB or GBFR expected)")

    def get_quantity_for_hour(self, hour_index: int, direction: str) -> int:
        """
        Returns energy quantity for a given hour
        """

        series = self._get_series(direction)
        period = series.find('ns:Period', NAMESPACE)
        points = period.findall('ns:Point', NAMESPACE)

        target_seconds = (hour_index + 1) * 3600

        last_value = None

        for point in points:
            position = int(point.find('ns:position', NAMESPACE).text)
            quantity = int(point.find('ns:quantity', NAMESPACE).text)

            if position <= target_seconds:
                last_value = quantity
            else:
                break

        if last_value is None:
            raise ValueError(f"No value found for hour {hour_index}")

        return last_value