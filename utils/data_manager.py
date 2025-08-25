import json
import os 
import tempfile
import shutil


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
            


    #  تابعی برای نوشتن در فایل جیسون 
    @staticmethod
    def write_json(file_path, data):
        '''نوشتن امن در یک فایل جیسون '''
        # اطمینان از اینکه پوشه مقصد وجود دارد 
        
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        # فایل موقت میسازیم
        fd, tmp = tempfile.mkstemp(prefix=".tmp_", dir=os.path.dirname(file_path) or ".")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                 json.dump(data, f, ensure_ascii=False, indent=4)

            # جابه جایی فایل موقت به اصلی 
            shutil.move(tmp, file_path)

        finally:
            # اگر به هردلیلی تمپ پاک نشد ان را پاک کنیم 
            if os.path.exists(tmp):
                 os.remove(tmp)


        
    

    @staticmethod
    def append_json(file_path, data):

        old_data = DataManager.read_json(file_path)
        if isinstance(data, list):
            old_data.extend(data)
        else:
            old_data.append(data)
        DataManager.write_json(file_path, old_data)
