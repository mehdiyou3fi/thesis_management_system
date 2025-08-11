import json
import os 

class DataMsnsger:

    @staticmethod
    def read_json (file_path):
        """این یک تابع است ک در ان یک فایل جسون را خوانده و باز میگرداند 

        Args:
            file_path (str): یک مسیر در سیستم است که فایل در ان قرار دارد 
        """
        # موجود بودن ان مسیر 
        if not os.path.exists(file_path):
            return []
        # خواندن فایل 
        with open(file_path, 'r',encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    # def write_json(file_path, data):
    #     with open (filr)
    
            

        

