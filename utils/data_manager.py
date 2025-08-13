import json
import os 

class DataManager:

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
    # نوشتن تابعی برای نوشتن در فایل جیسون 
    @staticmethod
    def write_json(file_path, data):
        '''نوشتن در یک فایل جیسون '''
        with open (file_path, 'w', encoding="utf-8") as file :
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    @staticmethod
    def append_json(file_path, data):

        old_data = DataManager.read_json(file_path)
        if isinstance(data, list):
            old_data.extend(data)
        else:
            old_data.append(data)
        DataManager.write_json(file_path, old_data)