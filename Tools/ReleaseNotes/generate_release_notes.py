"""Generate the commit-record section of the Vite release-notes topics.

Each release page in Writerside/topics/ReleaseNotes keeps its curated text
(summary, highlights, upgrade notes) by hand. Only the block between

    <!-- BEGIN GENERATED COMMIT RECORD -->
    <!-- END GENERATED COMMIT RECORD -->

is rewritten here, from real branch history, so the audit trail can be
refreshed without touching the editorial content.

Usage
-----
The engine repositories are far too large to clone for this. A treeless
partial clone holds every commit (message, author, dates) and no file data:

    git init --bare vite.git && cd vite.git
    git remote add pub https://github.com/GapingPixel/UnrealEngineVite-PhysX.git
    git remote add int https://github.com/ViteStudio-Tech/ueVite-Internal.git
    git config remote.pub.promisor true && git config remote.pub.partialclonefilter tree:0
    git config remote.int.promisor true && git config remote.int.partialclonefilter tree:0
    git fetch --filter=tree:0 --no-tags pub "+refs/heads/ueVite*:refs/remotes/pub/ueVite*" \
        "+refs/heads/4.27-plus:refs/remotes/pub/4.27-plus"
    git fetch --filter=tree:0 --no-tags int "+refs/heads/ueVite26-AugustMajor-staging-9:refs/remotes/int/ueVite26-AugustMajor-staging-9"

Then, from the repository root:

    python Tools/ReleaseNotes/generate_release_notes.py --git-dir path/to/vite.git
    python Tools/ReleaseNotes/generate_release_notes.py --git-dir path/to/vite.git --locale ja

Add a release by appending to RELEASES and creating its topic with the
marker block; the script fails loudly if a page lacks the markers.
"""
import argparse
import os
import re
import subprocess
import sys
from collections import Counter

PUBLIC_REPO = "https://github.com/GapingPixel/UnrealEngineVite-PhysX"
UPSTREAM = "pub/4.27-plus"

# Each source is (heading key, rev-list arguments, public?). Exclusions use
# "^ref", never "--not", because the upstream exclusion is appended as
# "^ref" too and --not would invert it. "public" decides
# whether commits get a link: internal staging commits are listed for the
# record but have no URL a reader outside the studio could open.
RELEASES = [
    {
        "topic": "ueVite26-SeptemberMajor.md",
        "branch": "ueVite26-SeptemberMajor-release",
        "sources": [
            ("public", ["pub/ueVite26-AugustMajor-release..pub/ueVite26-SeptemberMajor-release"], True),
        ],
    },
    {
        "topic": "ueVite26-AugustMajor.md",
        "branch": "ueVite26-AugustMajor-release",
        "sources": [
            ("public", ["pub/ueVite26-JulyMajor-release..pub/ueVite26-AugustMajor-release"], True),
            ("staging", ["int/ueVite26-AugustMajor-staging-9", "^pub/ueVite26-JulyMajor-release"], False),
        ],
    },
    {
        "topic": "ueVite26-JulyMajor.md",
        "branch": "ueVite26-JulyMajor-release",
        "sources": [
            ("public", ["pub/ueVite26-JuneMajor-release..pub/ueVite26-JulyMajor-release"], True),
        ],
    },
    {
        "topic": "ueVite26-JuneMajor.md",
        "branch": "ueVite26-JuneMajor-release",
        "sources": [
            ("public", ["pub/ueVite26-MarchMajor-release..pub/ueVite26-JuneMajor-release"], True),
        ],
    },
    {
        "topic": "ueVite26-MarchMajor.md",
        "branch": "ueVite26-MarchMajor-release",
        "sources": [
            ("public", ["pub/ueVite25-LTS..pub/ueVite26-MarchMajor-release"], True),
        ],
    },
    {
        "topic": "ueVite25-LTS.md",
        "branch": "ueVite25-LTS",
        # The LTS branch carries the full NvRTX/Epic history underneath it;
        # Vite's own work on this line starts in November 2025.
        "sources": [
            ("public", ["pub/ueVite25-LTS", "--since=2025-11-01"], True),
        ],
    },
]

