from app.core.analyzer import CodeAnalyzer

if __name__ == "__main__":
    analyzer = CodeAnalyzer("tests/sample.py")
    result = analyzer.analyze()

    print("Defined Functions:", result["defined"])
    print("Called Functions:", result["called"])
    print("Unused Functions:", result["unused"])