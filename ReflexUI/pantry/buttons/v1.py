import reflex as rx

def button_v1():
    return rx.button(
        rx.text("Button 1"),
        color_scheme="blue",
        variant="soft",
        cursor="pointer",
        width="100%",
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
            "bg": rx.color("blue", 3),
            "border": f"1px solid {rx.color('blue', 6)}",
        },
        _loading={
            "bg": rx.color("blue", 3),
            "border": f"1px solid {rx.color('blue', 6)}",
        },
)

