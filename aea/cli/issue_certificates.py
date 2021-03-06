# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2020 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Implementation of the 'aea issue_certificates' subcommand."""
import os
from typing import Dict, List, cast

import click
from click import ClickException

from aea.cli.utils.context import Context
from aea.cli.utils.decorators import check_aea_project
from aea.cli.utils.loggers import logger
from aea.cli.utils.package_utils import get_dotted_package_path_unified
from aea.configurations.base import PublicId
from aea.configurations.constants import CONNECTION
from aea.configurations.manager import AgentConfigManager, VariableDoesNotExist
from aea.crypto.helpers import make_certificate
from aea.crypto.registries import crypto_registry
from aea.exceptions import enforce
from aea.helpers.base import CertRequest


@click.command()
@click.pass_context
@check_aea_project
def issue_certificates(click_context):
    """Issue certificates for connections that require them."""
    ctx = cast(Context, click_context.obj)
    issue_certificates_(ctx)


def issue_certificates_(ctx: Context):
    """Issue certificates for connections that require them."""
    agent_config_manager = AgentConfigManager.load(ctx.cwd)

    # agent_config_manager.
    for connection_id in agent_config_manager.agent_config.connections:
        _process_connection(ctx, agent_config_manager, connection_id)

    click.echo("All certificates have been issued.")


def _process_certificate(
    ctx: Context, cert_request: CertRequest, connection_id: PublicId
):
    """Process a single certificate request."""
    ledger_id = cert_request.ledger_id
    output_path = cert_request.save_path
    if cert_request.key_identifier is not None:
        key_identifier = cert_request.key_identifier
        connection_private_key_path = ctx.agent_config.connection_private_key_paths.read(
            key_identifier
        )
        if connection_private_key_path is None:
            raise ClickException(
                f"Cannot find connection private key with id '{key_identifier}'. Connection '{connection_id}' requires this. Please use `aea generate-key {key_identifier} connection_{key_identifier}_private_key.txt` and `aea add-key {key_identifier} connection_{key_identifier}_private_key.txt --connection` to add a connection private key with id '{key_identifier}'."
            )
        connection_crypto = crypto_registry.make(
            key_identifier, private_key_path=connection_private_key_path
        )
        public_key = connection_crypto.public_key
    else:
        public_key = cast(str, cert_request.public_key)
        enforce(
            public_key is not None,
            "Internal error - one of key_identifier or public_key must be not None.",
        )
    crypto_private_key_path = ctx.agent_config.private_key_paths.read(ledger_id)
    if crypto_private_key_path is None:
        raise ClickException(
            f"Cannot find private key with id '{ledger_id}'. Please use `aea generate-key {key_identifier}` and `aea add-key {key_identifier}` to add a private key with id '{key_identifier}'."
        )
    message = cert_request.get_message(public_key)
    cert = make_certificate(
        ledger_id, crypto_private_key_path, message, os.path.join(ctx.cwd, output_path)
    )
    click.echo(f"Generated signature: '{cert}'")


def _process_connection(
    ctx: Context, agent_config_manager: AgentConfigManager, connection_id: PublicId
):
    path = get_dotted_package_path_unified(ctx, CONNECTION, connection_id)
    path_to_cert_requests = f"{path}.cert_requests"

    try:
        cert_requests = agent_config_manager.get_variable(path_to_cert_requests)
    except VariableDoesNotExist:
        logger.debug("No certificates to process.")
        return

    logger.debug(f"Processing connection '{connection_id}'...")
    cert_requests = cast(List[Dict], cert_requests)
    for cert_request_json in cert_requests:
        cert_request = CertRequest.from_json(cert_request_json)
        click.echo(
            f"Issuing certificate '{cert_request.identifier}' for connection {connection_id}..."
        )
        _process_certificate(ctx, cert_request, connection_id)
        click.echo(
            f"Dumped certificate '{cert_request.identifier}' in '{cert_request.save_path}' for connection {connection_id}."
        )
