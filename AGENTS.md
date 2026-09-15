# feincms-oembed

Django app providing FeinCMS content types that embed external content via oEmbed.
`CachedLookup` (models.py) fetches and caches arbitrary URLs; `contents.py` builds the
content types on top of it.

## Working agreements

- Commit feature by feature. Keep commit messages succinct — don't restate the diff.
- No attribution / co-author trailers in commits.

## Running the tests

tox is the source of truth (`tox.ini`): py310-dj42, py312/py313-dj52 and -djmain.
For a quick local run:

```bash
uv venv --python 3.13 .venv
VIRTUAL_ENV=.venv uv pip install -e '.[tests]' 'Django>=5.2,<6.0'
.venv/bin/python tests/manage.py test -v2 testapp
```

Settings live in `tests/testapp/settings.py`; `OEMBED_PROVIDER` is pointed at
`noembed_oembed_provider` there (the library's own default is embedly).

Tests that talk to the real provider are marked `@tag("live")` and excluded from the
tox run via `--exclude-tag=live`. The "Live provider" job in `tests.yml` runs them once
per workflow run with `continue-on-error: true`, so a provider outage is reported
without blocking a merge. Run them by hand with:

```bash
.venv/bin/python tests/manage.py test -v2 --tag=live testapp
```

## Learnings

- Merge-blocking tests must not touch the network. `CachedLookup.clean()` calls
  `urlopen()`, so patch `feincms_oembed.models.urlopen` with a fake response object
  exposing `read()` and `getcode()`. Coverage of the real service belongs in a
  `@tag("live")` test instead — mocking everything would hide the provider dying,
  which is the one failure the package cannot work around.
- noembed.com — the provider the test settings use — is unreliable. It intermittently
  answers `{"error": "Can't use string (\"servers\") as a HASH ref ..."}` instead of
  oEmbed data. This is *not* deterministic per URL: in run 34889438323 the py312 job
  got a good response for the Rick Astley URL while py313 got the error for the same
  URL minutes later. Swapping in a video that "works" today only hides the problem —
  mock instead.
- Matrix jobs failing on only some Python versions has so far always meant this
  flakiness, not a Django/Python incompatibility. Check whether the failing assertion
  depends on a network call before hunting for version issues.
