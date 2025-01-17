from typing import Callable

import reflex as rx

from .style import ChangelogStyle

from ...routes.routes import uisRoutes, ChartRoutes

info: Callable[[str, any], rx.Component] = lambda txt, *args: rx.text(
    txt, size="2", color=rx.color("slate", 11), *args
)


def blip():
    return rx.box(
        rx.icon(tag="calendar-days", size=11, color=rx.color("gray")),
        **ChangelogStyle.blip,
    )


def wrapper(title: str, date: str, components: list[rx.Component] = []):
    return rx.hstack(
        rx.vstack(
            rx.vstack(
                rx.hstack(
                    blip(),
                    rx.text(date, size="1", weight="bold", color=rx.color("slate", 10)),
                    align="center",
                ),
                rx.text(title, size="3", weight="bold", color=rx.color("slate", 11)),
                spacing="1",
            ),
            *components,
        ),
        **ChangelogStyle.wrapper,
    )


def changelog_badge(tag: str, text: str):
    return rx.hstack(
        rx.box(
            rx.icon(tag=tag, size=14),
            background=rx.color("gray", 2),
            border_radius="100%",
            padding="8px",
            align_items="center",
            justify_content="center",
            display="flex",
        ),
        rx.text(text, size="2", weight="medium"),
        height="35px",
        border_radius="35px",
        background=rx.color("gray", 3),
        align="center",
        justify="start",
        padding="0em 1em 0em 0.25em",
        spacing="2",
    )


def create_pantry_links(item_list: list[dict[str, str]]):
    return rx.vstack(
        *[
            rx.link(
                rx.text(
                    data["name"],
                    size="2",
                    weight="medium",
                    color=rx.color("slate", 11),
                    _hover={"color": rx.color("slate", 12)},
                    transition="color 350ms ease",
                ),
                href=data["path"],
                text_decoration="none",
            )
            for data in item_list
        ],
        spacing="1",
    )


def create_link(name: str, path: str):
    return rx.link(
        rx.text(
            name,
            size="2",
            weight="medium",
            color=rx.color("slate", 11),
            _hover={"color": rx.color("slate", 12)},
            transition="color 350ms ease",
        ),
        href=path,
        text_decoration="none",
    )


def changelog():
    return rx.vstack(
        rx.box(
            rx.vstack(
                wrapper(
                    "ReflexUI v1.0.1 Deployed to Reflex",
                    "january 16, 2025",
                    [
                        changelog_badge("party-popper", "ReflexUI v1.0.1"),
                    ],
                ),
                wrapper(
                    "ReflexUI v1.0.0 Deployed to Reflex",
                    "january 16, 2025",
                    [
                        changelog_badge("party-popper", "ReflexUI v1.0.0"),
                    ],
                ),
                wrapper("Initial Release", "january 16, 2025"),
                **ChangelogStyle.content,
            ),
            width="100%",
            align_items="center",
            justify_content="center",
            display="flex",
            padding="0px 24px",
        ),
        **ChangelogStyle.base,
    )
