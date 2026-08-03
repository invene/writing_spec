"""Citation resolution for Rule 5.4.3.

Section 8.2 requires the linter to run offline, from the standard library,
with no network access. Resolving a DOI or a URL needs exactly what that
guarantee withholds, so resolution is not part of the default run.

A run may still supply a resolver. ``tools/itws_validate.py --network``
installs :class:`UrllibResolver`, and a test installs a stub. Without one,
the checker reports each unresolved target as a reader obligation rather
than passing over it or claiming a check it never ran.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

#: How long one resolution attempt may take, in seconds.
RESOLVE_TIMEOUT = 10.0

#: Where a bare DOI resolves.
DOI_BASE = "https://doi.org/"


@dataclass(frozen=True)
class Resolution:
    """The outcome of one attempt to resolve one citation target."""

    target: str
    resolved: bool
    detail: str = ""


class CitationResolver(Protocol):
    """What Rule 5.4.3 needs of any resolution back end."""

    def resolve(self, target: str) -> Resolution: ...


class UrllibResolver:
    """Resolve a target over the network with the standard library only.

    The resolver reports whether the target answers, not whether it answers
    with the cited work. Rule 5.4.4 keeps that judgment with a reader.
    """

    def __init__(self, timeout: float = RESOLVE_TIMEOUT) -> None:
        self.timeout = timeout

    def resolve(self, target: str) -> Resolution:
        import urllib.error
        import urllib.request

        url = target
        if not target.startswith(("http://", "https://")):
            url = DOI_BASE + target

        request = urllib.request.Request(url, method="HEAD")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return Resolution(target, 200 <= response.status < 400)
        except urllib.error.HTTPError as error:
            if error.code in {403, 405}:
                # Some hosts refuse HEAD but serve the document.
                return self._resolve_with_get(url, target)
            return Resolution(target, False, f"HTTP {error.code}")
        except (urllib.error.URLError, OSError, ValueError) as error:
            return Resolution(target, False, str(error))

    def _resolve_with_get(self, url: str, target: str) -> Resolution:
        import urllib.error
        import urllib.request

        try:
            with urllib.request.urlopen(url, timeout=self.timeout) as response:
                return Resolution(target, 200 <= response.status < 400)
        except urllib.error.HTTPError as error:
            return Resolution(target, False, f"HTTP {error.code}")
        except (urllib.error.URLError, OSError, ValueError) as error:
            return Resolution(target, False, str(error))
