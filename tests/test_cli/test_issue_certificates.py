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
"""This test module contains tests for 'issue-certificates' command."""
import os
import shutil
from pathlib import Path
from typing import List

import pytest

from aea.cli.utils.config import dump_item_config
from aea.helpers.base import CertRequest
from aea.test_tools.test_cases import AEATestCaseEmpty

from tests.conftest import (
    CUR_PATH,
    FETCHAI,
    FETCHAI_PRIVATE_KEY_FILE,
    FETCHAI_PRIVATE_KEY_PATH,
)
from tests.data.dummy_connection.connection import DummyConnection


class BaseTestIssueCertificates(AEATestCaseEmpty):
    """Base test class for 'aea issue-certificates' tests."""

    @classmethod
    def setup_class(cls):
        """Set up the class."""
        super().setup_class()

        # add dummy connection
        shutil.copytree(
            os.path.join(CUR_PATH, "data", "dummy_connection"),
            os.path.join(cls.current_agent_context, "connections", "dummy"),
        )
        agent_config = cls.load_agent_config(cls.agent_name)
        agent_config.author = FETCHAI
        agent_config.connections.add(DummyConnection.connection_id)
        dump_item_config(agent_config, Path(cls.current_agent_context))

    @classmethod
    def add_cert_requests(cls, cert_requests: List[CertRequest], connection_name: str):
        """Add certificate requests to a target connection."""
        cls.nested_set_config(
            f"connections.{connection_name}.cert_requests", cert_requests
        )


class TestIssueCertificatesPositive(BaseTestIssueCertificates):
    """Test 'issue-certificates', positive case."""

    @classmethod
    def setup_class(cls):
        """Set up the class."""
        super().setup_class()

        cls.expected_path_1 = os.path.abspath("path_1")
        cls.expected_path_2 = os.path.abspath("path_2")
        cls.cert_id_1 = "cert_id_1"
        cls.cert_id_2 = "cert_id_2"
        cls.cert_request_1 = CertRequest(
            identifier=cls.cert_id_1,
            ledger_id=FETCHAI,
            not_after="2020-01-02",
            not_before="2020-01-01",
            public_key=FETCHAI,
            save_path=cls.expected_path_1,
        )
        cls.cert_request_2 = CertRequest(
            identifier=cls.cert_id_2,
            ledger_id=FETCHAI,
            not_after="2020-01-02",
            not_before="2020-01-01",
            public_key="0xABCDEF123456",
            save_path=cls.expected_path_2,
        )
        cls.add_cert_requests(
            [cls.cert_request_1, cls.cert_request_2], DummyConnection.connection_id.name
        )

        # add fetchai key and connection key
        shutil.copy(
            FETCHAI_PRIVATE_KEY_PATH,
            os.path.join(cls.current_agent_context, FETCHAI_PRIVATE_KEY_FILE),
        )
        cls.add_private_key()
        cls.add_private_key(connection=True)

    def test_issue_certificate(self):
        """Test 'aea issue-certificates' in case of success."""
        result = self.run_cli_command("issue-certificates", cwd=self._get_cwd())
        self._check_signature(self.cert_id_1, self.expected_path_1, result.stdout)
        self._check_signature(self.cert_id_2, self.expected_path_2, result.stdout)

    def _check_signature(self, cert_id, filename, stdout):
        """Check signature has been generated correctly."""
        path = Path(self.current_agent_context, filename)
        assert path.exists()
        signature = path.read_text()

        def is_ascii(s):
            """Check isascii method for all Python 3 versions"""
            return all(ord(c) < 128 for c in s)

        assert is_ascii(signature)
        int(signature, 16)  # this will fail if not hexadecimal

        cert_msg_1 = (
            f"Issuing certificate '{cert_id}' for connection fetchai/dummy:0.1.0..."
        )
        cert_msg_3 = f"Generated signature: '{signature}'"
        cert_msg_2 = f"Dumped certificate '{cert_id}' in '{filename}' for connection fetchai/dummy:0.1.0."
        assert cert_msg_1 in stdout
        assert cert_msg_2 in stdout
        assert cert_msg_3 in stdout


class TestIssueCertificatesWrongConnectionKey(BaseTestIssueCertificates):
    """Test 'aea issue-certificates' when a bad connection key id is provided."""

    @classmethod
    def setup_class(cls):
        """Set up class."""
        super().setup_class()
        cls.cert_id_1 = "cert_id_1"
        cls.cert_request_1 = CertRequest(
            identifier=cls.cert_id_1,
            ledger_id=FETCHAI,
            not_after="2020-01-02",
            not_before="2020-01-01",
            public_key="bad_ledger_id",
            save_path="path",
        )
        cls.add_cert_requests([cls.cert_request_1], DummyConnection.connection_id.name)

    def test_run(self):
        """Run the test."""
        with pytest.raises(
            Exception,
            match="Cannot find connection private key with id 'bad_ledger_id'",
        ):
            self.run_cli_command("issue-certificates", cwd=self._get_cwd())


class TestIssueCertificatesWrongCryptoKey(BaseTestIssueCertificates):
    """Test 'aea issue-certificates' when a bad crypto key id is provided."""

    @classmethod
    def setup_class(cls):
        """Set up class."""
        super().setup_class()
        cls.cert_id_1 = "cert_id_1"
        cls.cert_request_1 = CertRequest(
            identifier=cls.cert_id_1,
            ledger_id="bad_ledger_id",
            not_after="2020-01-02",
            not_before="2020-01-01",
            public_key=FETCHAI,
            save_path="path",
        )
        cls.add_cert_requests([cls.cert_request_1], DummyConnection.connection_id.name)
        # add fetchai key and connection key
        cls.generate_private_key()
        cls.add_private_key()
        cls.add_private_key(connection=True)

    def test_run(self):
        """Run the test."""
        with pytest.raises(
            Exception, match="Cannot find private key with id 'bad_ledger_id'",
        ):
            self.run_cli_command("issue-certificates", cwd=self._get_cwd())
