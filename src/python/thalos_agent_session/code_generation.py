"""
Code Generation Module Integration

Provides deterministic code generation capabilities for agent sessions.
All code generation is explicit, traceable, and reproducible.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, UTC
import hashlib


class CodeGenerationModule:
    """
    Deterministic code generation for Thalos Prime agent sessions.

    Provides explicit code generation with version tracking,
    templates, and validation.
    """

    def __init__(self):
        """Initialize code generation module."""
        self.templates: Dict[str, str] = {}
        self.generated_code: Dict[str, Dict[str, Any]] = {}
        self.generation_log: List[Dict[str, Any]] = []

    def register_template(self, name: str, template: str) -> bool:
        """
        Register a code template.

        Args:
            name: Template name
            template: Template string

        Returns:
            True if registered successfully
        """
        self.templates[name] = template
        return True

    def generate_code(
        self,
        session_id: str,
        template_name: str,
        parameters: Dict[str, Any],
        language: str = "python",
    ) -> Dict[str, Any]:
        """
        Generate code using a template and parameters.

        Args:
            session_id: Session identifier
            template_name: Name of template to use
            parameters: Template parameters
            language: Target language

        Returns:
            Generated code with metadata
        """
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} not found")

        template = self.templates[template_name]

        # Simple template substitution (in production, use proper templating)
        generated = template
        for key, value in parameters.items():
            generated = generated.replace(f"{{{key}}}", str(value))

        # Create deterministic hash
        code_hash = hashlib.sha256(generated.encode()).hexdigest()

        result = {
            "session_id": session_id,
            "template_name": template_name,
            "language": language,
            "code": generated,
            "hash": code_hash,
            "parameters": parameters,
            "generated_at": datetime.now(UTC).isoformat(),
        }

        # Store generated code
        code_id = f"{session_id}:{code_hash[:8]}"
        self.generated_code[code_id] = result

        # Log generation
        self._log_generation(session_id, template_name, code_hash)

        return result

    def validate_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Validate generated code.

        Args:
            code: Code to validate
            language: Programming language

        Returns:
            Validation result
        """
        # Basic validation (in production, use proper parsers/linters)
        validation = {
            "valid": True,
            "language": language,
            "errors": [],
            "warnings": [],
            "validated_at": datetime.now(UTC).isoformat(),
        }

        # Simple checks
        if not code.strip():
            validation["valid"] = False
            validation["errors"].append("Code is empty")

        if language == "python":
            try:
                compile(code, "<string>", "exec")
            except SyntaxError as e:
                validation["valid"] = False
                validation["errors"].append(f"Syntax error: {e}")

        return validation

    def get_generated_code(
        self, session_id: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve generated code for a session.

        Args:
            session_id: Session identifier
            limit: Maximum number of results

        Returns:
            List of generated code items
        """
        session_code = [
            code
            for code_id, code in self.generated_code.items()
            if code["session_id"] == session_id
        ]

        # Sort by generation time (most recent first)
        session_code.sort(key=lambda x: x["generated_at"], reverse=True)

        return session_code[:limit]

    def create_scaffold(
        self, session_id: str, scaffold_type: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a code scaffold for a session.

        Args:
            session_id: Session identifier
            scaffold_type: Type of scaffold (module, class, function)
            config: Scaffold configuration

        Returns:
            Scaffold structure
        """
        scaffolds = {
            "module": self._create_module_scaffold,
            "class": self._create_class_scaffold,
            "function": self._create_function_scaffold,
        }

        if scaffold_type not in scaffolds:
            raise ValueError(f"Unknown scaffold type: {scaffold_type}")

        scaffold = scaffolds[scaffold_type](config)

        return {
            "session_id": session_id,
            "scaffold_type": scaffold_type,
            "scaffold": scaffold,
            "config": config,
            "created_at": datetime.now(UTC).isoformat(),
        }

    def _create_module_scaffold(self, config: Dict[str, Any]) -> Dict[str, str]:
        """Create a module scaffold."""
        module_name = config.get("name", "new_module")
        return {
            "__init__.py": f'"""Module: {module_name}"""\n',
            f"{module_name}.py": f'"""Main module file for {module_name}"""\n\nclass {module_name.title()}:\n    pass\n',
        }

    def _create_class_scaffold(self, config: Dict[str, Any]) -> str:
        """Create a class scaffold."""
        class_name = config.get("name", "NewClass")
        return f'''class {class_name}:
    """
    {config.get("docstring", "Class description")}
    """
    
    def __init__(self):
        """Initialize {class_name}."""
        pass
'''

    def _create_function_scaffold(self, config: Dict[str, Any]) -> str:
        """Create a function scaffold."""
        func_name = config.get("name", "new_function")
        return f'''def {func_name}():
    """
    {config.get("docstring", "Function description")}
    """
    pass
'''

    def _log_generation(
        self, session_id: str, template_name: str, code_hash: str
    ) -> None:
        """
        Log code generation for audit trail.

        Args:
            session_id: Session identifier
            template_name: Template used
            code_hash: Hash of generated code
        """
        self.generation_log.append(
            {
                "session_id": session_id,
                "template_name": template_name,
                "code_hash": code_hash,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

    def get_generation_log(
        self, session_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve code generation log.

        Args:
            session_id: Optional session filter

        Returns:
            List of generation log entries
        """
        if session_id:
            return [
                entry
                for entry in self.generation_log
                if entry["session_id"] == session_id
            ]
        return self.generation_log.copy()
