import reflex as rx
from dataclasses import dataclass, field

@dataclass
class HeroStyle:
    base: dict[str, str] = field(
        default_factory=lambda: {
            "width": "100%",
            "padding": "4em 1em",
            "justify": "center",
            "align": "center",
            "text_align": "center",
            "background_color": "#f9f9f9",
        }
    )
    heading: dict[str, str] = field(
        default_factory=lambda: {
            "font_size": "2.5em",
            "font_weight": "bold",
            "margin_bottom": "0.5em",
            "color": "#333",
        }
    )
    subtitle: dict[str, str] = field(
        default_factory=lambda: {
            "font_size": "1.25em",
            "color": "#555",
            "margin_bottom": "1.5em",
        }
    )
    button: dict[str, str] = field(
        default_factory=lambda: {
            "padding": "0.75em 2em",
            "font_size": "1em",
            "border_radius": "5px",
            "cursor": "pointer",
            "background_color": "#007bff",
            "color": "#fff",
            "hover": {
                "background_color": "#0056b3",
            },
        }
    )

HeroStyle = HeroStyle()

def hero_v1():
    return rx.vstack(
        rx.vstack(
            rx.heading("Welcome to Our Platform", **HeroStyle.heading),
            rx.text(
                "We provide innovative solutions to help you succeed. Join us today to unlock new possibilities!",
                **HeroStyle.subtitle
            ),
            rx.button(
                "Get Started",
                **HeroStyle.button
            ),
            spacing="1em",
            align="center",
            width="100%",
        ),
        **HeroStyle.base
    )
