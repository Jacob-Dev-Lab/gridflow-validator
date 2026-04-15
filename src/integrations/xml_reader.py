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
        
    def _get_int_value(self, element, tag_name: str) -> int:
        if element is None:
            raise ValueError(f"{tag_name} element not found")

        if element.text is None:
            raise ValueError(f"{tag_name} value is missing")

        return int(element.text)

    def get_quantity_for_hour(self, hour_index: int, direction: str) -> int:
        """
        Returns energy quantity for a given hour
        """

        series = self._get_series(direction)
        period = series.find('ns:Period', NAMESPACE)

        if period is None:
            raise ValueError(f"{period} value is missing")
        
        points = period.findall('ns:Point', NAMESPACE)

        target_seconds = (hour_index + 1) * 3600

        last_value = None

        for point in points:
            position = self._get_int_value(
                point.find('ns:position', NAMESPACE), 
                "position")
            
            quantity = self._get_int_value(
                point.find('ns:quantity', NAMESPACE), 
                "quantity")

            if position <= target_seconds:
                last_value = quantity
            else:
                break

        if last_value is None:
            raise ValueError(f"No value found for hour {hour_index}")

        return last_value