import address_book
import importlib
import os

print("\n=======================================================")
print(" 🔍 THE JUICER: ADDRESS BOOK DIAGNOSTIC AUDIT")
print("=======================================================")

print("\n📁 File Path Audits:")
for key, path in address_book.PATHS.items():
    exists = "✅ FOUND" if os.path.exists(path) else "⚠️ NOT FOUND"
    print(f"  {key:<18} -> {path} [{exists}]")

print("\n📡 UI Tab Dispatch Audits:")
for tab, route in address_book.TAB_DISPATCH_REGISTRY.items():
    mod_name = route["module"]
    try:
        mod = importlib.import_module(mod_name)
        found_func = None
        for fn in route["entrypoints"]:
            if hasattr(mod, fn):
                found_func = fn
                break
        if found_func:
            print(f"  {tab:<14} -> {mod_name}.py::{found_func}() [✅ ROUTED]")
        else:
            print(f"  {tab:<14} -> {mod_name}.py [🚨 MISSING FUNCTION: {route['entrypoints']}]")
    except Exception as e:
        print(f"  {tab:<14} -> 🚨 IMPORT FAILED: {mod_name}.py ({e})")

print("\n=======================================================\n")
