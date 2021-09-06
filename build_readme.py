from python_graphql_client import GraphqlClient
import feedparser
import httpx
import json
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()
client = GraphqlClient(endpoint="https://api.github.com/graphql")

# 获取 token
TOKEN = os.environ.get("SIMONW_TOKEN", "")


def replace_chunk(content, marker, chunk):
    return "\n{}\n".format(chunk)

def fetch_blog_entries():
    entries = feedparser.parse("https://www.jonsam.site/feed")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["links"][0]["href"],
            "published": entry["published"].split("+")[0],
        }
        for entry in entries
    ]


if __name__ == "__main__":
    readme = root / "articles.md"

    entries = fetch_blog_entries()[:10]
    # print(entries)
    entries_md = "\n\n".join(
        ["- [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    # print(entries_md)
    rewritten = replace_chunk('', "blog", entries_md)
    print(rewritten)

    readme.open("w").write("# My recent blogs ")
    readme.open("a").write(rewritten)
