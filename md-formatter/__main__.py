import importlib
import os

import markdown
from bs4 import BeautifulSoup
from rpu.cli import ConsoleClient

client = ConsoleClient()

to_index = []
COLORS = [
    "aliceblue",
    "antiquewhite",
    "aqua",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanchedalmond",
    "blue",
    "blueviolet",
    "brown",
    "burlywood",
    "cadetblue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflowerblue",
    "cornsilk",
    "crimson",
    "cyan",
    "darkblue",
    "darkcyan",
    "darkgoldenrod",
    "darkgray",
    "darkgreen",
    "darkgrey",
    "darkkhaki",
    "darkmagenta",
    "darkolivegreen",
    "darkorange",
    "darkorchid",
    "darkred",
    "darksalmon",
    "darkseagreen",
    "darkslateblue",
    "darkslategray",
    "darkslategrey",
    "darkturquoise",
    "darkviolet",
    "deeppink",
    "deepskyblue",
    "dimgray",
    "dimgrey",
    "dodgerblue",
    "firebrick",
    "floralwhite",
    "forestgreen",
    "fuchsia",
    "gainsboro",
    "ghostwhite",
    "gold",
    "goldenrod",
    "gray",
    "green",
    "greenyellow",
    "grey",
    "honeydew",
    "hotpink",
    "indianred",
    "indigo",
    "ivory",
    "khaki",
    "lavender",
    "lavenderblush",
    "lawngreen",
    "lemonchiffon",
    "lightblue",
    "lightcoral",
    "lightcyan",
    "lightgoldenrodyellow",
    "lightgray",
    "lightgreen",
    "lightgrey",
    "lightpink",
    "lightsalmon",
    "lightseagreen",
    "lightskyblue",
    "lightslategray",
    "lightslategrey",
    "lightsteelblue",
    "lightyellow",
    "lime",
    "limegreen",
    "linen",
    "magenta",
    "maroon",
    "mediumaquamarine",
    "mediumblue",
    "mediumorchid",
    "mediumpurple",
    "mediumseagreen",
    "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise",
    "mediumvioletred",
    "midnightblue",
    "mintcream",
    "mistyrose",
    "moccasin",
    "navajowhite",
    "navy",
    "oldlace",
    "olive",
    "olivedrab",
    "orange",
    "orangered",
    "orchid",
    "palegoldenrod",
    "palegreen",
    "paleturquoise",
    "palevioletred",
    "papayawhip",
    "peachpuff",
    "peru",
    "pink",
    "plum",
    "powderblue",
    "purple",
    "rebeccapurple",
    "red",
    "rosybrown",
    "royalblue",
    "saddlebrown",
    "salmon",
    "sandybrown",
    "seagreen",
    "seashell",
    "sienna",
    "silver",
    "skyblue",
    "slateblue",
    "slategray",
    "slategrey",
    "snow",
    "springgreen",
    "steelblue",
    "tan",
    "teal",
    "thistle",
    "tomato",
    "turquoise",
    "violet",
    "wheat",
    "white",
    "whitesmoke",
    "yellow",
    "yellowgreen",
]
DEFAULT_HTML_CODE = """<html>

<head>
    <title>{TITLE}</title>
    <style>
        body {
            margin: 0;
            padding: 0;
        }

        a {
            color: lightblue;
            text-decoration: none;
        }

        .nr {
            color: inherit;
        }

        .index {
            float: left;
            background-color: rgb(68, 66, 66);
            width: 20%;
            height: 100%;
            max-height: 100%;
            overflow-x: hidden;
            overflow-y: auto;
        }

        .title {
            text-align: center;
            color: white;
        }

        .container {
            max-height: 100%;
            overflow-x: hidden;
            overflow-y: auto;
        }

        .contents {
            margin-left: 5vw;
            margin-right: 5vw;
        }

        .index-contents {
            margin-left: 10%;
            line-height: 12px;
        }

        .index-item-1 {
            margin-left: 0%;
        }

        .index-item-2 {
            margin-left: 10%;
        }

        .index-item-3 {
            margin-left: 20%;
        }

        .index-item-4 {
            margin-left: 30%;
        }

        .index-item-5 {
            margin-left: 40%;
        }

        .index-item-6 {
            margin-left: 50%;
        }

        .footer {
            background-color: black;
            width: 100%;
            text-align: right;
            color: white;
            min-height: 0.5vw;
        }

        .htag-u:hover {
            text-decoration: underline;
        }
    </style>
</head>

<body>
    <div class="index">
        <div class="title">
            <h1>{TITLE}</h1>
        </div>
        <hr><br>
        <div class="index-contents">
            {INDEX-HERE}
        </div>
    </div>
    <div class="container" id="cc">
        <div class="contents">
            {CONTENTS-HERE}
        </div>
    </div>
</body>

</html>"""


