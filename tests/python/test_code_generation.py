"""
Test suite for Code Generation Module

Tests deterministic code generation capabilities.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))

from thalos_agent_session.code_generation import CodeGenerationModule


class TestCodeGenerationModule:
    """Test CodeGenerationModule functionality."""

    def test_initialization(self):
        """Test code generation module initializes correctly."""
        cgm = CodeGenerationModule()
        assert cgm.templates == {}
        assert cgm.generated_code == {}
        assert cgm.generation_log == []

    def test_register_template(self):
        """Test registering a code template."""
        cgm = CodeGenerationModule()
        result = cgm.register_template("hello", "print('hello {name}')")

        assert result is True
        assert "hello" in cgm.templates
        assert cgm.templates["hello"] == "print('hello {name}')"

    def test_generate_code_with_template(self):
        """Test generating code from a template."""
        cgm = CodeGenerationModule()
        cgm.register_template("greet", "def greet():\n    return '{message}'")

        result = cgm.generate_code(
            session_id="test-session-123",
            template_name="greet",
            parameters={"message": "Hello World"},
        )

        assert result["session_id"] == "test-session-123"
        assert result["template_name"] == "greet"
        assert "Hello World" in result["code"]
        assert "hash" in result
        assert result["language"] == "python"

    def test_generate_code_stores_result(self):
        """Test that generated code is stored."""
        cgm = CodeGenerationModule()
        cgm.register_template("tmpl", "x = {value}")

        result = cgm.generate_code(
            session_id="session-1",
            template_name="tmpl",
            parameters={"value": "42"},
        )

        assert len(cgm.generated_code) == 1

    def test_generate_code_unknown_template_raises(self):
        """Test that generating code with unknown template raises ValueError."""
        cgm = CodeGenerationModule()

        with pytest.raises(ValueError, match="Template nonexistent not found"):
            cgm.generate_code(
                session_id="session-1",
                template_name="nonexistent",
                parameters={},
            )

    def test_generate_code_with_language(self):
        """Test generating code with specific language."""
        cgm = CodeGenerationModule()
        cgm.register_template("js_func", "function {name}() {{}}")

        result = cgm.generate_code(
            session_id="session-1",
            template_name="js_func",
            parameters={"name": "doSomething"},
            language="javascript",
        )

        assert result["language"] == "javascript"

    def test_generate_code_logs_generation(self):
        """Test that code generation is logged."""
        cgm = CodeGenerationModule()
        cgm.register_template("simple", "x = 1")

        cgm.generate_code(
            session_id="session-abc",
            template_name="simple",
            parameters={},
        )

        log = cgm.get_generation_log()
        assert len(log) == 1
        assert log[0]["session_id"] == "session-abc"
        assert log[0]["template_name"] == "simple"

    def test_validate_code_valid_python(self):
        """Test validating valid Python code."""
        cgm = CodeGenerationModule()
        result = cgm.validate_code("x = 1\nprint(x)")

        assert result["valid"] is True
        assert result["errors"] == []
        assert result["language"] == "python"

    def test_validate_code_empty_code(self):
        """Test validating empty code."""
        cgm = CodeGenerationModule()
        result = cgm.validate_code("")

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_code_invalid_python_syntax(self):
        """Test validating Python code with syntax error."""
        cgm = CodeGenerationModule()
        result = cgm.validate_code("def broken(:\n    pass")

        assert result["valid"] is False
        assert any("Syntax error" in e for e in result["errors"])

    def test_validate_code_non_python(self):
        """Test validating code in non-Python language (no syntax check)."""
        cgm = CodeGenerationModule()
        result = cgm.validate_code("const x = 1;", language="javascript")

        assert result["valid"] is True
        assert result["language"] == "javascript"

    def test_get_generated_code_for_session(self):
        """Test retrieving generated code for a specific session."""
        cgm = CodeGenerationModule()
        cgm.register_template("tmpl", "x = {n}")

        cgm.generate_code("session-A", "tmpl", {"n": "1"})
        cgm.generate_code("session-A", "tmpl", {"n": "2"})
        cgm.generate_code("session-B", "tmpl", {"n": "3"})

        results = cgm.get_generated_code("session-A")
        assert len(results) == 2
        for r in results:
            assert r["session_id"] == "session-A"

    def test_get_generated_code_limit(self):
        """Test that limit parameter works for get_generated_code."""
        cgm = CodeGenerationModule()
        cgm.register_template("tmpl", "x = {n}")

        for i in range(5):
            cgm.generate_code("session-X", "tmpl", {"n": str(i)})

        results = cgm.get_generated_code("session-X", limit=3)
        assert len(results) == 3

    def test_get_generated_code_empty_session(self):
        """Test getting generated code for a session with no code."""
        cgm = CodeGenerationModule()
        results = cgm.get_generated_code("nonexistent-session")
        assert results == []

    def test_create_scaffold_module(self):
        """Test creating a module scaffold."""
        cgm = CodeGenerationModule()
        result = cgm.create_scaffold(
            session_id="session-1",
            scaffold_type="module",
            config={"name": "my_module"},
        )

        assert result["session_id"] == "session-1"
        assert result["scaffold_type"] == "module"
        assert "__init__.py" in result["scaffold"]
        assert "my_module.py" in result["scaffold"]

    def test_create_scaffold_class(self):
        """Test creating a class scaffold."""
        cgm = CodeGenerationModule()
        result = cgm.create_scaffold(
            session_id="session-1",
            scaffold_type="class",
            config={"name": "MyClass", "docstring": "My class desc"},
        )

        assert result["scaffold_type"] == "class"
        assert "MyClass" in result["scaffold"]
        assert "My class desc" in result["scaffold"]

    def test_create_scaffold_function(self):
        """Test creating a function scaffold."""
        cgm = CodeGenerationModule()
        result = cgm.create_scaffold(
            session_id="session-1",
            scaffold_type="function",
            config={"name": "my_func", "docstring": "My function"},
        )

        assert result["scaffold_type"] == "function"
        assert "my_func" in result["scaffold"]

    def test_create_scaffold_unknown_type_raises(self):
        """Test that unknown scaffold type raises ValueError."""
        cgm = CodeGenerationModule()

        with pytest.raises(ValueError, match="Unknown scaffold type"):
            cgm.create_scaffold(
                session_id="session-1",
                scaffold_type="unknown_type",
                config={},
            )

    def test_get_generation_log_filtered(self):
        """Test getting generation log filtered by session."""
        cgm = CodeGenerationModule()
        cgm.register_template("tmpl", "pass")

        cgm.generate_code("session-A", "tmpl", {})
        cgm.generate_code("session-B", "tmpl", {})

        log_a = cgm.get_generation_log("session-A")
        assert len(log_a) == 1
        assert log_a[0]["session_id"] == "session-A"

    def test_get_generation_log_all(self):
        """Test getting full generation log."""
        cgm = CodeGenerationModule()
        cgm.register_template("tmpl", "pass")

        cgm.generate_code("session-A", "tmpl", {})
        cgm.generate_code("session-B", "tmpl", {})

        log = cgm.get_generation_log()
        assert len(log) == 2

    def test_generated_code_hash_is_deterministic(self):
        """Test that the same code generates the same hash."""
        cgm = CodeGenerationModule()
        cgm.register_template("tmpl", "x = {n}")

        result1 = cgm.generate_code("session-1", "tmpl", {"n": "42"})
        result2 = cgm.generate_code("session-2", "tmpl", {"n": "42"})

        assert result1["hash"] == result2["hash"]

    def test_validate_code_has_timestamp(self):
        """Test that validation result has a timestamp."""
        cgm = CodeGenerationModule()
        result = cgm.validate_code("x = 1")

        assert "validated_at" in result

    def test_scaffold_default_names(self):
        """Test scaffold creation with default names."""
        cgm = CodeGenerationModule()

        module_result = cgm.create_scaffold("s1", "module", {})
        assert "new_module.py" in module_result["scaffold"]

        class_result = cgm.create_scaffold("s1", "class", {})
        assert "NewClass" in class_result["scaffold"]

        func_result = cgm.create_scaffold("s1", "function", {})
        assert "new_function" in func_result["scaffold"]
