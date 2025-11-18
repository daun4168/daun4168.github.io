import markdown

# from game import Game

#
# if __name__ == "__main__":
#     game = Game()
#
#
# exec_local = {}




def handle_event(event):
    global editor
    print(type(event))
    print(event.__dir__())
    # will log `print(6 * 7)`
    print(event.code)
    # prevent default execution

    bag = {}

    safe_builtins = {'print': print, 'len': len}
    restricted_globals = {'__builtins__': safe_builtins, 'bag': bag}

    try:
        exec(event.code, restricted_globals)
    except Exception as e:
        # __import__ 함수에 접근할 수 없어 NameError가 발생하며 실행이 차단됨
        print(f"차단 성공: {type(e).__name__} 발생 - {e}")
    # editor.code = ""
    return False


