import code


class RestrictedConsole(code.InteractiveConsole):
    def runsource(self, source, filename="<input>", symbol="single"):
        # 1. import 구문 차단
        if source.strip().startswith("import") or "import " in source:
            print("⚠️ import is disabled in this shell.")
            return False
        # 2. from ... import ... 형태 차단
        if source.strip().startswith("from "):
            print("⚠️ from-import is disabled in this shell.")
            return False

        # 나머지는 기본 실행
        return super().runsource(source, filename, symbol)



RestrictedConsole(locals={"a": a, "b": b}).interact("Restricted interactive shell")
