x

This website requires javascript to properly function. Consider activating javascript to get access to all site functionality. 

## [LESSWRONG](https://www.lesswrong.com/)

## [LW](https://www.lesswrong.com/)

Login

interpreting GPT: the logit lens — LessWrong

[GPT](https://www.lesswrong.com/w/gpt)[Machine Learning (ML)](https://www.lesswrong.com/w/machine-learning-ml)[Gears-Level](https://www.lesswrong.com/w/gears-level)[Interpretability (ML & AI)](https://www.lesswrong.com/w/interpretability-ml-and-ai)[AI](https://www.lesswrong.com/w/ai)[Frontpage](https://www.lesswrong.com/posts/5conQhfa4rgb4SaWx/site-guide-personal-blogposts-vs-frontpage-posts)

[](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens)

# 279

# [interpreting GPT: the logit lens](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens)

by [nostalgebraist](https://www.lesswrong.com/users/nostalgebraist?from=post_header)

31st Aug 2020

[AI Alignment Forum](https://alignmentforum.org/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens)

13 min read

[38](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#comments)

[](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens)

# 279

# Ω 80

This post relates an observation I've made in my work with GPT-2, which I have not seen made elsewhere.

IMO, this observation sheds a good deal of light on how the GPT-2/3/etc models (hereafter just "GPT") work internally.

There is an accompanying [Colab notebook](https://colab.research.google.com/drive/1-nOE-Qyia3ElM17qrdoHAtGmLCPUZijg?usp=sharing) which will let you interactively explore the phenomenon I describe here.

_[Edit: updated with another section on comparing to the inputs, rather than the outputs. This arguably resolves some of my confusion at the end. Thanks to algon33 and Gurkenglas for relevant suggestions here.]_

_[Edit 5/17/21: I 've recently written a [new Colab notebook](https://colab.research.google.com/drive/1MjdfK2srcerLrAJDRaJQKO0sUiZ-hQtA?usp=sharing) which extends this post in various ways:_

  * _trying the "lens" on various models from 125M to 2.7B parameters, including GPT-Neo and CTRL_
  *  _exploring the contributions of the attention and MLP sub-blocks within transformer blocks/layers_
  *  _trying out a variant of the "decoder" used in this post, which dramatically helps with interpreting some models_



 _]_

# overview

  * GPT's probabilistic predictions are a linear function of the activations in its final layer. If one applies the same function to the activations of _intermediate_ GPT layers, the resulting distributions make intuitive sense.
    * This "logit lens" provides a simple (if partial) interpretability lens for GPT's internals.
    * Other work on interpreting transformer internals has focused mostly on what the attention is looking at. The logit lens focuses on _what_ GPT "believes" after each step of processing, rather than _how_ it updates that belief inside the step.
  * These distributions gradually converge to the final distribution over the layers of the network, often getting close to that distribution long before the end.
    * At some point in the middle, GPT will have formed a "pretty good guess" as to the next token, and the later layers seem to be refining these guesses in light of one another.
    * The general trend, as one moves from earlier to later layers, is 
      * "nonsense / not interpretable" (sometimes, in very early layers) -->
      * "shallow guesses (words that are the right part of speech / register / etc)" \-->
      * "better guesses"
    * ...though some of those phases are sometimes absent.
  * On the other hand, o _nly_ the inputs look like the input tokens.
    * In the logit lens, the early layers sometimes look like nonsense, and sometimes look like very simple guesses about the output. They almost never look like the input.
    * Apparently, the model does not "keep the inputs around" for a while and gradually process them into some intermediate representation, then into a prediction.
    * Instead, the inputs are _immediately_ converted to a very different representation, which is smoothly refined into the final prediction.
  * This is reminiscent of the perspective in [Universal Transformers ](https://arxiv.org/abs/1807.03819)which sees transformers as iteratively refining a guess.
    * However, Universal Transformers have both an encoder and decoder, while GPT is only a decoder. This means GPT faces a tradeoff between keeping around the input tokens, and producing the next tokens.
    * _Eventually_ it has to spit out the next token, so the longer it spends (in depth terms) processing something that looks like token _i,_ the less time it has to convert it into token _i+1_. GPT has a deadline, and the clock is ticking.
  * More speculatively, this suggests that GPT mostly "thinks in predictive space," immediately converting inputs to predicted outputs, then refining guesses in light of other guesses that are themselves being refined.
    * I think this might suggest there is some fundamentally better way to do sampling from GPT models? I'm having trouble writing out the intuition clearly, so I'll leave it for later posts.
  * Caveat: I call this a "lens" because it is one way of extracting information from GPT's internal activations. I imagine there is other information present in the activations that cannot be understood by looking at logits over tokens. The logit lens show us some of what is going on, not all of it.

  


# background on GPT's structure

You can skip or skim this if you already know it.

  * Input and output
    * As _input,_ GPT takes a sequence of tokens. Each token is a single item from a vocabulary of _N_v_ =50257 byte pairs (mostly English words).
    * As _output,_ GPT returns a probability distribution over the vocabulary. It is trained so this distribution predicts the next token.
    * That is, the model's outputs are shifted forward by one position relative to the inputs. The token at position _i_ should, after flowing through the layers of the model, turn into the token at position _i+1_. (More accurately, a distribution over the token at position _i+1._)
  * Vocab and embedding spaces
    * The vocab has size _N_v_ =50257, but GPT works internally in a smaller "embedding" vector space, of dimension _N_e_. 
      * For example, in the GPT-2 1558M model size, _N_e_ =1600. (Below, I'll often assume we're talking about GPT-2 1558M for concreteness.)
    * There is an _N_v_ -by-_N_e_ embedding matrix _W_ which is used to project the vocab space into the embedding space and vice versa.
  * In, blocks, out
    * The first thing that happens to the inputs is a multiplication by _W_ , which projects them into the embedding space. [[1]](about:blank#fn-AtHPnbaLw7d3539eA-1)
    * The resulting 1600-dimensional vector then passes through many neural network blocks, each of which returns another 1600-dimensional vector.
    * At the end, the final 1600-dimensional vector is multiplied by _W 's_ transpose to project back into vocab space.
    * The resulting 50257-dim vectors are treated as logits. Applying the softmax function to them gives you the output probability distribution.

  


# the logit lens

As described above, GPT schematically looks like

  * Project the input tokens from vocab space into the 1600-dim embedding space
  * Modify this 1600-dim vector many times
  * Project the final 1600-dim vector back into vocab space



We have a "dictionary," _W_ , that lets us convert between vocab space and embedding space at any point. We know that _some_ vectors in embedding space make sense when converted into vocab space:

  * The very first embedding vectors are just the input tokens (in embedding space) 
  * The very last embedding vectors are just the output logits (in embedding space) 



What about the 1600-dim vectors produced in the middle of the network, say the output of the 12th layer or the 33rd? If we convert them to vocab space, do the results make sense? The answer is _**yes**_.

## logits

For example: the plots below show the logit lens on GPT-2 as it predicts a segment of the abstract of the GPT-3 paper. (This is a segment in the middle of the abstract; it can see all the preceding text, but I'm not visualizing the activations for it.)

For readability, I've made two plots showing two consecutive stretches of 10 tokens. Notes on how to read them:

  * The input tokens are shown as 45-degree tilted axis labels at the bottom.
  * The correct output (i.e. the input shifted by one) is likewise shown at the top.
    * A (*) is added in these labels when the model's top guess matched the correct output.
  * The vertical axis indexes the layers (or "blocks"), zero-indexed from 0 to 47. To make the plots less huge I skip every other intermediate layer. The Colab notebook lets you control this skipping as you like.
  * The top guess for each token, according to the model's activations at a given layer, is printed in each cell.
  * The colors show the logit associated with the top guess. These tend to increase steadily as the model converges on a "good guess," then get refined in the last layers.
  * Cells are outlined when their top guess matches the final top guess.
  * _For transformer experts: the "activations" here are the block outputs after layer norm, but before the learned point-wise transformation._

  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/ccfmt4rt3aegjjfi7lo8)  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/iuhgaaogzzkoim0t85mn)

There are various amusing and interesting things one can glimpse in these plots. The "early guesses" are generally wrong but often sensible enough in some way:

  * "We train GPT-3..." _000?_ (someday!)
  * "GPT-3, an..." _enormous? massive?_ (not wrong!)
  * "We train GPT-3, an aut..." _oreceptor?_(later converges to the correct _oregressive_)
  * "model with 175..." _million_? (later converges to a comma, not the correct _billion_)



## ranks

The view above focuses only on the top-1 guess at each layer, which is a reductive window on the full distributions.

Another way to look at things: we still reduces the _final_ output to the top-1 guess, but we compare other distributions to the final one by looking at the rank of the final top-1 guess. 

Even if the middle of the model hasn't yet converged to the final answer, maybe it's got that answer somewhere in its top 3, top 10, etc. That's a lot better than "top 50257."

Here's the same activations as ranks. (Remember: these are ranks of _the model 's final top-1 prediction,_ not _the true token._)

  
  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/u4idlaozp3dnnom3qitn)  
  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/myvdodsqn089nxqqmm5j)

In most cases, network's uncertainty has drastically reduced by the middle layers. The order of the top candidates may not be right, and the probabilities may not be perfectly calibrated, but it's got the gist already.

## KL divergence and input discarding

Another way of comparing the similarity of two probability distributions is the KL divergence. Taking the KL divergence of the intermediate probabilities w/r/t the final probabilities, we get a more continuous view of how the distributions smoothly converge to the model's output.

Because KL divergence is a more holistic measure of the similarity between two distributions than the ones I've used above, it's also my preferred metric for making the point that _nothing looks like the input_.

In the plots above, I've skipped the input layer (i.e. the input tokens in embedding space). Why? Because they're so different from everything else, they distract the eye!

In the plots below, where color is KL divergence, I include the input as well. If we trust that KL divergence is a decent holistic way to compare two distributions (I've seen the same pattern with other metrics), then:

  * Immediately, after the very first layer, the input has been transformed into something that looks more like _the final output_(47 layers layer) than it does like the input.
  * After this one discontinuous jump, the distribution progresses in a much more smooth way to the final output distribution.

  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/zmbskn2mxxemmwzsexqh)  
  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/qwudyevttoligkn7neul)

# other examples

I show several other examples in the Colab notebook. I'll breeze through a few of them here.

## copying a rare token

Sometimes it's clear that the next token should be a "copy" of an earlier token: whatever arbitrary thing was in that slot, spit it out again.

If this is a token with relatively low prior probability, one would think it would be useful to "keep it around" from the input so later positions can look at it and copy it. But as we saw, the input is never "kept around"!

What happens instead? I tried this text:

> Sometimes, when people say plasma, they mean a state of matter. Other times, when people say plasma

As shown below (truncated to the last few tokens for visibility), the model correctly predicts "plasma" at the last position, but only figures it out in the very last layers.

Apparently it _is_ keeping around a representation of the token "plasma" with enough resolution to copy it . . . but it only retrieves this representation at the end! (In the rank view, the rank of plasma is quite low until the very end.)

This is surprising to me. The repetition is directly visible in the input: "when people say" is copied verbatim. If you just applied the rule "if input seems to be repeating, keep repeating it," you'd be good. Instead, the model scrambles away the pattern, then recovers it later through some other computational route.

  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/rivyv2ifkg7clagpde9y)

## extreme repetition

We've all seen GPT sampling get into a loop where text repeats itself exactly, over and over. When text is repeating like this, where is the pattern "noticed"?

At least in the following example, it's noticed in the upper half of the network, while the lower half can't see it even after several rounds of repetition.

  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/pi7xanxwfkyr1fu111wg)

