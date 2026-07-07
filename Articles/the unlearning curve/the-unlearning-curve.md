# The unlearning curve

### The novice was never the one at risk. When mastering a tool stops being necessary, it's the expert's fluency that gets marked to zero.

*Category: user-experience · 10 min read · draft, June 2026*
*Excerpt: For years, the thing keeping you in a tool was the effort you had already spent learning it. That effort is now refundable, and when it is refunded the tool goes quiet. A look at what happens to lock-in, mastery, and whole companies when the cost of learning falls to nothing.*

---

I spent a long time becoming fluent in Looker. Not just clicking around it, but knowing it: how its model was put together, where a given metric actually lived, the particular way it expressed an idea like "active account" that was its own. That fluency felt like competence, and for years it was. It was also, though I never once thought of it this way, the thing binding me to the tool.

Then the binding came undone. These days, when I need a specific cut of the data, some custom shape of a question that would once have meant opening Looker and assembling it the Looker way, I describe it to an agentic assistant and get it back directly. I have not decided Looker got worse. It did not. The governed layer it provides, the shared and audited definitions that stop two teams from meaning different things by "revenue," is a real job and still a hard one. What changed is narrower and stranger than "the tool is obsolete." The effort I had paid to learn its interface simply stopped being required for my own questions. And the moment that effort was no longer required, the interface went dark.

Sit with that, because it generalises. The thing holding me to the product was never really the product. It was the cost I had already sunk into learning it.

## The moat nobody named

Ask a product team what locks their customers in and you will hear a familiar list: the data trapped in the system, the integrations wired around it, the contract signed for three years. All real. But a large and under-acknowledged share of lock-in was never any of those things. It was cognitive. It was the sunk effort of having learned the taxonomy, absorbed the quirks, and memorised where everything lived.

