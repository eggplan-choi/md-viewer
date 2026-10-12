import os
import re
import json

CHAPTERS_DIR = 'chapters'  # 챕터 파일 폴더 경로
OUTPUT_FILE = 'manifest.json'

def build_manifest():
    if not os.path.exists(CHAPTERS_DIR):
        return

    # 파일 확장자 필터링 및 이름 순 정렬
    files = sorted([f for f in os.listdir(CHAPTERS_DIR) if f.endswith(('.md', '.html'))])
    manifest = []

    for filename in files:
        filepath = os.path.join(CHAPTERS_DIR, filename)
        file_id = os.path.splitext(filename)[0]
        title = file_id  # 기본값: 파일명

        # 마크다운 첫 머리의 '# 제목' 탐색
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                m = re.match(r'^#\s+(.+)$', line.strip())
                if m:
                    title = m.group(1).strip()
                    break

        manifest.append({
            "id": file_id,
            "title": title,
            "file": f"{CHAPTERS_DIR}/{filename}"
        })

    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    build_manifest()
