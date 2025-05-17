from PyQt6.QtGui import QSyntaxHighlighter, QColor, QTextCharFormat
from fadingtext import FadingTextEdit
from pygments.token import Token
import pygments


class PygmentsHighlighter(QSyntaxHighlighter):

    def __init__(self, parent, lexer):
        super().__init__(parent)
        self.lexer = lexer

        self.styles = {
            Token.Keyword: self._format("#EF9A9A"),
            Token.Keyword.Constant: self._format("#EF9A9A"),
            Token.Keyword.Declaration: self._format("#EF9A9A"),
            Token.Keyword.Namespace: self._format("#EF9A9A"),
            Token.Keyword.Pseudo: self._format("#EF9A9A"),
            Token.Keyword.Reserved: self._format("#EF9A9A"),
            Token.Keyword.Type: self._format("#80CBC4"),

            Token.Name.Class: self._format("#80CBC4"),
            Token.Name.Function: self._format("#90CAF9"),
            Token.Name.Decorator: self._format("#B39DDB"),

            Token.String: self._format("#C5E1A5"),
            Token.String.Char: self._format("#C5E1A5"),
            Token.String.Doc: self._format("#C5E1A5"),
            Token.String.Double: self._format("#C5E1A5"),
            Token.String.Escape: self._format("#C5E1A5"),
            Token.String.Heredoc: self._format("#C5E1A5"),
            Token.String.Interpol: self._format("#C5E1A5"),
            Token.String.Other: self._format("#C5E1A5"),
            Token.String.Regex: self._format("#C5E1A5"),
            Token.String.Single: self._format("#C5E1A5"),
            Token.String.Symbol: self._format("#C5E1A5"),

            Token.Number: self._format("#FFCC80"),
            Token.Number.Float: self._format("#FFCC80"),
            Token.Number.Hex: self._format("#FFCC80"),
            Token.Number.Integer: self._format("#FFCC80"),
            Token.Number.Integer.Long: self._format("#FFCC80"),
            Token.Number.Oct: self._format("#FFCC80"),

            Token.Operator: self._format("#FFFFFF"),
            Token.Operator.Word: self._format("#FFFFFF"),

            Token.Comment: self._format("#BBBBBB", True),
            Token.Comment.Hashbang: self._format("#BBBBBB", True),
            Token.Comment.Multiline: self._format("#BBBBBB", True),
            Token.Comment.Preproc: self._format("#BBBBBB", True),
            Token.Comment.Single: self._format("#BBBBBB", True),
            Token.Comment.Special: self._format("#BBBBBB", True),
        }

    def _format(self, color, italic=False):
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        if italic:
            format.setFontItalic(True)
        return format

    def highlightBlock(self, text):
        if not text:
            return

        tokens = pygments.lex(text, self.lexer)

        for token_type, token_text in tokens:
            style = None
            for token_class in token_type.split():
                if token_class in self.styles:
                    style = self.styles[token_class]
                    break

            if style is None:
                continue

            start = text.find(token_text)
            if start >= 0:
                self.setFormat(start, len(token_text), style)
                text = text.replace(token_text, ' ' * len(token_text), 1)


class PygmentsFadingEdit(FadingTextEdit):

    def __init__(self, parent=None, lexer=None):
        super().__init__(parent)
        if lexer:
            self.highlighter = PygmentsHighlighter(self.document(), lexer)
