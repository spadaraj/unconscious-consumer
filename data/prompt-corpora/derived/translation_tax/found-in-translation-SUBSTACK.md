# Found in translation

### Search taught us to strip the grammar from our thoughts. Conversation gave it back.

*The Unconscious Consumer · 11 min read*

[ HERO IMAGE — Metaphor — the same person at two input boxes: a one-line search field holding three clipped keywords, and a deep chat box holding the same request written out as a full sentence. One image for "the box changed, the language changed." ]

Watch one person use two boxes on the same afternoon. Into the search box at work she types: "crm deal pipeline add deal". An hour later, into a chat window, the same person writes: "I'm trying to set up a pipeline for my sales team and I can't work out where new deals are supposed to come in. Can you walk me through it?"

Nothing about her changed in that hour. Her goal did not change. What changed was the box.

For twenty-five years, nearly everything we knew about what people want from software came through the first kind of box. We studied the fragments, ranked the keywords, built taxonomies of intent from three-word scraps. And we quietly treated that clipped, grammarless style as how users naturally behave. It was not. It was how the box behaved. We were studying the container and calling it the contents.

## The tax you learned to pay

Keywordese had to be learned. Nobody's first instinct, handed a machine and a question, is to strip out the verbs. But early search engines could not parse a sentence, so people adapted, and the adaptation became invisible through sheer universality. The search-log research of the early web found queries averaging [about two to three terms](https://www.sciencedirect.com/science/article/abs/pii/S0306457399000564), with none of the grammar of ordinary language, and follow-up studies for two decades found [the same shape, unchanged](https://arxiv.org/abs/1805.09139): the average query held at roughly three words from the dial-up era to the smartphone. An entire literacy formed around the constraint. Think in a sentence, type in a fragment. Delete yourself, delete the context, keep the nouns.

