import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from a .env file in the parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)


connection = psycopg2.connect(
    os.getenv("DATABASE_URL")
    # host=os.getenv("DB_HOST"),
    # user=os.getenv("DB_USERNAME"),
    # password=os.getenv("DB_PASSWORD"),
    # dbname=os.getenv("DB_NAME"),
)

cursor = connection.cursor()

CHORDPRO_DIR = "src"

chordpro_file_names = os.listdir(CHORDPRO_DIR)

for file_name in chordpro_file_names:
    if file_name.endswith(".pro"):
        with open(f"{CHORDPRO_DIR}/{file_name}", "r") as f:
            song_sheet = f.read()
        slug = file_name[:-4]
        update_query = 'UPDATE bahai_songs."Song" SET sheet = %s, "updatedAt" = NOW() WHERE slug = %s AND (sheet is NULL OR sheet != %s)'
        cursor.execute(update_query, (song_sheet, slug, song_sheet))

connection.commit()
cursor.close()
connection.close()
