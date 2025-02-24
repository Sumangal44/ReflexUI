import reflex as rx
from reflex.constants.colors import Color
from typing_extensions import Callable

from .style import NavigationStyle
from ...templates.drawer.state import DrawerState
from ...states.routing import SiteRoutingState


nav_icon: Callable[[rx.Component], rx.badge] = lambda component: rx.badge(
    component,
    color_scheme="gray",
    variant="soft",
    width="21px",
    height="21px",
    display="flex",
    align_items="center",
    justify_content="center",
    background="none",
)

theme = nav_icon(
    rx.el.button(
        rx.color_mode.icon(
            light_component=rx.icon(
                "moon",
                size=14,
                color=rx.color("slate", 12),
            ),
            dark_component=rx.icon(
                "sun",
                size=14,
                color=rx.color("slate", 12),
            ),
        ),
        on_click=rx.toggle_color_mode,
    )
)

github = nav_icon(
    rx.link(
        rx.icon(
            tag="github",
            size=14,
            color=rx.color("slate", 12),
        ),
        href="https://github.com/chaseme24/ReflexUI",
        display=["none", "none", "none", "none", "none", "flex"],
    ),
)


def navigation_links(data: dict[str, str | Color]):
    return rx.link(
        rx.text(data["name"], size="1", weight="bold", color=rx.color("slate", 12)),
        href=data["path"],
        text_decoration="none",
        on_click=SiteRoutingState.toggle_page_change(data),
    )


def navigation_right_side_items():
    return rx.hstack(
        rx.hstack(
            rx.foreach(SiteRoutingState.NavigationRoutes, navigation_links),
            display=["none", "none", "none", "none", "none", "flex"],
            align="center",
        ),
        rx.divider(
            orientation="vertical",
            height="30px",
            width="0.75px",
            color_scheme="gray",
            display=["none", "none", "none", "none", "none", "flex"],
            margin="0em 0.5em",
        ),
        rx.hstack(github, theme, align="center", spacing="2"),
        rx.button(
            rx.icon(tag="align-justify", size=15),
            on_click=DrawerState.toggle_drawer,
            size="1",
            variant="soft",
            color_scheme="gray",
            cursor="pointer",
            display=["flex", "flex", "flex", "flex", "flex", "none"],
        ),
        align="center",
    )


def navigation_left_side_items():
    return rx.hstack(
        rx.image(src="/logo.jpg", **NavigationStyle.logo),
        rx.heading(
            "ReflexUI",
            font_size="1em",
            font_weight="900",
            cursor="pointer",
            on_click=[
                SiteRoutingState.toggle_page_change({"name": "Home", "path": "/"}),
                rx.redirect("/"),
            ],
        ),
        align="center",
        spacing="2",
    )


def navigation():
    return rx.hstack(
        navigation_left_side_items(),
        navigation_right_side_items(),
        **NavigationStyle.base,
    )


def docs_navigation():
    return rx.hstack(
        navigation_left_side_items(),
        rx.hstack(
            rx.hstack(github, theme, align="center", spacing="2"),
            rx.button(
                rx.icon(tag="align-justify", size=15),
                on_click=DrawerState.toggle_drawer,
                size="1",
                variant="soft",
                color_scheme="gray",
                cursor="pointer",
                display=["flex", "flex", "flex", "flex", "flex", "none"],
            ),
            align="center",
        ),
        **NavigationStyle.base,
    )


def landing_page_navigation():
    return rx.hstack(
        navigation_left_side_items(),
        navigation_right_side_items(),
        **NavigationStyle.landing_page_nav,
    )