This is not a new idea, only a neglected one. When economists first formalised switching costs, [learning costs sat right alongside transaction costs and contractual ones](https://academic.oup.com/qje/article-abstract/102/2/375/1931195) as a reason customers stay with a product they might otherwise leave. Some of the lock is structural. Some of it is sheer familiarity. And the trouble with the familiarity kind is that when learning *is* the lock, anything that removes the need to learn removes the lock with it. We are also, as a rule, [averse to cognitive effort in the first place](https://pubmed.ncbi.nlm.nih.gov/20853993/), which means the instant the effort of learning a tool becomes optional, our tolerance for paying it does not gently fade. It falls away.

A fair challenge lands here, and it sets the boundary of the whole argument. For plenty of software, the structural lock is the larger one, and refunding the cost of learning leaves the real moat untouched. True. The claim is not that cognitive lock dominated everywhere. It is that it dominated for a specific and overlooked cohort: the individual practitioner whose hold on a tool was mostly fluency, whose underlying data was portable, and for whom the skill carried a real professional standing. For that cohort, familiarity was not one lock among several. It was very nearly the whole of it. And that is exactly the cohort about to find out how little was holding them.

## Why the loyal don't simply leave

There is an obvious objection here, and it has to be met before anything else. If learning was the lock, then the moment learning is refunded, the most habituated users should be the first out of the door. They are not. They tend to stay.

The reason is one of the most durable findings in the field. People [disproportionately prefer to keep things as they are](https://link.springer.com/article/10.1007/BF00055564), and that preference is fed by sunk cost and by loss aversion, the same forces that built the familiarity in the first place. The years you spent learning a tool make it feel like yours, and what feels like yours is painful to give up. So the effect of a refunded learning cost is not a stampede. It is something quieter and more interesting, and it does not fall evenly across your users. It falls hardest on exactly the people you would least expect.

## The mastery that evaporates first

To see why, leave software for a moment and stand on a moped in London.

For decades, becoming a licensed London cab driver meant passing the Knowledge: three to four years memorising twenty-five thousand streets within six miles of Charing Cross, a feat so demanding that only about half of those who attempt the exams pass. The effort was so total that it [physically reshaped the drivers' brains](https://www.pnas.org/doi/10.1073/pnas.070039597), enlarging the rear of the hippocampus, the region that holds a map of space. Later work found this came [at a measurable cost to other kinds of memory](https://pubmed.ncbi.nlm.nih.gov/17024677/). The mastery was real enough to leave a mark you could scan.

Then satellite navigation arrived, and a tourist with a phone could route across London as well as a driver who had given years to the task. Notice who lost the most. It was not the casual map-reader, who had invested little and lost little. It was the expert, whose entire advantage, and a good part of whose standing, evaporated. The skill did not depreciate evenly. It stranded the person who had the most of it.

This is the shape of it, and it is worth stating plainly. When a tool removes the need for a hard-won, fluency-based skill, the casual user shrugs and the master is hollowed out. The master may not even leave. But the human capital they spent years accumulating has just been marked to zero, and with it the quiet professional standing that came from being the person who could do the thing.

## The hollow moat

Now bring it back to software, and add the one ingredient the cab driver did not have: a structural floor beneath the fluency.

When a generative feature was added to Photoshop, it let someone with no compositing or masking skill summon, from a sentence, results that professionals had spent years training their hands to produce. A close study of [hundreds of posts by working creative professionals](https://arxiv.org/html/2404.17781v1) found exactly the tension you would predict: the tool was genuinely useful, and it unsettled people's sense of where craft ended and the machine began. The mastery was being devalued in public, by the maker's own feature.

And yet the company did not suffer for it. [Adobe's revenue kept climbing](https://news.adobe.com/) through the period, because beneath the fluency lock sat a structural one: the subscription, the ecosystem, the file formats everyone else has to open. So the expert did not leave. They stayed, paid, and seethed. What the company kept was the customer. What it lost was the advocate, the power user who once evangelised the tool to everyone around them and now resents it. That is a hollow moat, not a lost one, and it is a worse position than it looks, because a moat made of resentful captives is a moat with no one left to defend it.

## The lock climbs a layer

So what happens when there is no structural floor, as there was none under the London cab trade? The lock does not vanish. It climbs a layer, and it gets shallower as it climbs.

When the Knowledge stopped being the differentiator, the value relocated upward, to the platform that organised the trade. Uber's advantage is no longer any driver's command of the streets; it is the density of its network and its data. But that moat is leaky. Analysts [rate it only a narrow advantage with little in the way of switching costs](https://www.morningstar.com/stocks/is-uber-stock-buy-after-earnings), because [riders and drivers keep rival apps open and switch on price in seconds](https://www.nfx.com/post/the-network-effects-map-nfx-case-study-uber).

An agentic assistant then climbs one layer higher again, and it does not fight that data moat head-on. It sits above the platform and owns the user's intent. "Get me across town" stops meaning "choose an app" and becomes a goal handed to something that treats every platform beneath it as an interchangeable supplier. Ben Thompson named this pattern years ago: [whoever owns demand commoditises the suppliers below it](https://stratechery.com/concept/aggregation-theory/commoditizing-suppliers/). Uber did it to drivers; an assistant that owns your intent does it to Uber. And it does not merely exploit the platform's leakiness, it industrialises it, multi-homing perfectly across every supplier where a person only ever did so lazily, until, in the reading of some strategy writers, [the providers grow portable enough that the relationship resets with each query](https://www.saastr.com/the-wave-of-ai-agent-churn-to-come-prompts-are-portable/).

## Where the moat re-deepens

If the moat keeps climbing, an honest question follows: what stops the agentic layer itself from being commoditised, queried and discarded like everything below it? Something has to make it sticky again, or the stack is churn all the way up.

There is one place the moat re-deepens, and it is the uncomfortable one. It re-deepens around the system that knows you best: your context, your patterns, your standing preferences, the shape of your intent. In commentary on where durable advantage is heading, the recurring claim is that [knowing the user becomes the edge, and trust becomes the product itself](https://medium.com/adventures-in-consumer-technology/aggregation-theory-2-0-the-trillion-dollar-outcome-revolution-c0d5d6f0fd61). Which is to say the lock returns as familiarity again, only inverted. It is no longer you who has learned the tool. It is the tool that has learned you.

It is fair to object that this is just preferences, and preferences are portable, the very leakiness that made every platform below interchangeable a moment ago. But a preference file is not the asset. The asset is an accumulated, continuously updated model of how you decide, earned over thousands of small interactions. You can export a setting; you cannot export the trust, nor skip the cold start of teaching a new system who you are from nothing. Re-running a prompt costs seconds; rebuilding that costs months of your attention. This is the first lock in the whole ascent that asks the user, not the supplier, to spend real effort again, which is why it holds. Not that it is unbreachable: a rival who could credibly import your history would breach it. But absent that, it is the one switching cost the agentic layer does not refund.

This is where the question this publication keeps returning to resurfaces, and it arrives at the top of the ladder rather than the bottom. Whoever holds an intimate model of your intent holds the single most exploitable position in the entire stack. The same intimacy that makes an assistant genuinely useful makes it the most powerful instrument of influence yet built, because it acts on your behalf, in a layer you have stopped inspecting, having stopped needing to know how any of it works. The [dark patterns this site has catalogued before](https://www.theunconsciousconsumer.com/article.html?slug=behind-dark-patterns) deceived you about a price or a pre-ticked box on a screen you were looking at. This one does not need a screen. That is what makes it harder to see, and far more worth watching.

## What to do about it

For product and design teams, the shift is less a feature brief than a question about what your moat is actually made of. A few pairings to work with.

**Cognitive lock-in.** Audit how much of your retention is learning-based rather than structural. The share that rests on users having learned your particular way of doing things is no longer a moat. It is a melting asset, and you should plan as though it is already gone.

**Stranded mastery.** Stop treating deep habituation as defensibility. Find where your most expert advocates are watching their mastery devalued, and decide what you owe them before they sour, because a resentful power user is a churned evangelist whether or not they ever cancel.

**The aggregation ladder.** Assume something will eventually sit above you and treat you as a supplier. Decide deliberately whether you intend to compete to be that aggregator or to be the best thing it can query, because drifting between the two is how you end up commoditised by accident.

**Knowing the user.** The intimacy layer is the new moat and the new dark pattern at the same time. Build it as trust, audibly and inspectably, because that is the whole of the line between ingenious and manipulative, and it is a line your users can no longer see you crossing.

## The last word

For thirty years, good design meant making tools easy to learn. The quiet irony is that the learning was the moat all along. We poured effort into lowering the cost of mastering software, never noticing that the cost of mastering it was the very thing keeping anyone loyal.

Now that cost is being refunded, and the moat is climbing: out of your head, up to the platform, up again to whatever holds your intent. At the top of the ladder it re-deepens into intimacy, the one thing an assistant cannot easily be made to forget, and the one thing you should be most careful about handing over. So the next time a familiar tool goes quiet, a thing you used to know your way around and now simply ask, do not only enjoy the relief. Ask the harder question underneath it. The effort that used to be yours has gone somewhere. It is worth knowing who is holding it now.

---

*Want to share your thoughts? Feel free to share them in the comments section below or on social media.*