def add_colors(txt: str) -> str:
    for color in COLORS:
        txt = txt.replace(f"[{color}| ", f'<span style="color: {color};">')
        txt = txt.replace(f" |{color}]", "</span>")

    return txt


def convert_file(filename: str, dont_index_tags) -> tuple[str, list[dict]]:
    with open(filename, "r") as f:
        text = f.read()

    translated = markdown.markdown(text)
    to_parse = BeautifulSoup(translated, "html.parser")

    # finding all h# tags

    found_h_tags = to_parse.find_all([f"h{i + 1}" for i in range(6)])

    for tag in found_h_tags:
        type_ = str(tag).split(">")[0].replace("<h", "")
        txt = tag.text
        cleanname = tag.text
        data = {}
        for color in COLORS:
            txt = txt.replace(f"[{color}| ", "")
            txt = txt.replace(f" |{color}]", "")
        if "{id:" in txt:
            raw = txt.split("{id:")
            raw.pop(0)
            x = "".join(raw)
            txt = x.split("}")[0]

            cleanname = tag.text.replace("{id:x}".replace("x", txt), "")

        if type_ not in dont_index_tags:
            data["type"] = type_
            data["inner"] = txt
            data["raw"] = tag.text
            data["name"] = cleanname
            to_index.append(data)

    after_parse = str(to_parse)
    return after_parse, to_index


