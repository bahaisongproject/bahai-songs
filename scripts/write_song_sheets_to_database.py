import os
import pymysql
from dotenv import load_dotenv

# Load environment variables from a .env file in the parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)


connection = pymysql.connect(
    host=os.getenv("DB_SERVER"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    ssl_verify_identity=True,
)

cursor = connection.cursor()

CHORDPRO_DIR = "src"


chordpro_file_names = os.listdir(CHORDPRO_DIR)

for file_name in chordpro_file_names:
    if file_name.endswith(".pro"):
        with open(f"{CHORDPRO_DIR}/{file_name}", "r") as f:
            song_sheet = f.read()
        slug = file_name[:-4]
        update_query = "UPDATE Song SET sheet = %s, updatedAt = NOW() WHERE slug = %s"
        cursor.execute(update_query, (song_sheet, slug))

connection.commit()
cursor.close()
connection.close()
