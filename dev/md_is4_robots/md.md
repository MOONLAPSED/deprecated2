MarkDown-Syntax

    formatting can be used to enhance the text further:

    Use # for headings, ## for subheadings, and ### for sub-subheadings.

    Employ **text** for bold formatting and *text* for italic formatting.

_footnote:

Here's a simple footnote,[^1] and here's a longer one.[^bignote] [^1]: meaningful #1! [^bignote]: Here's one with multiple paragraphs and code. Indent paragraphs to include them in the footnote. { my code } Add as many paragraphs as you like.

_tables:
First Header	Second Header
first column(n)	second column(n)
n+1 first column	n+2 second column

_list:

    Item 1
    Item 2
        Item 2a
        Item 2b

_blockquote:

    quote text

_inlinecode: code in backticks can be embedded in-line: `Return:, Commands: + args, flags & IO`

_codeblock: should be fenced with backticks like this:

```
import sys

print("cwd is: {}".format(os.getcwd()))
```