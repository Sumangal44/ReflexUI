import asyncio
import reflex as rx
from reflex.constants.colors import Color

from ...routes.routes import (
    GettingStartedRoutes,
    InteractiveRoutes,
    PantryRoutes,
    ChartRoutes,
    ResourcesRoutes,
)


active: dict[str, Color] = {"color": rx.color("slate", 12)}
passive: dict[str, Color] = {"color": rx.color("slate", 11)}


class SideMenuState(rx.State):
    GettingStartedRoutes: list[dict[str, str]] = [
        {**route, **passive} for route in GettingStartedRoutes
    ]
    InteractiveRoutes: list[dict[str, str]] = [
        {**route, **passive} for route in InteractiveRoutes
    ]
    ChartRoutes: list[dict[str, str]] = [{**route, **passive} for route in ChartRoutes]
    PantryRoutes: list[dict[str, str]] = [
        {**route, **passive} for route in PantryRoutes
    ]
    ResourcesRoutes: list[dict[str, str]] = [
        {**route, **passive} for route in ResourcesRoutes
    ]

    async def toggle_page_change(self, data: dict[str, str]):
        if data is not None:
            await asyncio.gather(
                self.update_menu_link(self.GettingStartedRoutes, data),
                self.update_menu_link(self.InteractiveRoutes, data),
                self.update_menu_link(self.ChartRoutes, data),
                self.update_menu_link(self.PantryRoutes, data),
            )

        # on_page = (
        #     data["path"].split("/")[1]
        #     if data["path"].startswith("/")
        #     else data["path"].split("/")[0]
        # )

    async def update_menu_link(self, menu: list[dict[str, str]], item: dict[str, str]):
        for index in menu:
            if index["name"] == item["name"]:
                index["color"] = active["color"]

            else:
                index["color"] = passive["color"]