# why? / is this surprising?

First, some words about why this trick can even work at all.

One can imagine models that perform the exact same computation as GPT-2, for which this trick would _not_ work. For instance, each layer could perform some arbitrary vector _rotation_ of the previous one before doing anything else to it. This would preserve all the information, but the change of basis would prevent the vectors from making sense when multiplied by _W^T._

Why doesn't the model do this? Two relevant facts:

1\. Transformers are residual networks. Every connection in them looks like _x + f(x)_ where _f_ is the learned part. So the identity is very easy to learn.

This tends to keep things in the same basis across different layers, unless there's some reason to switch.

2\. Transformers are usually trained with weight decay, which is _almost_ the same thing as L2 regularization. This encourages learned weights to have small L2 norm.

That means the model will try to "spread out" a computation across as many layers as possible (since the sum-of-squares is less than the square-of-sums). Given the task of turning an input into an output, the model will generally prefer changing the input a little, then a little more, then a little more, bit by bit.

1+2 are a good story if you want to explain why the same vector basis is used across the network, and why things change smoothly. This story _would_ render the whole thing unsurprising . . . except that the _input_ is discarded in such a discontinuous way!

I would have expected a U-shaped pattern, where the early layers mostly look like the input, the late layers mostly look like the output, and there's a gradual "flip" in the middle between the two perspectives. Instead, the input space immediately vanishes, and we're in output space the whole way.

