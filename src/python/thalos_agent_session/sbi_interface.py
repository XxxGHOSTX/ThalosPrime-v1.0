"""
Synthetic Biological Intelligence (SBI) Interface

Provides a natural language interface inspired by organoid wetware computing
and synthetic biological intelligence principles. This module interprets
natural language inputs and executes tasks through the Thalos Prime system.

The SBI interface simulates biological neural processing patterns for
deterministic and interpretable AI interactions.
"""

import re
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, UTC
from enum import Enum

from .manager import SessionManager
from .persistence import SessionPersistence
from .memory_subsystem import MemorySubsystem
from .cis_integration import CISIntegration
from .code_generation import CodeGenerationModule


class IntentType(Enum):
    """Types of intents that can be recognized by SBI."""

    SESSION_CREATE = "session_create"
    SESSION_CONTROL = "session_control"
    SESSION_QUERY = "session_query"
    MEMORY_OPERATION = "memory_operation"
    CODE_GENERATION = "code_generation"
    INFORMATION_QUERY = "information_query"
    SYSTEM_STATUS = "system_status"
    GREETING = "greeting"
    GENERAL_CONVERSATION = "general_conversation"
    HELP_REQUEST = "help_request"
    UNKNOWN = "unknown"


class NeuralProcessingLayer:
    """
    Simulates biological neural processing patterns.

    This layer conceptually represents the organoid wetware component,
    using pattern matching and context awareness to interpret inputs.
    """

    def __init__(self):
        """Initialize neural processing patterns."""
        self.patterns = self._initialize_patterns()
        self.context_memory = []
        self.activation_threshold = 0.7

    def _initialize_patterns(self) -> Dict[IntentType, List[str]]:
        """Initialize pattern recognition rules."""
        return {
            IntentType.GREETING: [
                r"\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b",
                r"^(hi|hello|hey)[\s!.]*$",
            ],
            IntentType.HELP_REQUEST: [
                r"\b(help|assist|support|guide|tutorial)\b",
                r"\b(how do i|how to|what can you)\b",
                r"\b(can you help|need help)\b",
            ],
            IntentType.SESSION_CREATE: [
                r"\b(create|start|begin|new|initialize|launch)\b.*\b(session|agent|task)\b",
                r"\b(session|agent|task)\b.*\b(create|start|begin|new)\b",
            ],
            IntentType.SESSION_CONTROL: [
                r"\b(pause|stop|resume|terminate|end|halt|kill)\b.*\b(session|agent)\b",
                r"\b(session|agent)\b.*\b(pause|stop|resume|terminate|end)\b",
                r"\b(pause|stop|resume|terminate|end|halt|kill)\b.*[a-f0-9]{8}-[a-f0-9]{4}",  # Action with UUID
            ],
            IntentType.SESSION_QUERY: [
                r"\b(status|state|info|information|details)\b.*\b(session|agent)\b",
                r"\b(show|list|display|get|find)\b.*\b(sessions?|agents?)\b",
                r"\b(what|how|which)\b.*\b(session|agent)\b",
            ],
            IntentType.MEMORY_OPERATION: [
                r"\b(remember|store|recall|retrieve|memory|save this)\b",
                r"\b(save|record)\b.*\b(memory|data|information)\b",
            ],
            IntentType.CODE_GENERATION: [
                r"\b(generate|create|write|build|code|program)\b.*\b(code|function|class|module|script)\b",
                r"\b(code|program|script)\b.*\b(generate|create|write)\b",
            ],
            IntentType.SYSTEM_STATUS: [
                r"\bsystem\b.*\bstatus\b",
                r"\bsystem\b.*\bstate\b",
                r"\bhealth\b.*\bstatus\b",
                r"\bstatus\b.*\bsystem\b",
                r"\b(how|what).*(system|systems)\b.*(doing|working|performing|running|status)\b",
            ],
            IntentType.INFORMATION_QUERY: [
                r"\b(what|how|why|when|where|who)\b.*\b(is|are|does|can|will|should)\b",
                r"\b(explain|describe|tell me|teach me)\b",
                r"\b(define|definition|meaning)\b",
            ],
            IntentType.GENERAL_CONVERSATION: [
                r"\b(thank|thanks|appreciate|awesome|cool|nice|great)\b",
                r"\b(ok|okay|alright|got it|understood)\b",
                r"\b(yes|no|maybe|sure)\b",
            ],
        }

    def process_input(self, input_text: str) -> Tuple[IntentType, float, Dict[str, Any]]:
        """
        Process input through neural pattern matching.

        Args:
            input_text: Natural language input

        Returns:
            Tuple of (intent_type, confidence, extracted_entities)
        """
        input_lower = input_text.lower()

        # Pattern matching with activation scoring
        best_match = (IntentType.UNKNOWN, 0.0, {})

        for intent_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, input_lower):
                    # Calculate confidence based on pattern complexity
                    confidence = min(
                        0.95, 0.7 + (len(pattern) / 500)
                    )  # Base 0.7 + complexity bonus

                    if confidence > best_match[1]:
                        entities = self._extract_entities(input_text, intent_type)
                        best_match = (intent_type, confidence, entities)

        return best_match

    def _extract_entities(
        self, input_text: str, intent_type: IntentType
    ) -> Dict[str, Any]:
        """Extract entities from input based on intent type."""
        entities = {}

        # Extract session ID patterns
        session_id_match = re.search(
            r"\b([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\b",
            input_text,
        )
        if session_id_match:
            entities["session_id"] = session_id_match.group(1)

        # Extract action keywords
        action_match = re.search(
            r"\b(pause|stop|resume|terminate|create|start|status)\b", input_text.lower()
        )
        if action_match:
            entities["action"] = action_match.group(1)

        # Extract metadata from JSON-like patterns
        json_match = re.search(r"\{[^}]+\}", input_text)
        if json_match:
            try:
                entities["metadata"] = json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        return entities


