# Theological Background/Framing of Question

Since 2000, with the publication of Bruce McCormack’s controversial essay, “Grace and Being…”, English language theologians have been engaged in a sporadic, intense, not always civil debate about the internal consistency of Karl Barth’s *Church Dogmatics*, specifically regarding the relation between the doctrine of the Trinity and the doctrine of election. According to self-labelled “traditionalists,” Barth’s Trinitarian theology is internally consistent, and while the doctrine of election, presented centrally in CD II/2, paragraph 33, is a revolution in Christian theology, it does not alter Barth’s theological ontology. The not self-labelled “revisionists” argue that Barth’s stunning doctrine of election  in paragraph 33 has implications for his theological ontology, such that parts of the *Dogmatics* after paragraph 33 are not logically coherent with the doctrine of God as Trinity presented prior to paragraph 33. The debate has been carried out through essays, books, and presentations, and, methodologically, has revolved around the close interpretation of a relatively small number of passages from Barth’s sprawling *Church Dogmatics*. Yet, fifteen years into the debate, there seems to be no consensus and little shift in perspective, as evidenced by the recent publication of a new book on the issue and a sharply critical essay of that book.[^1] In this paper, we ask whether approaching Barth’s *Church Dogmatics* differently, from an algorithmic view of the whole corpus, might provide a possible intervention into this debate. We argue that while some of the standard text analysis techniques - topic modeling, tf-idf analysis, k-means clustering, and document classification - provide interesting and useful insight into Barth’s *Dogmatics*, they provide minimal data particularly impactful for this debate.

Need to have a better, more accurate thesis statement here

## The brief history of the debate

In 2000, Bruce McCormack published “Grace and Being: The role of God’s gracious election in Karl Barth’s theological Ontology,” in *The Cambridge Companion to Karl Barth*.[^2] In this essay, McCormack pointedly argued that Barth’s most significant contribution to theology is his recasting of the doctrine of election, which is materially revolutionary and supplies a “hermeneutic rule which would allow the church to speak authoritatively about what God was doing - and, indeed, who and what God was/is - before the foundation of the world,’ *without engaging in speculation*.”[^3] Barth’s doctrine does this by reworking the Reformed doctrine of election. In the fairly traditional form of double predestination, the doctrine holds that God in a pre-temporal decision elects or determines some people for salvation, and some people for reprobation or damnation.[^4] As well, much of the Western theological tradition has held that God as the Trinity, the Father, Son, and Holy Spirit, is the subject of election, the One who elects, while the person Jesus of Nazareth, the Christ, is the object of election. Jesus Christ is the first object of God’s electing activity, and humanity is then an object through participation in Christ or as a secondary object of God’s act.

According to McCormack, Barth modifies both elements. While he first presents his thesis in “Grace and Being,” he presents the same points in a clearer manner in a later essay from 2010, “Election and Trinity: Theses in response to George Hunsinger,” and I’ll focus on that essay.[^5] First, for Barth, the double structure of God’s electing activity has as its object Jesus Christ. In Jesus, God elects Christ’s humanity to salvation, and Christ’s divinity to reprobation.[^6] This means that, in some way, damnation is part of God’s own life. Humanity, then, has its salvation in its ontological constitution through Christ’s own humanity.[^7] One might note also that situating Christ’s humanity, and perhaps all humanity in him, as the beneficiary of God’s electing will opens the possibility of but doesn’t necessarily logically entail a doctrine of universal salvation. Jesus Christ is not just the object of God’s eternal election though; Barth states that Jesus Christ is also the subject of election.[^8] According to McCormack, Barth’s explanation of this claim has significant implications for his theological ontology and his doctrine of the Trinity. For Jesus Christ to be the subject of election, then Jesus Christ, the temporally located historical person, must be the identity of the Son in all eternity. If this is correct, then there is not when the Logos had an identity other than that of Jesus Christ.[^9] McCormack traces this conclusion to its logical end: there is no  *Logos asarkos* prior to or apart from the *Logos incarnandus* and *Logos incarnatus*.[^10]

