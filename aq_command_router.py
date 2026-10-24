# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - DECOUPLED COMMAND DISPATCHER ROUTER
Module: aq_command_router.py
Author: Angkor Quant Institutional Infrastructure
Standard: Modular Dispatch and Exception Isolation for User Commands
O(1) Hash Table Lookup with Thread-Safe Execution Boundaries
"""

from typing import Dict, Callable, Any, List
import logging

logger = logging.getLogger("CommandRouter")


class CommandDispatcherRouter:
    def __init__(self) -> None:
        self._registry: Dict[str, Callable] = {}

    def register(self, command_name: str, handler_callable: Callable) -> None:
        """Registers a command handler with the hash registry."""
        clean_command = command_name.strip().lower().replace("/", "")
        self._registry[clean_command] = handler_callable

    def dispatch(
        self,
        command_name: str,
        user_id: int,
        context: Any,
        raw_message_text: str = ""
    ) -> bool:
        """Dispatches an incoming command to its isolated handler routine in O(1) time."""
        clean_command = command_name.strip().lower().replace("/", "")
        handler = self._registry.get(clean_command)

        if not handler:
            logger.warning(f"Unregistered command received: {command_name} from user {user_id}")
            return False

        try:
            handler(user_id=user_id, context=context, raw_text=raw_message_text)
            return True
        except Exception as exc:
            logger.error(f"Isolated command failure in /{clean_command} for user {user_id}: {exc}")
            return False

    def list_registered_commands(self) -> List[str]:
        """Returns a sorted list of all active registered command names."""
        return sorted(list(self._registry.keys()))


# Global Singleton Dispatcher Instance
router = CommandDispatcherRouter()
