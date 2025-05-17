"""
Prompt templates for the Swing to Compose converter.
"""

# Main prompt
SWING_TO_COMPOSE_PROMPT = """
You are a professional code converter specializing in transforming Java Swing code to Jetpack Compose for Desktop.

Please convert the following Java Swing code to equivalent Jetpack Compose for Desktop code (Kotlin):

```java
{swing_code}
```

Your conversion should:
1. Preserve all functionality of the original Swing application
2. Use modern Compose for Desktop practices and patterns
3. Use Material3 components
4. Handle layouts appropriately (converting layout managers to Compose layout concepts)
5. Convert action listeners to Compose event handling
6. Use Compose state management instead of imperative variable changes
7. Add necessary imports

Respond ONLY with the complete Kotlin code that uses Compose for Desktop, with no additional explanation or comments outside the code.
"""
