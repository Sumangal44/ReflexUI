import reflex as rx

def button_v2():
    return rx.button(
        rx.text("Click Me"),
        variant="ghost",
        color_scheme="red",
        cursor="pointer",
        width="100%",
        height="40px",
        border_radius="8px",
        padding="8px 16px",
        spacing="0",
        justify="center",
        align="center",
        border=f"1px solid {rx.color('red', 6)}",
        bg=rx.color("red", 3),
        font_size="12px",
        font_weight="bold",
        _hover={
            "bg": rx.color("red", 4),
            "border": f"1px solid {rx.color('red', 5)}",
        },
        _active={
            "bg": rx.color("red", 5),
            "border": f"1px solid {rx.color('red', 6)}",
        },
        _disabled={
            "bg": rx.color("red", 3),
            "border": f"1px solid {rx.color('red', 6)}",
        },
        _loading={
            "bg": rx.color("red", 3),
            "border": f"1px solid {rx.color('red', 6)}",
        },
)

