# 길드 엠블럼 색상 시안 도구

영역별(금속 / 날개 바깥+보석 3개 / 날개 안쪽 / 리본+가운데 보석 / 배경 / 글씨) 색을 바꿔 보고 PNG로 저장하는 정적 웹페이지.
구성 탭에서 리본 글씨(에린어 폰트, 기본 '마비팟'), 왕관 가운데 보석 위치, 2줄 둥근 프레임 켜기/끄기를 고른다. 남색 윤곽선 자리는 색이 아니라 빈 영역(배경색/투명).

## 파일
- `index.html` + `masks/` : GitHub Pages 용. 이 두 개를 저장소 루트에 올리면 됨. 에린어 폰트(ErinLang-Direct.ttf)는 index.html 안에 base64로 내장됨.
- `artifact.html` : claude.ai 아티팩트에 올리는 본체(스켈레톤 없음, 폰트 내장). build_site.py가 만든다.
- `emblem-colorizer-standalone.html` : 마스크가 내장된 단일 파일(약 1.7MB). 더블클릭으로 바로 열림.
- `emblem.svg` : 현재 디자인(리본+글씨, 원본 색) 벡터 파일. 사이트의 투명 저장과 같게, 남색이 보이던 자리(배경·방패 안쪽·윤곽선)는 전부 비어 있음. 글자는 패스로 변환되어 폰트 없이 열림.
- `make_svg.py` : 배경 사각형만 숨긴 1페이지 PDF → SVG 변환. 남색 영역을 luminance 마스크로 뚫는다. 사용: `python -I make_svg.py slide1_lines.pdf emblem.svg <pymupdf 폴더>`
- `page.html` : 소스. 수정은 여기서 하고 `build_site.py` 실행(폰트 자리표시 `/*__ERINLANG_FONT__*/`를 채워 넣음).
- `build_layers.py` : 원본 PNG 3장(src_*.png)에서 `masks/` 를 다시 만드는 스크립트.

## 원본 갱신 (pptx 1페이지가 바뀌었을 때)
파워포인트 COM으로 1페이지를 2475px PNG로 내보낸다. 사이트는 '리본 있음·글씨 없음' 렌더(TextBox 1 숨김)만 쓴다. 글씨는 사이트가 폰트로 직접 그린다(24pt=110px, 리본 처짐을 따라 반지름 4118px 원호).
방패 바깥선(Freeform 47·48)은 경로 시작점이 꼭짓점이라 파워포인트가 그 이음새에 선을 삐져나오게 그린다. SetSegmentType으로 고치면 오른쪽 어깨가 직선이 되므로 쓰지 말 것. 대신 slide1.xml의 두 path를 맨 아래 점에서 시작하도록 세그먼트 순서를 돌린 복사본(patched.pptx)을 만들어 거기서 내보낸다(원본 pptx는 수정하지 않음).
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
