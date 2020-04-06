yaml-based design
========

The overall design will be expressed in [yaml](https://yaml.org/).  A script
will transform this to [dot](https://www.graphviz.org/doc/info/lang.html), and
further transformed to SVG with [graphviz](https://graphviz.gitlab.io/).  After
all that's done, you can view the results in a browser.

# USAGE

make run
firefox index.html
