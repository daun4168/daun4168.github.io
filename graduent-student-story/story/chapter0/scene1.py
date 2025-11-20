
SCENE = {
    "name": "제 2 연구실",
    "initial_text": "문을 열자 퀴퀴한 곰팡이 냄새와 먼지가 뒤섞여 코를 찌른다. 이곳은 신성한 연구실인가, 고고학 발굴 현장인가.\n\n구석에는 정체를 알 수 없는 쓰레기통이 넘칠 듯이 차 있고, 벽 한쪽에는 굳게 닫힌 시약장과 낡은 박스들이 산더미처럼 쌓여 있다.\n먼지 쌓인 오래된 컴퓨터는 켜지기는 할지 의문이며, 바닥에는 정체불명의 의문의 액체가 흥건하다. 그 옆에 빗자루가 굴러다닌다.",
    "keywords": {
        "쓰레기통": {"type": "Object", "state": "hidden"}, "박스": {"type": "Object", "state": "hidden"},
        "빗자루": {"type": "Object", "state": "hidden"}, "오래된 컴퓨터": {"type": "Object", "state": "hidden"},
        "의문의 액체": {"type": "Object", "state": "hidden"}, "시약장": {"type": "Object", "state": "hidden"},
        "바닥": {"type": "Object", "state": "hidden"}, "벽": {"type": "Object", "state": "hidden", "sub_keyword": "메모"},
        "벽면": {"type": "Alias", "target": "벽"}, "문": {"type": "Object", "state": "hidden"},
        "컴퓨터": {"type": "Alias", "target": "오래된 컴퓨터"}
    }
}
