def print_html():
    print('Content-Type: text/html; charset=utf-8')
    print()

def redirect_to(url):
    print('''Status: 301 Redirect
Location: {url}
Content-Type: text/html

Moved permanently to <a href="{url}">{url}</a>
'''.format(url=url))
