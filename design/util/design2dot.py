# design.yaml
# 
# output design.yaml as a dot file

import json
from yaml import full_load
from typing import Dict

design_file = '../design.yaml'

class Indenter:
  def __init__(self):
    self.cur_indent = 0

  def _br(self):
    return '\n' + ' '*self.cur_indent
  
  def _indent(self):
    self.cur_indent += 2

  def _dedent(self):
    self.cur_indent -= 2
    if (self.cur_indent < 0):
      raise Exception('Dedented below 0!')

  # decorators
  def indent(self, target):
    def f(*args,**kwargs):
      result = self._br() + target(*args,**kwargs)
      self._indent()
      return result
    return f

  def dedent(self, target):
    def f(*args,**kwargs):
      self._dedent()
      result = self._br() + target(*args,**kwargs)
      return result
    return f

  def nodent(self, target):
    def f(*args,**kwargs):
      result = self._br() + target(*args,**kwargs)
      return result
    return f

class DotFormat:
  """a collection of static methods returning strings"""
  sanitize_map = { 
      ord('.'): '_',
      ord('/'): '_'
  }
  indenter = Indenter()

  @staticmethod
  def santize_name(name):
    return name.translate(DotFormat.sanitize_map)

  @staticmethod
  @indenter.indent
  def fopen(name) -> str:
    _name = DotFormat.santize_name(name)
    return f'strict digraph {_name} {{'

  @staticmethod
  @indenter.dedent
  def fclose() -> str:
    return '}'

  @staticmethod
  @indenter.indent
  def fopen_subgraph() -> str:
    return '{'

  @staticmethod
  @indenter.dedent
  def fclose_subgraph() -> str:
    return '}'

  @staticmethod
  def fattrs(**kwargs) -> str:
    return '[' + ', '.join(f'{k}="{v}"' for k,v in kwargs.items()
                           if not k.startswith('_')) + ']'

  @staticmethod
  @indenter.nodent
  def fnode_attrs(attrs: Dict) -> str:
    return 'node ' + DotFormat.fattrs(**attrs)

  @staticmethod
  @indenter.nodent
  def fnode(label: str, attrs: Dict) -> str:
    return f'{label} {DotFormat.fattrs(**attrs,id=label)}'

  @staticmethod
  @indenter.nodent
  def fedge(edge: Dict) -> str:
    return f'{edge["from"]} -> {edge["to"]} {DotFormat.fattrs(**edge["attrs"])}'

class Design:
  def __init__(self, filename):
    self.filename = filename
    self.read_file(filename)

  def read_file(self, filename):
    with open(filename) as file:
      self.raw_design = full_load(file.read())
  
  def get_nodes(self):
    return self.raw_design['nodes']

  def get_edges(self):
    nodes = self.get_nodes()
    edges = []
    for from_node in nodes:
      try:
        for to_node in nodes[from_node]['_to']:
          edges.append({'from':from_node, 
                        'to': to_node, 
                        'attrs': nodes[from_node]['_to'][to_node]})
      except KeyError:
        pass
    return edges

  # subgraphs are determined by the rank property of nodes
  def get_subgraphs(self):
    nodes = self.get_nodes()
    ranks = set(nodes[node]['rank'] for node in nodes)
    return [{node:nodes[node] for node in nodes 
                              if nodes[node]['rank'] == rank}
                  for rank in ranks]

  def get_node_attrs(self):
    return self.raw_design['node_attrs']

  def toDot(self) -> str:
    subgraphs = self.get_subgraphs()
    edges = self.get_edges()
    
    dot = DotFormat.fopen(self.filename)
    dot += DotFormat.fnode_attrs(self.get_node_attrs())
    for subgraph in subgraphs:
      dot += DotFormat.fopen_subgraph()
      dot += DotFormat.indenter._br() + 'rank=same'
      dot += ''.join(DotFormat.fnode(k,subgraph[k]) for k in subgraph)
      dot += DotFormat.fclose_subgraph()

    dot += ''.join(DotFormat.fedge(e) for e in edges)
    dot += DotFormat.fclose()
    return dot

  def toJson(self,indent=0) -> str:
    return json.dumps(self.raw_design,indent=indent)

if __name__ == '__main__':
  design = Design(design_file)
  with open('design.gv','w') as graph:
    print(design.toDot(), file=graph)
  with open('design.json','w') as graph:
    print(design.toJson(indent=2), file=graph)

