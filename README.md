# cognOS by MOONLAPSED@github © MIT 2024

### .wsb windows sandbox dev env
A sandbox for developing open source LLM agentic software with degrees of computer(sandbox) control.

The devenv contains: 

 - micromamba
 - VScode
 - Etc.


### docker & jupyter-python:

ENTRYPOINT ["jupyter", "notebook", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root"]
# docker build . -t jpt
# docker run -d -p 8888:8888 jpt:latest```

http://127.0.0.1:8888/lab - jupyter lab (kernel select, file manager, etc)

http://127.0.0.1:8888/tree? - files

TODO: docker workflow:

.sh script to be run by setup.py which git clones jupyter-python container image and repo (the repo itself is required)

j-p container image is naive and will be the 'runtime' for this application --> the .sh script above or the setup.py will need to 'pass' the program source code and any other data TO the container image.

## LOGLEAF BRANCH: /dev/diy/...

/dev/diy_llm_skim.py is meant to take diyllmdump.txt and transform it into output.md while removing all the undesired formatting. The undesired formatting is picked-up when preforming a 'ctrl+a' in the browser, in the chat-session.


```
"When aiming for a unified learning experience across knowledge bases A and B, aligning and integrating B's ontology and pedagogical structure with A's is crucial. This indicates that before incorporating B into A, we need to ensure that B's ontology (the nature and categorization of its concepts) and pedagogy (the methodology of teaching or organizing information) are compatible with A."
```




