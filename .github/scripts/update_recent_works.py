import os
from github import Github

# GitHub 설정
g = Github(os.getenv('GITHUB_TOKEN'))
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

# README.md 파일 가져오기
contents = repo.get_contents("README.md")
readme_content = contents.decoded_content.decode("utf-8")

# "📝 Recent Work Updates" 섹션 찾기 및 기존 표 제거
if "📝 Recent Work Updates" in readme_content:
    # 기존 표가 있다면 제거
    readme_content = readme_content.split("📝 Recent Work Updates")[0] + "📝 Recent Work Updates\n\n"

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
        # 파일 정보 추출
        date = commit.commit.author.date.strftime("%Y-%m-%d")
        # 폴더명 추출 (.github 폴더 제외)
        path_elements = file.filename.split('/')
        category = path_elements[0] if len(path_elements) > 1 else 'Root'
        name = path_elements[-1]
        url = file.raw_url
        description = commit.commit.message
        recent_updates.append([date, category, name, url, description])
        count += 1
        if count >= 10:
            break

# 표 형식으로 README.md에 추가
table_header = "| 날짜 | 분류 | 작업명 | 링크 | 설명 |\n| --- | --- | --- | --- | --- |\n"
table_rows = [f"| {item[0]} | {item[1]} | {item[2]} | [링크]({item[3]}) | {item[4]} |" for item in recent_updates]
table = table_header + "\n".join(table_rows)

readme_content += table

# README.md 업데이트
repo.update_file(contents.path, "README.md 업데이트: 최근 작업 업데이트 테이블 추가", readme_content, contents.sha)

print("README.md has been updated with recent work updates.")
