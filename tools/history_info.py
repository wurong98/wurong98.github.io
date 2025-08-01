# -*- coding: utf-8 -*-
# !/usr/bin/env python3

"""
在 _posts目录下找所有的markdown文件。将文件头的 tags 和 categories 展示出来 方便我复制
"""

import os
import yaml

def extract_front_matter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if lines[0].strip() != '---':
        return None

    # 找到 YAML front matter 的结束位置
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end = i
            break

    if end is None:
        return None

    front_matter = ''.join(lines[1:end])
    try:
        return yaml.safe_load(front_matter)
    except yaml.YAMLError as e:
        print(f"YAML解析错误: {filepath}")
        return None

def main():
    posts_dir = os.path.join(os.path.dirname(__file__) , "../_posts")
    all_categories = set()
    all_tags = set()

    for root, dirs, files in os.walk(posts_dir):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                front = extract_front_matter(filepath)
                if front:
                    cats = front.get('categories', [])
                    tags = front.get('tags', [])
                    if isinstance(cats, str):
                        cats = [cats]
                    if isinstance(tags, str):
                        tags = [tags]
                    all_categories.update(cats)
                    all_tags.update(tags)

    print("=================================categories===============================")
    for cat in sorted(all_categories):
        print(f"{cat}")

    print("=================================tags=====================================")
    for tag in sorted(all_tags):
        print(f"{tag}")

    print("==========================================================================")

if __name__ == '__main__':
    main()
