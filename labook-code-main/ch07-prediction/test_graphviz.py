from graphviz import Digraph

try:
    dot = Digraph(comment='The Test Table')
    dot.node('A', 'Test Node')
    dot.render('test-output/test_graph', format='png')
    print("Graphviz render successful")
except Exception as e:
    print(f"Graphviz failed: {e}")
