from utils.data_manager import DataManager
from utils.paths import STUDENT_JSON, PROFESSOR_JSON, EXTERNAL_REVIEWERS_JSON, DEFENDED_JSON
class User:
    def __init__(self, id, name, username, password):
        self.id = id
        self.name = name
        self.username= username
        self.password = password
    @staticmethod
    def search_defended_thesis():
        '''جست و جو در بانک پایان نامه ها 
        query : متن جستو جو 
        filed :یکی از title , reviewer , year, judges'''

        results   = DataManager.read_json(DEFENDED_JSON)
        print("\n--- Search in Defended Theses ---")
        title     = input("Thesis title (leave empty to skip): ").strip()
        professor = input("Supervisor code(professor_code) (leave empty to skip): ").strip()
        student   = input("Student code (leave empty to skip): ").strip()
        year      = input("Defense year (leave empty to skip): ").strip()
        judges    = input("Judge name (leave empty to skip): ").strip()

        if title:
            results = [r for r in results if title.lower() in r["title"].lower()]

        if professor:
            results = [r for r in results if professor.lower() in r["professor_code"].lower()]

        if student:
            results = [r for r in results if student.lower() in r["student_code"].lower()]

        if year:
            results = [r for r in results if str(year) in str(r.get("defense_date"))]

        if judges:
            results = [r for r in results if any(judges.lower() in j.lower() for j in r["judges"].values())]

        print("\n--- Search Results ---")
        if not results:
            print("❌ No results found.")
        else:
            for r in results:
                print(f"📘 Title: {r['title']}")
                print(f"👨‍🎓 Student: {r['student_code']}")
                print(f"👨‍🏫 Supervisor: {r['professor_code']}")
                print(f"⚖️ Judges: {', '.join(r['judges'].values())}")
                print(f"📅 Year: {r.get('defense_date', 'N/A')}")
                print(f"✅ Final Score: {r.get('final_score', 'N/A')}")
                print("-" * 40)