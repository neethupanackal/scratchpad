import os
from datetime import datetime


class BatchCheckpoint:
    def __init__(self, business_unit: str, default_datetime: str = "2000-01-01T00:00:00"):
        """
        Initialize the BatchCheckpoint class.
        
        :param business_unit: The prefix for the checkpoint file.
        :param default_datetime: The default datetime if there is no checkpoint (ISO format).
        """
        self.business_unit = business_unit
        self.checkpoint_file = f"{business_unit}_checkpoint.txt"
        self.default_datetime = datetime.fromisoformat(default_datetime)

    def get_last_processed(self):
        """
        Get the last processed table and timestamp from the checkpoint file.
        
        :return: A tuple of (last_processed_table, last_processed_timestamp).
                 Returns default datetime and None if no checkpoint exists.
        """
        if not os.path.exists(self.checkpoint_file):
            return None, self.default_datetime
        
        with open(self.checkpoint_file, "r") as file:
            data = file.read().strip()
            if data:
                table_name, timestamp = data.split(",")
                return table_name, datetime.fromisoformat(timestamp)
        
        return None, self.default_datetime

    def update_checkpoint(self, table_name: str):
        """
        Update the checkpoint file with the current table name and timestamp.
        
        :param table_name: The table name being processed.
        """
        timestamp = datetime.now().isoformat()
        with open(self.checkpoint_file, "w") as file:
            file.write(f"{table_name},{timestamp}")

    def reset_checkpoint(self):
        """
        Reset the checkpoint file after successful batch processing.
        """
        if os.path.exists(self.checkpoint_file):
            os.remove(self.checkpoint_file)
