Karl Barth's *Church Dogmatics* is widely considered to be one of the most influential works of Christian theology since the Reformation, and within it Barth's doctrine of election is considered a decisive contribution to modern theology. Over the past two decades, theologians have engaged in a rich questioning of the significance of Barth's doctrine of election for his own theology. His elaboration of the doctrine occurs in paragraphs 32 through 36 (of a total of 73), with paragraph 33 being the primary location for Barth's innovative reworking of the doctrine of election. Some scholars, such as Bruce McCormack and Paul Jones, contest that election is a turning point in Barth's theology, decisively shaping the remainder of the *Dogmatics* to the point that some formulations after election are incompatible with formulations made prior to the doctrine of election. Others, such as George Hunsinger and Paul Molnar, argue that while the doctrine of election is the heart of the *Dogmatics*, it is a part of a consistent and coherent whole; it doesn't constitute a break in Barth's work.

This paper engages the question of the significance of the doctrine of election, as elaborated in paragraphs 32 through 36, to the whole of the *Church Dogmatics* through algorithmic approaches. It suggests that if a portion of a corpora strongly determines the rest of the corpora after its appearance, there will be textual traces, such as changes in word frequencies and common semantic groupings, that can be detected through computational analysis. It approaches the corpora, consisting of the entire *Church Dogmatics*, including prefaces and forewords written by Barth as well as his unfinished fragments that have been published as the final volume of the *Dogmatics*, first through topic modeling. According to David Blei, topic modelling can uncover a hidden thematic structure in texts. (Blei, Probabilist Topic Models, Communications of the ACM) Producing topic models at different levels of granularity, with the corpora as a whole and broken up around the section explicitly on election, we examine the presence and absence of election as a theme.

Our topic models not only provide data for interpretation, but also supply a vocabulary for focusing further computational analysis. Based on words we determined to be distinctive to the theme of election, we examine overall frequency of key terms across the whole corpora, tracking the rise and fall of language specific to election. We also use term frequency-inverse document frequency (tf-idf) to examine which terms are particularly characteristic of individual paragraphs, paying attention to words typically associated with election. 


...At the same time, this paper asks whether some styles of writing, such as that of Barth, which notoriously circles around and repetitively approaches topics from different angles, prove resistant to current algorithmic approaches in textual analysis.



include at some point that we each paragraph is a document in the topic models



Use "we", "this paper", "this project"...?





"None the less, Barth is the most important Protestant theologian since Schleiermacher, and the extraordinary descriptive depth of his depiction of the Christian faith puts him in the company of a handful of thinkers in the classical Christian tradition." Webster, Barth, 1.

"the significance of Barth's work in his chosen sphere is comparable to that of, say, Wittgenstein, Heidegger, Freud, Weber or Saussure in theirs, in that he decisively reorganized an entire discipline." Webster, Barth, 1.

"The doctrine of election ... is one of the most crucial chapters in the *Church Dogmatics* as a whole, summing up much of what Barth as had to say so far and pointing forward to essential features of the doctrines of creation and reconciliation." Webster, Barth, 88.

"Von Balthasar's judgment that Barth's treatment of election is 'the most magnificent, unified and well-grounded section'  of the *Church Dogmatics*, 'the heartbeat of his whole theology', was reached before Barth had begun to publish on the doctrine of reconciliation; but he is not wide of the mark." Webster, Barth, 93. See Balthasar, *The Theology of Karl Barth*, 174.

"There can be no Christian truth which does not from the very first contain within itself as its basis the fact that from and to all eternity God is the electing God. There can be no tenet of Christian doctrine which, if it is to be a Christian tenet, does not reflect both in form and content this divine electing... There is no height or depth in which God can be God in any other way." Barth, CD II/2, 77.


Webster has a line about the way that Barth introduces a topic then comes around at it repetitively from a number of different angles. Look also at Paul's book (intro) to see if he has something similar about Barth's circling. This would explain why we would expect to not see a great deal of differentiation across paragraphs, but also would expect that once a topic is introduced, it becomes regular thereafter.

What is Barth actually trying to say with his doctrine of election? That is, what would a set of words be that reflects that work that doesn't explicitly use 'elect+' or 'predestination' or 'decision/decree' or 'eternal' or 'reject+'?

use logl/cosine similarity on chunks - 1-31, 32-35, 36+ and look at similarity of election chunk to chunks before and after
