import reflex as rx

from ...wrappers.component.state import ComponentWrapperState


data = [
    {"month": "Jan", "desktop": 186},
    {"month": "Feb", "desktop": 305},
    {"month": "Mar", "desktop": 237},
    {"month": "Apr", "desktop": 73},
    {"month": "May", "desktop": 209},
    {"month": "Jun", "desktop": 214},
]


def linechart_v3():
    return rx.center(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Line Chart - Type Linear With Label", size="5", weight="bold"
                ),
                rx.text("January - June 2024", size="1", color=rx.color("slate", 11)),
                spacing="1",
            ),
            rx.divider(height="1rem", opacity="0"),
            rx.recharts.line_chart(
                rx.recharts.graphing_tooltip(
                    label_style={"fontWeight": "700"}, item_style={"padding": "0px"}
                ),
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    fill_opacity=0.5,
                    stroke=rx.color("slate", 5),
                ),
                rx.recharts.line(
                    rx.recharts.label_list(position="top", offset=20),
                    data_key="desktop",
                    stroke=ComponentWrapperState.default_theme[1],
                    stroke_width=2,
                    type_="linear",
                    dot=True,
                ),
                rx.recharts.x_axis(
                    data_key="month",
                    axis_line=False,
                ),
                data=data,
                width="100%",
                height=300,
                margin={"left": 20, "right": 20, "top": 20},
            ),
            rx.vstack(
                rx.heading("Trending up by 5.2% this month", size="3", weight="bold"),
                rx.text(
                    "Showing total visitors for the last 6 months",
                    size="1",
                    color=rx.color("slate", 11),
                ),
                spacing="1",
            ),
            width="100%",
            margin_right="10px",
        ),
        width="100%",
        padding="12px",
    )
