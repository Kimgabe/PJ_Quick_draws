import os
from github import Github
from datetime import datetime

# GitHub 설정
g = Github(os.getenv('GITHUB_TOKEN'))
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

# README.md 파일 가져오기
contents = repo.get_contents("README.md")
readme_content = contents.decoded_content.decode("utf-8")

# "📝 Recent Work Updates" 섹션 찾기 및 기존 표 제거
if "📝 Recent Work Updates" in readme_content:
    # 기존 표가 있다면 제거
    readme_content = readme_content.split("📝 Recent Work Updates")[0]

# 커밋 로그에서 최근 10개의 항목 가져오기 (.github 폴더 및 README.md 제외)
commits = repo.get_commits()
recent_updates = []
count = 0

for commit in commits:
    if count >= 10:
        break
    files = commit.files
    for file in files:
        if file.filename.endswith("README.md") or file.filename.startswith(".github/"):
            continue
        # 파일 정보와 커밋 정보 추출
        date = commit.commit.author.date.strftime("%Y-%m-%d")
        author = commit.commit.author.name
        commit_message = commit.commit.message
        commit_type = commit_message.split(':')[0] if ':' in commit_message else 'N/A'
        # 폴더명 추출 (.github 폴더 제외)
        path_elements = file.filename.split('/')
        category = path_elements[0] if len(path_elements) > 1 else 'Root'
        name = path_elements[-1]
        url = file.raw_url
        recent_updates.append([date, category, name, url, author, commit_type])
        count += 1
        if count >= 10:
            break


# "👈 Git commit 컨벤션 확인하기" 섹션이 이미 있는지 확인
if "👈 Git commit 컨벤션 확인하기" not in readme_content:
    # 커밋 유형 설명 토글 추가
    commit_types_table = """
    <details>
    <summary>👈 Git commit 컨벤션 확인하기</summary>
    \n
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
    \n
    </details>
    \n
    """

    # "📝 Recent Work Updates" 섹션 바로 위에 커밋 유형 설명 토글 추가
    readme_content += commit_types_table + "📝 Recent Work Updates\n\n"

# 표 형식으로 README.md에 추가
table_header = "| 날짜 | 분류 | 작업명 | 링크 | 작업자 | Commit 유형 |\n| --- | --- | --- | --- | --- | --- |\n"
table_rows = [f"| {item[0]} | {item[1]} | {item[2]} | [링크]({item[3]}) | {item[4]} | {item[5]} |" for item in recent_updates]
table = table_header + "\n".join(table_rows)

readme_content += table

# README.md 업데이트
repo.update_file(contents.path, "README.md 업데이트: 커밋 컨벤션 토글 및 최근 작업 업데이트", readme_content, contents.sha)

print("README.md has been updated with the Git commit conventions and recent work updates.")
