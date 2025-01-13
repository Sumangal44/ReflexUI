"""App commands for the Reflex Cloud CLI."""

import json
from typing import Optional

import typer
from tabulate import tabulate
from typing_extensions import Annotated

from reflex_cli import constants
from reflex_cli.utils import console
from reflex_cli.utils.exceptions import NotAuthenticatedError

apps_cli = typer.Typer()


@apps_cli.command(name="history")
def app_history(
    app_id: Optional[str] = typer.Argument(None, help="The ID of the application."),
    app_name: Optional[str] = typer.Option(None, help="The name of the application."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in json format."
    ),
    interactive: bool = typer.Option(
        True, "-i", "--interactive", help="Whether to use interactive mode."
    ),
):
    """Retrieve the deployment history for a given application."""
    from reflex_cli.utils import hosting

    console.set_log_level(loglevel)
    try:

        if app_name is not None and app_id is None:
            result = hosting.search_app(
                app_name=app_name, project_id=None, token=token, interactive=interactive
            )
            app_id = result.get("id") if result else None

        if not app_id:
            console.error("No valid app_id or app_name provided.")
            raise typer.Exit(1)

        history = hosting.get_app_history(app_id=app_id, token=token)

        if as_json:
            console.print(json.dumps(history))
            return
        if history:
            headers = list(history[0].keys())
            table = [list(deployment.values()) for deployment in history]
            console.print(tabulate(table, headers=headers))
        else:
            console.print(str(history))
    except NotAuthenticatedError as err:
        console.error("You are not authenticated. Run `reflex login` to authenticate.")
        raise typer.Exit(1) from err


