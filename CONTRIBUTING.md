# Contributing to AI Travel Planner

Thank you for interest in contributing! 🙏

## How to Contribute

### 1. Report Bugs

Found a bug? Create an [issue](https://github.com/yourusername/ai-travel-planner/issues).

**Include:**
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Relevant logs or screenshots

### 2. Suggest Features

Have an idea? Create a [feature request](https://github.com/yourusername/ai-travel-planner/issues).

**Include:**
- Clear description of the feature
- Why it would be useful
- Proposed implementation (if you have one)
- Examples of similar features

### 3. Submit Code

#### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ai-travel-planner.git
cd ai-travel-planner

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r Backend/requirements.txt

# Install dev dependencies
pip install black flake8 pytest pytest-cov
```

#### Make Changes

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write code following guidelines** (see below)

3. **Test your changes**
   ```bash
   pytest tests/
   ```

4. **Format and lint**
   ```bash
   black Backend/
   flake8 Backend/
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: clear description"
   ```

#### Code Guidelines

##### Style Guide (PEP 8)

```python
# ✅ Good
def extract_destination(query: str) -> Optional[str]:
    """Extract destination from query."""
    destinations = ["Manali", "Goa", "Jaipur"]
    for dest in destinations:
        if dest.lower() in query.lower():
            return dest
    return None

# ❌ Bad
def extract_destination(query):
    destinations=["Manali","Goa","Jaipur"]
    for d in destinations:
     if d.lower() in query.lower():
      return d
```

##### Docstrings

```python
def search_vector_db(query: str, top_k: int = 5) -> List[Dict]:
    """
    Search vector database for similar travel information.
    
    Args:
        query: User search query
        top_k: Number of results to return
    
    Returns:
        List of search results with scores
    
    Raises:
        ValueError: If query is empty
        ConnectionError: If database unavailable
    
    Example:
        >>> results = search_vector_db("Manali hotels")
        >>> print(len(results))  # 5
    """
    pass
```

##### Type Hints

```python
# ✅ Always use type hints
def add_vector(
    text: str, 
    embedding: List[float], 
    metadata: Dict[str, Any]
) -> bool:
    """Add vector to database."""
    pass

# ❌ Avoid untyped functions
def add_vector(text, embedding, metadata):
    pass
```

##### Error Handling

```python
# ✅ Specific error handling
try:
    response = requests.post(url, timeout=5)
except requests.Timeout:
    logger.warning("Request timed out")
except requests.ConnectionError as e:
    logger.error(f"Connection failed: {e}")

# ❌ Avoid bare except
try:
    response = requests.post(url)
except:
    pass
```

##### Logging

```python
# ✅ Use appropriate levels
logger.info("Database loaded")
logger.warning("Endee unavailable, using fallback")
logger.error(f"Failed to connect: {error}")

# ❌ Avoid print for debugging
print("Debug info")  # Use logging instead
```

### 4. Submit Pull Request

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub
   - Clear title: "Add feature: ..."
   - Description of changes
   - Related issue: "Closes #123"

3. **Respond to review**
   - Make suggested changes
   - Mark conversations as resolved
   - Push updated code

4. **Celebrate!** 🎉
   - Your PR will be merged
   - You'll be credited

## Coding Standards

### File Structure

```python
# 1. Imports (sorted alphabetically by module)
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import requests
from sentence_transformers import SentenceTransformer

# 2. Constants
DEFAULT_MODEL = "all-MiniLM-L6-v2"
MAX_QUERY_LENGTH = 500

# 3. Classes
class VectorDB:
    """Vector database wrapper."""
    pass

# 4. Functions
def search(query: str) -> List[Dict]:
    """Search function."""
    pass

# 5. Main execution
if __name__ == "__main__":
    pass
```

### Naming Conventions

```python
# Constants: UPPER_CASE
MAX_RESULTS = 10
ENDEE_HOST = "localhost"

# Functions/Variables: snake_case
def extract_destination(): pass
query_embedding = []

# Classes: PascalCase
class RetrieverAgent: pass
class VectorDB: pass

# Private: leading underscore
def _internal_helper(): pass
_private_var = None
```

### Tests

```python
# tests/test_agents.py
import pytest
from agents.planner_agent import PlannerAgent

class TestPlannerAgent:
    def setup_method(self):
        """Setup for each test."""
        self.agent = PlannerAgent()
    
    def test_extract_destination(self):
        """Test destination extraction."""
        result = self.agent.extract_destination("Trip to Manali")
        assert result == "Manali"
    
    def test_extract_invalid(self):
        """Test with invalid query."""
        result = self.agent.extract_destination("Trip somewhere")
        assert result is None
```

## Documentation Requirements

### For New Features

1. **Update docstrings**
   ```python
   def new_feature():
       """Clear description of what it does."""
       pass
   ```

2. **Update README.md** if user-facing

3. **Update ARCHITECTURE.md** if system-level

4. **Add usage example** in docstring

### For Bug Fixes

1. **Reference issue** in commit message
   ```bash
   git commit -m "Fix: Handle empty queries (closes #42)"
   ```

2. **Add test** to prevent regression
   ```python
   def test_empty_query_handling():
       """Verify empty queries are rejected."""
       pass
   ```

## Commit Message Guidelines

```
# ✅ Good commit messages

"Add semantic search filtering"
"Fix: Handle missing API key gracefully"
"Refactor: Simplify vector search logic"
"Docs: Update Endee integration guide"
"Test: Add vector database tests"
"Chore: Update dependencies"

# ❌ Poor commit messages

"fix bug"
"update"
"asdf"
"working version"
```

### Format

```
[Type]: [Scope] - Brief description

Longer explanation if needed. Explain why this
change is needed and what problem it solves.

Fixes #123
Related to #456
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Dependencies, build, etc.

## Review Process

1. **Code Review**
   - Functionality check
   - Code quality review
   - Documentation review

2. **Testing**
   - Run tests
   - Check coverage
   - Manual testing

3. **Merge**
   - Rebase and merge
   - Update version if needed
   - Close related issues

## Areas We Need Help

### High Priority
- [ ] Integration tests for RAG pipeline
- [ ] Docker optimization
- [ ] Performance benchmarks
- [ ] Cloud deployment guides

### Medium Priority
- [ ] Web framework upgrade (React/Vue)
- [ ] Advanced filtering options
- [ ] Real-time API integrations
- [ ] Multi-language support

### Low Priority
- [ ] UI/UX enhancements
- [ ] Additional travel destinations
- [ ] Alternative embedding models
- [ ] More deployment options

## Community

- 💬 **Discussions**: Ask questions and share ideas
- 👥 **Community**: Join our community
- 🐦 **Twitter**: Follow @yourusername
- 📧 **Email**: your-email@example.com

## Code of Conduct

- Be respectful and inclusive
- No harassment or discrimination
- Welcome diverse perspectives
- Constructive feedback only
- Report violations to maintainers

## Recognition

Contributors will be:
- Listed in README.md
- Credited in releases
- Thanked in commits
- Recognized on website

## Questions?

- 📖 Check [README.md](README.md)
- 📚 Read [ARCHITECTURE.md](ARCHITECTURE.md)
- 💬 Create [Discussion](https://github.com/yourusername/ai-travel-planner/discussions)
- 📧 Email: your-email@example.com

---

**Thanks for contributing to AI Travel Planner! 🙏**

Your efforts help make travel planning accessible to everyone. 🧳
