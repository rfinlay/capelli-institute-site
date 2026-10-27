#!/usr/bin/env python3
"""
Resonant Mind — pull the channel's latest uploads into the repository.

Reads resonantMind.channelId from assets/data/copy.json, fetches the channel's public Atom feed
(https://www.youtube.com/feeds/videos.xml?channel_id=UC..., no API key, newest first, up to 15
entries) and writes:

    assets/data/videos.json            the list the page generator renders
    assets/img/videos/<videoId>.jpg    one poster per video, copied from YouTube at build time

The posters are committed so a visitor's browser makes NO request to YouTube until a video is
clicked; the page's content security policy allows images from this site only. The GitHub Action
runs this on every push and on a daily schedule (see .github/workflows/pages.yml), so a new upload
appears on the site by itself.

Failure policy: this script never breaks the build. If the feed cannot be fetched (network, YouTube
down, channel id wrong) it prints a warning, leaves the previous videos.json in place, and exits 0.
A channel with no public videos writes an empty list, which the page renders as "First videos
coming soon" with the Subscribe button.

    python3 tools/fetch-videos.py            # refresh from the channel named in copy.json
    python3 tools/fetch-videos.py --feed f.xml  # read a saved feed instead (tests, offline)
"""
import json, os, re, sys, urllib.request, urllib.error, xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets/data/videos.json")
POSTERS = os.path.join(ROOT, "assets/img/videos")
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
CHANNEL_ID = re.compile(r"^UC[A-Za-z0-9_-]{22}$")
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "media": "http://search.yahoo.com/mrss/"}
UA = "Mozilla/5.0 (compatible; capelli-institute-site build; +https://thecapelliinstitute.com)"
KEEP = 12   # newest uploads kept on the page

def get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def parse_feed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for e in root.findall("a:entry", NS):
        vid = (e.findtext("yt:videoId", default="", namespaces=NS) or "").strip()
        title = (e.findtext("a:title", default="", namespaces=NS) or "").strip()
        pub = (e.findtext("a:published", default="", namespaces=NS) or "").strip()
        if not VIDEO_ID.match(vid) or not title:
            print(f"  skipped a feed entry with an unusable id/title ({vid!r})", file=sys.stderr); continue
        items.append({"id": vid, "title": title, "published": pub[:10]})
    items.sort(key=lambda i: i["published"], reverse=True)
    return items[:KEEP]

def fetch_poster(vid):
    """Copy the video's poster into assets/img/videos/. maxres when YouTube has rendered one, else hq (always exists)."""
    os.makedirs(POSTERS, exist_ok=True)
    path = os.path.join(POSTERS, f"{vid}.jpg")
    if os.path.exists(path) and os.path.getsize(path) > 2000:
        return True
    for name in ("maxresdefault", "hqdefault"):
        try:
            data = get(f"https://i.ytimg.com/vi/{vid}/{name}.jpg")
        except urllib.error.HTTPError as ex:
            if ex.code == 404: continue
            print(f"  poster {vid}: HTTP {ex.code}", file=sys.stderr); return False
        except Exception as ex:
            print(f"  poster {vid}: {ex}", file=sys.stderr); return False
        # YouTube serves a 120x90 grey placeholder (about 1 KB) for a missing maxres; skip it.
        if len(data) < 2000: continue
        with open(path, "wb") as f: f.write(data)
        return True
    return False

def main(argv):
    with open(os.path.join(ROOT, "assets/data/copy.json"), encoding="utf-8") as f:
        copy = json.load(f)
    cid = ((copy.get("resonantMind") or {}).get("channelId") or "").strip()
    feed_path = argv[argv.index("--feed") + 1] if "--feed" in argv else None
    if feed_path:
        with open(feed_path, "rb") as f: xml_bytes = f.read()
    else:
        if not CHANNEL_ID.match(cid):
            print(f"fetch-videos: resonantMind.channelId in copy.json is not a channel id (got {cid!r}); videos.json left as is.", file=sys.stderr)
            return 0
        try:
            xml_bytes = get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")
        except Exception as ex:
            print(f"fetch-videos: could not fetch the channel feed ({ex}); videos.json left as is.", file=sys.stderr)
            return 0
    try:
        items = parse_feed(xml_bytes)
    except ET.ParseError as ex:
        print(f"fetch-videos: the feed was not valid XML ({ex}); videos.json left as is.", file=sys.stderr)
        return 0
    kept = []
    for it in items:
        if fetch_poster(it["id"]):
            kept.append(it)
        else:
            print(f"  no poster for {it['id']} ({it['title']}); left off the page this run", file=sys.stderr)
    # The editor's own featured list (Pages CMS) needs posters too; the generator reduces links to ids the same way.
    for row in (copy.get("resonantMind") or {}).get("featured") or []:
        raw = row.get("video") if isinstance(row, dict) else row
        m = re.search(r"(?:[?&]v=|youtu\.be/|/embed/|/shorts/|/live/)([A-Za-z0-9_-]{11})(?:[?&#/]|$)", raw or "")
        vid = raw.strip() if isinstance(raw, str) and VIDEO_ID.match(raw.strip()) else (m.group(1) if m else None)
        if vid and not fetch_poster(vid):
            print(f"  no poster for featured video {vid}; it renders with a plain navy poster", file=sys.stderr)
    # Posters for videos no longer in the feed are left in place (harmless, and the CMS featured list may still use them).
    out = {"_about": "Generated by tools/fetch-videos.py from the Resonant Mind channel feed. Do not edit by hand; "
                     "to pin or add a video use resonantMind.featured in copy.json (Pages CMS).",
           "channelId": cid, "fetched": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "items": kept}
    prev = None
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f: prev = json.load(f)
    if prev and prev.get("items") == kept and prev.get("channelId") == cid:
        print(f"fetch-videos: {len(kept)} video(s), unchanged.")
        return 0
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False); f.write("\n")
    print(f"fetch-videos: wrote {len(kept)} video(s) to assets/data/videos.json")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
