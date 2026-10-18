from pathlib import Path
import hashlib,json,re,csv,xml.etree.ElementTree as ET,collections
ROOT=Path(__file__).parent;DOC=ROOT.parent/'docs/research/legacy-launcher'
def append(n,s):
 p=DOC/n;p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n'+s.strip()+'\n',encoding='utf-8')
append('UPDATE-AND-RECOVERY.md','''## Additional path/configuration traces [E12/E13]

Installed MinecraftLauncher.unpackNatives directly combines the native directory with ZipEntry.getName (offsets337–340) and opens the resulting path for output (387). Its decoded direct path has directory/META-INF filtering but no demonstrated canonical-child containment check. Reachability of attacker-controlled archives and exploit impact were not established; this is not a confirmed vulnerability. Independent extraction should reject absolute/traversal/link escapes, and blocked guest tests should exercise synthetic ZIP names within a disposable environment. Do not copy this extraction pattern as a safety contract.

Configuration.init extracts argument configuration entries (35), tracks constant argument values (333), parses configuration representations (376) and attempts a save (722) with an I/O error handler. This confirms command-line/config interaction and persistence branches; actual precedence for every setting remains an observation target for W08, rather than a fabricated universal ordering.
''')
append('JVM-RUNTIME.md','''## Archived build classfile baseline [E13]

Static ZIP inspection finds classfile major52 (Java8-era format) in all964 archived launcher-namespace classes and183 archived bootstrap-namespace classes. The archived bootstrap manifest selects ru.turikhay.tlauncher.bootstrap.BootstrapStarter. Classfile format establishes a bytecode baseline, not a proof that all runtime/library/API requirements are Java8-only. Keep this distinct from installed launcher11+ metadata, bundled Java17, and selected game's Java21 requirement.
''')
# Explicitly label first-pass-only coverage statements where continuation supersedes them.
p=DOC/'EVIDENCE-INDEX.md';s=p.read_text(encoding='utf-8');s=s.replace('- No new target execution, installer extraction, live authentication, official component download, console test, or comprehensive third-party license review.','- First-pass boundary: no target execution, installer extraction, live authentication, official component download, console test, or comprehensive third-party license review. Continuation E11 later performs nonexecuting installer recovery.');p.write_text(s,encoding='utf-8')
p=DOC/'NATIVE-DEPENDENCIES.md';s=p.read_text(encoding='utf-8').replace('glfwExtensionSupported3978','glfwExtensionSupported3979').replace('glfwGetWin32Window4122','glfwGetWin32Window4123');p.write_text(s,encoding='utf-8')
# Improve number/prose spacing without changing code blocks, identifiers, hashes or URLs.
words=['all','All','Total','total','allotted','of','and','at','with','expects','offset','offsets','stored','decoded','produced','bytes','records','record','launcher','bootstrap','Java','Windows','DLLs','images','path','classes','methods','level','Phase','flags','version','versioning']
for p in DOC.glob('*.md'):
 s=p.read_text(encoding='utf-8');in_code=False;lines=[]
 for line in s.splitlines():
  if line.startswith('```'):in_code=not in_code;lines.append(line);continue
  if not in_code:
   # Avoid link targets and inline identifier/code spans. Format prose fragments only.
   chunks=re.split(r'(`[^`]*`|https?://\S+)',line)
   for i,c in enumerate(chunks):
    if c.startswith(('`','http')):continue
    c=re.sub(r'\b('+ '|'.join(words)+r')(?=\d)',r'\1 ',c)
    c=re.sub(r'\b(SHA256|SHA1)(?=[a-f0-9]{10})',r'\1 ',c)
    c=re.sub(r'(\d)(?=(?:-byte|byte|bytes|MiB|GiB|KiB|ms|GB|MB|KB)\b)',r'\1 ',c)
    c=re.sub(r'([.;:])(?=[A-Z][a-z])',r'\1 ',c)
    chunks[i]=c
   line=''.join(chunks)
  lines.append(line)
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
with (DOC/'evidence/SHA256SUMS.txt').open('w',encoding='utf-8') as f:
 for p in sorted(DOC.rglob('*')):
  if p.is_file() and p.name!='SHA256SUMS.txt':f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(DOC).as_posix()+'\n')
errors=[];required=['README.md','PROVENANCE.md','FILE-INVENTORY.md','ARCHITECTURE.md','INSTALLATION-PIPELINE.md','AUTH-BOUNDARIES.md','JVM-RUNTIME.md','XBOX-UWP-COMPATIBILITY.md','LEGACYFORGE-GAP-ANALYSIS.md','EVIDENCE-INDEX.md','UNKNOWN-SUBSYSTEMS.md','PHASE-6-ROADMAP.md']
for n in required:
 if not (DOC/n).is_file():errors.append('missing '+n)
for p in DOC.glob('*.md'):
 for dest in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if not dest.startswith(('http:','https:','#')) and not (p.parent/dest.split('#')[0]).is_file():errors.append(p.name+' broken '+dest)
for p in DOC.rglob('*'):
 if not p.is_file():continue
 if p.suffix.lower() not in ['.md','.json','.csv','.txt','.example']:errors.append('unexpected file '+p.name)
 text=p.read_text(encoding='utf-8')
 if re.search(r'C:[\\/]+Users[\\/]+arinze|[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}',text):errors.append('personal path/token-like content '+p.name)
 if p.suffix=='.json':json.loads(text)
rows=list(csv.DictReader((DOC/'evidence/target-validation-matrix.csv').open()))
if len(rows)!=56 or any(r['newRuntimeTestStatus']!='BLOCKED' for r in rows):errors.append('target matrix status/count')
ET.fromstring((DOC/'tests/offline.wsb.example').read_text())
for l in (DOC/'evidence/SHA256SUMS.txt').read_text().splitlines():
 h,n=l.split('  ',1)
 if hashlib.sha256((DOC/n).read_bytes()).hexdigest()!=h:errors.append('checksum '+n)
result={'required_documents':len(required),'total_markdown':len(list(DOC.glob('*.md'))),'publication_files':len([p for p in DOC.rglob('*') if p.is_file()]),'target_rows':len(rows),'new_behavioral_verdicts':dict(collections.Counter(x['newRuntimeTestStatus'] for x in rows)),'validated_installer_payload_records':770,'native_audit_observations':291,'errors':errors}
(ROOT/'publication-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert not errors
