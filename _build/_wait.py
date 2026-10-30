# -*- coding: utf-8 -*-
"""等待 Pages 构建并验证线上页面"""
import subprocess, json, urllib.request, ssl, time, re

tok = next((l[9:] for l in subprocess.run(['git', 'credential', 'fill'],
        input='protocol=https\nhost=github.com\n\n', capture_output=True, text=True
        ).stdout.splitlines() if l.startswith('password=')), '')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def api(path):
    req = urllib.request.Request('https://api.github.com' + path, headers={
        'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json',
        'User-Agent': 'wb-deploy'})
    try:
        with urllib.request.urlopen(req, timeout=40, context=ctx) as r:
            return r.status, json.loads(r.read().decode() or '{}')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]
    except Exception as e:
        return None, str(e)[:200]


for i in range(26):
    code, b = api('/repos/luofeicq/kb-site/pages/builds/latest')
    if isinstance(b, dict):
        st, cm = b.get('status'), (b.get('commit') or '')[:7]
        print('第 %2d 次  %s  %s' % (i + 1, st, cm))
        if st == 'built' and cm.startswith('783e5dd'):
            print('  耗时 %s ms' % b.get('duration'))
            break
        if st == 'errored':
            print('  错误:', b.get('error'))
            break
    else:
        print('查询失败', code, b)
    time.sleep(8)
