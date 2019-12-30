---
title: A Tutorial: "How to Use Anno"
author: Gregory Gundersen
date: 2019-12-01
labels: examples
extra: Extra metadata can be added as you like.
---

Anno renders [Markdown](https://daringfireball.net/projects/markdown/syntax). For example:

1. This is.
1. A list.

You can **bold** and _italicize_ text or use quotes,

> But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.
>
> _Source: [lipsum.com](https://www.lipsum.com/)_

or use any formatting you use in standard Markdown.


## Math

Using [Katex](https://katex.org/), you can write math in display mode,

$$
f(x) = \int_{0}^{\infty} e^{-ix} \text{d}x,
$$

or inline, $\text{Area} = \pi r^2$.

## Images

You can add images using the "Add image" button, which will create a Markdown image tag such as

```
![caption](</path/created/automatically>){ width=50% }
```

with the path set correctly. This copies an image from your hard drive to `CWD/_images` where `CWD` is the current working directory.