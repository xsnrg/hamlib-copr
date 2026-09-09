# AGENTS.md

This repo is a **Copr package build repo** for Hamlib. The only source of
truth is `hamlib.spec` — there is no application code, CI, or local test suite
here.

## Release workflow

- Copr **auto-builds on push to `master`** — commit and push to publish.
- To release: bump `Version:`, reset `Release:` to `1%{?dist}`, add a
  `%changelog` entry, commit, push.
- Changelog entries must be **newest first** (this was broken once and fixed
  in commit `363dc61`).
- Entry format, matching existing entries:

  ```
  * Thu Aug 13 2026 Jim Howard <xsnrg@users.noreply.github.com> - 4.7.2-1
  - Update to 4.7.2
  ```

## Spec constraints

- Fedora spec: uses `%{?dist}`, `%{?perl_default_filter}`, `%autosetup`,
  `%{python3_sitearch}` — keep it Fedora-compatible.
- Perl + Tcl bindings are **intentionally disabled**
  (`--without-perl-binding --without-tcl-binding`); do not re-enable.
- `--disable-static` is intentional. Subpackages: `devel`, `doc`, `c++`,
  `c++-devel`, `python3-hamlib`.
- `%check` runs the upstream autotools suite (`make V=1 check`) inside the
  Copr build — failures break the build.
- The custom `CFLAGS`/`CXXFLAGS`/`LDFLAGS` block in `%build` is
  intentionally commented out (distro portability); edit with care.

## Verification

No local tests. If `rpmbuild` is available, sanity-check with
`rpmbuild -bp hamlib.spec`; otherwise verify via the Copr build after push.