TEXT = {
    "en": {
        "public": "Public release branch",
        "staging": "Internal staging (released as one commit)",
        "staging_note": (
            "These commits were developed and reviewed on the internal staging branch "
            "<code>{staging}</code> and published to the public branch as a single release commit. "
            "They are listed for the record; the short hashes refer to the internal repository and are not linked."
        ),
        "branch_line": "Branch: [`{branch}`]({url})",
        "summary": "{n} commits ({merges} merge commits omitted from the table).",
        "summary_no_merges": "{n} commits.",
        "head": "| Date | Commit | Author | Change |",
        "title": "Full commit history",
        "title_source": "{label} — {n} commits",
        "areas": "Commits by area",
        "area_head": "| Area | Commits |",
    },
    "ja": {
        "public": "公開リリースブランチ",
        "staging": "内部ステージング（1 コミットとして公開）",
        "staging_note": (
            "これらのコミットは内部ステージングブランチ <code>{staging}</code> で開発・レビューされ、"
            "公開ブランチには 1 つのリリースコミットとして反映されました。記録として掲載していますが、"
            "短縮ハッシュは内部リポジトリのものであり、リンクはありません。"
        ),
        "branch_line": "ブランチ: [`{branch}`]({url})",
        "summary": "{n} 件のコミット（マージコミット {merges} 件は表から除外）。",
        "summary_no_merges": "{n} 件のコミット。",
        "head": "| 日付 | コミット | 作成者 | 変更内容 |",
        "title": "全コミット履歴",
        "title_source": "{label} — {n} 件",
        "areas": "領域別のコミット数",
        "area_head": "| 領域 | コミット数 |",
    },
}

