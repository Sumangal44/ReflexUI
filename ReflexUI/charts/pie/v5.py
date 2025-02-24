import reflex as rx
from typing import Callable

from ...wrappers.component.state import ComponentWrapperState


data = [
    {"browser": "chrome", "visitors": 275},
    {"browser": "safari", "visitors": 200},
    {"browser": "firefox", "visitors": 187},
    {"browser": "edge", "visitors": 173},
    {"browser": "other", "visitors": 90},
]

data = [
    {**item, "fill": rx.color(ComponentWrapperState.selected_theme, index + 5)}
    for index, item in enumerate(data)
]


info: Callable[[str, str, str], rx.Component] = (
    lambda title, titleSize, subtitle: rx.vstack(
        rx.heading(title, size=titleSize, weight="bold"),
        rx.text(subtitle, size="3", color=rx.color("slate", 11), weight="medium"),
        spacing="1",
        width="100%",
        align="center",
    )
)


def piechart_v5():
    return rx.vstack(
        info("Pie Chart - Doughnut", "6", "January - June 2024"),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=data,
                data_key="visitors",
                name_key="browser",
                stroke="0",
                inner_radius="60%",
                active_index=0,
            ),
            rx.recharts.pie(outer_radius="50%"),
            rx.recharts.graphing_tooltip(),
            width="100%",
            height=400,
        ),
        info(
            "Trending up by 5.2% this month",
            "4",
            "Showing total visitors for the last 6 months",
        ),
        width="100%",
        align="center",
        padding="1em 0em",
        spacing="1",
    )
