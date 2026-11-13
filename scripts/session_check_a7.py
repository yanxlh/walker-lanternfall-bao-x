#!/usr/bin/env python3
"""Assignment 7 after-session check: the agent session's transcript and a read-only git review of its commits.

Usage: python3 -I scripts/session_check_a7.py <session.jsonl> <base-commit> <out.json>

Transcript: whether a final `result` event exists and what it says (headless `claude -p` stream-json runs end with
one; Claude desktop transcripts do not), tool calls and tool errors, Stop-hook errors. Only counts, tool names and
the first line of each error are written out, never message text.
Git (read-only: log, diff, status): files changed since <base>, grouped, and any change to a path the brief puts
out of scope.
"""
import json
import subprocess
import sys
from collections import Counter

OUT_OF_SCOPE = [
    "godot/shaders/", "godot/effects/", "godot/a3/", "godot/a5/", "godot/audio/", "godot/assets/", "godot/ui/",
    "godot/features/enemies/", "godot/features/weapons/", "godot/features/pickups/", "godot/features/world/",
    "godot/game/game_state.gd", "godot/project.godot",
]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def transcript(path: str) -> dict:
    types = Counter()
    tools = Counter()
    errors = []
    results = []
    hook_errors = 0
    names = {}
    for line in open(path, encoding="utf-8"):
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = e.get("type")
        types[t] += 1
        if t == "result":
            results.append({k: e.get(k) for k in ("subtype", "is_error", "num_turns", "stop_reason")})
        if t == "system" and e.get("subtype") == "stop_hook_summary":
            hook_errors += len(e.get("hookErrors") or [])
        content = (e.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                tools[block.get("name")] += 1
                names[block.get("id")] = block.get("name")
            elif block.get("type") == "tool_result" and block.get("is_error"):
                body = block.get("content")
                if isinstance(body, list):
                    body = " ".join(x.get("text", "") for x in body if isinstance(x, dict))
                first = next((l for l in str(body).splitlines() if l.strip()), "")[:160]
                errors.append({"tool": names.get(block.get("tool_use_id"), "?"), "first_line": first})
    return {
        "result_events": results,
        "has_result_event": bool(results),
        "tool_calls": sum(tools.values()),
        "tool_calls_by_name": dict(tools.most_common()),
        "tool_errors": len(errors),
        "tool_error_lines": errors,
        "stop_hook_errors": hook_errors,
    }


def main() -> int:
    jsonl, base, out = sys.argv[1], sys.argv[2], sys.argv[3]
    head = git("rev-parse", "--short", "HEAD").strip()
    changed = [l for l in git("diff", "--name-only", f"{base}..HEAD").splitlines() if l]
    groups = Counter(p.split("/")[0] if not p.startswith("godot/") else "/".join(p.split("/")[:3]) for p in changed)
    out_of_scope = [p for p in changed if any(p == s or p.startswith(s) for s in OUT_OF_SCOPE)]
    commits = git("log", "--format=%h %s", f"{base}..HEAD").splitlines()
    status = [l for l in git("status", "--short").splitlines() if l]
    report = {
        "head": head,
        "base": base,
        "transcript": transcript(jsonl),
        "git": {
            "commits": len(commits),
            "files_changed": len(changed),
            "changed_by_area": dict(sorted(groups.items())),
            "godot_files_changed": [p for p in changed if p.startswith("godot/") and not p.startswith("godot/tests/")],
            "out_of_scope_changed": out_of_scope,
            "uncommitted": status,
        },
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    t = report["transcript"]
    print(json.dumps({"head": head, "result_event": t["has_result_event"], "tool_calls": t["tool_calls"],
                      "tool_errors": t["tool_errors"], "stop_hook_errors": t["stop_hook_errors"],
                      "files_changed": len(changed), "out_of_scope_changed": out_of_scope, "uncommitted": len(status)}))
    return 0 if not out_of_scope else 1


if __name__ == "__main__":
    sys.exit(main())
