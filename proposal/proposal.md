Karl Barth's *Church Dogmatics* is widely considered to be one of the most influential works of Christian theology since the Reformation, and within it Barth's doctrine of election is considered a decisive contribution to modern theology. Over the past two decades, theologians have engaged in a rich questioning of the significance of Barth's doctrine of election for his own theology. His elaboration of the doctrine occurs in the document sections, traditionally referred to as paragraphs, numbered 32 through 35 (of a total of 73 plus a fragment), with paragraph 33 being the primary location for Barth's innovative reworking of the doctrine of election. Some scholars, such as Bruce McCormack and Paul Jones, contest that election is a turning point in Barth's theology, decisively shaping the remainder of the *Dogmatics* to the point that some formulations after election are incompatible with formulations made prior to the doctrine of election. Others, such as George Hunsinger and Paul Molnar, argue that while the doctrine of election is the heart of the *Dogmatics*, it is a part of a consistent and coherent whole; it doesn't constitute a break or determinative shift in Barth's work.

This paper engages the question of the significance of the doctrine of election, as elaborated in paragraphs 32 through 35, to the whole of the *Church Dogmatics* through algorithmic approaches. It suggests that if a portion of a corpora strongly determines the rest of the corpora after its appearance, there will be textual traces, such as changes in word frequencies and common semantic groupings, that can be detected through computational analysis. It approaches the corpora, consisting of the entire *Church Dogmatics*, including prefaces and forewords written by Barth as well as his unfinished fragments that have been published as the final volume of the *Dogmatics*, though a variety of analytic techniques.

The initial explorations are conducted through topic modeling in order to discover hidden thematic structure in texts (Blei, Probabilistic Topic Models, Communications of the ACM).  Using Mallet, we first run topic models on different collections of paragraphs, from 15 to 30 topics, to discern the thematic structure of the entire corpora, noting especially those topics that seem definitively about the doctrine of election. Given the hypothesis that the *Dogmatics* from paragraph 36 on is determined by the theme of election in a way that the paragraphs leading up to paragraph 32 are not, we break the corpus into paragraphs 1 through 31, 32 through 35, and 36 through 73 plus the fragment that Barth was writing before his death. We then run topic models with the number of topics ranging from 15 to 30, looking for the presence of topics indicating the doctrine of election. We also run similar models for the entire corpus minus paragraphs 32 through 35 in order to see whether election would appear as a theme in the text without the presence of the paragraphs explicitly committed to explicating the doctrine. Examining the results, we find that election fails to surface as a topic at most levels of granularity when paragraphs 32 through 35 are not included. We find that at all levels of granularity in which the topics are meaningful and coherent, election does not appear as a topic in the corpus consisting of paragraphs 36 through 73, plus the fragment, and we offer an interpretation for why this is the case based on the rhetorical strategy that Barth employs throughout his lengthy work.

**TODO**: Insert graphic here

Our topic models not only provide data for interpretation, but also supply a vocabulary for focusing further computational analysis. Based on words we determined to be distinctive to the theme of election, we examine overall frequency of key terms across the whole corpora, tracking the rise and fall of language specific to election. We also use term frequency-inverse document frequency (tf-idf) to examine which terms are particularly characteristic of individual paragraphs, paying attention to words typically associated with election.


In the final analysis, we must ask ourselves whether Barth's style of writing, which notoriously circles around and repetitively approaches topics from different angles, proves resistant to current algorithmic approaches in textual analysis.



