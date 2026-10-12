import os
import re
import json

DOCS_DIR = 'docs'
OUTPUT_FILE = 'manifest.json'

def natural_sort_key(s):
    """문자열 내의 숫자를 실제 크기로 정렬하는 키 함수 (0-A-2가 0-A-10보다 앞에 오도록 처리)"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def build_manifest():
    if not os.path.exists(DOCS_DIR):
        print(f"'{DOCS_DIR}' 폴더를 찾을 수 없습니다.")
        return

    md_files = []
    # docs/ 하위 모든 폴더를 탐색
    for root, _, files in os.walk(DOCS_DIR):
        for f in files:
            if f.endswith('.md'):
                full_path = os.path.join(root, f).replace('\\', '/')
                md_files.append((f, full_path))

    # 자연 정렬 적용
    md_files.sort(key=lambda item: natural_sort_key(item[0]))

    manifest = []
    for filename, filepath in md_files:
        name_without_ext = os.path.splitext(filename)[0]

        # 1. id 추출: 파일명 앞단의 '0-A-1' 형태 추출 (일치하지 않으면 파일명 전체 사용)
        id_match = re.match(r'^([0-9A-Za-z\-]+)', name_without_ext)
        file_id = id_match.group(1) if id_match else name_without_ext

        # 2. 제목 추출: 파일 내부 첫 '# 제목' 우선 탐색, 없으면 파일명 사용
        title = name_without_ext
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'^#\s+(.+)$', line.strip())
                    if m:
                        title = m.group(1).strip()
                        break
        except Exception as e:
            print(f"파일 읽기 오류 ({filepath}): {e}")

        manifest.append({
            "id": file_id,
            "title": title,
            "file": filepath
        })

    # manifest.json 저장
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"manifest.json 갱신 완료: 총 {len(manifest)}개 문서")

if __name__ == '__main__':
    build_manifest()
