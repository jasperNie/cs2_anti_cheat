import sqlite3
import sys

def main(db_path):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    delete_query = """
    DELETE FROM player_stats
    WHERE wonGame = 0
    """
    cursor.execute(delete_query)

    update_query = """
    UPDATE player_stats
    SET isCheating = 1
    """
    cursor.execute(update_query)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_path = sys.argv[1]
    main(db_path)

# Example Command: python toggleIsCheat.py 76561198996682727\76561198996682727_info.db