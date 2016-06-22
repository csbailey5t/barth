# Context

## Conference

This is a short paper that I'm presenting with Eric Rochester, the Head of Research and Development at the Scholars' Lab, at Digital Humanities 2016. It is the largest digital humanities conference and pulls in people from all over the world for a mix of presentations, workshops, and professional meetings. We're presenting this short paper in a session on topic modeling, and are assuming that most people there have at least a basic understanding of topic modeling. Given that we aren't going to give too much background in the paper, I'll give you a basic rundown below.

What I'm giving you now is a rough draft that covers the framing of the question, the theological background, and our analyses and visualizations of the topic models. What it doesn't include is a section that we're going to write on the document classifier that we've built/are fine-tuning. The document classifier is an algorithmic model trained on the text of the *Dogmatics* that can, to a degree, distinguish between pre and post 33 paragraphs. You can feed it text and it will predict whether the text would come from before or after paragraph 33.

I have also have not finished writing the conclusion regarding the resistance of Barth's rhetorical strategy to popular methods of algorithmic analysis, such as topic modeling. I've outlined and given the brief point in the draft I've sent, and can talk through this a bit more at our meeting.

## Intro to Topic Modeling

[David Blei's "Probabilistic topic Models"](https://www.cs.princeton.edu/~blei/papers/Blei2012.pdf)

A nice, short introduction to topic modeling is the article I link to above. If you have time, it's worth reading and won't take long. Briefly, though, topic modeling is an algorithmic method of analyzing texts to uncover themes within the texts. With the type of model most commonly used, latent Dirichlet allocation, the algorithm examines which words are used in proximity most often. It then builds topics, which are collections of related words. The intuition is that these sets of collocated words will be thematically related, such that each topic should have a coherent theme. Each text is understood by the model to be composed of words from each topic, and the model determines what proportion of the text is from each topic. For instance, a text may be 40% words from topic 1, 20% from topic 2, and so forth. This probabilistic model should provide a decent sense of what the thematic concerns of any given text are then.

The goal of topic modeling is to discern the thematic structures that compose a text/set of texts. It is often used with large sets of texts, and used to study change over time in textual collections. In this case, I'm look at Barth's *Dogmatics*, looking for thematic structures, and looking at changes in themes throughout the *Dogmatics*. This is hopefully enough to understand what we're doing in the paper, but I can explain more as needed on Friday.
