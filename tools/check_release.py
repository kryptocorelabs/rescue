"""Validate public documentation and, optionally, the published preview archive."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile
import urllib.request
import zipfile

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--download',action='store_true')
args=parser.parse_args()
manifest=json.loads((root/'RELEASE_MANIFEST.json').read_text(encoding='utf-8'))
for key in ('executable_sha256','archive_sha256'):
    assert re.fullmatch('[0-9a-f]{64}',manifest[key]), key
assert re.fullmatch('[0-9a-f]{40}',manifest['source_commit'])
for key in ('executable','archive'):
    assert Path(manifest[key]).name==manifest[key] and '/' not in manifest[key] and '\\' not in manifest[key]
assert manifest['authenticode_signed'] is False
assert manifest['independent_audit'] is False
assert manifest['binary_reproducible'] is False
checks=(root/'SHA256SUMS.txt').read_text(encoding='ascii')
assert manifest['archive_sha256']+'  '+manifest['archive'] in checks
assert manifest['executable_sha256']+'  '+manifest['executable'] in checks
for markdown in root.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)|(?:src="([^"]+)")',markdown.read_text(encoding='utf-8')):
        path=target[0] or target[1]
        if '://' not in path and not path.startswith('#'):
            local=(root/path.split('#')[0]).resolve()
            assert local.is_relative_to(root) and local.exists(),(markdown.name,path)
assert (root/'third-party').is_dir()
for notice in (root/'third-party').rglob('*'):
    if notice.is_file():assert notice.stat().st_size>0,'Empty upstream notice: '+str(notice)
if args.download:
    product=manifest['application'].removeprefix('KryptoCore ').lower()
    assert product in ('msg','rescue','container')
    url='https://github.com/kryptocorelabs/'+product+'/releases/download/v'+manifest['version']+'/'+manifest['archive']
    with tempfile.TemporaryDirectory() as temp:
        archive=Path(temp)/manifest['archive']
        total=0; digest=hashlib.sha256()
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'KryptoCore-release-check'}),timeout=60) as response, archive.open('wb') as out:
            while chunk:=response.read(1024*1024):
                total+=len(chunk)
                assert total<=512*1024*1024,'Archive exceeds preview download bound'
                digest.update(chunk);out.write(chunk)
        assert digest.hexdigest()==manifest['archive_sha256'],'Archive checksum mismatch'
        with zipfile.ZipFile(archive) as package:
            matches=[entry for entry in package.infolist() if Path(entry.filename).name==manifest['executable']]
            assert len(matches)==1 and matches[0].file_size<=256*1024*1024
            digest=hashlib.sha256()
            with package.open(matches[0]) as file:
                while chunk:=file.read(1024*1024):digest.update(chunk)
            assert digest.hexdigest()==manifest['executable_sha256'],'Embedded executable checksum mismatch'
            assert any(entry.filename.endswith('/THIRD_PARTY_NOTICES.md') for entry in package.infolist())
            assert any('/third-party/' in entry.filename for entry in package.infolist())
            for entry in package.infolist():
                if '/third-party/' in entry.filename and not entry.is_dir():
                    assert entry.file_size>0,'Empty packaged upstream notice: '+entry.filename
    print('Published archive, embedded executable and notice presence verified.')
print('Release manifest, checksums and local documentation links passed.')