# Ordered: the first matching rule wins, so specific areas (physics, hair,
# ray tracing) come before the broad ones that would also match them
# (rendering, toolchain). Patterns run against the lower-cased subject.
AREAS = [
    ("Physics", r"physx|\bblast\b|\bapex\b|\bchaos\b|cloth|destruct|rigid ?bod|fixed ?timestep|kawaii|collision|sweep|heightfield|broad ?phase|aabbtree|geometry ?collection"),
    ("Hair", r"tressfx|\bhair\b|groom"),
    ("Gameplay framework", r"abilit|gameplay ?(tag|cue|effect)|\bgas\b|\basc\b|attributeset|\beqs\b|navmesh|navigation|recast|\bai\b|fpredictionkey|uniquenetid"),
    ("Ray tracing and GI", r"\[rt\]|ray ?trac|raytrac|rtxgi|ddgi|rtxdi|regir|\bsbt\b|shader binding table|caustic|path ?trac|rtpso|hwrt|\brelax\b|\bnrd\b|denois|\blpv\b|\brt clears?\b"),
    ("Upscaling and anti-aliasing", r"dlss|xess|xefg|xell|\bfsr|smaa|fxaa|\btaa\b|temporalaa|msaa|upscal|anti-?alias|frame[- ]?gen|\bngx\b|streamline|antilag|latency|halton"),
    ("Animation", r"anim|blend ?space|montage|\bpose|skeletal|retarget|\bcmc\b|character ?movement|motion ?(matching|symphony)|\bacl\b|rigvm|riglogic|\bpuma\b|warping"),
    ("Toolchain and platforms", r"toolchain|msvc|clang|\bvs ?20\d\d|\bvs ?18|visual studio|\bsdk\b|linux|android|\bndk\b|\bmac|xcode|\bios\b|c\+\+ ?20|cpp ?20|\.net\b|dotnet|\bnet upgrade|embree|lightmass|compil|\bbuild|\bubt\b|\buat\b|\bsetup|\.bat\b|\bbats?\b|gitdep|commit deps|python|steam ?deck|\bvr\b|openxr|oculus|quest|hololens|\bwmr\b|magic leap|lumin\b|html5|switch 2|\bneon\b|unity build|\bpch\b|static analy|\bpvs\b|\bsln\b|old cpu|rdna|virtual ?cores|\bgpa\b|graphics performance analyzer|debug symbols|callstack"),
    ("Rendering", r"\[rendering\]|render|shader|ssgi|ssao|gtao|hbao|\bssr\b|\bao\b|ao_|fog|volumetric|cloud|shadow|lumen|light|tonemap|bloom|\bdof\b|exposure|eye adaptation|material|\bibl\b|\bsky|\brhi\b|d3d1|\bdx1|vulkan|\bgpu|\bpso\b|hism|\bism\b|instanced ?static|mesh ?draw|occlusion|specular|brdf|shading|decal|translucen|velocity|post ?process|\blods?\b|landscape|foliage|texture|niagara|particle|colou?r|aces|\bhdr\b|scene ?capture|reflection|stereo|\buav\b|\bsrv\b|fullscreen|distance ?field|water|visualize ?buffer|barrier"),
    ("Plugins and media", r"plugin|imgui|renderdoc|cable|\beos|houdini|metasound|audio|sound|media|ffmpeg|movie|chunk ?downloader|significance|sunposition|crypto|budget allocator|feature pack"),
    ("Editor and workflow", r"editor|slate|\bumg\b|widget|blueprint|kismet|\bbps?\b|live ?coding|\bini\b|default|config|readme|\.md\b|gitignore|\bicons?\b|tooltip|context menu|outliner|content browser|console|insights|stat (unit|fps)|asset ?registry|asset data|thumbnail|toolbar|tutorial|launcher|marketplace|sequencer|\bddc\b|\bcook|\bpie\b|splash|\bui\b|reimport|message ?log|sdroptarget|simage|sscalebox|news ?feed|usage ?data|jump target|mouse|badge|scriptError|raisescripterror|linestoadd|csv|hitch"),
    ("Core and performance", r"optimi|perf|memory|alloc|hash|thread|task|uobject|\btick|\bcore\b|container|array|\btset|\btmap|string|ftext|async|cache|stall|slack|leak|\bgc\b|garbage|serializ|\bload|stream|oodle|\bpak\b|iodispatcher|deadlock|\brace\b|lock|utf8|\bmath|vector|clamp|const\b|constructor|intfitsin|mtaccessdetector|enumredirect|delegate|iteratedirectory"),
]
AREA_RES = [(name, re.compile(pattern)) for name, pattern in AREAS]
AREA_JA = {
    "Physics": "物理",
    "Hair": "ヘア",
    "Gameplay framework": "ゲームプレイフレームワーク",
    "Ray tracing and GI": "レイトレーシングと GI",
    "Upscaling and anti-aliasing": "アップスケーリングとアンチエイリアシング",
    "Animation": "アニメーション",
    "Toolchain and platforms": "ツールチェーンとプラットフォーム",
    "Rendering": "レンダリング",
    "Plugins and media": "プラグインとメディア",
    "Editor and workflow": "エディタとワークフロー",
    "Core and performance": "コアとパフォーマンス",
    "Other": "その他",
}


