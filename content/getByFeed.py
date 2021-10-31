import requests
import xmltodict
from os import listdir, path
import re
from markdownify import markdownify, ATX
from textwrap import dedent

feed_URL = "https://anchor.fm/s/9789fe8/podcast/rss"
response = requests.get(feed_URL)
parsed_content = xmltodict.parse(response.content)
podcast_content = parsed_content["rss"]["channel"]["item"]

html_tags = re.compile("<.*?>")


def string_parser(string):
    return (
        string.lower()
        .replace(".net", "dot_net")
        .replace(" ", "_")
        .replace("ç", "c")
        .replace("á", "a")
        .replace("ã", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("õ", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace("ü", "u")
        .replace(".", "_")
        .replace("-", "")
        .replace("/", "_")
        .replace("!", "")
        .replace("?", "")
        .replace("(", "")
        .replace(")", "")
        .replace("[", "")
        .replace("]", "")
        .replace("{", "")
        .replace("}", "")
        .replace("=", "_igual")
        .replace("+", "")
        .replace("*", "")
        .replace("&", "e")
        .replace("#", "_cerquilha")
        .replace("$", "")
        .replace("%", "_por_cento")
        .replace("'", "")
        .replace(",", "_e")
        .replace(":", "")
    )


def parse_description(string):
    description = re.sub(html_tags, "", string)
    return (
        description.replace("\n", " ")
        .replace("<p>", "")
        .replace("</p>", "")
        .replace("<br />", "")
        .strip()
    )[0:150].split("▸")[0] + "..."


def parse_content_to_markdown(string):
    return markdownify(string)


for item in podcast_content:
    podcast_file = string_parser(item["title"]) + ".md"

    if path.isfile("podcast/" + podcast_file):
        print("File already exists: " + podcast_file)
    else:
        with open("podcast/" + podcast_file, "w") as f:
            content = dedent(
                "---\n"
                + 'title: "'
                + item["title"]
                + '"\n'
                + 'description: "'
                + parse_description(item["description"])
                + '"\n'
                + 'date: "'
                + item["pubDate"]
                + '"\n'
                + 'audio: "'
                + item["enclosure"]["@url"]
                + '"\n'
                + "---\n"
                + "\n"
                + parse_content_to_markdown(item["description"])
            )
            f.write(content)
            f.close()
            print("File created:" + podcast_file)