@client.command(
    description="The main command to parse markdown files.\nFor configuration, create a `settings.config.py` file and use that.",
    brief="the main command",
)
def parse(*files: str):
    if not os.path.isfile("md_configuration.py"):
        print("No config file found\n")
        title = input("What will the title be?\n> ")
        print("Creating configuration with defaults...")
        underline_h_tags = True
        dont_index_tags = []
        dont_indent_tags = []
        print("Done creating configuration, working on files now...")
    else:
        print("Config file found")
        CONFIG = importlib.import_module("md_configuration")
        title = CONFIG.title

        if hasattr(CONFIG, "underline_h_tags"):
            underline_h_tags = CONFIG.underline_h_tags
        else:
            underline_h_tags = True

        if hasattr(CONFIG, "dont_index_tags"):
            dont_index_tags = CONFIG.dont_index_tags
        else:
            dont_index_tags = []

        if hasattr(CONFIG, "dont_indent_tags"):
            dont_indent_tags = CONFIG.dont_indent_tags
        else:
            dont_indent_tags = []

        print("Configuration done. working on files now...")

    H_TAG = """
    <div class="index-item-{type_}">
        <h{type_} id='{name}' class="htag">
            <a href="#{name}" class="nr">
                {inner}
            </a>
        </h{type_}>
    </div>
    <div class="index-item-{type_}">
    """

    if underline_h_tags:
        H_TAG = H_TAG.replace('class="htag"', 'class="htag-u"')

    temp = []
    to_index = []
    for fp in files:
        data, toindex = convert_file(fp, dont_index_tags)
        to_index.extend(toindex)
        temp.append(data)
        print(f"Finished converting {fp} to html")
    after_parse = "\n\n\n".join(temp)

    template = DEFAULT_HTML_CODE.replace("{TITLE}", title)
    print("Got template")

    # using h# tags to build the index

    template = template.replace(
        "{INDEX-HERE}",
        "\n".join(
            [
                f"<a href='#{tag['inner'].replace(' ', '_')}' class='index-item-{tag['type']}'>{tag['inner']}</a><br><br>"
                for tag in to_index
            ]
        ),
    )
    print("Created index")

    foo = False
    for tag in to_index:
        format_ = H_TAG.format(
            type_=tag["type"],
            name=tag["inner"].replace(" ", "_"),
            inner=add_colors(tag["name"]),
        )

        if foo:
            format_ = "</div>\n" + format_
        else:
            foo = True
        if int(tag["type"]) in dont_indent_tags:
            format_ = format_.replace(f'<div class="index-item-{tag["type"]}">', "")
            format_ = format_.replace("</div>", "")

        after_parse = after_parse.replace(
            f"<h{tag['type']}>{tag['raw']}</h{tag['type']}>", format_
        )
        print(f"Formatted: '{tag['name']}'")

    # adding special formatting

    after_parse = after_parse.replace("{/newline}", "[[{{nl}}]]")
    after_parse = after_parse.replace("{newline}", "<br>")
    after_parse = after_parse.replace("[[{{nl}}]]", "{newline}")

    after_parse = after_parse.replace("/[\\", "{{{{{{{{\\}}}}}}}}")
    after_parse = after_parse.replace("/]\\", "{{{{{{{{/}}}}}}}}")

    after_parse = after_parse.replace("[\\ ", '<div style="margin-left: 5%">')
    after_parse = after_parse.replace(" /]", "</div>")

    after_parse = after_parse.replace("{{{{{{{{\\}}}}}}}}", "[\\ ")
    after_parse = after_parse.replace("{{{{{{{{/}}}}}}}}", " /]")

    after_parse = add_colors(after_parse)

    print("Added special formating")

    # putting the md file(s) into the template

    final = template.replace("{CONTENTS-HERE}", after_parse)
    print("Put contents in template")
    final_txt = BeautifulSoup(final, "html.parser")

    with open("result.html", "w") as t:
        t.write(final_txt.prettify())

    print("\nDone. Saved file to `result.html`")


@client.command(
    name="generate-config",
    description="generates a configuration",
    brief="generates a configuration",
)
def cmd_gen_config():
    title = input("What should the title be?\n> ")
    underline_h_tags = input(
        "Should header tags be underlined when you hover over them? [y/n]\n> "
    )
    dont_index_tags = input(
        "What header tags should I not index? Give a list of numbers seperated by commas. Ex: `2,3,5`\n> "
    )
    dont_indent_tags = input(
        "What header tags should I not indent? Give a list of numbers seperated by commas. Ex: `2,3,5`\n> "
    )

    underline_h_tags = {"y": True, "n": False}.get(underline_h_tags[0])
    if underline_h_tags is not None:
        print(f"Good input for underline_h_tags, converted to {underline_h_tags}.")
    else:
        print(f"{underline_h_tags} is not `y` or `n`. Defaulting to `yes/True`")
        underline_h_tags = True

    if dont_index_tags:
        dont_index_tags = dont_index_tags.split(",")
        try:
            dont_index_tags = [int(tag.strip()) for tag in dont_index_tags]
        except (KeyError, ValueError):
            return print(f"Invalid input given for 'dont_index_tags'.")
    else:
        dont_index_tags = []

    if dont_indent_tags:
        dont_indent_tags = dont_indent_tags.split(",")
        try:
            dont_indent_tags = [int(tag.strip()) for tag in dont_indent_tags]
        except (KeyError, ValueError):
            return print(f"Invalid input given for 'dont_indent_tag'.")
    else:
        dont_indent_tags = []

    print("Inputs validated, generating code")

    code = f"""
title = "{title}"
underline_h_tags = {underline_h_tags}
dont_index_tags = {dont_index_tags}
dont_indent_tags = {dont_indent_tags}
"""

    print("Code generated, writing to file")

    with open("md_configuration.py", "w") as f:
        f.write(code)

    print("Done. config saved to `md_configuration.py`")


if __name__ == "__main__":
    client.run()
