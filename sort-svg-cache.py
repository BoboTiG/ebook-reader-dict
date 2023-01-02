from wikidict import svg_cache


with open(svg_cache.__file__, mode="w") as fh:
    fh.write("CACHE = {\n")
    for k, v in sorted(set(svg_cache.CACHE.items())):
        fh.write(f"    {k!r}: {v!r},\n")
    fh.write("}\n")
