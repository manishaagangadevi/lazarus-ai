from app.core.analyzer import CodeAnalyzer
from app.services.ai_service import analyze_function_with_ai


if __name__ == "__main__":
    analyzer = CodeAnalyzer("tests")
    result = analyzer.analyze_project()

    print("\n================ LAZARUS AI REPORT ================\n")

    if not result["unused"]:
        print("No unused functions detected 🎉")
    else:
        for func_name, info in result["unused"].items():
            print(f"\n🔎 Function: {func_name}")
            print(f"📂 File: {info['file']}")
            print(f"📍 Line: {info['line']}")
            print("\n--- Function Source ---")
            print(info["source"])

            print("\n🤖 AI Risk Analysis:\n")
            ai_response = analyze_function_with_ai(info["source"])
            print(ai_response)
            print("\n---------------------------------------------------")