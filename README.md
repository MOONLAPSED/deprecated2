# cognos by MOONLAPSED@github © MIT 2024

### primary outputs

```
"When aiming for a unified learning experience across knowledge bases A and B, aligning and integrating B's ontology and pedagogical structure with A's is crucial. This indicates that before incorporating B into A, we need to ensure that B's ontology (the nature and categorization of its concepts) and pedagogy (the methodology of teaching or organizing information) are compatible with A."
```
```
"While Obsidian supports a hierarchical folder structure, it also offers unique features for organizing and navigating content through markdown notes. To leverage this functionality and create a seamless user experience, we'll employ a method that generates markdown notes to represent folders and subfolders within the knowledge base. This approach will enable us to create a visually intuitive structure while retaining Obsidian's linking and backlinking capabilities, as well as its ability to display folder contents dynamically."
```


ENTRYPOINT ["jupyter", "notebook", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root"]
# docker build . -t jpt
# docker run -d -p 8888:8888 jpt:latest```







http://127.0.0.1:8888/lab - jupyter lab (kernel select, file manager, etc)

http://127.0.0.1:8888/tree? - files

TODO: docker workflow:

.sh script to be run by setup.py which git clones jupyter-python container image and repo (the repo itself is required)

j-p container image is naive and will be the 'runtime' for this application --> the .sh script above or the setup.py will need to 'pass' the program source code and any other data TO the container image.

jpt container image will be the 'runtime' for the program itself.

