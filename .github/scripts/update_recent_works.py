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
    # 커밋 유형 설명 토글 추가
    # 여기 커밋 유형 설명은 위에서 이미 제공했으므로 생략

# "📝 Recent Work Updates" 섹션 찾기 및 기존 표 제거
if "📝 Recent Work Updates" in readme_content:
    readme_content = readme_content.split("📝 Recent Work Updates")[0] + "## 📝 Recent Work Updates\n\n"
else:
    readme_content += "\n\n## 📝 Recent Work Updates\n\n"

# 커밋 로그에서 최근 항목 가져오기 (.github 폴더, README.md, .DS_Store 제외)
commits = repo.get_commits()
unique_updates = {}  # 작업명을 키로 하고, 가장 최신의 커밋 정보를 값으로 하는 딕셔너리

for commit in commits:
    if len(unique_updates) >= 10:
        break
    files = commit.files
    for file in files:
        if file.filename.endswith(("README.md", ".DS_Store")) or file.filename.startswith(".github/"):
            continue
        name = file.filename.split('/')[-1]  # 파일명만 추출
        if name not in unique_updates:  # 동일한 작업명의 커밋이 아직 없으면 추가
            date = commit.commit.author.date.strftime("%Y-%m-%d")
            author = commit.commit.author.name
            commit_message = commit.commit.message.split('\n')[0]
            commit_type = commit_message.split(':')[0] if ':' in commit_message else 'N/A'
            category = file.filename.split('/')[0] if '/' in file.filename else 'Root'
            url = file.raw_url
            unique_updates[name] = [date, category, name, url, author, commit_type]

# 최근 업데이트 정보를 표 형식으로 추가
table_header = "| 날짜 | 분류 | 작업명 | 링크 | 작업자 | Commit 유형 |\n| --- | --- | --- | --- | --- | --- |\n"
table_rows = [f"| {v[0]} | {v[1]} | {v[2]} | [View]({v[3]}) | {v[4]} | {v[5]} |" for v in unique_updates.values()]
table = table_header + "\n".join(table_rows)
readme_content += table

# README.md 업데이트
commit_message = "Docs : README.md 업데이트: 커밋 컨벤션 토글 및 최근 작업 업데이트"
repo.update_file(contents.path, commit_message, readme_content, contents.sha)

print("README.md가 성공적으로 업데이트되었습니다.")
