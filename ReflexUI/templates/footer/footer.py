import reflex as rx

from .style import FooterStyle
from ...states.routing import SiteRoutingState


def create_footer_item(title: str, routes: list[dict[str, str]]):
    def item(data):
        return rx.hstack(
            rx.link(
                rx.text(
                    data["name"], size="1", weight="bold", color=rx.color("slate", 12)
                ),
                href=data["path"],
                text_decoration="none",
                on_click=SiteRoutingState.toggle_page_change(data),
            ),
            rx.cond(
                data["is_beta"],
                rx.badge("In Progress", color_scheme="orange"),
                rx.cond(
                    data["is_new"],
                    rx.badge("New", color_scheme="grass"),
                    rx.spacer(),
                ),
            ),
            width="100%",
            align="center",
        )

    return rx.vstack(
        rx.text(title, weight="bold", size="1", color=rx.color("gray", 11)),
        rx.hstack(rx.foreach(routes, item), **FooterStyle.footer_item),
        width="100%",
        padding="0.5em 0em",
        spacing="2",
    )


def footer():
    return rx.vstack(
        create_footer_item("Home", SiteRoutingState.GettingStartedRoutes),
        create_footer_item(
            "Interactive Applications", SiteRoutingState.InteractiveRoutes
        ),
        create_footer_item("Charts UI", SiteRoutingState.ChartRoutes),
        create_footer_item("UIs", SiteRoutingState.uisRoutes),
        create_footer_item("Resources", SiteRoutingState.ResourcesRoutes),
        rx.divider(height="2em", opacity="0"),
        rx.vstack(
            rx.heading("ReflexUI", size="3", font_weight="900"),
            rx.text(
                "© 2024 chaseme24 & sumangal44. All rights reserved.",
                size="1",
                weight="bold",
                color=rx.color("gray", 11),
            ),
            width="100%",
            spacing="2",
        ),
        **FooterStyle.base,
    )


def desktop_footer():
    return rx.vstack(
        rx.vstack(
            rx.heading("ReflexUI", size="3", font_weight="900"),
            rx.text(
                "© 2024 chaseme24 & sumangal44. All rights reserved.",
                size="1",
                weight="bold",
                color=rx.color("gray", 11),
            ),
            spacing="2",
            width="100%",
        ),
        **FooterStyle.base,
    )
