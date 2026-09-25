import sqlite3
import os

DB_FILE = "action_grid.db"

def run_self_audit():
    print("=" * 65)
    print("📋 [SELF-AUDIT] Verifying Raw Intelligence Database...")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            
            # Query the raw articles table
            cur.execute("SELECT id, title, content FROM raw_slate_articles")
            rows = cur.fetchall()
            
            if not rows:
                print("   ⚠️ No data found in raw_slate_articles table.")
            else:
                total_lines = 0
                print(f"   ✅ Found {len(rows)} articles successfully loaded.\n")
                
                for row_id, title, content in rows:
                    line_count = len(content.splitlines())
                    char_count = len(content)
                    total_lines += line_count
                    
                    # Grab a short preview of the text to prove it's there
                    snippet = content[:65].replace("\n", " ").strip() + "..."
                    
                    print(f"   [{row_id}] {title}")
                    print(f"       -> Lines: {line_count} | Chars: {char_count}")
                    print(f"       -> Preview: {snippet}")
                    print("-" * 65)
                    
                print(f"   🟢 TOTAL RAW LINES SECURED: {total_lines}")
                
    except sqlite3.OperationalError as e:
        print(f"   ❌ Database Error (Table might not exist yet): {e}")
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    run_self_audit()
