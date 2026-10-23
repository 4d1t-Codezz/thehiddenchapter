"""Sync only this public site; never reads the auto-poster or its secrets."""
import argparse, base64, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO="4d1t-Codezz/thehiddenchapter"
def api(path, method="GET", data=None):
    args=["gh","api",f"repos/{REPO}/{path}","--method",method]
    if data is not None: args += ["--input","-"]
    result=subprocess.run(args,input=json.dumps(data) if data is not None else None,text=True,capture_output=True,check=True)
    return json.loads(result.stdout)
def main():
    mode=argparse.ArgumentParser(); mode.add_argument("action",choices=["download","publish"]); args=mode.parse_args()
    ref=api("git/ref/heads/main"); parent=ref["object"]["sha"]
    tree=api(f"git/trees/{parent}?recursive=1")
    if args.action=="download":
        for entry in tree["tree"]:
            if entry["type"]!="blob": continue
            target=(ROOT/entry["path"]).resolve()
            if not target.is_relative_to(ROOT.resolve()): raise ValueError("Invalid repository path")
            blob=api("git/blobs/"+entry["sha"])
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(base64.b64decode(blob["content"]))
        print("Downloaded existing public website."); return
    # Explicit allowlist prevents accidental upload of credentials or workspace data.
    files=[*ROOT.glob("*.html"),*ROOT.glob("*.css"),*ROOT.glob("*.js"),ROOT/".nojekyll",ROOT/"README.md",ROOT/"build_site.py",ROOT/"sync_github.py",ROOT/"catalog.json",ROOT/"social-posts.md"]
    for folder in ("books","niches","assets","posts"):
        files += [p for p in (ROOT/folder).rglob("*") if p.is_file() and p.suffix in (".html",".svg",".json")]
    entries=[]
    old={e["path"]:e["sha"] for e in tree["tree"] if e["type"]=="blob"}
    import hashlib
    for file in sorted(set(files)):
        if not file.exists(): continue
        raw=file.read_bytes(); rel=file.relative_to(ROOT).as_posix()
        sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        if old.get(rel)==sha: continue
        blob=api("git/blobs","POST",{"content":base64.b64encode(raw).decode(),"encoding":"base64"})
        entries.append({"path":rel,"mode":"100644","type":"blob","sha":blob["sha"]})
    if not entries: print("No changes to publish."); return
    created=api("git/trees","POST",{"base_tree":tree["sha"],"tree":entries})
    commit=api("git/commits","POST",{"message":"Build niche book catalog and Facebook post drafts","tree":created["sha"],"parents":[parent]})
    api("git/refs/heads/main","PATCH",{"sha":commit["sha"],"force":False})
    print("Published commit "+commit["sha"])
if __name__=="__main__": main()