Maybe there is some math fact I'm missing here.

Or, maybe there's some sort of "hidden" invertible relationship between

  * the embedding of a given token, and 
  * the model's prior for what token comes after it (given no other information)



so that a token like "plasma" _is_ kept around from the input -- but not in the form "the output is plasma," instead in the form "the output is _[the kind of word that comes after plasma]._ "

However, I'm not convinced by that story as stated. For one thing, GPT layers don't share their weights, so the mapping between these two spaces would have to be separately memorized by each layer, which seems costly. Additionally, if this were true, we'd expect the very early activations to look like naive context-less guesses for the next token. Often they are, but just as often they're weird nonsense like "Garland."

# addendum: more on "input discarding"

In comments, Gurkenglas noted that the plots showing KL(final || layer) don't tend the whole story.

The KL divergence is not a metric: it is not symmetric and does not obey the triangle inequality. Hence my intuitive picture of the distribution "jumping" from the input to the first layer, then smoothly converging to the final layer, is misleading: it implies we are measuring distances along a path through some space, but KL divergence does not measure distance in any space.

Gurkenglas and algon33 suggested plotting the KL divergences of everything w/r/t the _input_ rather than the output: KL(input || layer).

Note that the input is close to a distribution that just assigns probability 1 to the input token ("close" because W * W^T is not invertible), so this is similar to asking "how probable is the input token, according to each layer?" That's a question which is also natural to answer by plotting ranks: what rank is assigned to the input token by each layer?

Below, I show both: KL(input || layer), and the rank of the input token according to later layers.

  * For KL(input || layer), I use the same color scale as in the plots for KL(final || layer), so the two are comparable.
  * For the ranks, I do _not_ use the same color scale: I have the colors bottom out at rank 1000 instead of rank 100. This gives more visual insight into where the model could be preserving input information.

  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/p004czhfds4wuzlvbgdv)  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/boqqfxm2onkxqjerczt2)  


  * There is still a fast jump in KL(input || layer) after the input.
    * However, it's far smaller than the jump in KL(output || layer) at the same point.
    * Note that the darkest color, meaning KL=30 does not appear on the plot of KL(input || layer).
    * On the plot of KL(output || layer), however, the maximum values were in fact much _greater_ than 30; I cut off the color scale at 30 so other distinctions were perceptible at all.
  * Likewise, while ranks jump quickly after the input, they often stay relatively high in the context of a ~50K vocab.
    * I am curious about the differences here: some tokens are "preserved" much more in this sense than others.
    * This is apparently contextual, not just based on the token itself. Note the stark differences between the rank trajectories of the first, second, and third commas in the passage.



It's possible that the relatively high ranks -- in the 100s or 1000s, but not the 10000s -- of input tokens in many cases is (related to) the mechanism by which the model "keeps around" rarer tokens in order to copy them later.

As some evidence for this, I will show plots like the above for the plasma example. Here, I show a segment including the _first_ instance of "plasma," rather than the second which copies it.

  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/nrhodujtfpqooqi3qq2x)  
  
![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/AcKRB8wDpdaN6v6ru/t6oibgjkaykknyt6itnj)

