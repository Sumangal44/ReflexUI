import reflex as rx

from .wrappers.base import base

from .routes.routes import Routes

from .pantry.exports import pantry_exports_config
from .charts.exports import charts_exports_config
from .pages.started_items.exports import getting_started_config
from .pages.interactive.exports import interactive_config
from .pages.landing.hero import landing_page


AppFontURL: str = (
    "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap"
)

app = rx.App(
    stylesheets=[AppFontURL],
    style={rx.heading: {"font_family": "Inter"}, rx.text: {"font_family": "Inter"}},
)


def get_exports(directory, config_file):
    return [export() for export in config_file[directory]]


def add_routes(routes, export_config):
    for route in routes:

        @base(route["path"], route["name"])
        def export_page() -> callable:
            if route["name"] == "Standard Tables":
                return get_exports(route["dir"], export_config)[:1]
            elif route["name"] == "Table Pagination":
                return get_exports(route["dir"], export_config)[1:]
            return get_exports(route["dir"], export_config)

        app.add_page(
            export_page(), route=route["path"], title=f"{route['name']} - Reflex UI"
        )


# ... set the DEV var to True for faster hot reload
# ... ... change the ENV to match the page in progress
DEV: bool = False

if DEV:

    ENV = {
        "path": "/pantry/footers/",
        "name": "Footers",
        "dir": "footers",
        "config": pantry_exports_config,
    }

    @base(ENV["path"], ENV["name"])
    def __() -> callable:
        return [export() for export in ENV["config"][ENV["dir"]]]

    app.add_page(landing_page(), route="/", title="Reflex UI")
    app.add_page(__(), route=ENV["path"], title=f"{ENV['name']} - Reflex UI")


else:
    app.add_page(landing_page(), route="/", title="Reflex UI")
    add_routes(Routes.interactive, interactive_config)
    add_routes(Routes.pantries, pantry_exports_config)
    add_routes(Routes.charts, charts_exports_config)
    add_routes(Routes.started, getting_started_config)
