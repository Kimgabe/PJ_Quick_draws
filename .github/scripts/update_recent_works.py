import os
from github import Github
from datetime import datetime

# GitHub 설정
g = Github(os.getenv('GITHUB_TOKEN'))  # GitHub API 토큰을 사용하여 Github 인스턴스 생성
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))  # 환경 변수에서 저장소 이름을 가져와 저장소 객체를 얻음

# README.md 파일 가져오기
contents = repo.get_contents("README.md")  # README.md 파일의 내용을 가져옴
readme_content = contents.decoded_content.decode("utf-8")  # README.md 파일의 내용을 문자열로 디코딩

# "👈 Git commit 컨벤션 확인하기" 섹션이 이미 있는지 확인
if "👈 Git commit 컨벤션 확인하기" not in readme_content:
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
    readme_content += commit_types_table  # 커밋 유형 설명을 README 내용에 추가

# "📝 Recent Work Updates" 섹션 찾기 및 기존 표 제거
if "📝 Recent Work Updates" in readme_content:
    # 기존 표가 있다면 제거하고 섹션 제목만 남김
    readme_content = readme_content.split("📝 Recent Work Updates")[0] + "## 📝 Recent Work Updates\n\n"
else:
    # 섹션 제목 추가
    readme_content += "\n\n## 📝 Recent Work Updates\n\n"

# 커밋 로그에서 최근 10개의 항목 가져오기 (.github 폴더 및 README.md 제외)
commits = repo.get_commits()  # 저장소의 커밋 목록을 가져옴
recent_updates = []  # 최근 업데이트 정보를 저장할 리스트
count = 0  # 처리된 커밋 수를 세기 위한 카운터

for commit in commits:
    if count >= 10:
        break
    files = commit.files
    for file in files:
        if file.filename.endswith("README.md") or file.filename.startswith(".github/"):
            continue
        date = commit.commit.author.date.strftime("%Y-%m-%d")
        author = commit.commit.author.name
        commit_message = commit.commit.message.split('\n')[0]  # 커밋 메시지의 첫 줄만 사용
        commit_type = commit_message.split(':')[0] if ':' in commit_message else 'N/A'
        path_elements = file.filename.split('/')
        category = path_elements[0] if len(path_elements) > 1 else 'Root'
        name = path_elements[-1]
        url = file.raw_url
        recent_updates.append(f"| {date} | {category} | {name} | [View]({url}) | {author} | {commit_type} |")  # 줄바꿈을 공백으로 대체하여 추가
        count += 1
        if count >= 10:
            break

# 표 형식으로 README.md에 최근 업데이트 정보 추가
if recent_updates:  # 최근 업데이트가 있으면 표를 추가
    table_header = "| 날짜 | 분류 | 작업명 | 링크 | 작업자 | Commit 유형 |\n| --- | --- | --- | --- | --- | --- |\n"
    table = table_header + "\n".join(recent_updates)
    readme_content += table  # 테이블 내용을 README 내용에 추가

# README.md 업데이트
commit_message = "Docs : README.md 업데이트: 커밋 컨벤션 토글 및 최근 작업 업데이트"
repo.update_file(contents.path, commit_message, readme_content, contents.sha)

print("README.md가 성공적으로 업데이트되었습니다.")