@apps_cli.command("build-logs")
def deployment_build_logs(
    deployment_id: str = typer.Argument(..., help="The ID of the deployment."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
):
    """Retrieve the build logs for a specific deployment."""
    from reflex_cli.utils import hosting

    try:
        logs = hosting.get_deployment_build_logs(
            deployment_id=deployment_id, token=token
        )
        console.print(logs)
    except NotAuthenticatedError as err:
        console.error("You are not authenticated. Run `reflex login` to authenticate.")
        raise typer.Exit(1) from err


@apps_cli.command(name="status")
def deployment_status(
    deployment_id: str = typer.Argument(..., help="The ID of the deployment."),
    watch: Optional[bool] = typer.Option(
        False, help="Whether to continuously watch the status."
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
):
    """Retrieve the status of a specific deployment."""
    from reflex_cli.utils import hosting

    console.set_log_level(loglevel)

    try:
        if watch:
            hosting.watch_deployment_status(deployment_id=deployment_id, token=token)
        else:
            status = hosting.get_deployment_status(
                deployment_id=deployment_id, token=token
            )
            console.error(status) if "failed" in status else console.print(status)
    except NotAuthenticatedError as err:
        console.error("You are not authenticated. Run `reflex login` to authenticate.")
        raise typer.Exit(1) from err


# TODO combine with deployment_status later
# @apps_cli.command(name="status")
# def app_status(
#     app_id: str,
#     token: Optional[str] = None,
#     loglevel: constants.LogLevel = typer.Option(
#         constants.LogLevel.INFO, help="The log level to use."
#     ),
# ):
#     """Retrieve the status of a specific app."""
#     from reflex_cli.utils import hosting

#     console.set_log_level(loglevel)

#     try:
#         status = hosting.get_app_status(app_id=app_id, token=token)
#     except NotAuthenticatedError as err:
#         console.error(
#             "You are not authenticated. Run `reflex login` to authenticate."
#         )
#         raise typer.Exit(1) from err
#     except Exception as e:
#         status = f"Unable to get app status: {e}"

#     console.info(status)


#     return None


@apps_cli.command(name="stop")
def stop_app(
    app_id: Optional[str] = typer.Argument(None, help="The ID of the application."),
    app_name: Optional[str] = typer.Option(None, help="The name of the application."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    interactive: bool = typer.Option(
        True, "-i", "--interactive", help="Whether to use interactive mode."
    ),
):
    """Stop a running application."""
    from reflex_cli.utils import hosting

    console.set_log_level(loglevel)

    try:
        if app_name is not None and app_id is None:
            app_result = hosting.search_app(
                app_name=app_name, project_id=None, token=token, interactive=interactive
            )
            app_id = app_result.get("id") if app_result else None

        if not app_id:
            console.error("No valid app_id or app_name provided.")
            raise typer.Exit(1)

        result = hosting.stop_app(app_id=app_id, token=token)
        if result:
            console.error(result) if "failed" in result else console.success(result)
    except NotAuthenticatedError as err:
        console.error("You are not authenticated. Run `reflex login` to authenticate.")
        raise typer.Exit(1) from err


@apps_cli.command(name="start")
def start_app(
    app_id: Optional[str] = typer.Argument(None, help="The ID of the application."),
    app_name: Optional[str] = typer.Option(None, help="The name of the application."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    interactive: bool = typer.Option(
        True, "-i", "--interactive", help="Whether to use interactive mode."
    ),
):
    """Start a stopped application."""
    from reflex_cli.utils import hosting

    console.set_log_level(loglevel)

    try:
        if app_name is not None and app_id is None:
            app_result = hosting.search_app(
                app_name=app_name, project_id=None, token=token, interactive=interactive
            )
            app_id = app_result.get("id") if app_result else None

        if not app_id:
            console.error("No valid app_id or app_name provided.")
            raise typer.Exit(1)

        result = hosting.start_app(app_id=app_id, token=token)
        if result:
            console.error(result) if "failed" in result else console.success(result)
    except NotAuthenticatedError as err:
        console.error("You are not authenticated. Run `reflex login` to authenticate.")
        raise typer.Exit(1) from err


@apps_cli.command(name="delete")
def delete_app(
    app_id: Optional[str] = typer.Argument(None, help="The ID of the application."),
    app_name: Optional[str] = typer.Option(None, help="The name of the application."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    interactive: bool = typer.Option(
        True, "-i", "--interactive", help="Whether to use interactive mode."
    ),
):
    """Delete an application."""
    from reflex_cli.utils import hosting

    if not app_id:
        console.error("No app_id provided.")
        raise typer.Exit(1)

    console.set_log_level(loglevel)
    try:
        if app_name is not None and app_id is None:
            app_result = hosting.search_app(
                app_name=app_name, project_id=None, token=token, interactive=interactive
            )
            app_id = app_result.get("id") if app_result else None

        if not app_id:
            console.error("No valid app_id or app_name provided.")
            raise typer.Exit(1)

        result = hosting.delete_app(app_id=app_id, token=token)
        if result:
            console.warn(result)
    except NotAuthenticatedError as err:
        console.error("You are not authenticated. Run `reflex login` to authenticate.")
        raise typer.Exit(1) from err


@apps_cli.command(name="logs")
def app_logs(
    app_id: Optional[str] = typer.Argument(
        None,
        help="The ID of the application. If no app_id is provided start/end must both be provided.",
    ),
    app_name: Optional[str] = typer.Option(None, help="The name of the application."),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    offset: Optional[int] = typer.Option(
        None, help="The offset in seconds from the current time."
    ),
    start: Optional[int] = typer.Option(
        None, help="The start time in Unix epoch format."
    ),
    end: Optional[int] = typer.Option(None, help="The end time in Unix epoch format."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    interactive: bool = typer.Option(
        True, "-i", "--interactive", help="Whether to use interactive mode."
    ),
):
    """Retrieve logs for a given application."""
    from reflex_cli.utils import hosting

    if app_name is not None and app_id is None:
        app_result = hosting.search_app(
            app_name=app_name, project_id=None, token=token, interactive=interactive
        )
        app_id = app_result.get("id") if app_result else None

    if not app_id:
        console.error("No valid app_id or app_name provided.")
        raise typer.Exit(1)

    if offset is None and start is None and end is None:
        offset = 3600
    if offset is not None and start or end:
        console.error("must provide both start and end")
        raise typer.Exit(1)

    console.set_log_level(loglevel)

    try:
        result = hosting.get_app_logs(
            app_id=app_id, offset=offset, start=start, end=end, token=token
        )
        if result:
            if isinstance(result, list):
                result.reverse()
                for log in result:
                    console.warn(log)
            else:
                console.warn("Unable to retrieve logs.")
    except NotAuthenticatedError as err:
        console.error("You are not authenticated. Run `reflex login` to authenticate.")
        raise typer.Exit(1) from err


@apps_cli.command(name="list")
def list_apps(
    project_id: Optional[str] = typer.Option(
        None, "--project", help="The project ID to filter deployments."
    ),
    project_name: Optional[str] = typer.Option(
        None,
        help="The name of the project. ",
    ),
    token: Optional[str] = typer.Option(None, help="The authentication token."),
    loglevel: Annotated[
        constants.LogLevel, typer.Option(help="The log level to use.")
    ] = constants.LogLevel.INFO,
    as_json: bool = typer.Option(
        False, "-j", "--json", help="Whether to output the result in JSON format."
    ),
    interactive: bool = typer.Option(
        True,
        help="Whether to list configuration options and ask for confirmation.",
    ),
):
    """List all the hosted deployments of the authenticated user. Will exit if unable to list deployments."""
    from reflex_cli.utils import hosting

    console.set_log_level(loglevel)

    if project_name and not project_id:
        result = hosting.search_project(
            project_name, token=token, interactive=interactive
        )
        project_id = result.get("id") if result else None

    if project_id is None:
        project_id = hosting.get_selected_project()
    try:
        deployments = hosting.list_apps(project=project_id, token=token)
    except Exception as ex:
        console.error("Unable to list deployments")
        raise typer.Exit(1) from ex

    if as_json:
        console.print(json.dumps(deployments))
        return
    if deployments:
        headers = list(deployments[0].keys())
        table = [list(deployment.values()) for deployment in deployments]
        console.print(tabulate(table, headers=headers))
    else:
        console.print(str(deployments))
