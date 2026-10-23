# 길드 엠블럼 색상 시안 도구

영역별(금속 / 날개 바깥+보석 3개 / 날개 안쪽 / 리본+가운데 보석 / 배경 / 글씨) 색을 바꿔 보고 PNG로 저장하는 정적 웹페이지.

## 파일
- `index.html` + `masks/` : GitHub Pages 용. 이 두 개를 저장소 루트에 올리면 됨.
- `emblem-colorizer-standalone.html` : 마스크가 내장된 단일 파일(약 1.8MB). 더블클릭으로 바로 열림. 카톡/디스코드로 보내도 됨.
- `page.html` : 소스(아티팩트 본체, 스켈레톤 없음). 수정은 여기서 하고 `build_site.py` 실행.
- `build_layers.py` : 원본 PNG 3장(src_*.png)에서 `masks/` 를 다시 만드는 스크립트.

## GitHub Pages 올리기
1. 새 저장소 만들기 (public).
2. `index.html` 과 `masks/` 폴더를 올림.
3. Settings → Pages → Branch: main, folder: / (root) → Save.
4. 1~2분 뒤 `https://<계정>.github.io/<저장소>/` 에서 열림.

## 다시 빌드
```
..\.venv\Scripts\python.exe -I build_layers.py masks src_plain.png src_ribbon.png src_text.png
..\.venv\Scripts\python.exe -I build_site.py
```

## 시안 코드
`버전.금속.날개바깥.날개안쪽.리본.배경.글씨.보석위치[.t]` 형식. 예:
`text.E0C7A9.DE80A6.F4EEE8.DE80A6.222A39.FFFFFF.mid`
URL 뒤에 `#코드` 를 붙이면 그 상태로 열림.
