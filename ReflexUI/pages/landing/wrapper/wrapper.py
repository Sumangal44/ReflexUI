from typing import Literal, Callable

import reflex as rx
from  ....states.routing import SiteRoutingState 

from .style import LandingPageSectionWrapperStyle , LandingPageButtons

ButtonStyle = Literal["classic", "ghost", "outline", "soft", "solid", "surface"]

keyDisplay = ["none" if i <= 2 else "flex" for i in range(6)]

button: Callable[[str, str, ButtonStyle, callable], rx.Component] = (
    lambda tag, name, style, func: rx.button(
        rx.icon(tag=tag, size=18),
        rx.text(name, size="2", weight="bold"),
        on_click=func,
        variant=style,
        **LandingPageButtons.base,
    )
)

button_with_key: Callable[[str, str, str, ButtonStyle, callable], rx.Component] = (
    lambda tag, cmd, name, style, func: rx.button(
        rx.icon(tag=tag, size=18),
        rx.text(name, size="2", weight="bold"),
        rx.badge(
            rx.text(cmd),
            width="20px",
            height="20px",
            variant="soft",
            box_shadow="0px 2px 8px 0px rgba(0, 0, 0, 0.25)",
        ),
        on_click=func,
        variant=style,
        **LandingPageButtons.base,
    )
)

# def landing_page_main_button(name: str, style: ButtonStyle, **kwargs) -> rx.button:
#     return rx.button(name, variant=style, cursor="pointer", **kwargs)


def landing_page_section_wrapper(
    badge: str,
    title: str,
    subtitle: str,
    link: str,
    path: str,
    components: list[rx.Component] = [],
) -> rx.vstack:
    return rx.vstack(
        # ... badge, title, subtitle, and link
        rx.vstack(
            rx.badge(badge, variant="surface", size="3"),
            rx.heading(title, font_weight="900", size="8"),
            rx.text(subtitle),
            rx.link(link, href=path),
            **LandingPageSectionWrapperStyle.titles_secondary,
        ),
        *components,
        # ... wrapper style
        **LandingPageSectionWrapperStyle.wrapper_secondary,
    )

def landing_page_section_wrapper_main(
    badge: str, title: str, subtitle: str
) -> rx.vstack:
    return rx.vstack(
        # ... badge, title, subtitle, and link
        rx.vstack(
            rx.badge(badge, variant="surface", size="3"),
            rx.heading(title, font_weight="900", size="9"),
            rx.text(subtitle),
            rx.hstack(
                button(
                    "component",
                    "Explore Pantry",
                    "solid",
                    SiteRoutingState.toggle_page_change({"name": "Animations", "path": "/pantry/animations"})
                    
                )
                ,
                button(
                    "component",
                    "Get Started",
                    "solid",
                    SiteRoutingState.toggle_page_change({"name": "Getting Started", "path": "/getting-started/introduction"})
                ),
            ),

            **LandingPageSectionWrapperStyle.titles,
        ),
        # ... wrapper style
        min_height="60vh",
        **LandingPageSectionWrapperStyle.wrapper,
    )


def blip(tag: str) -> rx.box:
    return rx.box(
        rx.icon(tag=tag, size=12),
        **LandingPageSectionWrapperStyle.blip
    )


def landing_page_features_wrapper(
    subtitle: str, title: str, tag: str, components: list[rx.Component] = []
) -> rx.hstack:
    return rx.hstack(
        rx.vstack(
            rx.vstack(
                rx.hstack(
                    blip(tag),
                    rx.text(title, size="3", font_weight="900"),
                ),
                rx.text(
                    subtitle,
                    size="4",
                ),
                spacing="1",
            ),
            *components,
        ),
        **LandingPageSectionWrapperStyle.features,
    )
