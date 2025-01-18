import git
import matplotlib.pyplot as plt
import os
import json
from collections import Counter
from datetime import datetime

# 配置中文显示
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 使用黑体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

def analyze_commits(repo_url, clone_dir, data_dir):
    # 克隆仓库
    if not os.path.exists(clone_dir):
        repo = git.Repo.clone_from(repo_url, clone_dir)
    else:
        repo = git.Repo(clone_dir)

    # 获取提交历史
    commits = list(repo.iter_commits("main"))  # 获取 main 分支的提交记录，pytest 使用的是 main 分支

    # 分析作者的提交次数
    authors = [commit.author.name for commit in commits]
    author_counts = Counter(authors)

    # 分析每个提交的时间
    commit_times = [datetime.fromtimestamp(commit.committed_date) for commit in commits]

    # 输出提交作者统计
    print("提交作者及其提交次数:")
    for author, count in author_counts.items():
        print(f"{author}: {count} 次")

    # 画出作者提交次数的分布图
    plt.figure(figsize=(10, 6))
    plt.bar(author_counts.keys(), author_counts.values())
    plt.xlabel("作者")
    plt.ylabel("提交次数")
    plt.title("提交作者提交次数分布")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(data_dir, "author_commit_counts.png"))
    plt.show()

    # 画出提交时间分布图
    commit_dates = [commit_time.date() for commit_time in commit_times]
    commit_date_counts = Counter(commit_dates)

    print("提交日期统计:")
    for date, count in commit_date_counts.items():
        print(f"{date}: {count} 次")

    plt.figure(figsize=(10, 6))
    plt.plot(commit_date_counts.keys(), commit_date_counts.values(), marker="o")
    plt.xlabel("日期")
    plt.ylabel("提交次数")
    plt.title("提交时间分布")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(data_dir, "commit_time_distribution.png"))
    plt.show()

    # 将提交信息保存为 JSON 文件
    commit_data = []
    for commit in commits:
        commit_info = {
            "author": commit.author.name,
            "email": commit.author.email,
            "date": datetime.fromtimestamp(commit.committed_date).isoformat(),
            "message": commit.message.strip(),
            "hash": commit.hexsha,
        }
        commit_data.append(commit_info)

    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "commit_info.json"), "w", encoding="utf-8") as f:
        json.dump(commit_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    repo_url = "https://github.com/pytest-dev/pytest.git"  # pytest 仓库地址
    clone_dir = "pytest"  # 克隆到本地的目录
    data_dir = "./data"  # 存储分析结果和图表的目录

    analyze_commits(repo_url, clone_dir, data_dir)
