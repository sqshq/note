---
title: Topic 7 - Hash Table
toc: false
date: 2017-10-30
tags: [Hash Table]
top: 7
---

<span class="badge badge-pill badge-info">Hash Table</span>
<span class="badge badge-pill badge-info">Linear Probing</span>


#### Hash Function


### Separate Chaining

Use an array of $M$ < $N$ linked lists. [H. P. Luhn, IBM 1953] 

* Hash: map key to integer $i$ between 0 and $M$ - 1. 
* Insert: put at front of $i$th chain (if not already there). 
* Search: need to search only $i$th chain.



### Linear Probing