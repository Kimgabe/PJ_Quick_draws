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
unique_updates = {}

for commit in commits:
    files = commit.files
    for file in files:
        if ".DS_Store" in file.filename or file.filename.endswith("README.md"):
            continue
        file_key = (file.filename, commit.commit.author.name)  # 파일명과 작업자 이름을 키로 사용
        if file_key not in unique_updates:
            unique_updates[file_key] = commit
        else:
            # 이미 저장된 커밋과 날짜를 비교하여 더 최신 커밋으로 업데이트
            existing_commit_date = unique_updates[file_key].commit.author.date
            current_commit_date = commit.commit.author.date
            if current_commit_date > existing_commit_date:
                unique_updates[file_key] = commit

# 최근 업데이트 정보를 표 형식으로 추가
table_header = "| 날짜 | 분류 | 작업명 | 링크 | 작업자 | Commit 유형 |\n| --- | --- | --- | --- | --- | --- |\n"
table_rows = [f"| {v[0]} | {v[1]} | {v[2]} | [View]({v[3]}) | {v[4]} | {v[5]} |" for v in unique_updates.values()]
table = table_header + "\n".join(table_rows)
readme_content += table

# README.md 업데이트
commit_message = "Docs : README.md 업데이트: 커밋 컨벤션 토글 및 최근 작업 업데이트"
repo.update_file(contents.path, commit_message, readme_content, contents.sha)

print("README.md가 성공적으로 업데이트되었습니다.")