McCormack’s argument in support of the above claims is impressive, and a number of scholars have found his work compelling both as a constructive theological ontology and a reading of significant line in Barth’s theology coming out of the doctrine of election. Yet, a significant segment of Barth scholars and theologians have vigorously resisted his account. George Hunsinger is, perhaps, foremost among those who argue for a reading of Barth that emphasizes internal consistency across the span of the *Dogmatics*, along with Barth’s coherence with Chalcedonian Orthodoxy in his Trinitarian and Christological positions.[^11] Relevant to the above points from McCormack, Hunsinger argues that while we must take Barth seriously when he writes that Jesus Christ is the subject of election, we must understand what Barth meant by it by way of Barth’s theological commitments expressed throughout the whole of the *Dogmatics*.[^12] Concretely, Hunsinger argues that due to Barth’s commitment to the perfection of God’s being-in-Godself, often referred to as the immanent Trinity, God’s eternal identity is wholly independent from creation, which is a contingent, temporal existence.[^13] When Barth says that Jesus Christ is the subject of election, an eternal decision or act of God, we must understand that the eternal Son or Logos is the subject of election, and Jesus of Nazareth is only the subject of election in a certain way (in alium quid).[^14] In accordance with the unity of the human and divine in Jesus Christ, it is theological appropriate to speak of Jesus as the subject of election, but only according to his divinity, not his humanity. Christ’s humanity is part of finite, contingent reality, and, on this reading, cannot be part of an eternal decision in and by God. On Hunsinger’s reading, Barth would still support the existence of a *Logos asarkos* that is neither *incarnandus* or *incarnatus*, who identity has nothing to do in itself with the historical person Jesus of Nazareth.[^15]

As mentioned at the beginning of this paper, this is an ongoing, fractious debate. It is also a debate that has hinged on close interpretation of a relatively small set of passages from the *Church Dogmatics*. Where, then, and how, can an algorithmic approach intervene in this debate? Part of the debate is about the internal consistency of Barth, and about just how significant a shift in the *Dogmatics* the doctrine of election of paragraph 33 is. At the broadest level, then, an algorithmic approach can attempt to determine whether there are identifiable, significant shifts in the text. If there are, can they be materially connected to Barth’s doctrine of election? More narrowly, can we detect changes in Barth’s writing that directly reflect the shifted theological ontology and Christology that McCormack argues are evident in Barth’s work post-election?

# Topic modeling

Our first approach to the *Dogmatics* is through topic modeling, one of the most popular textual analysis methods. David Blei suggests that topic modeling can “uncover hidden thematic structure” in texts.[^16] Given our particular questions, we approached the corpus in two ways. We ran topic models at various numbers of topics on the *Church Dogmatics* as a whole, gaining insight into the large scale themes that seem to structure the work and how the balance of themes changes throughout the *Dogmatics*. Since our concern is with shifts based on paragraph 33, we also broke the corpus into two large chunks: paragraphs 1 to 32, and paragraphs 34 through 73 plus the fragment that Barth was writing just before his death.[^17] We ran topic models on both chunks, aiming to get a slightly more fine-grained image of the two parts of Barth's work, and determining whether any surfaced topics were constituted in a manner that reflects the doctrine of election as a determinative force. While we paid close attention to the topics that explicitly referenced election or immediately related terms[^18], we were also attentive to topics engaged with Christology, the Trinity, reconciliation, and theological ontology more broadly, given the interconnection of these areas with Barth’s doctrine of election.

At the level of the whole *Dogmatics* we found that running only 20 topics provided a strong and clear image of the textual themes. While running at higher numbers of topics provided more granular thematic focus, close attention to the broader 20 topics was sufficient to gain a sense of the overall scope and movement of the *Dogmatics*. Within the 20 topics, there were topics that could be clearly identified with two different aspects of Barth's doctrine of election, including the ontological aspect of concern here, as well as topics that clearly represented his doctrine of God according to its more classical formulation and his doctrine of reconciliation, considered to be his most mature work. The doctrine of reconciliation is also a key area of concern in the debate over theological ontology between McCormack and Hunsinger.

