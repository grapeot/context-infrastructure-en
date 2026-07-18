# External Article Prose and Rhetoric Guide

## Metadata

- **Type**: BestPractice
- **Use cases**: Long-form articles, reports, and blog posts for strangers without shared context, public channels, customers, or external course audiences.
- **Created**: 2026-07-06

## Core Design Philosophy

The first principle of external writing is to **reduce decision and cognitive friction for an unfamiliar reader**. At the sentence and word level, remove AI-sounding prose, translation-like phrasing, and inflated false consensus.

---

## 1. Rhetoric, Metaphors, and Abstract Labels to Avoid

For systems, abstract concepts, and analytical judgments, describe the mechanism and difference directly. Avoid colloquial action metaphors, literary language, and labels without concrete referents:

*   **Colloquial action metaphors (prohibited throughout the article)**: This prohibition applies to the entire article. Do not use "grow out of," "grow into," "unpack," "break through," "pierce," "lock in," "rock solid," "sharp," or similar action metaphors anywhere in place of explanation.
    *   *Rewrite*: Replace the metaphor with a mechanism. "Breaks through the assumption" becomes "invalidates the assumption" or "the boundary no longer holds." "Unpack" becomes "analyze," "separate into layers," or "check item by item."
*   **Structural as an explanation**: Do not use vague labels such as "structural reason" or "structural contradiction."
    *   *Rewrite*: State the underlying mechanism, source of the constraint, or location of the conflict.
*   **Narrative arc as a placeholder**: Do not use "narrative arc" to avoid stating how an article or event develops.
    *   *Rewrite*: State the sequence and what drives it.
*   **Vague system-state words**: Avoid words such as "collapsed," "broke," or "couldn't hold" as summaries of a system or argument.
    *   *Rewrite*: Use verifiable descriptions such as "terminated abnormally," "the request failed," "the session drifted," "the premise no longer holds," or "the state cannot be maintained."

---

## 2. Translation-Like Prose and Meaning Mismatch

Do not mechanically transfer the semantic range of a word from another language. Common mismatches include:

*   **expensive / cheap**: For abstract trade-offs, use "high cost," "low cost," "high consequence," or "low consequence" rather than vocabulary reserved for a product's price.
*   **natural**: Distinguish "not artificial" from "inherent," "built in," or "native to the system."
*   **model / framework**: Distinguish machine-learning models from a mental model, line of reasoning, evaluation method, or conceptual framework.
*   **Literal metaphor translation**:
    *   Replace "stand on a layer" with "belongs to a layer."
    *   Replace "serves X" when necessary with the concrete audience or purpose it addresses.
    *   Remove "an uncomfortable fact" preambles. State the fact directly or say that it contradicts the prevailing narrative.
    *   Replace "blast radius" outside a necessary technical context with "scope of impact."

### No Redundant Bilingual Parentheticals

When the article's primary language already expresses a concept clearly, do not immediately repeat an English translation in parentheses. Forms equivalent to a translated ordinary concept followed by its English gloss add visual noise, create a translation-like cadence, and become a template that models repeat across articles.

Use the article's primary language for ordinary concepts without a parenthetical gloss. Preserve official product names, API names, protocol names, code identifiers, and standard industry abbreviations, such as `Turso Sync`, `push()`, and `RLS`. If the English term is more common than its translation, use the English term directly and explain it naturally once; do not turn the sentence into a bilingual lookup table.

A bilingual form is justified only when the article analyzes translation differences, resolves terminology ambiguity, or gives readers the original phrase needed to find primary sources. In those cases, state why the original term matters rather than silently appending it.

---

## 3. Article Openings, Presumptive Patterns, and Article-Wide Prohibitions

Do not pull the reader in through false consensus or a superior tone:

*   **"If you X, chances are Y" openings**: Do not use this pattern to open an article or paragraph. It manufactures consensus without adding information.
    *   *Rewrite*: State the fact directly or open with a concrete event.
*   **"If you X, you probably know Y" reader assumptions**: This excludes readers who do not know Y and wastes the time of readers who do.
    *   *Rewrite*: State Y directly with the objective subject as the grammatical subject.
*   **"Worth noting/considering/remembering" recommendations (prohibited throughout the article)**: This prohibition applies to the entire article, not only its opening. Do not use "worth noting," "worth considering," "worth remembering," or other "worth + X" expressions anywhere in the article. Do not tell readers which facts deserve their attention.
    *   *Rewrite*: Remove the label and present the fact or mechanism directly.

---

## 4. Downgrading Template-Like AI Rhetoric

AI systems frequently repeat these rhetorical templates. Replace or reduce them:

*   **"Not X, but Y" contrast**: If it appears three or more times in one article, rewrite it.
    *   *Rewrite*: State Y directly or use a light contrast such as "less X, more Y" or "X appears on the surface; the constraint is Y."
