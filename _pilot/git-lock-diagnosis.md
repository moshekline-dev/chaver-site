# Git Lock Diagnosis

**Date:** 2026-05-12 (lock observed at ~15:35 UTC)
**Mode:** Investigation only — no `.git/` state was modified.

---

## TL;DR

A single stale `.git/index.lock` exists. **It was created by Cowork's own `git status` command earlier in this session** (~78 minutes ago). Git tried to clean it up but the OneDrive-mounted filesystem rejected the unlink ("Operation not permitted"). The lock is **safe to remove manually**, but Moshe should do it — Cowork should not delete it while GitHub Desktop is also watching the directory.

---

## 1. Lock Files Found

Only one lock file exists under `.git/`. No other `*.lock` files (no `HEAD.lock`, no `refs/heads/main.lock`, no `packed-refs.lock`, no `config.lock`).

| Path | Size | Modified (UTC) | Age | Contents |
|---|---:|---|---:|---|
| `.git/index.lock` | **0 bytes** | 2026-05-12 14:17:19 | **~78 min** | empty |

The 0-byte size is the signature of a **stale lock**. When a Git operation is actively holding the index lock, the file usually contains a serialized in-progress index. An empty lock file means: a process started writing to it, then either crashed or was unable to atomically rename the lock onto `.git/index`. In this case, the latter — see Section 4 for the unlink-permission evidence.

---

## 2. Active Git / GitHub Desktop Processes

From inside the Cowork Linux sandbox (the only process table Cowork can see):

- **No `git` processes are running** in the sandbox.
- The only sandbox processes are the bash invocation that just ran and its children — none of them are `git`.

Cowork cannot inspect Windows processes (`GitHubDesktop.exe`, host-side `git.exe`, etc.) from inside its sandbox. Moshe should check on the Windows host:

```cmd
tasklist | findstr /i "git"
tasklist | findstr /i "GitHubDesktop"
```

If neither command shows any active processes, it confirms the lock has no living owner.

---

## 3. Cowork's Own Git Activity in This Repo

**Cowork created this lock.** Evidence:

1. **Owner UID matches the sandbox user.** The lock file's owner is `dreamy-elegant-newton` (UID 1028) — the user identity Cowork runs as inside its Linux sandbox. The same user owns `.git/index` (and every other file in the repo, because of how the OneDrive mount maps Windows ownership to a single sandbox UID), so on its own this isn't conclusive. But it's consistent with sandbox-side authorship.

2. **The lock's mtime matches when Cowork ran `git status`.** During an earlier task in this session I ran `git status --short _templates/Academic-Content-EN.html` to inspect the working tree state. That invocation produced this exact warning in the output (captured in the prior conversation):

   ```
   warning: unable to unlink '/sessions/dreamy-elegant-newton/mnt/chaver-site/.git/index.lock': Operation not permitted
   ```

   That warning is Git telling us: *I created the lock to refresh the stat cache, but I couldn't delete the lock when I was done.* The mtime on the current lock (`14:17:19`) lines up with that earlier `git status`.

3. **No other tmp/MERGE files exist** in `.git/` from a half-completed operation. Just this single 0-byte lock.

The root cause is the OneDrive-mounted filesystem refusing to let the sandbox user delete a file it had just created. This is the same mount inconsistency that's been showing up in this session as stale bash views of `_templates/*.html` files — a write-after-create permission boundary somewhere in the OneDrive layer that doesn't behave like a normal POSIX filesystem.

---

## 4. Verdict

**The lock is STALE — leftover from a crashed/interrupted Cowork operation, not from an active Git or GitHub Desktop process.**

Signals:

- 0-byte file (active operations write content)
- 78 minutes old (real index updates take milliseconds)
- No `git` processes in the Cowork sandbox
- The git command that created it explicitly logged its inability to clean up
- The error from GitHub Desktop ("A lock file already exists") matches exactly what would happen if it tried to acquire the index lock while a stale one is present

---

## 5. Recommendation

**Manual cleanup by Moshe, from Windows, with GitHub Desktop closed first.** Three reasons not to do this from Cowork:

1. Cowork already failed to delete this same file once (the unlink-permission warning); a second attempt from inside the sandbox is likely to fail the same way.
2. If Cowork did somehow delete it while GitHub Desktop is open and trying its own retry, you'd have two processes racing on the same lock path — unsafe.
3. The task spec was explicit: *"let Moshe close GitHub Desktop and clear it manually so we don't risk Cowork's process and GitHub Desktop fighting over the same file."*

### Recommended steps for Moshe

1. **Close GitHub Desktop** (entirely — confirm no GitHub Desktop processes remain in Task Manager).
2. **Open a Windows command prompt or PowerShell** and run:
   ```cmd
   tasklist | findstr /i "git"
   ```
   Confirm no `git.exe` is running.
3. **Delete the lock file** from Windows:
   ```cmd
   del "C:\Users\Moshe\OneDrive\Documents\GitHub\chaver-site\.git\index.lock"
   ```
   (or in PowerShell: `Remove-Item ...`; or just delete it from File Explorer with hidden files visible).
4. **Reopen GitHub Desktop** and try the commit again.

### If the lock comes back

If `index.lock` reappears within seconds of deletion, something else is actively re-creating it — most likely a stalled GitHub Desktop "Git Helper" process. In that case, reboot or kill all `git.exe` / `mintheme.exe` / GitHub-related processes via Task Manager before retrying.

### Going forward

To avoid future occurrences, **Cowork should refrain from running `git` commands** against this repo via `bash` while GitHub Desktop has it open. The OneDrive mount's permission model breaks Git's cleanup atomicity. If Cowork needs Git state, it can read `.git/HEAD`, `.git/refs/...`, and `.git/logs/...` directly via the file tools — those reads never create lock files. Or Moshe can run `git` commands on his Windows host instead and paste output.

---

## Anomalies / Things Worth Knowing

- Cowork created the lock, accidentally, via what should have been a read-only `git status`. Git's "refresh stat cache" optimization writes the index file when stat results have changed, which is what triggered the lock acquisition.
- No commits were lost. The actual `.git/index` (1.9 MB, mtime `14:12:26`) is intact — only the lock file is stale.
- The repo working tree is in good shape; the lock is the only blocker to committing.

---

## Files Touched

| File | Action |
|---|---|
| `_pilot/git-lock-diagnosis.md` | This report |
| `.git/...` | **Nothing.** Investigation only. |