Figure 1. 20 Topics for whole *Dogmatics*

<!-- TODO: look at overall vis of all 20 - stacked -->

The most important topics for our analysis are topics 2, 5, 11, 12, 14, 16, and 19. I'll briefly look at the shape of each topic across all the paragraphs of Barth's work, then look at general trends in related topics across the whole in connection to our question.

Figure 2: topic-02 across all paragraphs
Figure 3: topic-05

I take topic 2 to be indicating an aspect of Barth's Christology, especially in terms of God's activity. It's inclusion of words such as 'god,' 'man,' 'jesus,' 'word,' and 'divine' seem to indicate focus on the person of Jesus as both divine and human. Other top words, such as 'act' and 'grace', might provide a context of God's activity for this particular Christological theme. Looking at its distribution, we can see the presence of topic 2 throughout the whole corpus, with a peak in paragraph 44 ("Man as the Creature of God"), and a number of spikes, primarily after paragraph 33, where Barth's elaborates his doctrine of election, in its Trinitarian and Christological focus. We can see that on average, this topic is more present in texts after paragraph 33, with several chunks: 33-39, 43-47, 55-61, and 63-66. This would accord with the explicit structure of the *Dogmatics*, as it shifts from the Trinity and epistemology, through the doctrine of God, to creation, and finally the doctrine of reconciliation. The topic distribution also indicates the increasing presence of this Christological formulation throughout after the doctrine of election.

Topic 5 is closely related to topic 2. While it doesn't specifically mentioned reconciliation, it focuses on Jesus Christ and includes key words for the understanding of God's saving action in Christ: "grace," "judgement", "death," "sin," "justification," and "righteousness." We might label this more specifically related to the doctrine of justification in traditional Protestant doctrinal loci, but it a significant part of Barth's doctrine of reconciliation, and itself very focused on what happens for humanity at the highest level within the activity of God in relation Jesus Christ. We see, accordingly, presence in many paragraphs throughout the *Dogmatics*, but a much more substantial presence in paragraphs 57 through 66, which explicitly constitute Barth's doctrine of reconciliation.

<!-- TODO: fold in topic 05 into the above paragraph, since it also is Christology and god's reconciling action -->

Figure 4: topic-11

Topic 11 represents Barth's more classically formulated doctrine of God, where Barth describes God's identity in terms of the divine attributes. We see these in the topic's words: "power," "love," "freedom," "glory," and "omnipotence." As generally expected, this topic has its peak and spikes within paragraphs 28 through 31, Barth's explicit doctrine of God. Examining the distribution of the topic over all paragraphs, we can note that while it appears regularly and somewhat substantially in the paragraphs from the beginning of the *Dogmatics* through those just mentioned, it regularly constitutes very little of the texts after paragraph 53, and largely disappears within the paragraphs detailing Barth's doctrine of reconciliation.

Figure 5: topic-14

Topic 14 also strongly indicates the doctrine of God, though with a focus on the doctrine of the Trinity. We see the names of all three person (Spirit, Son, and Father), along with "God," "Trinity", and "Christ." Moreover, given "doctrine," "statement," and "concept," this topic seems to refer to Barth's more formal and focused explication of the doctrinal locus. In contrast, Barth is well known for elaborating an account of the Trinity in IV/1 indirectly by way of his doctrine of reconciliation. Topic 14 peaks early in the *Dogmatics*, in paragraphs 9 and 12, and has its other high points in paragraphs between 8 and 16. More broadly, we can see that the topic is very strong in the early sections of the *Dogmatics*, has some presence in paragraphs 29 through 33 (which deal explicitly with the doctrine of God and election), and has little to no presence after paragraph 42. Given that Barth did engage with the doctrine of the Trinity, though indirectly, throughout volume IV, we might ask why the only topic that very directly references all three persons of the Trinity has little presence therein.

