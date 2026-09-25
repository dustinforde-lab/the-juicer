import os
import ast

def audit_codebase():
    print("=== 🕵️ THE JUICER: CODEBASE AUDIT ===\n")
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    defined_functions = set()
    called_functions = set()
    
    for file in py_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 1. Syntax Check
                compile(content, file, 'exec')
                
                # 2. AST Parsing for Dead Code
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        defined_functions.add(node.name)
                    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        called_functions.add(node.func.id)
                        
            print(f"✅ {file}: Syntax Clean")
        except SyntaxError as e:
            print(f"❌ {file}: SYNTAX ERROR at line {e.lineno} - {e.msg}")
        except Exception as e:
            print(f"⚠️ {file}: Could not parse - {e}")

    print("\n🔍 DEAD CODE CHECK (Functions defined but not called locally):")
    unused = defined_functions - called_functions
    # Filter out standard Streamlit callbacks or main functions
    unused = {f for f in unused if not f.startswith('_') and f != 'main'}
    if unused:
        for f in unused:
            print(f"  ❓ Def {f}() found, but no direct calls detected.")
    else:
        print("  ✅ All defined functions appear to be utilized.")
        
    print("\n==========================================")

if __name__ == "__main__":
    audit_codebase()