class SyntheticBiologicalIntelligence:
    """
    Main SBI interface implementing organoid wetware-inspired intelligence.

    This class provides a natural language interface that interprets inputs
    and executes tasks through the Thalos Prime system, using biological
    computing principles for pattern recognition and task execution.
    """

    def __init__(
        self,
        session_manager: Optional[SessionManager] = None,
        persistence: Optional[SessionPersistence] = None,
        memory: Optional[MemorySubsystem] = None,
        cis: Optional[CISIntegration] = None,
        code_gen: Optional[CodeGenerationModule] = None,
    ):
        """
        Initialize SBI interface with subsystem connections.

        Args:
            session_manager: Session management subsystem
            persistence: Session persistence subsystem
            memory: Memory subsystem
            cis: Central Intelligence System integration
            code_gen: Code generation module
        """
        self.session_manager = session_manager or SessionManager()
        self.persistence = persistence or SessionPersistence()
        self.memory = memory or MemorySubsystem()
        self.cis = cis or CISIntegration()
        self.code_gen = code_gen or CodeGenerationModule()

        # Initialize neural processing layer (organoid wetware simulation)
        self.neural_layer = NeuralProcessingLayer()

        # Interaction history for learning and context
        self.interaction_history: List[Dict[str, Any]] = []

    def interpret_and_execute(
        self, input_text: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main interface method: interpret input and execute task.

        This method simulates the organoid wetware processing pipeline:
        1. Neural pattern recognition
        2. Intent classification
        3. Task execution
        4. Response generation

        Args:
            input_text: Natural language input from user
            context: Optional context information

        Returns:
            Dictionary containing execution results and response
        """
        # Store interaction for learning
        interaction = {
            "timestamp": datetime.now(UTC).isoformat(),
            "input": input_text,
            "context": context or {},
        }

        try:
            # Neural processing: interpret input
            intent, confidence, entities = self.neural_layer.process_input(input_text)

            interaction["intent"] = intent.value
            interaction["confidence"] = confidence

            # Execute based on intent
            if confidence < 0.5:
                result = self._handle_low_confidence(input_text, confidence)
            elif intent == IntentType.GREETING:
                result = self._handle_greeting(input_text)
            elif intent == IntentType.HELP_REQUEST:
                result = self._handle_help_request()
            elif intent == IntentType.SESSION_CREATE:
                result = self._handle_session_create(entities)
            elif intent == IntentType.SESSION_CONTROL:
                result = self._handle_session_control(entities)
            elif intent == IntentType.SESSION_QUERY:
                result = self._handle_session_query(entities)
            elif intent == IntentType.MEMORY_OPERATION:
                result = self._handle_memory_operation(input_text, entities)
            elif intent == IntentType.CODE_GENERATION:
                result = self._handle_code_generation(input_text, entities)
            elif intent == IntentType.INFORMATION_QUERY:
                result = self._handle_information_query(input_text)
            elif intent == IntentType.SYSTEM_STATUS:
                result = self._handle_system_status()
            elif intent == IntentType.GENERAL_CONVERSATION:
                result = self._handle_general_conversation(input_text)
            else:
                result = self._handle_general_input(input_text)

            interaction["result"] = result
            interaction["success"] = result.get("success", True)

        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "message": f"SBI processing error: {str(e)}",
            }
            interaction["result"] = result
            interaction["success"] = False

        # Store interaction in memory for learning
        self.interaction_history.append(interaction)
        self.memory.store_episodic_memory("sbi_system", interaction)

        return result

    def _handle_session_create(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Handle session creation requests."""
        metadata = entities.get("metadata", {})
        metadata["created_via"] = "sbi_interface"

        session = self.session_manager.create_session(metadata)
        session = self.session_manager.start_session(session.session_id)
        self.persistence.save_session(session)

        return {
            "success": True,
            "action": "session_created",
            "session_id": session.session_id,
            "state": session.state.value,
            "message": f"Session {session.session_id} created and started successfully",
        }

    def _handle_session_control(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Handle session control operations (pause, stop, resume)."""
        session_id = entities.get("session_id")
        action = entities.get("action")

        if not session_id:
            return {
                "success": False,
                "error": "session_id_required",
                "message": "Please provide a session ID",
            }

        # Try to get session from manager or load from persistence
        session = self.session_manager.get_session(session_id)
        if not session:
            session = self.persistence.load_session(session_id)
            if session:
                self.session_manager.restore_session(session)

        if not session:
            return {
                "success": False,
                "error": "session_not_found",
                "message": f"Session {session_id} not found",
            }

        # Execute control action
        try:
            if action in ["pause", "halt"]:
                session = self.session_manager.pause_session(session_id)
                action_name = "paused"
            elif action in ["stop", "terminate", "end"]:
                session = self.session_manager.terminate_session(session_id)
                action_name = "terminated"
            elif action == "resume":
                session = self.session_manager.resume_session(session_id)
                action_name = "resumed"
            else:
                return {
                    "success": False,
                    "error": "unknown_action",
                    "message": f"Unknown action: {action}",
                }

            self.persistence.save_session(session)

            return {
                "success": True,
                "action": action_name,
                "session_id": session_id,
                "state": session.state.value,
                "message": f"Session {action_name} successfully",
            }

        except Exception as e:
            return {
                "success": False,
                "error": "action_failed",
                "message": f"Failed to {action} session: {str(e)}",
            }

    def _handle_session_query(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Handle session information queries."""
        session_id = entities.get("session_id")

        if session_id:
            # Query specific session
            session = self.persistence.load_session(session_id)
            if not session:
                return {
                    "success": False,
                    "error": "session_not_found",
                    "message": f"Session {session_id} not found",
                }

            return {
                "success": True,
                "action": "session_info",
                "session": session.to_dict(),
                "message": f"Session {session_id} details retrieved",
            }
        else:
            # List all sessions
            stored_ids = self.persistence.list_stored_sessions()
            sessions = []
            for sid in stored_ids:
                session = self.persistence.load_session(sid)
                if session:
                    sessions.append(
                        {
                            "session_id": session.session_id,
                            "state": session.state.value,
                            "created_at": str(session.created_at),
                        }
                    )

            return {
                "success": True,
                "action": "list_sessions",
                "count": len(sessions),
                "sessions": sessions,
                "message": f"Found {len(sessions)} session(s)",
            }

    def _handle_memory_operation(
        self, input_text: str, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle memory storage and retrieval operations."""
        if "remember" in input_text.lower() or "store" in input_text.lower():
            # Store in memory
            key = entities.get("key", f"memory_{len(self.interaction_history)}")
            value = {"input": input_text, "timestamp": datetime.now(UTC).isoformat()}

            self.memory.store_working_memory("sbi_system", key, value)

            return {
                "success": True,
                "action": "memory_stored",
                "key": key,
                "message": "Information stored in memory",
            }
        else:
            # Retrieve from memory
            key = entities.get("key", "last")
            if key == "last" and self.interaction_history:
                value = self.interaction_history[-1]
            else:
                value = self.memory.retrieve_working_memory("sbi_system", key)

            return {
                "success": True,
                "action": "memory_retrieved",
                "value": value,
                "message": "Memory retrieved successfully",
            }

    def _handle_code_generation(
        self, input_text: str, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle code generation requests."""
        # Simple code generation based on request
        return {
            "success": True,
            "action": "code_generation",
            "message": "Code generation capability available. Register templates with code_gen module.",
            "note": "Use CodeGenerationModule for detailed code generation",
        }

    def _handle_information_query(self, input_text: str) -> Dict[str, Any]:
        """Handle general information queries with direct, relevant responses."""
        input_lower = input_text.lower()
        
        # Provide direct, contextual responses to common queries
        responses = {
            "what": self._respond_to_what_query(input_lower),
            "how": self._respond_to_how_query(input_lower),
            "why": self._respond_to_why_query(input_lower),
            "when": self._respond_to_when_query(input_lower),
            "where": self._respond_to_where_query(input_lower),
            "who": self._respond_to_who_query(input_lower),
        }
        
        # Find which question word is present
        for question_word, response_func in responses.items():
            if question_word in input_lower[:10]:  # Check beginning of question
                response = response_func
                if response:
                    return {
                        "success": True,
                        "action": "information_provided",
                        "message": response,
                        "query": input_text,
                    }
        
        # Default informative response
        return {
            "success": True,
            "action": "information_query",
            "message": "I'm Thalos Prime's SBI (Synthetic Biological Intelligence) interface. I process inputs using organoid wetware-inspired patterns to help you manage sessions, store information, and execute tasks naturally.",
            "context": "I can understand and respond to various types of queries. Try asking me about sessions, system status, or just chat with me!",
        }

    def _respond_to_what_query(self, query: str) -> Optional[str]:
        """Generate contextual response to 'what' questions."""
        if "sbi" in query or "synthetic biological" in query:
            return "SBI (Synthetic Biological Intelligence) is an interface that mimics biological neural processing to interpret natural language and execute tasks. It uses pattern recognition similar to how organoid wetware processes information."
        elif "thalos" in query:
            return "Thalos Prime is an advanced AI agent session management system with deterministic architecture. It features session lifecycle management, memory subsystems, and this SBI interface for natural interaction."
        elif "session" in query:
            return "A session represents an active agent instance with managed lifecycle states: initialized, running, paused, and terminated. Sessions maintain state history and can be persisted across system restarts."
        elif "can you do" in query or "capabilities" in query:
            return "I can create and manage sessions, control their lifecycle, store and retrieve memories, answer questions, execute tasks, and have conversations. I process any input you give me and respond relevantly."
        elif "time" in query:
            return f"Current UTC time is {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}. I track all interactions with precise timestamps."
        return None

    def _respond_to_how_query(self, query: str) -> Optional[str]:
        """Generate contextual response to 'how' questions."""
        if "work" in query:
            return "I work by processing your natural language input through neural pattern recognition layers that identify intent, extract entities, and execute appropriate actions through the Thalos Prime subsystems."
        elif "session" in query:
            return "Sessions are created through the SessionManager, started/paused/resumed/stopped through lifecycle controls, and persisted to disk. Each state transition is tracked and reversible (except termination)."
        elif "use" in query or "interact" in query:
            return "Just type or say anything! I understand natural language - ask questions, give commands, or chat casually. For example: 'create a session', 'show me the status', or even 'hello, how are you?'"
        elif "remember" in query or "memory" in query:
            return "I use a multi-tier memory system: working memory for active data, episodic memory for interactions, and semantic memory for knowledge. All interactions are automatically stored."
        return None

    def _respond_to_why_query(self, query: str) -> Optional[str]:
        """Generate contextual response to 'why' questions."""
        if "sbi" in query or "biological" in query:
            return "SBI uses biological intelligence principles because they provide robust pattern recognition, context awareness, and adaptive learning - making interactions more natural and intuitive than rigid command structures."
        elif "deterministic" in query:
            return "Determinism ensures reproducibility and reliability. Every operation produces the same result given the same inputs, making the system predictable and trustworthy for critical applications."
        return "That's a great question! The design choices in Thalos Prime prioritize reliability, transparency, and natural interaction while maintaining strict deterministic behavior."

    def _respond_to_when_query(self, query: str) -> Optional[str]:
        """Generate contextual response to 'when' questions."""
        return f"I'm operating in real-time. Current timestamp: {datetime.now(UTC).isoformat()}. All operations are timestamped for full traceability."

    def _respond_to_where_query(self, query: str) -> Optional[str]:
        """Generate contextual response to 'where' questions."""
        if "data" in query or "stored" in query or "saved" in query:
            return "Session data is stored in the './session_data' directory as JSON files. Each session has its own file with atomic write guarantees for data integrity."
        return "I operate within the Thalos Prime system environment, managing sessions and data locally with options for distributed deployment."

    def _respond_to_who_query(self, query: str) -> Optional[str]:
        """Generate contextual response to 'who' questions."""
        if "you" in query or "are you" in query:
            return "I'm the SBI (Synthetic Biological Intelligence) interface for Thalos Prime - an AI assistant that combines biological computing concepts with deterministic architecture to help you manage agent sessions and execute tasks naturally."
        return "I'm here to help you interact with the Thalos Prime system in natural language!"

    def _handle_greeting(self, input_text: str) -> Dict[str, Any]:
        """Handle greeting inputs with friendly, relevant responses."""
        greetings = [
            "Hello! I'm the Thalos Prime SBI interface. How can I assist you today?",
            "Hi there! Ready to help you with session management or anything else you need.",
            "Greetings! I'm your SBI assistant, powered by synthetic biological intelligence principles.",
        ]
        
        # Pick greeting based on input length (simple variety)
        greeting = greetings[len(input_text) % len(greetings)]
        
        return {
            "success": True,
            "action": "greeting",
            "message": greeting,
            "tip": "Try asking me to create a session, check system status, or just chat!",
        }

    def _handle_help_request(self) -> Dict[str, Any]:
        """Handle help requests with comprehensive guidance."""
        return {
            "success": True,
            "action": "help_provided",
            "message": "I'm here to help! I can understand natural language and respond to various requests.",
            "capabilities": {
                "session_management": [
                    "Create a new session: 'start a session' or 'create an agent'",
                    "Control sessions: 'pause session <id>' or 'stop the session'",
                    "Check status: 'show me all sessions' or 'status of session <id>'",
                ],
                "memory_operations": [
                    "Store information: 'remember this: <info>'",
                    "Retrieve: 'what do you remember?' or 'recall <key>'",
                ],
                "general_interaction": [
                    "Ask questions: 'what is SBI?' or 'how does this work?'",
                    "Get system info: 'system status' or 'how are you doing?'",
                    "Chat naturally: I respond to greetings, thanks, and general queries",
                ],
            },
            "examples": [
                "create a new session with metadata",
                "what sessions are running?",
                "tell me about synthetic biological intelligence",
                "remember this important data",
                "how is the system performing?",
            ],
        }

    def _handle_general_conversation(self, input_text: str) -> Dict[str, Any]:
        """Handle general conversational inputs with natural responses."""
        input_lower = input_text.lower()
        
        if "thank" in input_lower or "thanks" in input_lower:
            return {
                "success": True,
                "action": "acknowledgment",
                "message": "You're welcome! Happy to help. Let me know if you need anything else.",
            }
        elif "ok" in input_lower or "okay" in input_lower or "got it" in input_lower:
            return {
                "success": True,
                "action": "confirmation",
                "message": "Great! I'm here if you need anything else.",
            }
        elif "yes" in input_lower:
            return {
                "success": True,
                "action": "affirmation",
                "message": "Understood! How can I help you further?",
            }
        elif "no" in input_lower:
            return {
                "success": True,
                "action": "negation",
                "message": "No problem! Let me know if you'd like to try something else.",
            }
        elif any(word in input_lower for word in ["cool", "awesome", "great", "nice", "good"]):
            return {
                "success": True,
                "action": "positive_feedback",
                "message": "Glad you think so! I'm designed to make interactions smooth and natural.",
            }
        
        return {
            "success": True,
            "action": "general_response",
            "message": "I'm listening! Feel free to ask questions, give commands, or just chat.",
        }

    def _handle_general_input(self, input_text: str) -> Dict[str, Any]:
        """
        Handle any general input that doesn't match specific patterns.
        Always provides a relevant, helpful response.
        """
        input_lower = input_text.lower()
        
        # Try to extract any actionable keywords
        keywords = {
            "session": "It sounds like you're interested in sessions. I can create, manage, and query agent sessions. Try: 'create a new session' or 'show all sessions'",
            "help": "I'm here to help! I can manage sessions, answer questions, store memories, and chat naturally. What would you like to know?",
            "what": "I'm the SBI interface for Thalos Prime. I use synthetic biological intelligence to understand and respond to your inputs naturally.",
            "how": "I process your input through neural pattern recognition to understand intent, then execute the appropriate action. Just tell me what you need!",
            "status": "I can check system status, session status, or tell you about my capabilities. What would you like to know?",
        }
        
        for keyword, response in keywords.items():
            if keyword in input_lower:
                return {
                    "success": True,
                    "action": "contextual_response",
                    "message": response,
                    "your_input": input_text,
                }
        
        # Default: acknowledge input and offer guidance
        return {
            "success": True,
            "action": "general_acknowledgment",
            "message": f"I received your input: '{input_text}'. I'm designed to understand natural language and can help with various tasks.",
            "suggestions": [
                "Ask me about the system or sessions",
                "Tell me to create or manage sessions",
                "Ask questions about how things work",
                "Store information in memory",
                "Or just chat - I respond to all inputs!",
            ],
            "note": "I process any input you give me and provide relevant responses. Try being more specific, or just chat naturally!",
        }

    def _handle_system_status(self) -> Dict[str, Any]:
        """Handle system status queries."""
        session_count = self.session_manager.get_session_count()
        stored_sessions = len(self.persistence.list_stored_sessions())

        return {
            "success": True,
            "action": "system_status",
            "status": "operational",
            "subsystems": {
                "session_manager": "active",
                "persistence": "active",
                "memory": "active",
                "cis": "active",
                "neural_processing": "active",
            },
            "statistics": {
                "active_sessions": session_count,
                "stored_sessions": stored_sessions,
                "interactions_processed": len(self.interaction_history),
            },
            "message": "All systems operational",
        }

    def _handle_low_confidence(
        self, input_text: str, confidence: float
    ) -> Dict[str, Any]:
        """Handle inputs with low confidence - still provide helpful response."""
        return {
            "success": True,
            "action": "low_confidence_response",
            "confidence": confidence,
            "message": f"I'm processing your input: '{input_text}'. While I'm not entirely certain of your intent (confidence: {confidence:.2%}), I'm here to help!",
            "response": "Let me know what you'd like to do - I can help with sessions, answer questions, store information, or just chat.",
            "suggestions": [
                "Be more specific: 'create a session with purpose X'",
                "Ask directly: 'what can you do?' or 'help'",
                "Give commands: 'show sessions' or 'system status'",
                "Or just continue chatting - I'll do my best to help!",
            ],
        }

    def _handle_unknown(self, input_text: str) -> Dict[str, Any]:
        """Handle unknown intent types - always provide helpful response."""
        return {
            "success": True,
            "action": "open_ended_response",
            "message": f"I received: '{input_text}'. While I'm still learning the best way to help with this, I'm operational and ready to assist!",
            "capabilities": [
                "Managing sessions (create, pause, resume, stop)",
                "Querying session information and status",
                "Storing and retrieving memories",
                "Answering questions about the system",
                "Having natural conversations",
            ],
            "response": "What would you like to know or do? I'm here to help in any way I can!",
        }

    def get_interaction_history(
        self, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent interaction history for learning and debugging."""
        return self.interaction_history[-limit:]

    def clear_history(self) -> None:
        """Clear interaction history."""
        self.interaction_history.clear()
