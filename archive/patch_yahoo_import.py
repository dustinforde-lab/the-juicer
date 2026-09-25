with open("yahoo_sync.py", "r", encoding="utf-8") as f:
    code = f.read()

# Fix the import statement
old_import = "from yahoo_fantasy_api import OAuth2, Game"
new_import = "from yahoo_oauth import OAuth2\n        from yahoo_fantasy_api import Game"

if old_import in code:
    code = code.replace(old_import, new_import)
    with open("yahoo_sync.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Fixed OAuth2 import in yahoo_sync.py")
else:
    print("⚠️ Could not find the target import statement to replace.")