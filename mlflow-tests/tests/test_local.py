"""Standalone connection and MCP registry checks using existing credentials."""

import pytest

from .actions.mcp_actions import (
    action_create_mcp_server,
    action_delete_mcp_server,
    action_get_mcp_server,
    action_search_mcp_servers,
)
from .base import TestBase
from .constants.config import Config
from .shared import TestData, TestStep
from .validations.mcp_validations import (
    validate_mcp_server_created,
    validate_mcp_server_deleted,
    validate_mcp_server_retrieved,
)

pytestmark = pytest.mark.skipif(not Config.LOCAL, reason="Requires LOCAL=true")


def validate_server_in_search(context):
    assert context.active_mcp_server_name in {
        server.name for server in context.mcp_server_search_results
    }


class TestLocalDeployment(TestBase):
    def test_connection(self):
        self.admin_client.search_experiments(max_results=1)

    @pytest.mark.MCPRegistry
    def test_mcp_server_lifecycle(self):
        self._execute_test_steps(TestData(
            test_name="Standalone MCP server lifecycle",
            test_steps=[
                TestStep(action_func=action_create_mcp_server, validate_func=validate_mcp_server_created),
                TestStep(action_func=action_get_mcp_server, validate_func=validate_mcp_server_retrieved),
                TestStep(action_func=action_search_mcp_servers, validate_func=validate_server_in_search),
                TestStep(action_func=action_delete_mcp_server, validate_func=validate_mcp_server_deleted),
            ],
        ))
