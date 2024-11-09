from ...user_functions import extract_keywords_from

# def render_deveno3(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
#     """
#     >>> render_deveno3("deveno3", ["eo", "egy", "Aa"], defaultdict(str, {"sg": "granda"}))
#     'la egipta antikva vorto " <b>Aa</b> " <sup>→ egy</sup> (= granda)'
#     >>> render_deveno3("deveno3", ["eo", "egy", "Aa"], defaultdict(str, {"sg": "-"}))
#     'la egipta antikva vorto " <b>Aa</b> " <sup>→ egy</sup>'
#     >>> render_deveno3("deveno3", ["en", "ang", "bridd"], defaultdict(str))
#     'la anglosaksa vorto " <b>bridd</b> " <sup>→ ang</sup>'
#     """
#     parts.pop(0)  # Remove the source lang
#     lang = parts.pop(0)
#     phrase = f'la {langs[lang]} vorto " {strong(parts.pop(0))} "'
#     if lang != "grc":
#         phrase += f" {superscript('→ ' + lang)}"
#     if (sg := data["sg"]) not in {"", "-"}:
#         phrase += f" (= {sg})"
#     return phrase


template_mapping = {
    # "deveno3": render_deveno3,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
