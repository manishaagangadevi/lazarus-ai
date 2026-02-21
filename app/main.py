from app.core.analyzer import CodeAnalyzer

if __name__ == "__main__":
    analyzer = CodeAnalyzer("tests")
    result = analyzer.analyze_project()

    print("\nDefined Functions:")
    print(result["defined"])

    print("\nCalled Functions:")
    print(result["called"])

    print("\nUnused Functions:")
    print(result["unused"])