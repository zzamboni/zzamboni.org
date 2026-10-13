#!/usr/bin/env python3
"""Read historical Netlify logs via an authenticated CLI; write CSV and SVG."""
import argparse
import csv
from datetime import datetime
from html import escape
import json
from pathlib import Path
import re
import subprocess
import sys


def cli(*args):
    return subprocess.check_output(['netlify', *args], text=True)


def timings(log):
    log = re.sub(r'(?:\x1b|\\u001b)\[[0-9;]*m', '', log)

    def duration(pattern):
        matches = re.findall(pattern, log)
        if not matches:
            return None
        units = {'ms': .001, 's': 1, 'm': 60, 'h': 3600}
        parts = re.findall(r'([\d.]+)\s*(ms|s|m|h)', matches[-1])
        return round(sum(float(n) * units[u] for n, u in parts), 3) if parts else None

    total = duration(r'Finished processing build request in ([^\r\n]+)')
    source = 'reported'
    if total is None:
        stamps = [re.search(r'(\d{4}-\d\d-\d\dT[\d:.]+Z)[^\n]*' + marker, log)
                  for marker in ['build-image version:', 'Section completed: cleanup']]
        if all(stamps):
            start, end = [datetime.fromisoformat(m[1]) for m in stamps]
            total = round((end - start).total_seconds(), 3)
        source = 'log timestamps'
    return duration(r'build\.command completed in ([^)]+)'), total, source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', help='Netlify project ID (not deploy ID)')
    parser.add_argument('branch')
    parser.add_argument('--days', type=int, default=90)
    parser.add_argument('--limit', type=int, default=100, help='Maximum deploys examined')
    parser.add_argument('--out', type=Path, default=Path('/tmp/netlify-build-history'))
    args = parser.parse_args()
    if args.days < 1 or args.limit < 1:
        parser.error('--days and --limit must be positive')
    args.out.mkdir(parents=True, exist_ok=True)
    cutoff = datetime.now().timestamp() - args.days * 86400
    rows, examined, page = [], 0, 1
    while examined < args.limit:
        batch = json.loads(cli('api', 'listSiteDeploys', '--data', json.dumps({
            'site_id': args.project, 'branch': args.branch, 'page': page, 'per_page': 100,
        })))
        if not batch:
            break
        for deploy in batch:
            examined += 1
            if examined > args.limit:
                break
            if deploy.get('branch') != args.branch or deploy.get('skipped'):
                continue
            if deploy.get('state') != 'ready' or not deploy.get('build_id'):
                continue
            if datetime.fromisoformat(deploy['created_at']).timestamp() < cutoff:
                continue
            ident = deploy['id']
            print(f'Reading {ident} ({deploy["created_at"]})', file=sys.stderr)
            try:
                log = cli('logs', '--source', 'deploy', '--deploy-id', ident,
                          '--since', f'{args.days}d')
            except subprocess.CalledProcessError:
                print(f'Skipping {ident}: log retrieval failed', file=sys.stderr)
                continue
            (args.out / f'{ident}.log').write_text(log)
            hugo, total, source = timings(log)
            if total is None:
                print(f'Skipping {ident}: no complete build timing in log', file=sys.stderr)
                continue
            rows.append(dict(date=deploy['created_at'], deploy_id=ident,
                             commit=deploy.get('commit_ref', ''), build_command_s=hugo,
                             total_s=total, total_source=source))
        page += 1
    if not rows:
        sys.exit('No complete build logs found. Check project, branch, window, and log availability.')
    rows.sort(key=lambda row: row['date'])
    with (args.out / 'history.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # Standalone SVG avoids plotting dependencies and external chart services.
    times = [datetime.fromisoformat(row['date']).timestamp() for row in rows]
    span = max(times[-1] - times[0], 1)
    ceiling = max(1, max(max(row['total_s'], row['build_command_s'] or 0) for row in rows)) * 1.1
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="460" viewBox="0 0 1000 460">',
           '<rect width="100%" height="100%" fill="white"/>',
           '<g font-family="sans-serif" font-size="13" fill="#333">',
           f'<text x="70" y="25">{escape(args.project)} / {escape(args.branch)} - successful builds</text>']
    for tick in range(6):
        value = ceiling * tick / 5
        y = 370 - 300 * tick / 5
        svg.extend([f'<path d="M70 {y} H960" stroke="#ddd"/>',
                    f'<text x="5" y="{y + 4}">{value:.0f}s</text>'])
    for key, color, label, legend_x in [('total_s', '#167d9a', 'Total (excludes queue)', 70),
                                        ('build_command_s', '#b45309', 'Build command (Hugo)', 360)]:
        svg.append(f'<text x="{legend_x}" y="445" fill="{color}">{label}</text>')
        for timestamp, row in zip(times, rows):
            if row[key] is None:
                continue
            x = 70 + (timestamp - times[0]) / span * 890
            y = 370 - row[key] / ceiling * 300
            title = escape(f'{row["date"]}: {row[key]}s; {row["deploy_id"]}')
            svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"><title>{title}</title></circle>')
    svg.extend([f'<text x="70" y="405">{escape(rows[0]["date"][:10])}</text>',
                f'<text x="960" y="405" text-anchor="end">{escape(rows[-1]["date"][:10])}</text>', '</g></svg>'])
    (args.out / 'history.svg').write_text('\n'.join(svg))
    print(f'Saved {len(rows)} builds to {args.out}/history.csv and history.svg')


if __name__ == '__main__':
    main()
