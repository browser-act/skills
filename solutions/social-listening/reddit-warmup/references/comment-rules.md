# AI Comment Generation Rules

Guidelines for generating Reddit comments that read like a real person wrote them. The goal is genuine engagement, not spam -comments that add value to the conversation while building the account's credibility.

---

## Core Principle

A good comment does one of these things:
- Directly answers or responds to what the post is actually asking
- Shares a relevant personal experience that relates to the topic
- Asks a genuine follow-up question that shows you read the post
- Adds a useful piece of information the post didn't cover

If you can't do any of these naturally, skip this post and find another.

---

## Length Guidelines

| Subreddit type | Word count | Why |
|----------------|-----------|-----|
| Warmup subs (casual, high-traffic) | 15-50 words | These subs are busy; medium-length comments feel natural |
| Target niche subs (your domain) | 20-80 words | Domain communities reward slightly more depth and specificity |
| Large generic subs (r/AskReddit, etc.) | 10-40 words | Shorter, punchier; longer comments get lost |

Never write a single word (like "Agreed"). Never write an essay. The sweet spot is 2-4 sentences.

---

## Tone and Voice

Match the tone of the subreddit and the account's `content` persona (supplied by the user -never invented by the skill). The through-line is: direct, specific, and sounds like someone who actually knows the topic.

**Shape of a good comment:**
> "I ran into this exact problem [specific-timeframe]. The root cause was [concrete detail tied to the poster's situation]. [One-line description of what fixed it, including a detail only someone who lived through it would know]."

Whatever specific content goes into `[...]` comes from the persona the user configured -the skill reads it, never supplies it.

**Bad (any persona):**
> "This is a great question! I have extensive experience in this area and I believe that the best solution would be to leverage industry-standard best practices combined with modern tooling approaches."

The bad version sounds like a press release. Real people are specific about what they tried, what happened, and what they'd recommend. Generic comments hurt the account -if the persona doesn't have something specific to say on a given post, skip the post.

---

## Forbidden Patterns

Never include these in warmup/comment stage comments (Days 15-29):

| Pattern | Why it gets flagged |
|---------|-------------------|
| Links (any URL) | Instant spam signal for new accounts |
| Brand names (your product or competitors) | Brand mentions before Day 30 look like paid promotion |
| Generic filler: "great post", "this!", "^^", "I agree" | Zero value, looks like a bot upvote farm |
| Repeating a previous comment you made | Reddit's systems detect this. Hard-blocked pre-approval via jaccard similarity >=0.80 vs the last 200 entries in activity_log.jsonl -see `stage2-comment.md ->Duplicate Content Check`. Applies cross-account in multi-account mode. |
| Starting with "As an AI..." or similar | Obviously wrong, but worth stating |
| Emoji spam | 1 emoji occasionally is fine; 3+ looks non-human |
| Hashtags | Reddit doesn't use hashtags; this instantly reads as cross-platform bot |

### AI-smell vocabulary (forbidden in every stage)

These words and phrases are near-universal tells that a language model wrote the text. They're common in academic/formal English but almost never appear in native casual Reddit comments. Downvoters spot them instantly.

**Transitions / structure:**
`Furthermore`, `Moreover`, `Additionally`, `In conclusion`, `To summarize`, `Overall`, `Firstly`/`Secondly`/`Thirdly`, `It's worth noting that`, `It's important to remember`, `That being said` (when used as a pivot)

**Empty-intensifier verbs:**
`leverage`, `utilize` (use "use"), `facilitate`, `delve into` (use "dig into" or "get into"), `navigate the landscape of`, `explore the nuances of`

**Hype adjectives masquerading as analysis:**
`robust`, `seamless`, `comprehensive`, `cutting-edge`, `game-changer`, `revolutionary`, `holistic`, `synergistic`, `crucial` (overused), `paramount`

