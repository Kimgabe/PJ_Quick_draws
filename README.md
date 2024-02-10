![image](https://github.com/Kimgabe/PJ_Quick_draws/assets/74717033/6d729fbc-15c0-4de9-985c-c96d5ed97df7)

# AIFFEL_Sidethon : Quick Draw!
---
## 📌Intro.
- AIFFEL에서 진행하는 AI Core 과정 7기 동기들끼리 사이드 프로젝트를 진행합니다.
- 교육과정 최종 프로젝트인 AIFFELthon (AI 모델을 탑재한 flutter 기반 모바일 앱 만들기) 를 진행합니다.
- 이번 sidethon 기간은 flutter를 배우는 기간(24.01.30 ~ 24.02.19) 동안 AI 모델링 경험 및 커뮤니케이션 역량 강화를 목적으로 진행합니다.

---
## 프로젝트 작업 Log (점차 추가 예정)
- 프로젝트 기간 : 24.01.30 ~ 24.02.19
  - 팀원 모집 : 24.01.29 ~ 24.01.31
  - 참가 프로젝트(kaggle competition) 선정 및 자료조사 : 24.01.31 ~ 24.02.04
  - 데이터 기초 전처리(chunk를 통한 경량화 및 샘플링) : 24.02.04 ~ 24.02.07
---

<details>
<summary>👈 Git commit 컨벤션 확인하기</summary>


| 커밋 유형 | 의미 |
| --- | --- |
| Feat | (어떤 유형이든) 파일의 최초 등록 시에 사용 |
| Model | 모델 구조변경 혹은 새로운 모델 추가 |
| Param | 하이퍼파라미터 수정 |
| Data | 데이터 전처리 방식 변경, 새로운 데이터 추가 |
| Metric | 평가지표 변경 |
| Train | 훈련과정 변경(Epoch수, Batch size 변경 등) |
| Eval | 검증/테스트 과정 변경 |
| Deploy | 모델 배포 관련 변경 |
| Fix | 버그 수정 (일반, ML/DL) |
| Docs | 문서 수정 (일반, ML/DL) |
| Style | 코드 formatting, 세미콜론 누락, 코드 자체의 변경이 없는 경우 |
| Refactor | 코드 리팩토링 (일반, ML/DL) |
| Test | 테스트 코드, 리팩토링 테스트 코드 추가 |
| Chore | 패키지 매니저 수정, 그 외 기타 수정 ex) .gitignore |
| Design | CSS 등 사용자 UI 디자인 변경 |
| Comment | 필요한 주석 추가 및 변경 (일반, ML/DL) |
| Rename | 파일 또는 폴더 명을 수정하거나 옮기는 작업만인 경우 |
| Remove | 파일을 삭제하는 작업만 수행한 경우 |
| !BREAKING CHANGE | 커다란 API 변경의 경우 |
| !HOTFIX | 급하게 치명적인 버그를 고쳐야 하는 경우 |


</details>


| 날짜 | 분류 | 작업명 | 링크 | 작업자 | Commit 유형 |
| --- | --- | --- | --- | --- | --- |
| 2024-02-07 | EDA | Simple_EDA.ipynb | [링크](https://github.com/Kimgabe/PJ_Quick_draws/raw/586b07010b43be5d8aa85c6ba5b597f7272ee427/EDA%2Fseungsoon%2FSimple_EDA.ipynb) | seungsoon Kim | Rename  |
| 2024-02-07 | EDA | Sidethon_EDA_seul_v1.ipynb | [링크](https://github.com/Kimgabe/PJ_Quick_draws/raw/ff7e4b2be72dcf84428f6662858e073a3c0148ee/EDA%2Fseul%2FSidethon_EDA_seul_v1.ipynb) | seulwithlove | Data |
| 2024-02-07 | Preprocessing | [공통] data_pipeline(데이터 가져오기 및 시각화).ipynb | [링크](https://github.com/Kimgabe/PJ_Quick_draws/raw/3958f7b97d918fb5b7914ec259fddf38a0601189/Preprocessing%2Fseungsoon%2F%5B%EA%B3%B5%ED%86%B5%5D%20data_pipeline(%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0%20%EB%B0%8F%20%EC%8B%9C%EA%B0%81%ED%99%94).ipynb) | seungsoon Kim | Feat  |
| 2024-02-07 | config | label_names.pkl | [링크](https://github.com/Kimgabe/PJ_Quick_draws/raw/fb42f33a6e0aabfaddabe3dc20385cb9c490868e/config%2Flabel_names.pkl) | seungsoon Kim | Feat  |
| 2024-02-07 | Preprocessing | [공통] data_pipeline(데이터 가져오기 및 시각화).ipynb | [링크](https://github.com/Kimgabe/PJ_Quick_draws/raw/ec2aac6ce53a2c647cb20b556eb609e64c9072e1/Preprocessing%2Fseungsoon%2F%5B%EA%B3%B5%ED%86%B5%5D%20data_pipeline(%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0%20%EB%B0%8F%20%EC%8B%9C%EA%B0%81%ED%99%94).ipynb) | seungsoon Kim | Feat  |
| 2024-02-07 | Preprocessing | [공통] preprocessing_train_df.ipynb | [링크](https://github.com/Kimgabe/PJ_Quick_draws/raw/b41381d8160060539051f129265728609e2e13b7/Preprocessing%2Fseungsoon%2F%5B%EA%B3%B5%ED%86%B5%5D%20preprocessing_train_df.ipynb) | seungsoon Kim | Feat  |
| 2024-02-07 | Preprocessing | QuickDraw (LeakyReLU).ipynb | [링크](https://github.com/Kimgabe/PJ_Quick_draws/raw/77fd05f28037b286783637900d48943b4516ffb5/Preprocessing%2Fwoojin%2FQuickDraw%20(LeakyReLU).ipynb) | seungsoon Kim | Merge branch 'main' of https |
| 2024-02-07 | Preprocessing | QuickDraw (ReLU).ipynb | [링크](https://github.com/Kimgabe/PJ_Quick_draws/raw/77fd05f28037b286783637900d48943b4516ffb5/Preprocessing%2Fwoojin%2FQuickDraw%20(ReLU).ipynb) | seungsoon Kim | Merge branch 'main' of https |
| 2024-02-07 | Preprocessing | [simplified] preprocessing_train_df.ipynb | [링크](https://github.com/Kimgabe/PJ_Quick_draws/raw/e9574f84d3c523eb569e4348c961325e0b17d5f6/Preprocessing%2Fseungsoon%2Fold_tasks%2F%5Bsimplified%5D%20preprocessing_train_df.ipynb) | seungsoon Kim | Rename  |
| 2024-02-06 | Preprocessing | QuickDraw (LeakyReLU).ipynb | [링크](https://github.com/Kimgabe/PJ_Quick_draws/raw/9c46b5bb3bf90a45821777cc0b7e6826cf9d65af/Preprocessing%2Fwoojin%2FQuickDraw%20(LeakyReLU).ipynb) | woojinOh | Data |
