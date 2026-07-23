from __future__ import annotations

from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
LOGO = ROOT / "logo.jpg"


def jpeg_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("profile artwork must be a JPEG")

    offset = 2
    while offset < len(data):
        while offset < len(data) and data[offset] != 0xFF:
            offset += 1
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        if offset >= len(data):
            break

        marker = data[offset]
        offset += 1
        if marker in {0xD8, 0xD9}:
            continue
        if offset + 2 > len(data):
            break

        length = struct.unpack(">H", data[offset : offset + 2])[0]
        if length < 2 or offset + length > len(data):
            break
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            height, width = struct.unpack(">HH", data[offset + 3 : offset + 7])
            return width, height
        offset += length

    raise ValueError("profile artwork has no JPEG dimensions")


class ProfileArtworkTests(unittest.TestCase):
    def test_readme_uses_local_approved_profile(self) -> None:
        readme = README.read_text(encoding="utf-8")
        self.assertIn(
            '<img src="./logo.jpg" width="420" alt="Cave Pony logo">',
            readme,
        )
        for stale_reference in (
            "logo.svg",
            "logo.png",
            "raw.githubusercontent.com",
            "?raw=true",
        ):
            self.assertNotIn(stale_reference, readme)

    def test_profile_artwork_is_renderable_and_sufficiently_large(self) -> None:
        self.assertTrue(LOGO.is_file(), "missing approved profile artwork")
        width, height = jpeg_dimensions(LOGO)
        self.assertEqual(width, height)
        self.assertGreaterEqual(width, 512)


if __name__ == "__main__":
    unittest.main()
