from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Routes:
    landing: dict[str, str] = field(default_factory=lambda: {"path": "/"})

    started: List[Dict[str, str]] = field(
        default_factory=lambda: [
            {
                "name": "Introduction",
                "path": "/getting-started/introduction",
                "dir": "introduction",
            },
            {
                "name": "Installation",
                "path": "/getting-started/installation",
                "dir": "installation",
            },
            {
                "name": "Who is Buridan?",
                "path": "/getting-started/who-is-buridan",
                "dir": "buridan",
            },
            {
                "name": "Changelog",
                "path": "/getting-started/changelog",
                "dir": "changelog",
            },
        ]
    )

    interactive: List[Dict[str, str]] = field(
        default_factory=lambda: [
            {
                "name": "RAG Application",
                "path": "/interactive/retrieval-augmented-generation",
                "dir": "rag",
            },
            {
                "name": "PubMed Application",
                "path": "/interactive/pubmed-ai",
                "dir": "pubmed",
                "is_new": True,
            },
        ]
    )

    pantries: List[Dict[str, str]] = field(
        default_factory=lambda: [
            {"name": "Logins", "path": "/ui/logins", "dir": "logins"},
            {
                "name": "Standard Forms",
                "path": "/ui/standard-forms",
                "dir": "forms",
            },
            {
                "name": "Standard Tables",
                "path": "/ui/standard-tables",
                "dir": "tables",
            },
            {
                "name": "Pricing Sections",
                "path": "/ui/pricing-sections",
                "dir": "pricing",
            },
            {
                "name": "Popups",
                "path": "/ui/popups",
                "dir": "popups",
            },
            {
                "name": "Payments & Billing",
                "path": "/ui/payments-and-billing",
                "dir": "payments",
            },
            {
                "name": "Table Pagination",
                "path": "/ui/table-pagination",
                "dir": "tables",
            },
            {
                "name": "Onboarding & Progress",
                "path": "/ui/onboarding-and-progress",
                "dir": "onboardings",
            },
            {
                "name": "Menus",
                "path": "/ui/menus",
                "dir": "menus",
            },
            {
                "name": "Backgrounds",
                "path": "/ui/backgrounds",
                "dir": "backgrounds",
            },
            {
                "name": "Featured",
                "path": "/ui/featured",
                "dir": "featured",
            },
            {
                "name": "Descriptive Lists",
                "path": "/ui/descriptive-lists",
                "dir": "lists",
            },
            {
                "name": "Timeline",
                "path": "/ui/timeline",
                "dir": "timeline",
            },
            {
                "name": "Animations",
                "path": "/ui/animations",
                "dir": "animations",
            },
            {
                "name": "Prompt Boxes",
                "path": "/ui/prompt-boxes",
                "dir": "prompts",
            },
            {
                "name": "Cards",
                "path": "/ui/cards",
                "dir": "cards",
            },
            {
                "name": "Subscribe",
                "path": "/ui/subscribe",
                "dir": "subscribe",
            },
            {
                "name": "Frequently Asked Questions",
                "path": "/ui/frequently-asked-questions",
                "dir": "faq",
            },
            {
                "name": "Footers",
                "path": "/ui/footers",
                "dir": "footers",
            },
            {
                "name": "Inputs",
                "path": "/ui/inputs",
                "dir": "inputs",
                "is_new": True,
            },
        ]
    )

    charts: List[Dict[str, str]] = field(
        default_factory=lambda: [
            {"name": "Bar Charts", "path": "/charts/bar-charts", "dir": "bar"},
            {"name": "Area Charts", "path": "/charts/area-charts", "dir": "area"},
            {"name": "Line Charts", "path": "/charts/line-charts", "dir": "line"},
            {
                "name": "Pie Charts",
                "path": "/charts/pie-charts",
                "dir": "pie",
                "is_new": True,
            },
        ]
    )

    resources: List[Dict[str, str]] = field(
        default_factory=lambda: [
            {"name": "Reflex Framework", "path": "https://reflex.dev/"},
            {"name": "Source Code", "path": "https://github.com/chaseme24/ReflexUI"},
            {"name": "GitHub", "path": "https://github.com/chaseme24"},
            {"name": "@LineIndent", "path": "https://www.youtube.com/@DasiCodeDaires"},
        ]
    )


@dataclass
class NavigationRoutes:
    base: List[Dict[str, str]] = field(
        default_factory=lambda: [
            {"name": "Home", "path": "/"},
            {"name": "Getting Started", "path": GettingStartedRoutes[0]["path"]},
            {"name": "Interactive Apps", "path": InteractiveRoutes[0]["path"]},
            {"name": "ui", "path": PantryRoutes[0]["path"]},
            {"name": "Charts", "path": ChartRoutes[0]["path"]},
        ]
    )


Routes: Routes = Routes()

GettingStartedRoutes: List[Dict[str, str]] = Routes.started
InteractiveRoutes: List[Dict[str, str]] = Routes.interactive
PantryRoutes: List[Dict[str, str]] = sorted(Routes.pantries, key=lambda x: x["name"])
ChartRoutes: List[Dict[str, str]] = sorted(Routes.charts, key=lambda x: x["name"])
ResourcesRoutes: List[Dict[str, str]] = Routes.resources

NavigationRoutes: List[Dict[str, str]] = NavigationRoutes().base