**Formulaic closers:**
`I hope this helps!`, `Feel free to ask if you have any questions`, `Happy to dive deeper if useful`, `At the end of the day,` (as sentence opener)

**Fake humility / hedging stacks:**
`It's important to consider that, while X, it's also worth noting that Y, however Z` -the telltale three-clause balanced sentence

Before publishing any generated comment or post, scan it for items in this list and either rewrite or skip. When in doubt: read the comment aloud -if it sounds like a LinkedIn post or a help-desk reply, it's AI-smelly. If it sounds like a real person grumbling or explaining, it's fine.

---

## The `content` Keyword Persona

The `config.yaml ->keywords.content` list (or the richer `persona_file` if set) defines who this account is -their background, experience, and perspective. **All persona content is user-supplied.** The skill reads it and uses it as a lens, nothing more.

Expected shape:
```yaml
keywords:
  content:
    - "<role / identity>"
    - "<concrete experience or domain knowledge>"
    - "<additional perspective, optional>"
```

When generating a comment, write from that identity. Different personas answer the same post differently -a deep-expert persona leads with specifics and caveats; a practitioner persona leads with lived experience and outcomes. Pick whichever lens matches what the user configured, and keep it consistent across all of this account's comments.

During warmup/comment-stage work, persona should shape voice lightly, not topic selection. A professional persona can still comment like a normal person in broad communities; do not force the account into marketing, startup, technical, finance, legal, medical, or other expert threads just to match the persona.

Don't literally paste the keywords into the comment -internalize them as who you're pretending to be.

---

## Using `find` Keywords

Before generating a comment, search for posts using the `find` keywords. You want posts where your persona naturally has something useful to say.

Example: if `find` keywords include "bypass captcha", look for posts where people are struggling with CAPTCHAs and where you can share a relevant experience or insight.

---

## Comment Quality Checklist

Before posting, verify:
- [ ] Responds to something specific in the post (not generic)
- [ ] Length is in the right range for this subreddit
- [ ] No links, no brand names (before Day 30)
- [ ] Written in casual, conversational tone
- [ ] Adds real value (answers, shares experience, or asks a genuine question)
- [ ] Not a copy of a previous comment in `activity_log.jsonl`

---

## What a "good comment" looks like (structure, not content)

Whatever the persona, a good comment follows this shape:

1. **React to a specific detail** from the post or top comments in the first sentence -not a general statement about the topic.
2. **Share one concrete piece of personal experience** -"I hit this when...", "last time I tried X it...", "the thing that surprised me was..." -something a reader can't tell you didn't live through.
3. **End with either a specific recommendation or a genuine follow-up question** -not a feel-good closer.

All three pieces come from the persona the user configured. The skill's job is to enforce the structure and strip generic filler; the content itself is user-supplied.

---

### What to do when you can't write a natural comment

Don't force it. If the post is:
- In a domain the account's persona doesn't credibly know
- Already fully answered with nothing to add
- A joke/meme post where the persona's angle is out of place

->Just upvote and move to the next post. Forced, generic comments hurt the account more than silence.

---

## Stage 3 Promotional Comments

From Day 30 onward, brand keywords (user-supplied in `config.yaml ->keywords.brand`) can appear -but they should feel earned, not planted.

**Shape that works:**
1. Describe a concrete problem the persona had (not in the abstract).
2. What was tried that didn't work.
3. One line on what did work -brand mentioned naturally, once, not at the start.
4. Outcome in one line, optionally inviting follow-up.

No superlatives, no marketing language, no CTAs, no links. If the brand isn't genuinely relevant to the thread, leave it out -a non-promotional comment still builds karma and credibility.

**Signal that a promo comment is off:** it reads like ad copy. Any of these patterns = rewrite:
- Starts with the brand or the recommendation
- Uses "amazing" / "incredible" / "game-changer" / "revolutionary"
- Ends with a URL or "check it out"
- Explains what the product does in marketing terms rather than what it did for the commenter specifically

