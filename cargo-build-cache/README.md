# Cargo Build Cache Actions

## Description

`cargo-build-cache/restore` and `cargo-build-cache/save` cache a Cargo `target/` directory between workflow runs, including the build output of the workspace's own crates. A run then only recompiles the crates that changed and the crates that depend on them.

Caching `target/` alone is not enough. Cargo decides whether a workspace crate is up to date by comparing the modification times of its source files with those of its build output, and a fresh checkout gives every file the current time. So:

- **restore** restores the cache, sets every tracked file to a fixed old time, and marks as new only the files whose hash differs from the hashes stored with the cache. It keeps the current hashes for save.
- **save** stores those hashes next to the build output as the record of its inputs, then saves the cache.

Without a stored list of hashes (nothing restored, or a cache saved without one), every workspace crate is rebuilt. That is slower but never stale.

## How to Use It

Run `restore` after installing Rust and before the build, and `save` after the build, only if the build succeeded.

```yaml
- name: Install Rust
  uses: dtolnay/rust-toolchain@b725eda525362e7cf34af9a7243cac1e3f01a7ec # stable
  with:
    toolchain: stable

# Caches the downloaded crates. The build cache below holds target/.
- name: Cache cargo registry
  uses: Swatinem/rust-cache@779680da715d629ac1d338a641029a2f4372abb5 # v2.8.2
  with:
    cache-targets: false

- name: Restore build output
  uses: bitwarden/gh-actions/cargo-build-cache/restore@main
  with:
    key: test

- name: Build
  id: build
  run: cargo test --workspace --no-run

- name: Save build output
  if: always() && steps.build.outcome == 'success'
  uses: bitwarden/gh-actions/cargo-build-cache/save@main

- name: Test
  run: cargo test --workspace
```

The hashes are taken when `restore` runs, so steps between the build and `save`, such as tests, may change tracked files. Steps between `restore` and the build must not change them.

### Cache key

The build output is saved under `cargo-build-<runner os>-<key>-<compiler>-<YYYY-MM>-<commit sha>`, where `<compiler>` is a hash of `rustc -vV` in the working directory.

- Runs start a new cache every month, so build output of old dependency versions doesn't accumulate. Schedule a run on the default branch early each month (e.g. `cron: "0 2 1 * *"`) so pull requests don't wait for the next merge to get the new month's cache.
- Pull requests fall back to the previous month's cache until the default branch has built the new one. Other events only restore caches from the current month.
- `save` skips saving when `restore` found an exact match of the key, because that entry already exists.
- Every build that produces different output needs its own `key`: a different command, profile, feature set or target. If the output also depends on something Cargo doesn't track, such as a container image with the linker, add it to the `key`.

### Restore inputs

| Input                  | Required | Default | Description                                                                                                                                                          |
| ---------------------- | -------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`                  | Yes      |         | Name of the build variant, part of the cache key. Letters, digits, `.`, `_` and `-` only.                                                                            |
| `path`                 | No       | `""`    | Additional paths and exclusions to cache, one per line, relative to the repository root (actions/cache syntax). The Cargo target directory is always cached.         |
| `working_directory`    | No       | `.`     | Root of the Cargo workspace, relative to the repository root. Only the files git tracks below it are hashed.                                                         |
| `toolchain`            | No       | `""`    | Rustup toolchain the build uses, when it is not the default one for the working directory (e.g. a pinned nightly). Used for the cache key and for the sysroot reset. |
| `reset_sysroot_mtimes` | No       | `false` | Set all files in the toolchain's sysroot to a fixed old time. Needed for builds that track sysroot files, see below.                                                 |

### Restore outputs

| Output              | Description                                                           |
| ------------------- | --------------------------------------------------------------------- |
| `cache_hit`         | `true` if the cache was restored from an exact match of the key.      |
| `cache_primary_key` | The key the build output is saved under.                              |
| `cache_matched_key` | The key of the restored cache entry. Empty when nothing was restored. |

`save` has no inputs: it reads the key and paths that `restore` stored for the job. Each job can use one build cache.

### Builds that track the toolchain's files

Some builds make Cargo compare the modification times of files inside the Rust toolchain, which a fresh toolchain install gives the current time:

- `-Zbuild-std` builds the standard library from the `rust-src` sources.
- `-Zbinary-dep-depinfo`, used for example by `cargo-udeps`, tracks the standard library binaries.

Set `reset_sysroot_mtimes: true` for these, and `toolchain` when the build uses another toolchain than the default one. The toolchain is part of the cache key, so the cached output always comes from the same toolchain files.

```yaml
- name: Restore build output
  uses: bitwarden/gh-actions/cargo-build-cache/restore@main
  with:
    key: lint-udeps
    toolchain: ${{ steps.nightly-toolchain.outputs.RUST_NIGHTLY_TOOLCHAIN }}
    reset_sysroot_mtimes: true
```

## Notes

- Path dependencies outside `working_directory` keep their checkout time, so crates that use them are rebuilt on every run.
- Builds in containers, such as `cross`, must see the workspace with the same file times. `cross` mounts it at the same path.
- Symlinks are hashed by the path they point to, like git stores them. When a tracked symlink changed since the cached build, `restore` rebuilds all workspace crates: Cargo follows symlinks, so the file times of the new target can't tell it what changed. Submodules are not hashed, so crates that use their files are rebuilt on every run.
- Tracked paths that contain a newline can't be hashed. `restore` then rebuilds all workspace crates, and `save` fails.
