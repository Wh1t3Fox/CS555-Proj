Zero-Knowledge Subgraph Isomorphism
===================================
<br/>

##Problem
 Given a graph G = (V, E), a graph G′ = (V′, E′) is said to be a subgraph of G if and only if V′ is a subset of V , E′ is a subset of E, and for every edge (i, j) in E′ both i and j are in V′. The subgraph isomorphism problem is: “Given two graphs G1 and G2, ﬁnd an isomorphism between G1 and a subgraph of G2 if such an isomorphism exists”. Subgraph isomorphism seems to be more diﬃcult than graph isomorphism because it involves ﬁguring out which subgraph of G2, as well as an isomorphism (in fact subgraph isomorphism is NP-complete, whereas graph isomorphism is not known to be NP-complete although there is no known polynomial time algorithm for it). Design a zero-knowledge interactive protocol for subgraph isomorphism. That is, assume that both Peggy and Victor know G1 and G2, but Peggy also knows a subgraph G′ of G2 and an isomorphism between G′ and G1. Your protocol must convince Victor of Peggy’s knowledge without making it any easier for Victor to ﬁnd either G′ or its isomorphism with G1. Also give a noninteractive version of your protocol.
 
 
##Solution
1. Peggy generates a random permutation α of the vertices of G2, and applies it to G2
thereby obtaining graph Q. Of course Q is isomorphic to G2, and α describes that
isomorphism. Since Peggy knows G′ and α, she can obtain the subgraph of Q (call
it Q′) that corresponds to G′. Her knowledge of the isomorphism between G1 and G′
implies that she can obtain (again using α) the isomorphism π between G1 and Q′.
2. Peggy commits to Q by giving Victor a version of the adjacency matrix of Q modiﬁed
by replacing every 0 (respectively, 1) in that adjacency matrix by a commitment to 0
(respectively, to 1).
3. Victor challenges Peggy to produce his choice of exactly one of the following items:
(a) α, and all of the adjacency matrix of Q.
(b) π, and the portion of the adjacency matrix of Q that describes Q′.
4. Peggy obliges by producing what Victor requested.
5. Victor veriﬁes that the information Peggy has produced is good. That is, in case 3(a)
he veriﬁes that the matrix revealed is consistent with what Peggy had committed to
in Step 2, and that applying α to G2 results in a graph Q that has the just-revealed
adjacency matrix. In case 3(b) he veriﬁes that the submatrix revealed is consistent
with what Peggy had committed to in Step 2, and that re-naming the vertices of G1
according to permutation π produces a graph Q′
that has the just-revealed adjacency
submatrix. If the information Peggy has produced turns out to be good, this round
of the protocol has terminated successfully.
Of course Victor would need a large enough number (call it n) of successful rounds before
he is convinved.
That the protocol is zero-knowledge can be seen by observing the following:
• In case 3(a) of Victor’s challenge, Victor himself could have produced such an α and
the corresponding Q, and hence this information is of no help to him in ﬁnding an
isomorphism between G1 and a subgraph of G2.
• In case 3(b) of Victor’s challenge, all Victor learns is an isomorphism between G1 and
some other graph Q′, informaton that he could have generated himself (by randomly
permuting G1) and hence is of no help to him in ﬁnding an isomorphism between G1
and a subgraph of G2.

Observe what would have happened if, rather than merely commit to Q, Peggy had instead
revealed Q: The protocol would not have been zero-knowledge because the second case
of Victor’s challenge could simplify Victor’s problem to one of graph isomorphism (i.e.,
ﬁnding α). The protocol would still be secure (because graph isomorphism is itself a diﬃcult
problem), but it could no longer be called zero-knowledge.





####Simplified Version, hopefully it is correct.
We are given two graphs G1 and G2.
- Randomly permute G2 to get a new graph which we save as Q. The permutation is saved as α.
- Obtain a subgraph of Q using α and save it as Q'.
- the isomorphism between G1 and Q' using α is stored as π
- Commit to Q and send to Victor
- Victor either asks for:
    1. α and the permutation Q
    2. π and the subgraph Q'
    
######Resources
- [Explanation of Permutation Matrix](http://www.witno.com/discrete/chap5.pdf)
- [Isomorphic Graph Examples](http://www.cs.laurentian.ca/jdompierre/html/MATH2056E_W2011/cours/s9.3_graph_isomorphism_BW.pdf)
- [Ullmann's Algorithm PPT](http://oldwww.prip.tuwien.ac.at/teaching/ss/strupr/vogl.pdf)
- [Stackoverflow Algorithm](http://stackoverflow.com/questions/13537716/how-to-partially-compare-two-graphs)

