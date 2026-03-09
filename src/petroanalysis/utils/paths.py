from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent.parent
RESOURCES_ROOT = PACKAGE_ROOT / "resources"


def resource_path(*parts: str) -> Path:
    return RESOURCES_ROOT.joinpath(*parts)


def image_path(filename: str) -> Path:
    return resource_path("images", filename)


def ui_resource_path(filename: str) -> Path:
    return resource_path("ui", filename)
