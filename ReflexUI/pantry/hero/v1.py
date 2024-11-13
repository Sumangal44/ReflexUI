import reflex as rx
from dataclasses import dataclass, field

# @dataclass
# class HeroStyle:
#     base: dict[str, str] = field(
#         default_factory=lambda: {
#             "width": "100%",
#             "padding": "4em 1em",
#             "justify": "center",
#             "align": "center",
#             "text_align": "center",

#         }
#     )
#     heading: dict[str, str] = field(
#         default_factory=lambda: {
#             "font_size": "2.5em",
#             "font_weight": "bold",
#             "margin_bottom": "0.5em",
#             "color": "#333",
#         }
#     )
#     subtitle: dict[str, str] = field(
#         default_factory=lambda: {
#             "font_size": "1.25em",
#             "color": "#555",
#             "margin_bottom": "1.5em",
#         }
#     )
#     button: dict[str, str] = field(
#         default_factory=lambda: {
#             "padding": "0.75em 2em",
#             "font_size": "1em",
#             "border_radius": "5px",
#             "cursor": "pointer",
#             "background_color": "#007bff",
#             "color": "#fff",
#             "hover": {
#                 "background_color": "#0056b3",
#             },
#         }
#     )

# HeroStyle = HeroStyle()

def hero_v1():
    return rx.center(
        rx.vstack(
            rx.heading("Welcome to Our Platform", size="6", weight="bold", margin="0" ),
            rx.text(
                "We provide innovative solutions to help you succeed. Join us today to unlock new possibilities!",
                size="2",
                margin="0",

                # **HeroStyle.subtitle
            ),
            rx.button(

                "Get Started",
                color_scheme="blue",
                variant="solid",
                cursor="pointer",
                size="3",
                height="40px",
                border_radius="8px",
                padding="8px 16px",
                spacing="0",
                justify="center",
                align="center",
                border=f"1px solid {rx.color('blue', 6)}",
                bg=rx.color("blue", 3),
                font_size="12px",
                font_weight="bold",
                _hover={
                    "bg": rx.color("blue", 4),
                    "border": f"1px solid {rx.color('blue', 5)}",
                },
                _active={
                    "bg": rx.color("blue", 5),
                    "border": f"1px solid {rx.color('blue', 6)}",
                },
                _disabled={
                    
                }

                

                # **HeroStyle.button
            ),
            spacing="1em",
            align="center",
            width="100%",
        ),
        background_size="100px 100px",
        background_image="linear-gradient(hsl(0, 0%, 39%) 1px, transparent 1px), linear-gradient(to right, transparent 99%, hsl(0, 0%, 39%) 100%)",
        mask="radial-gradient(50% 100% at 50% 50%, hsl(0, 0%, 0%, 1), hsl(0, 0%, 0%, 0))",
        width="100%",
        height="65vh",

        # **HeroStyle.base
    )
