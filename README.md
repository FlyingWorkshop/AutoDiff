# AutoDiff
Exploring automatic differentiation!

## Numerical Differentiation

ADD plot and description

## Forward Mode

### Operator Overloading

#### Aside: Custom Computational Graphing API 

The first milestone I set for myself in the project was creating a visualizer for a computational graph. Here we see the computational graph (CG) for the equation $\sqrt{p + p + q} / 3 + \ln(p(pq)) + 3$.

```python
import compgraph as cg

p = cg.Variable("p")
q = cg.Variable("q")
k = cg.Variable(3)
expression = cg.sqrt(p + p + q) / k + cg.ln(p * (p * q)) + k
expression.graph()
```
<p align="center">
  <img src="readme_images/cg_output.png"  alt="Computational Graph Example"/>
</p>


### Compiler Stuff

## Reverse mode

### Back Prop