Might need to add a footnote explaining paragraphs and the structure of CD. (ER: I included this information in the narrative, but you're right, a footnote might be more appropriate.)

**TODO**: (For ER) Find a similar word-usage study to add to this.


Balthasar, Hans Urs von, *The Theology of Karl Barth: Exposition and Interpretation*, trans. Edward T. Oakes (San Francisco: Ignatius, 1992).

Barth, Karl, *Church Dogmatics*, 13 part volumes, ed. G.W. Bromiley and T.F. Torrance (Edinburgh: T&T Clark, 1969-80).

Blei, David M., 'Probabilistic Topic Models', *Communications of the ACM* 55/4 (2012), pp. 77-84.

Hunsinger, George, *Disruptive Grace: Studies in the Theology of Karl Barth* (Grand Rapids: Eerdmans, 2000).

Hunsinger, George, 'Election and the Trinity: Twenty-Five Theses on the Theology of Karl Barth', *Modern Theology* 24/2 (2008), pp. 179-98.

Jones, Paul, *The Humanity of Christ: Christology in Karl Barth's Church Dogmatics* (London: T&T Clark, 2011).

Jüngel, Eberhard, *God's Being is in Becoming: The Trinitarian Being of God in the Theology of Karl Barth. A Paraphrase"*, trans. John Webster (Edinburg: T&T Clark, 2001).

McCormack, Bruce, 'Election and the Trinity: Theses in response to George Hunsinger', *Scottish Journal of Theology* 63/2 (2010), pp. 203-224.

McCormack, Bruce, 'Grace and Being: The Role of God's Gracious Election in Karl Barth's Theological Ontology', in John Webster (ed.), *The Cambridge Companion to Karl Barth* (Cambridge: Cambridge University Press, 2000), pp. 92-110.

McCormack, Bruce, *Karl Barth's Critically Realistic Dialectical Theology. Its Gensis and Development, 1909-1936* (Oxford: Clarendon Press, 1995).

Molnar, Paul D., *Divine Freedom and the Doctrine of the Immanent Trinity: In Dialogue with Karl Barth and Contemporary Theology* (London: T&T Clark, 2002).

Molnar, Paul. D., 'The Trinity, Election, and God's Ontological Freedom: A Response to Kevin W. Hector', *International Journal of Systematic Theology* 8/3 (2006), pp. 294-306.

Webster, John, *Barth* (London: Continuum, 2nd edn, 2004).








"None the less, Barth is the most important Protestant theologian
since Schleiermacher, and the extraordinary descriptive depth of his
depiction of the Christian faith puts him in the company of a handful
of thinkers in the classical Christian tradition." Webster, Barth, 1.

"the significance of Barth's work in his chosen sphere is comparable
to that of, say, Wittgenstein, Heidegger, Freud, Weber or Saussure in
theirs, in that he decisively reorganized an entire discipline."
Webster, Barth, 1.

"The doctrine of election ... is one of the most crucial chapters in
the *Church Dogmatics* as a whole, summing up much of what Barth as
had to say so far and pointing forward to essential features of the
doctrines of creation and reconciliation." Webster, Barth, 88.

"Von Balthasar's judgment that Barth's treatment of election is 'the
most magnificent, unified and well-grounded section' of the *Church
Dogmatics*, 'the heartbeat of his whole theology', was reached before
Barth had begun to publish on the doctrine of reconciliation; but he
is not wide of the mark." Webster, Barth, 93. See Balthasar, *The
Theology of Karl Barth*, 174.

"There can be no Christian truth which does not from the very first
contain within itself as its basis the fact that from and to all
eternity God is the electing God. There can be no tenet of Christian
doctrine which, if it is to be a Christian tenet, does not reflect
both in form and content this divine electing... There is no height or
depth in which God can be God in any other way." Barth, CD II/2, 77.


Webster has a line about the way that Barth introduces a topic then
comes around at it repetitively from a number of different
angles. Look also at Paul's book (intro) to see if he has something
similar about Barth's circling. This would explain why we would expect
to not see a great deal of differentiation across paragraphs, but also
would expect that once a topic is introduced, it becomes regular
thereafter.

What is Barth actually trying to say with his doctrine of election?
That is, what would a set of words be that reflects that work that
doesn't explicitly use 'elect+' or 'predestination' or
'decision/decree' or 'eternal' or 'reject+'?

use logl/cosine similarity on chunks - 1-31, 32-35, 36+ and look at
similarity of election chunk to chunks before and after
