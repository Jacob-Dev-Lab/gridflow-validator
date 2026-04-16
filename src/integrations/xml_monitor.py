import os
from typing import List

class DSXMLMonitor:
    def __init__(self, watch_dir: str):
        self.watch_dir = os.path.abspath(watch_dir)
        os.makedirs(self.watch_dir, exist_ok=True)

        self.seen_files = set()

    def monitor(self) -> List[str]:
        """
        Detect newly added XML files in the directory.
        """

        current_files = {
            f for f in os.listdir(self.watch_dir) if f.endswith(".xml")
        }

        new_files = current_files - self.seen_files

        # Update state
        self.seen_files.update(current_files)

        return list(new_files)