The preservation of "plasma" here is striking.

My intuitive guess is that the rarity, or (in some sense) "surprisingness," of the token causes early layers to preserve it: this would provide a mechanism for providing raw access to rare tokens in the later layers, which otherwise only be looking at more plausible tokens that GPT had guessed for the corresponding positions.

On the other hand, this story has trouble explaining why "G" and "PT" are not better preserved in the GPT3 abstract plots just above. This is the first instance of "GPT" in the full passage, so the model can't rely on copies of these at earlier positions. That said, my sense of scale for "well-preservedness" is a wild guess, and these particular metrics may not be ideal for capturing it anyway.

  
  


* * *

  1. Right after this, positional embeddings are added. I'm ignoring positional embeddings in the post, but mention them in this footnote for accuracy. [↩︎](about:blank#fnref-AtHPnbaLw7d3539eA-1)  




[interpreting GPT: the logit lens](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens)

[18gwern](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#cuyTAeQBbeEDE4mtr)

[7nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#X3beSnXb7AYmzWEd2)

[1oceaninthemiddleofanisland](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#v2CXmq8PfGGmr3HhR)

[3John Steidley](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#LXRSbKR4k5dvjbWEv)

[6gwern](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#6Lmv5yhEJjhX9GM9B)

[13evhub](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#hNXG59KWePbscydyG)

[7nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#j7ifsoeJSsFWwtEoo)

[3evhub](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#scDtsZ5dTecHbjHcA)

[5nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#4voSYQNDELj4wK8PC)

[5Vlad Mikulik](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#oQv4u7XsczdcKaphu)

[8gwern](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#8dierpoMbMWdekLzP)

[4Joseph Miller](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#YMJXShTPKDHswZr9p)

[3p.b.](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#zWmqxw9vYBFNac9A8)

[3Gurkenglas](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#KdFJgvgKE7XjPZEFm)

[3oekenta](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#6wbu8GCdEPHDWEdbK)

[2nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#bv9o3qTQEsYHczaqN)

[4Gurkenglas](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#KGFij5dbdfZbDQGPR)

[4nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#iAvRS3on8LrmMH9cW)

[2Gurkenglas](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#pnfbjAGkrKg6jRh38)

[2nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#9obzuuGpcSkWby4LZ)

[4gwern](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#o7LJmhLA9xBNvqw7S)

[2Gurkenglas](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#4zji3d2nw56qYM23Q)

[2algon33](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#uwNG3gytxEMas7PTB)

[2nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#Yf9CW7L6jDZ9W6r5y)

[2nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#3XcjQ4BnZNWBadQWz)

[2Gurkenglas](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#qsJfes3sRFa5QSuwi)

[2Riccardo Volpato](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#HEf5abD7hqqAY2GSQ)

[2SoerenMind](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#EezZefybpMHA7vWfx)

[1Chris Krapu](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#nfH5mvdgbPit4RQEg)

[3nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#Ebp3kvScCXMbLwKDv)

[1Chris Krapu](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#9bEu9qFpixp8ao86p)

[1dbl001](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#G7PpwgeGF9dCdNGEE)

[1Ram Bharadwaj](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#sMwMQMaWdkxKxuEat)

[1Douglas Summers-Stay](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#podpZCiqsbPxQTBiX)

[1nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#dqTwo4otdyyNs7caJ)

[1oekenta](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#Xh7HKWimSPmJqZcnc)

[7nostalgebraist](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#rxCwCErmB5ZRTLiSe)

[2oekenta](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#9x6bsazTEjCPQK3eQ)

[38Comments](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens#comments)

38

[GPT](https://www.lesswrong.com/w/gpt)[Machine Learning (ML)](https://www.lesswrong.com/w/machine-learning-ml)[Gears-Level](https://www.lesswrong.com/w/gears-level)[Interpretability (ML & AI)](https://www.lesswrong.com/w/interpretability-ml-and-ai)[AI](https://www.lesswrong.com/w/ai)[Frontpage](https://www.lesswrong.com/posts/5conQhfa4rgb4SaWx/site-guide-personal-blogposts-vs-frontpage-posts)

# 279

# Ω 80

New Comment

Submit

38 comments, sorted by 

top scoring

Click to highlight new comments since: Today at 1:28 AM

[-][gwern](https://www.lesswrong.com/users/gwern)6yΩ818

0

> I think this might suggest there is some fundamentally better way to do sampling from GPT models? I'm having trouble writing out the intuition clearly, so I'll leave it for later posts.

Unroll the sampling process: hook up all the individual GPT instances into a single long model, bypass the discretizing/embedding layers to make it differentiable end-to-end, and [do gradient ascent](https://www.gwern.net/GPT-2-preference-learning#optimization-by-backprop-not-blackbox) to find the sequence which maximizes likelihood conditional on the fixed input.

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)6yΩ47

0

Interesting, but not (I think?) the direction I was headed in.

I was thinking more about the way the model seems to be managing a tradeoff between preserving the representation of token _i_ and producing the representation of token _i+1_.

The depth-wise continuity imposed by weight decay means late layers are representing something close to the final output -- in late layers the model is roughly looking at its own guesses, _even if they were wrong_ , which seems suboptimal.

Consider this scenario:

  * The model does poorly at position _i_ , assigning very low probability to the true token residing at _i+1_. 
  * To retain a clear view of the input sequence, the model now needs to "keep around" the true token at _i+1_ , since its own guess is a poor proxy.
  * But early layers don't know that: they can't "look up" and notice the poor prediction. So they just treat _i+1_ like any other position. (I.e. there's no way to implement a selective "copy when we got it wrong" mechanism)
  * In late layers, position _i+1_ has been converted into a guess about _i+2_ by the earlier layers, so we can't rely on it to tell us what really occupied _i+1_.
  * And position _i_ has been converted to a _bad_ guess about position _i+1_ , so if we use it as a proxy for _i+1_ we'll do poorly.



My sampling idea was something like "let's replace (or interpolate) late activations with embeddings of the actual next token, so the model can see what really happened, even when its probability was low." (This is for _sampling_ specifically because it'd be too slow in training, where you want to process a whole window at once with matrix operations; sampling has to be a loop anyway, so there's no cost to adding stuff that only works as a loop.)

But, thinking about it more, the model clearly _can_ perform well in scenarios like the above, e.g. my plasma example and also many other cases naturally arising in language which GPT handles well.

I have no idea _how_ it does it -- indeed the connection structure feels weirdly adverse to such operations -- but apparently it does. So it's probably premature to assume it _can 't_ do this well, and attempt to "help it out" with extra tricks.

Reply

[-][oceaninthemiddleofanisland](https://www.lesswrong.com/users/oceaninthemiddleofanisland)6yΩ01

0

How far away is this from being implementable?

Reply

[-][John Steidley](https://www.lesswrong.com/users/john-steidley)6yΩ23

0

It doesn't sound hard at all. The things Gwern is describing are the same sort of thing that people do for interpretability where they, eg, find an image that maximizes the probability of the network predicting a target class.

Of course, you need access to the model, so only OpenAI could do it for GPT-3 right now.

Reply

[-][gwern](https://www.lesswrong.com/users/gwern)6yΩ26

0

Doing it with GPT-3 would be quite challenging just for compute requirements like RAM. You'd want to test this out on GPT-2-117M first, definitely. If the approach works at all, it should work well for the smallest models too.

Reply

[-][evhub](https://www.lesswrong.com/users/evhub)6y*Ω813

0

This is very neat. I definitely agree that I find the discontinuity from the first transformer block surprising. One thing which occurred to me that might be interesting to do is to try and train a linear model to reconstitute the input from the activations at different layers to get an idea of how the model is encoding the input. You could either train one linear model on data randomly sampled from different layers, or a separate linear model for each layer, and then see if there are any interesting patterns like whether the accuracy increases or decreases as you get further into the model. You could also see if the resulting matrix has any relationship to the embedding matrix (e.g. are the two matrices farther apart or closer together than would be expected by chance?). One possible hypothesis that this might let you test is whether the information about the input is being stored indirectly via what the model's guess is given that input or whether it's just being stored in parts of the embedding space that aren't very relevant to the output (if it's the latter, the linear model should put a lot of weight on basis elements that have very little weight in the embedding matrix).

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)6yΩ47

0

> One thing which occurred to me that might be interesting to do is to try and train a linear model to reconstitute the input from the activations at different layers to get an idea of how the model is encoding the input. You could either train one linear model on data randomly sampled from different layers, or a separate linear model for each layer, and then see if there are any interesting patterns like whether the accuracy increases or decreases as you get further into the model.

That's a great idea!

> One possible hypothesis that this might let you test is whether the information about the input is being stored indirectly via what the model's guess is given that input or whether it's just being stored in parts of the embedding space that aren't very relevant to the output (if it's the latter, the linear model should put a lot of weight on basis elements that have very little weight in the embedding matrix).

Hmm... I guess there is some reason to think the basis elements have special meaning (as opposed to the elements of any other basis for the same space), since the layer norm step operates in this basis.

But I doubt there are actually individual components the embedding cares little about, as that seems wasteful (you want to compress 50K into 1600 as well as you possibly can), and if the embedding cares about them even a _little_ bit then the model needs to slot in the appropriate predictive information, eventually.

Thinking out loud, I imagine there might be pattern where embeddings of _unlikely_ tokens (given the context) are repurposed in the middle for computation (you know they're near-impossible so you don't need to track them closely), and then smoothly subtracted out at the end. There's probably a way to check if that's happening.

Reply

[-][evhub](https://www.lesswrong.com/users/evhub)6yΩ23

0

> That's a great idea!

Thanks! I'd be quite excited to know what you find if you end up trying it.

> Hmm... I guess there is some reason to think the basis elements have special meaning (as opposed to the elements of any other basis for the same space), since the layer norm step operates in this basis.
> 
> But I doubt there are actually individual components the embedding cares little about, as that seems wasteful (you want to compress 50K into 1600 as well as you possibly can), and if the embedding cares about them even a little bit then the model needs to slot in the appropriate predictive information, eventually.
> 
> Thinking out loud, I imagine there might be pattern where embeddings of unlikely tokens (given the context) are repurposed in the middle for computation (you know they're near-impossible so you don't need to track them closely), and then smoothly subtracted out at the end. There's probably a way to check if that's happening.

I wasn't thinking you would do this with the natural component basis—though it's probably worth trying that also—but rather doing some sort of matrix decomposition on the embedding matrix to get a basis ordered by importance (e.g. using PCA or NMF—PCA is simpler though I know NMF is what OpenAI Clarity usually uses when they're trying to extract interpretable basis elements from neural network activations) and then seeing what the linear model looks like in that basis. You could even just do something like what you're saying and find some sort of basis ordered by the frequency of the tokens that each basis element corresponds to (though I'm not sure exactly what the right way would be to generate such a basis).

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)6yΩ35

0

I also thought of PCA/SVD, but I imagine matrix decompositions like these would be misleading here.

What matters here (I think) is not some basis of N_emb orthogonal vectors in embedding space, but some much larger set of [~exp(N_emb) _almost_ orthogonal vectors](https://en.wikipedia.org/wiki/Johnson%E2%80%93Lindenstrauss_lemma). We only have 1600 degrees of freedom to tune, but they're continuous degrees of freedom, and this lets us express >>1600 distinct vectors in vocab space as long as we accept some small amount of reconstruction error.

I expect GPT and many other neural models are effectively working in such space of nearly orthogonal vectors, and picking/combining elements of it. A decomposition into orthogonal vectors won't really illuminate this. I wish I knew more about this topic -- are there standard techniques?

Reply

[-][Vlad Mikulik](https://www.lesswrong.com/users/vlad-mikulik)6yΩ35

0

You might want to look into NMF, which, unlike PCA/SVD, doesn't aim to create an orthogonal projection. It works well for interpretability because its components cannot cancel each other out, which makes its features more intuitive to reason about. I think it is essentially what you want, although I don't think it will allow you to find directly the 'larger set of almost orthogonal vectors' you're looking for. 

Reply

[-][gwern](https://www.lesswrong.com/users/gwern)6yΩ48

0

Related layer visualizations: ["Looking for Grammar in All The Right Places"](https://aletheap.github.io/posts/2020/07/looking-for-grammar/).

Reply

[-][Joseph Miller](https://www.lesswrong.com/users/joseph-miller)1y4

1

I just found the paper [**BERT 's output layer recognizes all hidden layers? Some Intriguing Phenomena and a simple way to boost BERT**](https://arxiv.org/abs/2001.09309), which precedes this post by a few months and invents essentially the same technique as the logit lens.

So consider also citing that paper when citing this post.

As an aside, I would guess that this is the most cited LessWrong post in the academic literature, but it would be cool if anyone had stats on that.

Reply

[-][p.b.](https://www.lesswrong.com/users/p-b-1)6y3

0

Maybe I am misunderstanding something, but to me it is very intuitive that there is a big jump from the embedding output to the first transformer block output. The embedding is backpropagated into so it makes sense to see all representations as representations of the prediction we are trying to make, i.e. of the next word. 

But the embedding is a prediction of the next word based on only a single word, the word that is being embedded. So the prediction of the next word is by necessity very bad (the BPE ensures that, IIUC, because tokens that would always follow one another are merged). 

The first transformer block integrates hundreds of words of context into the prediction, that’s where the big jump comes from. 

Reply

[-][Gurkenglas](https://www.lesswrong.com/users/gurkenglas)6y3

0

Is it really trained to output the input offset by one, or just to have the last slot contain the next word? Because I would expect it to be better at copying the input over by one...

If each layer were trained to give its best guess at the next token, this myopia would prevent all sorts of hiding data for later. This would be a good experiment for your last story, yes? I expect this would perform very poorly, though if it doesn't, hooray, for I really don't expect that version to develop inner optimizers.

Reply

[-][oekenta](https://www.lesswrong.com/users/oekenta)6y3

0

I think I understand your question and was also confused by this for a bit so I wanted add in some points of clarification. First I want out that I really couldn't find a satisfactory explanation of this particular detail (at least one that I could understand) so I pieced this together myself from looking at the [huggingface code](https://huggingface.co/transformers/_modules/transformers/modeling_gpt2.html#GPT2LMHeadModel) for GPT2. I may get some details wrong. 

During training at each step the GPT2 takes in an N tokens and outputs N tokens. But the i-th output token is computed in such away that it only relies on the information from tokens 1, ..., i and is meant to predict i+1-th token from these. I think it's best to think of each output being computed independently of the others (though this isn't strictly true since the separate outputs are computed by shared matrices). So for each i, we train the network so that the i-th output produces the correct result given the _input_ tokens 1, ..., i. There is a term in the loss function for each output token and the total loss is the sum of all the losses of the output tokens. The outputs at other positions do not play a role in the i-th output token, only the first 1,..., i input tokens do.

During inference, given an input of k tokens, we are only concerned with the k-th output token (which should predict the token following the first k). GPT-3 also produces predictions for the outputs before position k but these are just ignored since we already know what these values should be. 

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)6y2

0

> Is it really trained to output the input offset by one, or just to have the last slot contain the next word? Because I would expect it to be better at copying the input over by one...

Not sure I understand the distinction, could you rephrase?

If by "last slot" you mean last layer (as opposed to earlier layers), that seems like the same thing as outputting the input offset by one.

If by "last slot" you mean the token N+1 given tokens (1, 2, ... N), then no, that's not how GPT works. If you put in tokens (1, 2, ... N), you always get guesses for tokens (2, 3, ..., N+1) in response. This is true even if all you care about is the guess for N+1.

Reply

[-][Gurkenglas](https://www.lesswrong.com/users/gurkenglas)6y4

0

I meant your latter interpretation.

Can you measure the KL-divergence at each layer from the input, rather than the output? KL does not satisfy the triangle inequality, so maybe most of the layers are KL-close to both input and output?

GPT uses ReLU, yes? Then the regularization would make it calculate using small values, which would be possible because ReLU is nonlinear on small values. If we used an activation function that's linear on small values, I would therefore expect more of the calculation to be visible.

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)6y*4

0

> Can you measure the KL-divergence at each layer from the input, rather than the output? KL does not satisfy the triangle inequality, so maybe most of the layers are KL-close to both input and output?

One can do this in the Colab notebook by calling `show_token_progress` with `comparisons_vs="first"` rather than the default `"final"`. IIRC, this also shows a discontinuous flip at the bottom followed by slower change.

(This is similar to asking the question "do the activations assign high or low probability the input token?" One can answer the same question by plotting logits or ranks with the input layer included.)

> GPT uses ReLU, yes? Then the regularization would make it calculate using small values, which would be possible because ReLU is nonlinear on small values.

It uses gelu, but gelu has the same property. However, note that I am extracting activations right after the application of a layer norm operation, which shifts/scales the activations to mean 0 and L2 norm 1 before passing them to the next layer.

Reply

[-][Gurkenglas](https://www.lesswrong.com/users/gurkenglas)5y2

0

> gelu has the same property

Actually, gelu is differentiable at 0, so it is linear on close-to-zero values.

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)5y2

0

Ah, I think we miscommunicated.

I meant "gelu(x) achieves its maximum curvature somewhere near x=0."

People often interpret relu as a piecewise linear version of functions like elu and gelu, which are curved near x=0 and linear for large |x|. In this sense gelu is like relu.

It sounds like you were, instead, talking about the property of relu that you can get nonlinear behavior for _arbitrarily_ small inputs.

This is indeed unique to relu -- I remember some DeepMind (?) paper that used floating point underflow to simulate relu, and then made NNs out of just _linear_ floating point ops. Obviously you can't simulate a differentiable function with that trick.

Reply

[-][gwern](https://www.lesswrong.com/users/gwern)5y4

0

([OpenAI](https://openai.com/blog/nonlinear-computation-in-linear-networks/)?)

Reply

[-][Gurkenglas](https://www.lesswrong.com/users/gurkenglas)5y2

0

> floating point underflow to simulate relu

Oh that's not good. Looks like we'd need a version of float that keeps track of an interval of possible floats (by the two floats at the end of the interval). Then we could simulate the behavior of infinite-precision floats so long as the network keeps the bounds tight, and we could train the network to keep the simulation in working order. Then we could see whether, in a network thus linear at small numbers, every visibly large effect has a visibly large cause.

By the way - have you seen what happens when you finetune GPT to reinforce this pattern that you're observing, that every entry of the table, not just the top right one, predicts an input token?

Reply

[-][algon33](https://www.lesswrong.com/users/algon33)6y2

0

> IIRC, this also shows a discontinuous flip at the bottom followed by slower change. 

Maybe edit the post so you include this? I know I was wondering about this too.

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)6y2

0

Post has been now updated with a long-ish addendum about this topic.

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)6y2

0

Good idea, I'll do that.

I know I'd run those plots before, but running them again after writing the post felt like it resolved some of the mystery. If our comparison point is the input, rather than the output, the jump in KL/rank is still there but it's smaller.

Moreover, the rarer the input token is, the more it seems to be preserved in later layers (in the sense of low KL / low vocab rank). This may be how tokens like "plasma" are "kept around" for later use.

Reply

[-][Gurkenglas](https://www.lesswrong.com/users/gurkenglas)6y2

0

Consider also trying the other direction - after all, KL is asymmetric.

Reply

[-][Riccardo Volpato](https://www.lesswrong.com/users/riccardo-volpato)6y2

0

> Apparently it _is_ keeping around a representation of the token "plasma" with enough resolution to copy it . . . but it only retrieves this representation at the end! (In the rank view, the rank of plasma is quite low until the very end.)
> 
> This is surprising to me. The repetition is directly visible in the input: "when people say" is copied verbatim. If you just applied the rule "if input seems to be repeating, keep repeating it," you'd be good. Instead, the model scrambles away the pattern, then recovers it later through some other computational route.

One more reason on why this is suprising, is that other experiments found that this behaviour (forgetting then recalling) is common in MLM (masked language models) but not in simple language models like GPT-2 (see this [blog post](https://lena-voita.github.io/posts/emnlp19_evolution.html) and more specifically [this graph](https://lena-voita.github.io/resources/posts/emnlp19_evolution/ib_mi_tasks-min.png)). The intepretation is that _" for MLMs, representations initially acquire information about the context around the token, partially forgetting the token identity and producing a more generalized token representation; the token identity then gets recreated at the top layer" _(citing from the blog post).

However, the logit lense here seems indicating that this may happen in GPT-2 (large) too. Could this be a virtue of scale? Where the same behaviour that one obtains with a MLM is reached by a LM as well with sufficient scale?

Reply

[-][SoerenMind](https://www.lesswrong.com/users/soerenmind)6y2

1

Are these known facts? If not, I think there's a paper in here.

Reply

[-][Chris Krapu](https://www.lesswrong.com/users/chris-krapu)2y1

0

In all of this, there seems to be an implicit assumption that the ordering of the embedding dimensions is consistent across layers, in the sense that "dog" is more strongly associated with dimension 12 in layers 2, 3, 4, etc.  
  
I don't see any reason why this should be the case from either a training or model structure perspective. How, then, does the logit lens (which should clearly not be invariant with regard to a permutation of its inputs) still produce valid results for some intermediate layers?

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)2y*3

1

Because the model has residual connections.

Reply

[-][Chris Krapu](https://www.lesswrong.com/users/chris-krapu)2y1

0

Ah, got it. Thanks a ton!

Reply

[-][dbl001](https://www.lesswrong.com/users/dbl001)2y1

0

Cool project. There were some changes in HuggingFace's transformer package which are affecting you Colab implementation. See here:

https://github.com/huggingface/transformers/issues/29576

Reply

[-][Ram Bharadwaj](https://www.lesswrong.com/users/ram-bharadwaj)3y1

0

> 47 layers layer

47 layers later ?

Reply

[-][Douglas Summers-Stay](https://www.lesswrong.com/users/douglas-summers-stay)6y1

0

Could you try a prompt that tells it to end a sentence with a particular word, and see how that word casts its influence back over the sentence? I know that this works with GPT-3, but I didn't really understand how it could.

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)6y1

0

Interesting topic! I'm not confident this lens would reveal much about it (vs. attention maps or something), but it's worth a try.

I'd encourage you to try this yourself with the [Colab notebook](https://colab.research.google.com/drive/1-nOE-Qyia3ElM17qrdoHAtGmLCPUZijg?usp=sharing), since you presumably have more experience writing this kind of prompt than I do.

Reply

[-][oekenta](https://www.lesswrong.com/users/oekenta)6yΩ11

0

Hey I'm not finished reading this yet but I noticed something off about what you said. 

> At the end, the final 1600-dimensional vector is multiplied by _W 's_ transpose to project back into vocab space.

  


This isn't quite right. They don't multiply by W's transpose at the end. Rather there is a completely new matrix at the end, whose shape is the same as the transpose of W.

You can see this in huggingface's code for GPT2. In the class [GPT2LMHeadModel](https://huggingface.co/transformers/_modules/transformers/modeling_gpt2.html#GPT2LMHeadModel) the final matrix multiplication is performed by the matrix called "lm_head", where as the matrix you call W which is used to map 50,257 dimensional vectors into 1600 dimensional space is called "wte" (found in the [GPT2Model ](https://huggingface.co/transformers/_modules/transformers/modeling_gpt2.html#GPT2Model)class). You can see from the code that wte has shape "Vocab size x Embed Size" while lm_head has shape "Embed Size x Vocab size" so lm_head does have the same shape as W transpose but doesn't have the same numbers. 

  


Edit: I could be wrong here, though. Maybe lm_head was set to be equal to wte transpose? I'm looking through the GPT-2 paper but don't see anything like that mentioned. 

Reply

[-][nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)6yΩ47

0

> Maybe lm_head was set to be equal to wte transpose?

Yes, this is the case in GPT-2. Perhaps the huggingface implementation supports making these two matrices different, but they are the same in the official GPT-2.

  * In OpenAI's tensorflow code, see lines [154](https://github.com/openai/gpt-2/blob/master/src/model.py#L154) and [171](https://github.com/openai/gpt-2/blob/master/src/model.py#L171) of src/model.py. The variable "wte" is defined on 151, then re-used on 171.
  * In the [original GPT paper](https://s3-us-west-2.amazonaws.com/openai-assets/research-covers/language-unsupervised/language_understanding_paper.pdf), see eqs. (2) in section 3.1. The same matrix W_e is used twice. (The GPT-2 and GPT-3 papers just refer you back to the GPT paper for architecture details, so the GPT paper is the place to look.)



Edit: I think the reason this is obscured in the huggingface implementation is that they always distinguish the internal layers of a transformer from the "head" used to convert the final layer outputs into predictions. The intent is easy swapping between different "heads" with the same "body" beneath.

This forces their code to _allow_ for heads that differ from the input embedding matrix, even when they implement models like GPT-2 where the official specification says they are the same.

Edit2: might as well say explicitly that I find the OpenAI tensorflow code much more readable than the huggingface code. This isn't a critique of the latter; it's trying to support every transformer out there in a unified framework. But if you only care about GPT, this introduces a lot of distracting abstraction.

Reply

[-][oekenta](https://www.lesswrong.com/users/oekenta)6yΩ12

0

Thanks for the info. 

This was a great read, very informative. 

Reply

[Moderation Log](https://www.lesswrong.com/moderation)

More from [nostalgebraist](https://www.lesswrong.com/users/nostalgebraist)

[View more](https://www.lesswrong.com/users/nostalgebraist)

Curated and popular this week

Mentioned in

336[Against Almost Every Theory of Impact of Interpretability](https://www.lesswrong.com/posts/LNA8mubrByG7SFacm/against-almost-every-theory-of-impact-of-interpretability-1)

200[The Singular Value Decompositions of Transformer Weight Matrices are Highly Interpretable](https://www.lesswrong.com/posts/mkbGjzxD8d8XqKHzA/the-singular-value-decompositions-of-transformer-weight)

159[Inside the mind of a superhuman Go model: How does Leela Zero read ladders?](https://www.lesswrong.com/posts/FF8i6SLfKb4g7C4EL/inside-the-mind-of-a-superhuman-go-model-how-does-leela-zero-2)

154[Activation Oracles: Training and Evaluating LLMs as General-Purpose Activation Explainers](https://www.lesswrong.com/posts/rwoEz3bA9ekxkabc7/activation-oracles-training-and-evaluating-llms-as-general)

145[An Extremely Opinionated Annotated List of My Favourite Mechanistic Interpretability Papers v2](https://www.lesswrong.com/posts/NfFST5Mio7BCAQHPA/an-extremely-opinionated-annotated-list-of-my-favourite)

[Load More (5/63)](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens)