*   **Personification of abstract subjects**: Do not give buildings, years, neighborhoods, or systems intentional actions such as "writes to," "catches," or "draws a line."
    *   *Rewrite*: Restore the concrete actor and action.
*   **Mechanical parallelism**: Avoid repeated sentence templates such as "one rule defines materials, one style defines composition." Split them into ordinary sentences.

---

## 5. Prose Bad-to-Good Pairs

When drafting external articles, the main thread and writing agents should use these pairs to calibrate sentence structure and vocabulary:

### Pair 1: Split Overloaded Modifiers
*   ❌ **Bad**: The migration, cleanup, and boilerplate work that appears inefficient when viewed only through time spent becomes free in the AI era.
*   ✅ **Good**: These tasks look low-value on a schedule. A manager may classify them as inefficiency. For the brain, they still matter.

### Pair 2: Replace Elevated Words and Abstract Subjects
*   ❌ **Bad**: The release of this technology produced a stronger sense of fatigue, significantly correlating with user cognitive overload through a mechanism of critical importance.
*   ✅ **Good**: People became more tired after the technology arrived. Their attention was overloaded.

### Pair 3: Soften the Not-X-But-Y Contrast
*   ❌ **Bad**: You are not doing more physical work, but remaining in a high-cognitive-bandwidth state for longer.
*   ✅ **Good**: You are doing no more physical work. You are simply spending longer in a high-cognitive-bandwidth state.

### Pair 4: Replace a Presumptive Hook
*   ❌ **Bad**: If you followed AI engineering in early 2026, you probably heard that multi-agent systems were the major trend.
*   ✅ **Good**: Early 2026 put two opposing signals in front of AI engineers. Swarm systems set new benchmark highs while production frameworks continued to report high failure rates.

---

## 6. Anti-Textbook Tone: Make Explanations Sound Like a Person Talking

Low cognitive burden is not the same as "easy to understand." Many sentences are factually accurate, grammatically concise, and conceptually complete, yet still read like a product manual or textbook. The typical symptom: first define the object, then announce "this adjustment produced some impact," and finally summarize the discussion with an abstract noun. The reader understands every sentence, but never feels the author discovering the problem alongside them.

Familiarity is not the same as adding filler words, internet slang, or second person. It comes from a more basic way of writing: the author and the reader face the same concrete problem, and the author explains the anomalies, questions, and reasoning in the order they actually encountered them. Concepts are introduced when needed, not lined up to receive definitions.

### 6.1 Do Not Write "Concept Introduction" as a Dictionary Definition

The following patterns are not absolutely forbidden, but when several appear within a single paragraph, the prose has usually reverted to manual tone:

- "X is a ... that allows users to ..."
- "X refers to ..., whose main purpose is ..."
- "This adjustment changed / affected ..."
- "This sparked discussion in the industry about X."
- "In this process / under this system / from this perspective ..."
- "This laid the foundation for subsequent X."

When revising, do not just swap synonyms. Ask first: what does the reader actually want to know at this moment? Who did what? Where is it different from before? When something goes wrong, what specific judgment capability does the person lose? Write the answer; the concept will be introduced naturally.

### 6.2 Carry Concepts with Action and Question

*   ❌ **Bad**: Codex is an open-source local programming agent client that allows developers to invoke OpenAI's large models in the local environment to execute tasks.
*   ✅ **Good**: Codex reads and writes files on your machine, runs terminal commands, and saves execution records locally. When something goes wrong, developers usually trace back along those records.

*   ❌ **Bad**: This adjustment directly affected local auditing.
*   ✅ **Good**: The trouble shows up when you go back to investigate. You know the main agent opened a sub-agent, and you can see what the sub-agent did later, but the middle sentence "go do X" is now only a string of ciphertext.

*   ❌ **Bad**: This sparked discussion in the technical community about agent transparency.
*   ✅ **Good**: So what people追问 in issue #28058 is actually quite concrete: what task did this sub-agent actually receive? When it later did something wrong, was the task dispatched wrongly, or did it execute wrongly?

These Good examples show the conversion method, not a new fixed template. Do not mechanically reuse "the trouble shows up" or "what people追问 is actually quite concrete" or any set of readymade phrasings in every article.

### 6.3 Sentences Need to Breathe; Do Not Cut Everything into Manual Short Sentences

Short sentences reduce local burden, but continuous "subject + is/will/can + definition" creates a broadcast feel. Natural prose usually mixes long and short: short sentences land judgments, slightly longer ones connect cause, example, and transition. Do not, to satisfy a word count cap, cut a coherent paragraph into five equally long declaratives.

The criterion is not average sentence length; it is whether, read aloud, it sounds like someone familiar with the problem explaining it to another smart person. If every sentence could go into a product document but none sounds like a real conversational explanation, rewrite the whole paragraph rather than continuing to split sentences.