Figure 6: topic-16
<!-- TODO: consider pulling this into the first set of topics - about reconciliation -->
As a contrast to previous doctrines that specifically engaged the doctrine of God by way of Christology, the Trinity, or divine attributes, topic 16 engages Christian life within the context of reconciliation. The presence of this final word is fairly indicative, but we find also reference to "world," "word," "history," "act," and "event." These words give context to reconciliation, indicating its character as part of God's working toward and with the world, in the person of Jesus Christ. The presence of "christ" and "jesus" are also important; reconciliation has a Christological focus for Barth, but one wherein Jesus is a primary agent. When we look at the distribution of this topic, we can see quickly that it has little presence throughout the *Dogmatics* until the final paragraphs, especially 69 through the fragment at the end. Finally, the inclusion of both "act" and "event" in this topic is significant. Reconciliation is an event that occurs in the relation between God and humanity, centered and enacted in the person of Jesus Christ. McCormack would read these inclusions as perhaps indicative of the fully actualistic ontology that he argues that Barth embraces throughout volume IV, and its composition generally supports this point. However, Hunsinger could just as well accept the increasing presence of an actualistic ontology, given that his interpretation of it has it cohere well with his more traditional metaphysical understanding of Barth's doctrine of the Trinity throughout the *Dogmatics.*

Figure 7: topic-19

Topic 19 is the most self-evidently relevant topic for our research question. It specifically mentions "election," "predestination," and "providence," clearly indicating that it is about the doctrine of election. Even more specifically it contains "eternal," "decree," and "decision," perfectly indicating it's high peak, paragraph 33, in which Barth engages election as God's eternal decree or decision. We do in fact see paragraph 33 as the peak of this topic, with spikes in 32, 48, 49, and 57. Paragraph 57, notably, is the first paragraph of Barth's doctrine of reconciliation, entitled, "The Work of God the Reconciler." Overall, this topic is low throughout the whole of the *Dogmatics*, with high chunks only in paragraphs 32-33, 48-49, and 57. This is not unsurprising, given that the topic is significantly defined by words explicitly constrained to the doctrine of election, with less applicability in other doctrines, e.g. predestination, providence, election.

Figure 8: Topic-03

We have one other election topic, which I consider less relevant to this question, but which has to be noted. Topic 3 also specifically engages "election", but is packed with terms related specificaly to Israel and God's history with Israel. It casts election specifically in terms of the election of Israel and the Jews, and relates that to the election of Jesus Christ. Not surprisingly, this topic has it's peak at paragraph 34, "The Election of the Community," and its only other high point in paragraph 35, "The Election of the Individual." It has little to no presence prior to paragraph 30, and only a very low presence after 35. Given its focus on the community and Israel, it has little to do with election as it is a concern for McCormack, Hunsinger, and their other conversation partners.



 topic-19, topic-05, topic-16, topic-11, topic-14, and topic-02


[^1]:	Footnote both

[^2]:	need citation

[^3]:	G&B, 92

[^4]:	For Calvin see institutes, bk 3, ch 21, sec. 5.

[^5]:	Need reference to this essay

[^6]:	citation

[^7]:	check this to be sure its right and footnote it

[^8]:	Add a quote here and cite

[^9]:	McCormack uses this formulation…quote him directly here

[^10]:	get some quotes/reference here, and probably drop the technical latin, since most of the audience would have no clue what it means

[^11]:	Hunsinger is also, notably, the one who labels his camp the “traditionalists,” and McCormack’s the “revisionists.” McCormack argues for a reversal of the labels based on older German readings of Barth. Give reference here to front of election and trinity by McC

[^12]:	find a reference

[^13]:	need reference

[^14]:	fix this latin and get a reference/quote

[^15]:	Find a reference

[^16]:	Blei , 2012. Get the real quote and reference

[^17]:	While the paragraphs immediately surround 33 also directly pertain to Barth’s doctrine of election…

[^18]:	Give a list of these terms
