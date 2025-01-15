import os
from collections import defaultdict
from typing import List, Dict

from ...templates.thumbnail.thumbnail import ui_thumbnail
from ...routes.routes import uisRoutes


def get_svg_files(
    base_url: str = "https://raw.githubusercontent.com/chaseme24/ReflexUI/master/assets/thumbnails",
) -> List[Dict[str, str]]:

    svg_files = [
        os.path.basename(directory)
        for directory, _, _ in os.walk("ReflexUI/ui")
        if os.path.basename(directory) not in {"ui", "__pycache__"}
    ]

    return sorted(
        [{"image": f"{base_url}/{f}.svg", "filename": f"{f}.svg"} for f in svg_files],
        key=lambda x: x["filename"],
    )


def get_component_quantities(
    ui_folder: str = "ReflexUI/ui",
) -> Dict[str, int]:
    quantities = defaultdict(int)
    for subdir, _, files in os.walk(ui_folder):
        if os.path.basename(subdir) not in {"ui", "__pycache__"}:
            quantities[os.path.basename(subdir)] = len(files)
    return dict(quantities)


def get_uis_items() -> List[Dict[str, str]]:
    return [item for item in uisRoutes if item["name"] != "Table Pagination"]


NORMALIZATION_MAP = {
    # ... key name == ui_ROUTE[name]: value name == ui dir names
    "Animations": "animations",
    "Backgrounds": "backgrounds",
    "Cards": "cards",
    "Frequently Asked Questions": "faq",
    "Descriptive Lists": "lists",
    "Featured": "featured",
    "Logins": "logins",
    "Menus": "menus",
    "Onboarding & Progress": "onboardings",
    "Payments & Billing": "payments",
    "Popups": "popups",
    "Pricing Sections": "pricing",
    "Prompt Boxes": "prompts",
    "Subscribe": "subscribe",
    "Standard Forms": "forms",
    "Standard Tables": "tables",
    "Timeline": "timeline",
    "Footers": "footers",
    "Inputs": "inputs",
}


def combine_items(
    svg_files: List[Dict[str, str]],
    quantity_map: Dict[str, int],
    ui_items: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    combined_items = []
    for ui_item in ui_items:
        filename_key = NORMALIZATION_MAP.get(ui_item["name"])
        quantity = quantity_map.get(filename_key, 0)
        corresponding_image = next(
            (
                svg["image"]
                for svg in svg_files
                if svg["filename"].startswith(filename_key)
            ),
            None,
        )

        combined_items.append(
            {
                "image": corresponding_image,
                "quantity": quantity,
                "name": ui_item["name"],
                "path": ui_item["path"],
            }
        )
    return combined_items


def create_thumbnails(combined_items: List[Dict[str, str]]) -> List[str]:

    return [
        ui_thumbnail(
            item["path"], item["image"], item["name"], str(item["quantity"])
        )
        for item in combined_items
    ]


def main():
    svg_files = get_svg_files()
    quantity_map = get_component_quantities()
    pantry_items = get_uis_items()
    combined_items = combine_items(
        svg_files,
        quantity_map,
        pantry_items,
    )
    thumbnails = create_thumbnails(combined_items)
    return thumbnails


export_thumbnail = main()