def git(git_dir, *args):
    out = subprocess.run(
        ["git", f"--git-dir={git_dir}", *args],
        check=True, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return out.stdout


def commits(git_dir, rev_args):
    fmt = "%H%x1f%cs%x1f%an%x1f%P%x1f%s%x1e"
    # "^ref" rather than "--not ref": a source may already use --not, and a
    # second --not would flip the exclusion back into an inclusion.
    raw = git(git_dir, "log", "--date-order", f"--format={fmt}", *rev_args, "^" + UPSTREAM)
    rows = []
    for rec in raw.split("\x1e"):
        rec = rec.strip("\n")
        if not rec:
            continue
        sha, date, author, parents, subject = rec.split("\x1f")
        rows.append({
            "sha": sha, "date": date, "author": author,
            # Some imported messages carry CR/LF inside the subject line.
            "merge": len(parents.split()) > 1, "subject": " ".join(subject.split()),
        })
    return rows


def area_of(subject):
    s = subject.lower()
    for name, pattern in AREA_RES:
        if pattern.search(s):
            return name
    return "Other"


def escape(text, limit=200):
    """Make a commit subject safe inside a Writerside Markdown table cell."""
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    text = text.replace("\\", "\\\\")
    # Writerside reads %name% as a variable and {...} as an attribute list.
    text = text.replace("%", "&#37;").replace("{", "&#123;").replace("}", "&#125;")
    text = text.replace("&", "&amp;").replace("&amp;#", "&#")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    for ch in "|*_`[]":
        text = text.replace(ch, "\\" + ch)
    return text or "&mdash;"


def render(release, git_dir, locale):
    t = TEXT[locale]
    lines = [f"## {t['title']} {{id=\"commit-history\"}}", ""]
    branch_url = f"{PUBLIC_REPO}/tree/{release['branch']}"
    lines += [t["branch_line"].format(branch=release["branch"], url=branch_url), ""]

    all_rows = []
    sections = []
    for key, rev_args, public in release["sources"]:
        rows = commits(git_dir, rev_args)
        all_rows += rows
        sections.append((key, rev_args, public, rows))

    # Area overview first: a reader skimming wants the shape, not 400 rows.
    counts = Counter(area_of(r["subject"]) for r in all_rows if not r["merge"])
    if counts:
        lines += [f"### {t['areas']}", "", t["area_head"], "|---|---:|"]
        for name, n in counts.most_common():
            lines.append(f"| {AREA_JA.get(name, name) if locale == 'ja' else name} | {n} |")
        lines.append("")

    for key, rev_args, public, rows in sections:
        shown = [r for r in rows if not r["merge"]]
        merges = len(rows) - len(shown)
        label = t[key]
        lines += [f"### {t['title_source'].format(label=label, n=len(shown))} {{collapsible=\"true\" default-state=\"collapsed\"}}", ""]
        if not public:
            staging = rev_args[0].split("/", 1)[1]
            lines += ["<note>", "<p>", t["staging_note"].format(staging=staging), "</p>", "</note>", ""]
        lines.append(t["summary"].format(n=len(shown), merges=merges) if merges else t["summary_no_merges"].format(n=len(shown)))
        lines += ["", t["head"], "|---|---|---|---|"]
        for r in shown:
            short = r["sha"][:10]
            commit = f"[`{short}`]({PUBLIC_REPO}/commit/{r['sha']})" if public else f"`{short}`"
            lines.append(f"| {r['date']} | {commit} | {escape(r['author'], 40)} | {escape(r['subject'])} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n", len([r for r in all_rows if not r["merge"]])


BEGIN = "<!-- BEGIN GENERATED COMMIT RECORD -->"
END = "<!-- END GENERATED COMMIT RECORD -->"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--git-dir", required=True)
    ap.add_argument("--locale", choices=("en", "ja"), default="en")
    ap.add_argument("--dump", help="write tab-separated commit lists to this folder instead")
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    module = "Writerside" if args.locale == "en" else "WritersideJP"
    topics = os.path.join(root, module, "topics", "ReleaseNotes")

    for release in RELEASES:
        if args.dump:
            os.makedirs(args.dump, exist_ok=True)
            with open(os.path.join(args.dump, release["topic"].replace(".md", ".tsv")), "w", encoding="utf-8") as fh:
                for key, rev_args, public in release["sources"]:
                    for r in commits(args.git_dir, rev_args):
                        fh.write("\t".join([key, r["date"], r["sha"][:10], r["author"], "M" if r["merge"] else "", area_of(r["subject"]), r["subject"]]) + "\n")
            continue

        path = os.path.join(topics, release["topic"])
        text = open(path, encoding="utf-8-sig").read()
        if BEGIN not in text or END not in text:
            sys.exit(f"{path}: missing generated-record markers")
        block, n = render(release, args.git_dir, args.locale)
        text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), BEGIN + "\n\n" + block.replace("\\", "\\\\") + "\n" + END, text, flags=re.S)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print(f"{release['topic']}: {n} commits")


if __name__ == "__main__":
    main()