### 6.4 Abstract Nouns Must Land on Reader-Observable Consequences

"Declining transparency," "auditing blocked," "shifting information boundary" can all serve as paragraph conclusions, but they cannot replace explanation. On first appearance they must land on a concrete consequence, for example:

- You can see the agent being created, but not the task it received;
- You can see commands executing, but cannot tell whether a command came from a wrong dispatch or a wrong understanding;
- You can replay the tool record, but cannot reconstruct the complete causal chain.

Let the reader see these facts first, then name them. Do not lead with "auditability declined" and then spend three paragraphs explaining what those six characters mean.

### 6.5 Familiar Prose Is Not Colloquial; It Is Shortening the Narrative Distance

Sometimes an article already has no long sentences or rare words and still feels stiff. The reason is often not that the words are too hard, but that the narrator stands too far away: it invents a set of role names for the system, describes actions from an institutional viewpoint, and summarizes consequences in abstract nouns. A real person explaining the same thing would usually say directly "you will see what," "where a step is missing," "how to investigate when it breaks."

Focus on four categories of translation-tone:

- **Redundant role nouns**: `the client and its operator`, `the task recipient`, `the execution subject`. When the reader's identity is clear, write "you" / "the developer" directly, or drop the subject.
- **Nominalized actions**: `perform encryption on that state`, `complete task distribution`, `achieve plaintext recovery`. Restore ordinary verbs: "encrypt this content," "send the task out," "recover the plaintext."
- **System-viewpoint result sentences**: `make local logs unable to reveal their specific content`. State what happened first, then what the reader sees: "this part returns locally as ciphertext, so you cannot see the specific content from the logs."
- **Abstract consequences replacing real losses**: `lost key causal input`, `lacked direct observation point`, `unable to perform pre-validation`. Write directly which piece of information is missing and therefore what cannot be distinguished.

The three rewrites below come from the same actual article. They show viewpoint shift, not fixed sentence patterns:

*   ❌ **Bad**: The Codex client running locally and its operator can no longer read the text of this delegated task from local records.
*   ✅ **Good**: What is lost is your ability to look back at that sentence: what the main agent actually told it to do, the local record no longer tells you.

*   ❌ **Bad**: The Responses API encrypts that state when returning data, making local logs unable to reveal its specific content.
*   ✅ **Good**: This content returns locally as ciphertext. You can see the final answer, but cannot read from the logs what it was actually thinking in between.

*   ❌ **Bad**: After the instruction text becomes ciphertext locally, the developer loses this direct observation point for causal input.
*   ✅ **Good**: You can still see when the sub-agent was created, and you can see which commands it ran later. But that middle sentence "go do X" is now only a string of ciphertext.

The final criterion is not "did you use second person," but whether someone familiar with the problem would explain it this way to a smart reader. Do not, to seem familiar, add slang, internet memes, exaggerated metaphors, or excessive filler words; those only swap formal tone for performative colloquialism.

### 6.6 Do Not Write the Editing Conversation into the Body

When an editor or user points out a confusion, it usually signals missing prerequisite information in the body, not that the article should answer it verbatim. The most common bad form is to write the editor's misunderstanding directly as a heading or negation. A new reader who has not seen that conversation suddenly encounters the author rebutting a view that never appeared.

*   ❌ **Bad**: Choosing 1.7B is not picking a winner between two training results.
*   ✅ **Good**: Every training job must specify a starting checkpoint before the GPU starts; the options are 0.6B and 1.7B. The proportion of jobs later choosing 1.7B rose, indicating the training budget allocation shifted.

*   ❌ **Bad**: prime-rl is not another chosen model.
*   ✅ **Good**: Once the starting model is fixed, prime-rl runs the inner-loop reinforcement learning training per the job config.

After revising, run the "hidden conversation test": delete all editing records and read only the body. Does the reader already know from preceding text what this sentence is answering? If not, supplement the action order, roles, and impact, rather than keeping the rebuttal aimed at a misunderstanding.

### 6.7 The Goal Is Not Colloquial, but Natural Introduction

The most common stylistic misjudgment in external technical writing is to treat "accurate and easy to understand" as "familiar." An article can have no long sentences, no rare words, every concept explained, and still read like a textbook. The cause is usually paragraph architecture: the author first announces the section topic, then defines the object, then explains the mechanism, and finally closes with an abstract judgment. What the reader receives is a simplified lecture, not a person sharing a change they just figured out.

A qualified natural introduction usually proceeds differently:

1. First state the contrast, question, or observation unique to this piece, so the reader knows why the author wants to talk about it now.
2. Follow a real process. Concepts appear as actions happen, not in glossary order.
3. The author's judgment can enter lightly, e.g., "what I find most interesting about this change is ...". First person only signals focus; it does not render emotion or replace evidence.
4. Each section answers the next thing the reader would naturally ask at that point. Paragraphs land on who has to wait, what has to be moved, which capability is lost, where the cost is counted, rather than announcing industry significance once per section.

Three voices to separate:

*   **Textbook voice**: `The reason lies in the two stages of a single generation request. The scheduler therefore trades off between two types of goals.` The facts are right, but the author is lecturing from an outline.
*   **Performative colloquial**: `vLLM is like a bus. Several stages fight each other.` The sentences are livelier, but exaggerated metaphor and slang replace mechanism, and may induce factual oversimplification.
*   **Natural introduction**: `vLLM wants the whole fleet of machines to do more work; TileRT wants this one request to finish faster. Why can't one engine do both well? The answer starts from how a model generates one reply.` The author is present, the question is concrete, and there is a natural causal entry for what follows.

These examples show narrative distance, not copyable templates. A new article must find its own entry from its own evidence, and must not mechanically reuse phrasings like "originally unlikely to come together," "the most interesting part," or "the trouble is here."

#### Bidirectional Calibration Method

For every prose pass, prepare one positive sample and two negative extremes:

* The positive sample is an article the user has explicitly approved, with a topic of similar explanation difficulty. Use an existing approved technical article as the voice reference; pick one with a similar topic and confirmed user approval.
* The textbook negative sample: pull 2-3 paragraphs from this draft's structural draft or IC-2 first draft, and mark the repeated "definition → mechanism → summary" rhythm.
* The over-colloquial negative sample: pull 2-3 paragraphs and mark decorative metaphors, slang, personification, and absolute judgments.

When calibrating, learn only the narrative distance of the positive sample: how the author enters, how the question arises naturally, how concepts land with the action. Do not imitate its fixed openings, first-person position, metaphors, or paragraph count.

#### One-Minute Read-Aloud Check

After the full text is done, read continuously the opening, the first paragraph of every H2, and the ending. For each paragraph judge:

* Would someone who truly understands this open this way to a smart friend?
* After deleting the heading, does the paragraph still sound like it is announcing "this section will introduce X"? If so, rewrite the entry.
* After deleting metaphors or slang, is the mechanism still clear? If not, the familiarity is built on performance.
* Does the author appear only when there is a judgment? If "I think" is followed by only a fact summary, delete the first person.

This check has higher priority than average sentence length, connector count, or "colloquial word" hit count. All the latter passing cannot override a single veto from textbook voice or performative voice.

### 6.8 Understandable Does Not Mean Comfortable to Read

Low cognitive burden has two different layers. First, whether the reader has the context needed to understand each concept. Second, how many new concepts and relations the reader must hold in mind at any moment. Passing the first does not guarantee the second: every term has an explanation, no paragraph has long sentences, yet the reader still has to pause to sort out the four axes, three object layers, and two exception sets the author just listed.

The most common cause is turning the author's own analysis process directly into body text. To think the problem through, the author may need four inspection axes: stable identity, state ownership, extension unit, recovery unit; the reader does not necessarily need to learn this framework first. Unless the article's deliverable is itself teaching the reader to use that checklist, first walk one concrete object through a real process, and let the reader see the difference before naming it.

*   ❌ **Bad**: To understand a platform, you need to check stable identity, state ownership, extension unit, and recovery unit at the same time.
*   ✅ **Good**: The same support ticket, on one platform, is read back by a freshly started program from the database; on another platform, the next message finds the original local state by Agent ID; on a third, after approval returns, the task resumes from the step where it stopped.

The Good version is not better because the words are more colloquial, but because four abstract relations are carried by one familiar object in time order. The reader just follows the same ticket forward; they do not have to operate an analysis matrix at the same time.

Follow four principles when reducing this kind of burden:

* **Same process first**: when comparing multiple schemes horizontally, try to let the same request, person, order, or file run through each section. Changing the scene every section forces the reader to rebuild context.
* **Action before naming**: first write "after approval returns, resume from the next step," then introduce Workflow; first write "the next message returns to the same customer assistant," then introduce Agent ID.
* **Headings should be cold-readable**: an H2 alone should also express an action, change, or reader question. A heading understandable only by mastering the article's internal taxonomy charges a concept cost before the reader even enters the body.
* **One paragraph advances one main relation**: splitting short sentences cannot solve concept stacking. If a paragraph simultaneously introduces platform, component, state model, and failure boundary, re-arrange the information order so each paragraph starts from an object the reader already knows.

Finally, run the retelling test: after reading the first paragraph of a section, without using the jargon just introduced, can you state who did what, what changed, and why it differs from the previous scheme? If you can only retell the classification labels, the article is still handing the author's framework to the reader.
