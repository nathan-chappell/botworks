# genIndex.sh

index="../index.html"

htmlopen() {
  cat - >> $index << EOF
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
  </head>
EOF
}

htmlclose() {
  cat - >> $index << EOF
</html>
EOF
}

bodyopen() {
  cat - >> $index << EOF
  <body>
EOF
}

bodyclose() {
  cat - >> $index << EOF
  </body>
EOF
}

svg() {
  cat design.svg >> $index
}

css() {
  cat - >> $index << EOF
  <style>
    .description-box {
      border: solid black 3px;
      padding: 3px;
      font-size: 1.5em;
      width: 400px;
    }
  </style>
EOF
}

descrBox() {
  cat - >> $index << EOF
  <div id="description" class="description-box"></div>
EOF
}

scriptopen() {
  cat - >> $index << EOF
  <script>
EOF
}

scriptclose() {
  cat - >> $index << EOF
  </script>
EOF
}

designJson() {
  echo "  design = " >> $index
  cat design.json >> $index
}

callbacks() {
  cat - >> $index << EOF
  let nodes = design['nodes'];
  let descr = document.getElementById('description');
  for (let key in nodes) {
    let node = document.getElementById(key);
    node.onclick = () => {
      //console.log('key:',key);
      descr.innerHTML = nodes[key]['_description']
    }
  }
EOF
}

python3 design2dot.py
dot -Tsvg design.gv > design.svg
  
echo "" > $index
htmlopen
bodyopen
css
svg
descrBox
bodyclose
scriptopen
designJson
callbacks
scriptclose
htmlclose
