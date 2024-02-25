# Markdown syntax
- formatting can be used to enhance the text further:

- Use `#` for headings, `##` for subheadings, and `###` for sub-subheadings.

- Employ `**text**` for bold formatting and `*text*` for italic formatting.
___footnote__:
Here's a simple footnote,[^1] and here's a longer one.[^bignote]
[^1]: meaningful #1!
[^bignote]: Here's one with multiple paragraphs and code.
    Indent paragraphs to include them in the footnote.
    `{ my code }`
    Add as many paragraphs as you like.

___tables__:
First Header | Second Header
------------ | ------------
first column(n) | second column(n)
n+1 first column | n+2 second column

___list__:
- Item 1
- Item 2
  - Item 2a
  - Item 2b

___blockquote__:

> quote text 

___inlinecode__: `code` in backticks can be embedded in-line

`Return:`, `Commands:` + args, flags & IO


___codeblock__: should be fenced with backticks
```python
import os
print(sys.path)
```

```yaml
entities:
  - name: user
    type: entity
    attributes:
      - name
      - role
      - perspective: $mind_map_user

  - name: $mind_map_user
    type: $mind_map
    attributes:
      - elements:
          - thoughts
          - knowledge
          - intentions
      - edges:
          - from: thoughts
            to: knowledge
          - from: knowledge
            to: intentions

  - name: $mind_map_bot
    type: $mind_map
    attributes:
      - elements:
          - understanding
          - responses
          - context
      - edges:
          - from: understanding
            to: responses
          - from: responses
            to: context
```
In this YAML representation:

- `entities` is the main list containing definitions for each entity.
- Each entity definition includes a `name` and `type` field, representing the entity's name and type.
- The `attributes` field contains a list of attributes associated with the entity.
- For entities that are mind maps, the `elements` field lists the elements within the mind map, and the `edges` field describes the relationships between those elements.
____