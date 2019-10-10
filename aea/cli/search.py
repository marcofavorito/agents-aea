# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
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

"""Implementation of the 'aea add' subcommand."""
from pathlib import Path

import click

from aea.cli.common import Context, pass_ctx, _try_to_load_agent_config


@click.group()
@pass_ctx
def search(ctx: Context):
    """Add a resource to the agent."""
    _try_to_load_agent_config(ctx)


@search.command()
@pass_ctx
def connections(ctx: Context):
    """List all the available connections."""
    registry_path = ctx.agent_config.registry_path
    for c in Path(registry_path).glob("connections/[!_]*"):
        print(c.name)


@search.command()
@pass_ctx
def protocols(ctx: Context):
    """List all the available connections."""
    registry_path = ctx.agent_config.registry_path
    for c in Path(registry_path).glob("protocols/[!_]*"):
        print(c.name)


@search.command()
@pass_ctx
def skills(ctx: Context):
    """List all the available connections."""
    registry_path = ctx.agent_config.registry_path
    for c in Path(registry_path).glob("skills/[!_]*"):
        print(c.name)
