from __future__ import annotations

from pathlib import Path
import hashlib
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
LOGO = ROOT / "assets/cave-pony-logo.png"
SOCIAL_PREVIEW = ROOT / "assets/cave-pony-social-preview.png"
APPROVED_LOGO_GIT_BLOB_SHA = "7641946df2d6b11f1cad8a6b109fee7766a4411f"
APPROVED_SOCIAL_PREVIEW_GIT_BLOB_SHA = "2d44d734d88bc1b72ea794d37e4f9803738777c1"


def png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or not header.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("project artwork must be a PNG")
    return struct.unpack(">II", header[16:24])


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


class ProfileArtworkTests(unittest.TestCase):
    def test_readme_uses_local_approved_profile(self) -> None:
        readme = README.read_text(encoding="utf-8")
        self.assertIn(
            '<img src="./assets/cave-pony-logo.png" width="420" alt="Cave Pony logo">',
            readme,
        )
        for stale_reference in (
            'src="./logo.jpg"',
            'src="./logo.svg"',
            'src="./logo.png"',
            "raw.githubusercontent.com",
            "?raw=true",
            "file_00000000",
        ):
            self.assertNotIn(stale_reference, readme)

    def test_profile_artwork_is_exact_approved_asset(self) -> None:
        self.assertTrue(LOGO.is_file(), "missing approved profile artwork")
        self.assertEqual((1254, 1254), png_dimensions(LOGO))
        self.assertEqual(APPROVED_LOGO_GIT_BLOB_SHA, git_blob_sha(LOGO))

    def test_social_preview_is_exact_approved_asset(self) -> None:
        self.assertTrue(SOCIAL_PREVIEW.is_file(), "missing approved social preview")
        self.assertEqual((1280, 640), png_dimensions(SOCIAL_PREVIEW))
        self.assertEqual(
            APPROVED_SOCIAL_PREVIEW_GIT_BLOB_SHA,
            git_blob_sha(SOCIAL_PREVIEW),
        )


if __name__ == "__main__":
    unittest.main()
