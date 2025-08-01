# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import os
from datetime import datetime

# 模板内容
template = '''---
title: "请填写标题"
author: "wurong"
date: "{date}"
categories: "请填写分类"
tags: []
math: true # 是否启用数学公式支持
---
'''

def get_next_post_filename(posts_dir, date_prefix):
    existing_ids = []
    for filename in os.listdir(posts_dir):
        if filename.startswith(date_prefix) and filename.endswith('.md'):
            parts = filename.replace('.md', '').split('-p')
            if len(parts) == 2 and parts[1].isdigit():
                existing_ids.append(int(parts[1]))
    next_id = max(existing_ids + [0]) + 1
    return f"{date_prefix}-p{next_id}.md"

def create_new_post():
    posts_dir = os.path.join(os.path.dirname(__file__) , "../_posts")
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    filename = get_next_post_filename(posts_dir, date_prefix)
    filepath = os.path.join(posts_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template.format(date=now_str))

    print(f"已创建: {filepath}")

if __name__ == "__main__":
    create_new_post()