Regular readers will recognise this as the [translation tax](article.html?slug=repriced-overnight): the continuous, unnoticed work of converting what you mean into what the machine can accept. We are [reliably averse to mental effort](https://pubmed.ncbi.nlm.nih.gov/20853993/), and effort [quietly discounts the value](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0068210) of whatever it buys, so a tax like this does not get protested. It gets normalised. For a generation there was no way to know whether keyword search was what people preferred or merely what they tolerated, because there was no condition without the constraint. Every box demanded translation, so translation looked like behaviour.

Then we got something close to a control group.

## What 357,000 unforced sentences show

Public research corpora now contain millions of real messages that ordinary people typed to conversational agents, collected with consent in the wild. Set those beside real search logs, and you can compare, at scale, what people type when the machine demands compression against what they type when it does not. We analysed roughly 357,000 prompt messages against 400,000 genuine search queries, and the difference is not a difference of degree. It is two different languages.

The honest baseline for real search behaviour is ORCAS, a public log of millions of genuine Bing queries that led to clicks; the figures that follow use it. The median query in those click logs is three words. The median prompt is sixteen. Only 0.3 per cent of those search queries end in sentence punctuation, because they are not sentences; 41.7 per cent of prompts do, a gap of roughly 130-fold on the most basic marker of "is this a sentence". The word "I" appears in about 2 per cent of queries and in 31.8 per cent of prompts. "You" appears in under 1 per cent of queries and in 26.6 per cent of prompts: people address the machine, as a matter of course, the way they address someone. And the grammar itself returns. The share of words that are articles, pronouns, prepositions and auxiliaries, the connective tissue of natural language, runs at 0.10 in the query logs, a near-pure keyword bag, and 0.38 in prompts, which is simply ordinary written English.

[ IMAGE — Data — barcode wall: 44 real messages per column rendered as word-segment strips, connective words in colour. Search queries are short, dark, fragmented; prompts are long and threaded with grammar. Static export of the interactive; caption: "Explore the live version, message by message →" linking to the website article with a UTM tag. ]

A note on rigour, because corpora like these are full of traps: they contain roleplay fiction and mass-copied prompt templates, both of which can masquerade as user behaviour. We stripped out both and ran everything again. The numbers above are from the stripped, freehand cut, and they barely moved. A flashier finding from the same dataset, one we rather liked, collapsed entirely under that same test, and we killed it. This one survived. That is why you can trust it.

In plain terms: the moment a machine could parse full intent, people stopped compressing. They did not do it gradually, and nobody instructed them. Given somewhere to put the sentence, the sentence came back.

## The big text box objection

A sceptic should raise two objections here, and the first is good enough to deserve a section.

The objection: perhaps nothing sprang back at all. A chat window is an invitation to write prose, the way a large canvas invites a large painting. Different tasks flow to chat than to search. These corpora capture different people in different tools, not the same person released from a constraint. Maybe the interface changed what people produce without anything about people changing.

Concede the structure of that point: this data cannot follow one user across the boundary, and no honest reading of it supports claims about how common any behaviour is in the population. Concede, too, that task mix inflates the raw magnitudes. People bring generation work to a conversational agent, "write an email to my landlord", and a request like that is sentence-shaped by nature; some share of the first person in the corpus is the shape of the jobs, not the shape of the speaker. But the objection still fails to explain what arrived. An affordance for more text predicts longer fragments: "crm deal pipeline add deal new pipeline stages custom" is more text. What the corpus shows instead is a change of register. Punctuation, pronouns, address, grammar: the specific machinery that keywordese deleted is precisely what returned. People did not expand their queries. They reverted to a different way of speaking, the one they use with humans, and they did it without being taught.

And there is a harder version of the rebuttal, which is the persistence test. A chat window is still a text box. Nothing about it prevents keywordese; three words remain fewer keystrokes than sixteen. If two decades of query discipline were genuinely the efficient way to ask machines for things, laziness alone should have carried it across. Instead, people voluntarily type five times the words. That only makes sense if the compression was never saving them anything: the costly part was the translation itself, the mental work of shrinking a thought into machine-legible fragments, and typing more words of ordinary thought is cheaper than typing fewer words of a learned dialect.

Be precise about what did and did not happen. Keywordese is not dead; billions of fragments will be typed into search boxes today, and when usability researchers [watched people meet Google's conversational search](https://www.nngroup.com/articles/google-ai-mode/), some initially typed keyword strings like "shop refrigerator smart" into it, muscle memory outliving its moment. What the corpus shows is not a dialect dying but a dialect refusing to travel. People maintain keywordese exactly where it is still levied, and declined to carry it into the one context where it became optional. That is the tell. A taste travels with you; a tax stays at the tollbooth. Context-bound persistence is precisely how imposed costs behave, and precisely how preferences do not.

## The person was always there

Why that register, though? Why does unconstrained input snap to the social form, complete with "you", rather than to some third shape, telegraphic but grammatical?

Because the social treatment of machines was never absent. It was suppressed. Thirty years ago, Reeves and Nass showed in [a long programme of experiments](https://press.uchicago.edu/ucp/books/book/distributed/M/bo3618528.html) that people apply human social rules to computers automatically and unconsciously: they are polite to machines, they treat them as social actors, and they do so while flatly denying it. The finding always carried a puzzle, which is that the interfaces of the time gave this instinct nowhere to go. A search box does not accept relationship. You cannot say "you" to a list of links.

[ IMAGE — Data — the "lights come on" panel: 300 real messages per side, dots lighting warm for "I" and cool for "you". The search panel is near-black; the prompt panel is a constellation. Static export; same "explore live" caption-link as above. ]

Read against that background, the corpus is not evidence of a new behaviour but of an old one finally finding its outlet. The 26.6 per cent of prompts that address the machine as "you" are not people learning to socialise with software. They are people ceasing to suppress what came naturally all along. The spring-back was spring-loaded, decades before a box arrived that could receive it. The surprise is not that people talk to software like a person. The surprise is that we ever got them to stop.

## The dialect that never formed

The second objection a sceptic should raise: surely people are just learning a new machine dialect. Anyone who has seen prompt-engineering advice online, the "act as an expert" incantations, the rigid output templates, might assume keywordese is simply being replaced by promptese, and the tax has changed its name.

The corpus says otherwise, and this is the finding that genuinely surprised us. Rigid template scaffolding appears in at most 0.04 per cent of real prompts. Role-assignment phrases hold flat at roughly 1 to 2.6 per cent of messages across thirteen months of data, with no visible growth. (One platform, one year: the honest scope of that trend.) The elaborate prompt-craft aesthetic that fills social media is, in naturalistic use, a rounding error. In the wild, people do not perform incantations. They just write.

No new dialect is forming, because none is needed. That is the deeper meaning of the whole dataset: adaptation tracks constraint, and when the constraint went, so did the adapting.

## The tax was paid twice

Here is the part I have watched from the inside. At a customer-software company I once worked with, the product search logs looked exactly like the corpus says they should: "deal pipeline add new deal", "how to import contacts", fragments written for a machine rather than the way anyone would explain a problem to a colleague. And on the other side of those logs sat people like me, whose job was decompression: reconstructing from three words what the person was actually trying to do, what went wrong upstream of the search, and what they would need to see to succeed, so the company could serve the right content, or fix the product and remove the search entirely.

Notice what that means. The translation tax was levied twice. Users paid it typing; companies paid it again in the interpretive apparatus built to reverse it. Keyword research, query-log analysis, intent taxonomies: a whole discipline of inference that exists because fragments were all the input format could collect. What the corpus shows arriving now, the first person, the stated goal, the surrounding context, is the very material that discipline spent two decades trying to reconstruct. People now volunteer it, unprompted, in sentences.

Even the institution that defined the keyword era has published its own version of this finding. A year into its conversational search mode, [Google reported](https://blog.google/products-and-platforms/products/search/ai-mode-us-insights/) that those searches run triple the length of traditional queries, with open-ended, deliberative asks, the "where should I" and "ideas for" kind, among the fastest growing. Treat the numbers with the scepticism first-party promotion deserves: people plausibly select the conversational mode for their complex questions, which would stretch its averages all on its own. But the statistic decorates a piece of evidence that is much harder to argue with, because it runs against the grain of self-interest: the company has rebuilt its most valuable piece of real estate, the search box itself, so that it now expands as you type, in its words giving you room to describe exactly what you need. Companies say many things in blog posts. They do not redesign the front door of a trillion-dollar business around a behaviour they doubt. Twenty-five years of training users to shrink, reversed in a product decision.

[ SUBSCRIBE BUTTON — Substack native. Placed here, immediately after the Google case study: the persuasive peak, where the reader is most convinced the argument holds. Not in the footer. ]

And here the site's recurring question resurfaces, because it must. If users now hand over what analysts once had to infer, their goals, their context, their worries, in first person, then the interface that hears you like a person also knows you like one. Stated intent is richer for the company in exactly the proportion it is more revealing of the user. Whether that exchange is ingenious or manipulative depends entirely on what is done with the confession, and it is a question this publication will be returning to.

## Actionable recommendations

**Adaptation is not preference.** Inventory every surface where users must translate intent into your structure: query syntax, filter trees, category pickers, form fields that demand your ontology. Each one is now measurable debt. The corpus prices what users do the moment translation stops being required.

**The spring-back is one-way.** Effort aversion means users who have stopped compressing will not resume it for your product. You cannot re-train what was never learned willingly, only resent it.

**Social scripts arrive with sentences.** If your input accepts natural language, users bring the human register and, with it, human expectations of being understood. An interface that looks conversational but parses like a keyword box makes a promise it breaks on the first message. Better an honest search box than a dishonest chat window.

**Read the stated intent you already have.** If any part of your product accepts free text today, the raw logs are the closest thing to unmediated user intent your company has ever possessed. Read them before commissioning another keyword study. The fragments were the compressed file; you now have the original.

## The last word

Go back to the woman with two boxes. The strangest thing about her first query is that for twenty-five years nobody found it strange: a literate adult, mid-thought, deleting herself from her own sentence to be understood by a machine. Billions of people performed that compression, all day, for decades, and it was effort so universal it disappeared, which is this publication's oldest theme. The most powerful constraints are the ones we stop noticing.

The corpus matters because it caught the moment the constraint lifted, and measured what people do when software stops asking them to be smaller. They do not invent a new way to speak to machines. They go back to the way they always spoke, sentence structure, second person and all, as if the box had finally earned it. Software used to teach us its language. The milestone in this data is not that the machines got smarter. It is that, for the first time since the search box was invented, the people stopped having to translate.

---

What I am turning over next: if stated intent is a richer confession than a keyword ever was, the same interface that finally understands us is also the one that finally reads us. That asymmetry — helpfulness and exposure arriving in the same sentence — is where this series goes next.

---

**Further reading:** [Repriced Overnight](https://theunconsciousconsumer.substack.com/p/repriced-overnight) — the companion piece that argued this same translation tax exists and, once revealed, silently repriced the software you already owned. This piece is its measurement.

---

*Want to share your thoughts? The comments are open, and I read every one.*
