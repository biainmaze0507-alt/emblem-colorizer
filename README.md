# 길드 엠블럼 색상 시안 도구

영역별(금속 / 날개 바깥+보석 3개 / 날개 안쪽 / 리본+가운데 보석 / 배경 / 윤곽선 / 글씨) 색을 바꿔 보고 PNG로 저장하는 정적 웹페이지.
버전 탭에서 리본 유무, 왕관 가운데 보석 위치, 둥근 프레임 켜기/끄기를 고른다.

## 파일
- `index.html` + `masks/` : GitHub Pages 용. 이 두 개를 저장소 루트에 올리면 됨.
- `emblem-colorizer-standalone.html` : 마스크가 내장된 단일 파일(약 1.7MB). 더블클릭으로 바로 열림.
- `emblem.svg` : 현재 디자인(리본+글씨, 원본 색) 벡터 파일. 글자는 패스로 변환되어 폰트 없이 열림.
- `page.html` : 소스(아티팩트 본체, 스켈레톤 없음). 수정은 여기서 하고 `build_site.py` 실행.
- `build_layers.py` : 원본 PNG 3장(src_*.png)에서 `masks/` 를 다시 만드는 스크립트.

## 원본 갱신 (pptx 1페이지가 바뀌었을 때)
파워포인트 COM으로 1페이지를 2475px PNG로 내보낸다(리본+글씨 / 글씨 숨김 / 리본도 숨김 3장).
방패 바깥선 Freeform 47은 꼭짓점에서 선이 삐져나오므로 내보내기 전에 `Nodes.SetSegmentType(19, 0)` 적용.
남색 윤곽선만 흰 배경에 렌더한 참고 이미지(lineref_plain/ribbon.png)도 함께 뽑아 넘기면 배경/윤곽선 분리가 정확해진다.

```
..\.venv\Scripts\python.exe -I build_layers.py masks src_plain.png src_ribbon.png src_text.png lineref_plain.png lineref_ribbon.png
..\.venv\Scripts\python.exe -I build_site.py
```

프레임 비율은 pptx 8·11·12페이지 기준: 540pt 슬라이드에서 프레임 24.5pt 안쪽 490.9pt, 선 6pt, 모서리 adj 0.29065, 엠블럼은 52.2pt 위치에 435.7pt.

## GitHub Pages 올리기
1. 새 저장소 만들기 (public).
2. `index.html` 과 `masks/` 폴더를 올림.
3. Settings → Pages → Branch: main, folder: / (root) → Save.
4. 1~2분 뒤 `https://<계정>.github.io/<저장소>/` 에서 열림.
