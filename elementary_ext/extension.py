"""Meltano elementary extension."""
from __future__ import annotations

import os
import pkgutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import structlog
from meltano.edk import models
from meltano.edk.extension import ExtensionBase
from meltano.edk.process import Invoker, log_subprocess_error

log = structlog.get_logger()


class elementary(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        self.elementary_bin = "edr"  # verify this is the correct name
        self.dbt_project_dir = Path(os.getenv("ELEMENTARY_PROJECT_DIR", "transform"))
        self.dbt_profiles_dir = Path(
            os.getenv("ELEMENTARY_PROFILES_DIR", self.dbt_project_dir / "profiles")
        )
        self.file_path = Path(os.getenv("ELEMENTARY_FILE_PATH", "utilities/elementary/report.html"))
        self.slack_channel_name = Path(
            os.getenv("ELEMENTARY_SLACK_CHANNEL_NAME", "")
        )
        self.slack_channel_token = Path(
            os.getenv("ELEMENTARY_SLACK_CHANNEL_TOKEN", "")
        )
        self.dbt_profiles_dir = Path(
            os.getenv("ELEMENTARY_PROFILES_DIR", self.dbt_project_dir / "profiles")
        )
        # self.skip_pre_invoke = Path(
        #     os.getenv("ELEMENTARY_EXT_SKIP_PRE_INVOKE", "false").lower() == "true"
        # )
        self.elementary_invoker = Invoker(self.elementary_bin, cwd=self.dbt_profiles_dir)



    def pre_invoke(self, invoke_name: str | None, *invoke_args: Any) -> None:
        """Pre-invoke hook.
        Runs `dbt deps` to ensure dependencies are up-to-date on every invocation.
        Args:
            invoke_name: The name of the command that will eventually be invoked.
            invoke_args: The arguments that will be passed to the command.
        """
        if self.skip_pre_invoke:
            log.debug("skipping pre-invoke as DBT_EXT_SKIP_PRE_INVOKE is set")
            return

        if invoke_name in ["deps", "clean"]:
            log.debug("skipping pre-invoke as command being invoked is deps or clean")
            return

        try:
            log.info("Extension executing `dbt clean`...")
            self.dbt_invoker.run_and_log("clean")
        except subprocess.CalledProcessError as err:
            log_subprocess_error(
                "dbt clean", err, "pre invoke step of `dbt clean` failed"
            )
            sys.exit(err.returncode)

        try:
            log.info("Extension executing `dbt deps`...")
            self.dbt_invoker.run_and_log("deps")
        except subprocess.CalledProcessError as err:
            log_subprocess_error(
                "dbt deps", err, "pre invoke step of `dbt deps` failed"
            )
            sys.exit(err.returncode)

    def invoke(self, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.
        """
        try:
            self.elementary_invoker.run_and_log(command_name, *command_args)
        except subprocess.CalledProcessError as err:
            log_subprocess_error(
                f"elementary {command_name}", err, "elementary invocation failed"
            )
            sys.exit(err.returncode)

    def describe(self) -> models.Describe:
        """Describe the extension.

        Returns:
            The extension description
        """
        # TODO: could we auto-generate all or portions of this from typer instead?
        return models.Describe(
            commands=[
                models.ExtensionCommand(
                    name="elementary_extension", description="extension commands"
                ),
                models.InvokerCommand(
                    name="elementary_invoker", description="pass through invoker"
                ),
            ]
        )
