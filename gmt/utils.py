import html


def clean_html(html_string):
    return (
        html.escape(html_string, quote=False)
        .replace("<script>", "&lt;script&gt;")
        .replace("</script>", "&lt;/script&gt;")
        .replace("<style>", "&lt;style&gt;")
        .replace("</style>", "&lt;/style&gt;")
    )
