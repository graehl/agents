# Positive-Unlabeled Learning with Non-Negative Risk Estimator

Ryuichi Kiryo1,<sup>2</sup> Gang Niu1,<sup>2</sup> Marthinus C. du Plessis Masashi Sugiyama2,<sup>1</sup> <sup>1</sup>The University of Tokyo, 7-3-1 Hongo, Tokyo 113-0033, Japan <sup>2</sup>RIKEN, 1-4-1 Nihonbashi, Tokyo 103-0027, Japan { kiryo@ms., gang@ms., sugi@ }k.u-tokyo.ac.jp

# Abstract

From only *positive* (P) and *unlabeled* (U) data, a binary classifier could be trained with PU learning, in which the state of the art is *unbiased PU learning*. However, if its model is very flexible, empirical risks on training data will go negative, and we will suffer from serious overfitting. In this paper, we propose a *non-negative risk estimator* for PU learning: when getting minimized, it is more robust against overfitting, and thus we are able to use very flexible models (such as deep neural networks) given limited P data. Moreover, we analyze the *bias*, *consistency*, and *mean-squared-error reduction* of the proposed risk estimator, and bound the *estimation error* of the resulting *empirical risk minimizer*. Experiments demonstrate that our risk estimator fixes the overfitting problem of its unbiased counterparts.

# 1 Introduction

*Positive-unlabeled* (PU) *learning* can be dated back to [\[1,](#page-9-0) [2,](#page-9-1) [3\]](#page-9-2) and has been well studied since then. It mainly focuses on binary classification applied to retrieval and novelty or outlier detection tasks [\[4,](#page-9-3) [5,](#page-9-4) [6,](#page-9-5) [7\]](#page-9-6), while it also has applications in matrix completion [\[8\]](#page-9-7) and sequential data [\[9,](#page-9-8) [10\]](#page-9-9).

Existing PU methods can be divided into two categories based on how U data is handled. The first category (e.g., [\[11,](#page-9-10) [12\]](#page-9-11)) identifies possible *negative* (N) data in U data, and then performs ordinary supervised (PN) learning; the second (e.g., [\[13,](#page-9-12) [14\]](#page-9-13)) regards U data as N data with smaller weights. The former heavily relies on the heuristics for identifying N data; the latter heavily relies on good choices of the weights of U data, which is computationally expensive to tune.

In order to avoid tuning the weights, *unbiased PU learning* comes into play as a subcategory of the second category. The milestone is [\[4\]](#page-9-3), which regards a U data as weighted P and N data simultaneously. It might lead to *unbiased risk estimators*, if we unrealistically assume that the class-posterior probability is one for all P data.[1](#page-0-0) A breakthrough in this direction is [\[15\]](#page-9-14) for proposing the first unbiased risk estimator, and a more general estimator was suggested in [\[16\]](#page-9-15) as a common foundation. The former is unbiased but non-convex for loss functions satisfying some symmetric condition; the latter is always unbiased, and it is further convex for loss functions meeting some linear-odd condition [\[17,](#page-9-16) [18\]](#page-9-17). PU learning based on these unbiased risk estimators is the current state of the art.

However, the unbiased risk estimators will give negative empirical risks, if the model being trained is very flexible. For the general estimator in [\[16\]](#page-9-15), there exist three partial risks in the total risk (see Eq. [\(2\)](#page-1-0) defined later), especially it has a negative risk regarding P data as N data to cancel the bias caused by regarding U data as N data. The worst case is that the model can realize any measurable function and the loss function is not upper bounded, so that the empirical risk is not lower bounded. This needs to be fixed since the original risk, which is the target to be estimated, is non-negative.

<span id="page-0-0"></span><sup>1</sup> It implies the P and N class-conditional densities have disjoint support sets, and then any P and N data (as the test data) can be perfectly separated by a fixed classifier that is sufficiently flexible.

To this end, we propose a novel *non-negative risk estimator* that follows and improves on the state-of-the-art unbiased risk estimators mentioned above. This estimator can be used for two purposes: first, given some validation data (which are also PU data), we can use our estimator to evaluate the risk—for this case it is *biased* yet *optimal*, and for some symmetric losses, the *mean-squared-error reduction* is guaranteed; second, given some training data, we can use our estimator to train binary classifiers—for this case its risk minimizer possesses an *estimation error bound* of the same order as the risk minimizers corresponding to its unbiased counterparts [15, 16, 19].

In addition, we propose a *large-scale* PU learning algorithm for minimizing the unbiased and non-negative risk estimators. This algorithm accepts any *surrogate loss* and is based on *stochastic optimization*, e.g., [20]. Note that [21] is the only existing large-scale PU algorithm, but it only accepts a single surrogate loss from [16] and is based on *sequential minimal optimization* [22].

The rest of this paper is organized as follows. In Section 2 we review unbiased PU learning, and in Section 3 we propose non-negative PU learning. Theoretical analyses are carried out in Section 4, and experimental results are discussed in Section 5. Conclusions are given in Section 6.

## <span id="page-1-1"></span>2 Unbiased PU learning

In this section, we review unbiased PU learning [15, 16].

**Problem settings** Let  $X \in \mathbb{R}^d$  and  $Y \in \{\pm 1\}$   $(d \in \mathbb{N})$  be the input and output random variables. Let p(x,y) be the *underlying joint density* of (X,Y),  $p_p(x) = p(x \mid Y = +1)$  and  $p_n(x) = p(x \mid Y = -1)$  be the *P and N marginals* (a.k.a. the P and N class-conditional densities), p(x) be the *U marginal*,  $\pi_p = p(Y = +1)$  be the *class-prior probability*, and  $\pi_n = p(Y = -1) = 1 - \pi_p$ .  $\pi_p$  is assumed known throughout the paper; it can be estimated from P and U data [23, 24, 25, 26].

Consider the *two-sample problem setting* of PU learning [5]: two sets of data are sampled independently from  $p_{\rm p}(x)$  and p(x) as  $\mathcal{X}_{\rm p} = \{x_i^{\rm p}\}_{i=1}^{n_{\rm p}} \sim p_{\rm p}(x)$  and  $\mathcal{X}_{\rm u} = \{x_i^{\rm u}\}_{i=1}^{n_{\rm u}} \sim p(x)$ , and a classifier needs to be trained from  $\mathcal{X}_{\rm p}$  and  $\mathcal{X}_{\rm u}$ . If it is PN learning as usual,  $\mathcal{X}_{\rm n} = \{x_i^{\rm n}\}_{i=1}^{n_{\rm n}} \sim p_{\rm n}(x)$  rather than  $\mathcal{X}_{\rm u}$  would be available and a classifier could be trained from  $\mathcal{X}_{\rm p}$  and  $\mathcal{X}_{\rm n}$ .

**Risk estimators** Unbiased PU learning relies on unbiased risk estimators. Let  $g: \mathbb{R}^d \to \mathbb{R}$  be an arbitrary *decision function*, and  $\ell: \mathbb{R} \times \{\pm 1\} \to \mathbb{R}$  be the *loss function*, such that the value  $\ell(t,y)$  means the loss incurred by predicting an output t when the ground truth is y. Denote by  $R_{\mathrm{p}}^+(g) = \mathbb{E}_{\mathrm{p}}[\ell(g(X),+1)]$  and  $R_{\mathrm{n}}^-(g) = \mathbb{E}_{\mathrm{n}}[\ell(g(X),-1)]$ , where  $\mathbb{E}_{\mathrm{p}}[\cdot] = \mathbb{E}_{X \sim p_{\mathrm{p}}}[\cdot]$  and  $\mathbb{E}_{\mathrm{n}}[\cdot] = \mathbb{E}_{X \sim p_{\mathrm{n}}}[\cdot]$ . Then, the *risk* of g is  $R(g) = \mathbb{E}_{(X,Y) \sim p(x,y)}[\ell(g(X),Y)] = \pi_{\mathrm{p}}R_{\mathrm{p}}^+(g) + \pi_{\mathrm{n}}R_{\mathrm{n}}^-(g)$ . In PN learning, thanks to the availability of  $\mathcal{X}_{\mathrm{p}}$  and  $\mathcal{X}_{\mathrm{n}}$ , R(g) can be approximated directly by

<span id="page-1-3"></span>
$$\hat{R}_{\rm pn}(g) = \pi_{\rm p} \hat{R}_{\rm p}^{+}(g) + \pi_{\rm n} \hat{R}_{\rm n}^{-}(g),$$
 (1)

where  $\widehat{R}_{\mathrm{p}}^{+}(g)=(1/n_{\mathrm{p}})\sum_{i=1}^{n_{\mathrm{p}}}\ell(g(x_{i}^{\mathrm{p}}),+1)$  and  $\widehat{R}_{\mathrm{n}}^{-}(g)=(1/n_{\mathrm{n}})\sum_{i=1}^{n_{\mathrm{n}}}\ell(g(x_{i}^{\mathrm{n}}),-1)$ . In PU learning,  $\mathcal{X}_{\mathrm{n}}$  is unavailable, but  $R_{\mathrm{n}}^{-}(g)$  can be approximated indirectly, as shown in [15, 16]. Denote by  $R_{\mathrm{p}}^{-}(g)=\mathbb{E}_{\mathrm{p}}[\ell(g(X),-1)]$  and  $R_{\mathrm{u}}^{-}(g)=\mathbb{E}_{X\sim p(x)}[\ell(g(X),-1)]$ . As  $\pi_{\mathrm{n}}p_{\mathrm{n}}(x)=p(x)-\pi_{\mathrm{p}}p_{\mathrm{p}}(x)$ , we can obtain that  $\pi_{\mathrm{n}}R_{\mathrm{n}}^{-}(g)=R_{\mathrm{u}}^{-}(g)-\pi_{\mathrm{p}}R_{\mathrm{p}}^{-}(g)$ , and R(g) can be approximated indirectly by

$$\widehat{R}_{pu}(g) = \pi_{p} \widehat{R}_{p}^{+}(g) - \pi_{p} \widehat{R}_{p}^{-}(g) + \widehat{R}_{u}^{-}(g),$$
(2)

where 
$$\widehat{R}_{\mathrm{p}}^{-}(g)=(1/n_{\mathrm{p}})\sum_{i=1}^{n_{\mathrm{p}}}\ell(g(x_{i}^{\mathrm{p}}),-1)$$
 and  $\widehat{R}_{\mathrm{u}}^{-}(g)=(1/n_{\mathrm{u}})\sum_{i=1}^{n_{\mathrm{u}}}\ell(g(x_{i}^{\mathrm{u}}),-1).$ 

The empirical risk estimators in Eqs. (1) and (2) are unbiased and consistent w.r.t. all popular loss functions.<sup>3</sup> When they are used for evaluating the risk (e.g., in cross-validation),  $\ell$  is by default the zero-one loss, namely  $\ell_{01}(t,y) = (1-\mathrm{sign}(ty))/2$ ; when used for training,  $\ell_{01}$  is replaced with a surrogate loss [27]. In particular, [15] showed that if  $\ell$  satisfies a symmetric condition:

<span id="page-1-5"></span><span id="page-1-0"></span>
$$\ell(t, +1) + \ell(t, -1) = 1, \tag{3}$$

<span id="page-1-2"></span> $<sup>^2\</sup>mathcal{X}_p \text{ is a set of independent data and so is } \mathcal{X}_u \text{, but } \mathcal{X}_p \cup \mathcal{X}_u \text{ does not need to be such a set.}$ 

<span id="page-1-4"></span><sup>&</sup>lt;sup>3</sup>The consistency here means for fixed g,  $\widehat{R}_{pn}(g) \to R(g)$  and  $\widehat{R}_{pu}(g) \to R(g)$  as  $n_p, n_n, n_u \to \infty$ .

we will have

$$\widehat{R}_{\rm DU}(g) = 2\pi_{\rm D}\widehat{R}_{\rm D}^{+}(g) + \widehat{R}_{\rm D}^{-}(g) - \pi_{\rm D},\tag{4}$$

which can be minimized by separating  $\mathcal{X}_p$  and  $\mathcal{X}_u$  with ordinary cost-sensitive learning. An issue is  $\widehat{R}_{pu}(g)$  in (4) must be non-convex in g, since no  $\ell(t,y)$  in (3) can be convex in t. [16] showed that  $\widehat{R}_{pu}(g)$  in (2) is convex in g, if  $\ell(t,y)$  is convex in t and meets a linear-odd condition [17, 18]:

<span id="page-2-2"></span><span id="page-2-1"></span>
$$\ell(t, +1) - \ell(t, -1) = -t. \tag{5}$$

Let g be parameterized by  $\theta$ , then (5) leads to a convex optimization problem so long as g is linear in  $\theta$ , for which the globally optimal solution can be obtained. Eq. (5) is not only sufficient but also necessary for the convexity, if  $\ell$  is unary, i.e.,  $\ell(t, -1) = \ell(-t, +1)$ .

**Justification** Thanks to the unbiasedness, we can study *estimation error bounds* (EEB). Let  $\mathcal G$  be the *function class*, and  $\widehat g_{\mathrm{pn}}$  and  $\widehat g_{\mathrm{pu}}$  be the *empirical risk minimizers* of  $\widehat R_{\mathrm{pn}}(g)$  and  $\widehat R_{\mathrm{pu}}(g)$ . [19] proved EEB of  $\widehat g_{\mathrm{pu}}$  is tighter than EEB of  $\widehat g_{\mathrm{pn}}$  when  $\pi_\mathrm{p}/\sqrt{n_\mathrm{p}}+1/\sqrt{n_\mathrm{u}}<\pi_\mathrm{n}/\sqrt{n_\mathrm{n}}$ , if (a)  $\ell$  satisfies (3) and is *Lipschitz continuous*; (b) the *Rademacher complexity* of  $\mathcal G$  decays in  $\mathcal O(1/\sqrt{n})$  for data of size n drawn from p(x),  $p_\mathrm{p}(x)$  or  $p_\mathrm{n}(x)$ . In other words, under mild conditions, PU learning is likely to outperform PN learning when  $\pi_\mathrm{p}/\sqrt{n_\mathrm{p}}+1/\sqrt{n_\mathrm{u}}<\pi_\mathrm{n}/\sqrt{n_\mathrm{n}}$ . This phenomenon has been observed in experiments [19] and is illustrated in Figure 1(a).

## <span id="page-2-0"></span>3 Non-negative PU learning

In this section, we propose the non-negative risk estimator and the large-scale PU algorithm.

#### 3.1 Motivation

Let us look inside the aforementioned justification of unbiased PU (uPU) learning. Intuitively, the advantage comes from the transformation  $\pi_{\rm n}R_{\rm n}^-(g)=R_{\rm u}^-(g)-\pi_{\rm p}R_{\rm p}^-(g).$  When we approximate  $\pi_{\rm n}R_{\rm n}^-(g)$  from N data  $\{x_i^{\rm n}\}_{i=1}^{n_{\rm n}}$ , the convergence rate is  $\mathcal{O}_p(\pi_{\rm n}/\sqrt{n_{\rm n}}),$  where  $\mathcal{O}_p$  denotes the order in probability; when we approximate  $R_{\rm u}^-(g)-\pi_{\rm p}R_{\rm p}^-(g)$  from P data  $\{x_i^{\rm p}\}_{i=1}^{n_{\rm p}}$  and U data  $\{x_i^{\rm u}\}_{i=1}^{n_{\rm u}},$  the convergence rate becomes  $\mathcal{O}_p(\pi_{\rm p}/\sqrt{n_{\rm p}}+1/\sqrt{n_{\rm u}}).$  As a result, we might benefit from a tighter uniform deviation bound when  $\pi_{\rm p}/\sqrt{n_{\rm p}}+1/\sqrt{n_{\rm u}}<\pi_{\rm n}/\sqrt{n_{\rm n}}.$ 

However, the critical assumption on the Rademacher complexity is indispensable, otherwise it will be difficult for EEB of  $\widehat{g}_{\mathrm{pu}}$  to be tighter than EEB of  $\widehat{g}_{\mathrm{pn}}$ . If  $\mathcal{G} = \{g \mid \|g\|_{\infty} \leq C_g\}$  where  $C_g > 0$  is a constant, i.e., it has all measurable functions with some bounded norm, then  $\mathfrak{R}_{n,q}(\mathcal{G}) = \mathcal{O}(1)$  for any n and q(x) and all bounds become trivial; moreover if  $\ell$  is not bounded from above,  $\widehat{R}_{\mathrm{pu}}(g)$  becomes not bounded from below, i.e., it may diverge to  $-\infty$ . Thus, in order to obtain high-quality  $\widehat{g}_{\mathrm{pu}}$ ,  $\mathcal{G}$  cannot be too complex, or equivalently the model of g cannot be too flexible.

This argument is supported by an experiment as illustrated in Figure 1(b). A *multilayer perceptron* was trained for separating the even and odd digits of MNIST hand-written digits [29]. This model is so flexible that the number of parameters is 500 times more than the total number of P and N data. From Figure 1(b) we can see:

- (A) on training data, the risks of uPU and PN both decrease, and uPU is faster than PN;
- (B) on test data, the risk of PN decreases, whereas the risk of uPU does not; the risk of uPU is lower at the beginning but higher at the end than that of PN.

To sum up, the overfitting problem of uPU is serious, which evidences that in order to obtain high-quality  $\hat{g}_{pu}$ , the model of g cannot be too flexible.

#### 3.2 Non-negative risk estimator

Nevertheless, we have no choice sometimes: we are interested in using flexible models, while labeling more data is out of our control. Can we alleviate the overfitting problem with neither changing the model nor labeling more data?

<span id="page-2-3"></span><sup>&</sup>lt;sup>4</sup>Let  $\sigma_1, \ldots, \sigma_n$  be n Rademacher variables, the Rademacher complexity of  $\mathcal G$  for  $\mathcal X$  of size n drawn from q(x) is defined by  $\mathfrak R_{n,q}(\mathcal G) = \mathbb E_{\mathcal X} \mathbb E_{\sigma_1,\ldots,\sigma_n}[\sup_{g\in\mathcal G} \frac{1}{n} \sum_{x_i\in\mathcal X} \sigma_i g(x_i)]$  [28]. For any fixed  $\mathcal G$  and  $q, \mathfrak R_{n,q}(\mathcal G)$  still depends on n and should decrease with n.

<span id="page-3-0"></span>![](_page_3_Figure_0.svg)

The dataset is MNIST; even/odd digits are regarded as the P/N class, and  $\pi_{\rm p}\approx 1/2;\, n_{\rm p}=100$  and  $n_{\rm n}=50$  for PN learning;  $n_{\rm p}=100$  and  $n_{\rm u}=59,900$  for unbiased PU (uPU) and non-negative PU (nnPU) learning. The model is a plain linear model (784-1) in (a) and an MLP (784-100-1) with ReLU in (b); it was trained by Algorithm 1, where the loss  $\ell$  is  $\ell_{\rm sig}$ , the optimization algorithm  ${\cal A}$  is [20], with  $\beta=1/2$  for uPU, and  $\beta=0$  and  $\gamma=1$  for nnPU. Solid curves are  $\widehat{R}_{\rm pn}(g)$  on test data where  $g\in\{\widehat{g}_{\rm pn},\widehat{g}_{\rm pu},\widehat{g}_{\rm pu},\widehat{g}_{\rm pu}\}$ , and dashed curves are  $\widehat{R}_{\rm pn}(\widehat{g}_{\rm pn})$ ,  $\widehat{R}_{\rm pu}(\widehat{g}_{\rm pu})$  and  $\widehat{R}_{\rm pu}(\widehat{g}_{\rm pu})$  on training data. Note that nnPU is identical to uPU in (a).

<span id="page-3-2"></span>Figure 1: Illustrative experimental results.

The answer is affirmative. Note that  $\widehat{R}_{pu}(\widehat{g}_{pu})$  keeps decreasing and goes negative. This should be fixed since  $R(g) \geq 0$  for any g. Specifically, it holds that  $R_u^-(g) - \pi_p R_p^-(g) = \pi_n R_n^-(g) \geq 0$ , but  $\widehat{R}_u^-(g) - \pi_p \widehat{R}_p^-(g) \geq 0$  is not always true, which is a potential reason for uPU to overfit. Based on this key observation, we propose a *non-negative risk estimator* for PU learning:

$$\widetilde{R}_{pu}(g) = \pi_p \widehat{R}_p^+(g) + \max \left\{ 0, \widehat{R}_u^-(g) - \pi_p \widehat{R}_p^-(g) \right\}.$$
 (6)

Let  $\widetilde{g}_{\mathrm{pu}} = \arg\min_{g \in \mathcal{G}} \widetilde{R}_{\mathrm{pu}}(g)$  be the empirical risk minimizer of  $\widetilde{R}_{\mathrm{pu}}(g)$ . We refer to the process of obtaining  $\widetilde{g}_{\mathrm{pu}}$  as non-negative PU (nnPU) learning. The implementation of nnPU will be given in Section 3.3, and theoretical analyses of  $\widetilde{R}_{\mathrm{pu}}(g)$  and  $\widetilde{g}_{\mathrm{pu}}$  will be given in Section 4.

Again, from Figure 1(b) we can see:

- (A) on training data, the risk of nnPU first decreases and then becomes more and more flat, so that the risk of nnPU is closer to the risk of PN and farther from that of uPU; in short, the risk of nnPU does not go down with uPU after a certain epoch;
- (B) on test data, the tendency is similar, but the risk of nnPU does not go up with uPU;
- (C) at the end, nnPU achieves the lowest risk on test data.

In summary, nnPU works by explicitly constraining the training risk of uPU to be non-negative.

#### <span id="page-3-1"></span>3.3 Implementation

A list of popular loss functions and their properties is shown in Table 1. Let g be parameterized by  $\theta$ . If g is linear in  $\theta$ , the losses satisfying (5) result in convex optimizations. However, if g needs to be flexible, it will be highly nonlinear in  $\theta$ ; then the losses satisfying (5) are not advantageous over others, since the optimizations are anyway non-convex. In [15], the  $ramp\ loss$  was used and  $\widehat{R}_{pu}(g)$  was minimized by  $the\ concave-convex\ procedure\ [30]$ . This solver is fairly sophisticated, and if we replace  $\widehat{R}_{pu}(g)$  with  $\widehat{R}_{pu}(g)$ , it will be more difficult to implement. To this end, we propose to use the  $sigmoid\ loss\ \ell_{sig}(t,y)=1/(1+\exp(ty))$ : its gradient is everywhere non-zero and  $\widehat{R}_{pu}(g)$  can be minimized by off-the-shelf gradient methods.

In front of big data, we should scale PU learning up by stochastic optimization. Minimizing  $\widehat{R}_{\mathrm{pu}}(g)$  is *embarrassingly parallel* while minimizing  $\widetilde{R}_{\mathrm{pu}}(g)$  is not, since  $\widehat{R}_{\mathrm{pu}}(g)$  is *point-wise* but  $\widetilde{R}_{\mathrm{pu}}(g)$  is not due to the max operator. That being said,  $\max\{0,\widehat{R}_{\mathrm{u}}^{-}(g;\mathcal{X}_{\mathrm{u}})-\pi_{\mathrm{p}}\widehat{R}_{\mathrm{p}}^{-}(g;\mathcal{X}_{\mathrm{p}})\}$  is no greater than  $(1/N)\sum_{i=1}^{N}\max\{0,\widehat{R}_{\mathrm{u}}^{-}(g;\mathcal{X}_{\mathrm{u}}^{i})-\pi_{\mathrm{p}}\widehat{R}_{\mathrm{p}}^{-}(g;\mathcal{X}_{\mathrm{p}}^{i})\}$ , where  $(\mathcal{X}_{\mathrm{p}}^{i},\mathcal{X}_{\mathrm{u}}^{i})$  is the *i*-th mini-batch, and hence the corresponding upper bound of  $\widetilde{R}_{\mathrm{pu}}(g)$  can easily be minimized in parallel.

Table 1: Loss functions for PU learning and their properties.

<span id="page-4-2"></span>

| Name              | Definition                       | (3) | (5)          | Bounded      | Lipschitz    | $\ell'(z) \neq 0$     |
|-------------------|----------------------------------|-----|--------------|--------------|--------------|-----------------------|
| Zero-one loss     | $(1 - \operatorname{sign}(z))/2$ | <   | ×            | ✓            | ×            | z = 0                 |
| Ramp loss         | $\max\{0, \min\{1, (1-z)/2\}\}$  | ✓   | ×            | $\checkmark$ | $\checkmark$ | $z \in [-1, +1]$      |
| Squared loss      | $(z-1)^2/4$                      | ×   | $\checkmark$ | ×            | ×            | $z\in\mathbb{R}$      |
| Logistic loss     | $\ln(1 + \exp(-z))$              | ×   | $\checkmark$ | ×            | $\checkmark$ | $z\in\mathbb{R}$      |
| Hinge loss        | $\max\{0, 1-z\}$                 | ×   | X            | ×            | $\checkmark$ | $z \in (-\infty, +1]$ |
| Double hinge loss | $\max\{0, (1-z)/2, -z\}$         | ×   | $\checkmark$ | ×            | $\checkmark$ | $z \in (-\infty, +1]$ |
| Sigmoid loss      | $1/(1+\exp(z))$                  | <   | ×            | $\checkmark$ | $\checkmark$ | $z\in\mathbb{R}$      |

All loss functions are unary, such that  $\ell(t,y) = \ell(z)$  with z = ty. The ramp loss comes from [15]; the double hinge loss is from [16], in which the squared, logistic and hinge losses were discussed as well. The ramp and squared losses are scaled to satisfy (3) or (5). The sigmoid loss is a horizontally mirrored *logistic function*; the logistic loss is the negative logarithm of the logistic function.

## <span id="page-4-1"></span>Algorithm 1 Large-scale PU learning based on stochastic optimization

```
Input: training data (\mathcal{X}_{p}, \mathcal{X}_{u});
                   hyperparameters 0 \le \beta \le \pi_{\mathrm{p}} \sup_{t} \max_{y} \ell(t,y) and 0 \le \gamma \le 1
    Output: model parameter \theta for \widehat{g}_{pu}(x;\theta) or \widetilde{g}_{pu}(x;\theta)
  1: Let \mathcal{A} be an external SGD-like stochastic optimization algorithm such as [20] or [31]
 2: while no stopping criterion has been met:
            Shuffle (\mathcal{X}_p, \mathcal{X}_u) into N mini-batches, and denote by (\mathcal{X}_p^i, \mathcal{X}_u^i) the i-th mini-batch
 3:
            for i = 1 to N:
 4:
                 if R_{\mathbf{u}}^{-}(g; \mathcal{X}_{\mathbf{u}}^{i}) - \pi_{\mathbf{p}} \widehat{R}_{\mathbf{p}}^{-}(g; \mathcal{X}_{\mathbf{p}}^{i}) \ge -\beta:
 5:
                       Set gradient \nabla_{\theta} \widehat{R}_{\mathrm{pu}}(g; \mathcal{X}_{\mathrm{p}}^{i}, \mathcal{X}_{\mathrm{u}}^{i})
 6:
 7:
                       Update \theta by \mathcal{A} with its current step size \eta
 8:
                       Set gradient \nabla_{\theta}(\pi_{\mathrm{p}}\widehat{R}_{\mathrm{p}}^{-}(g;\mathcal{X}_{\mathrm{p}}^{i}) - \widehat{R}_{\mathrm{u}}^{-}(g;\mathcal{X}_{\mathrm{u}}^{i}))
Update \theta by \mathcal{A} with a discounted step size \gamma\eta
 9:
10:
```

The large-scale PU algorithm is described in Algorithm 1. Let  $r_i = \widehat{R}_{\mathbf{u}}^-(g; \mathcal{X}_{\mathbf{u}}^i) - \pi_{\mathbf{p}} \widehat{R}_{\mathbf{p}}^-(g; \mathcal{X}_{\mathbf{p}}^i)$ . In practice, we may tolerate  $r_i \geq -\beta$  where  $0 \leq \beta \leq \pi_{\mathbf{p}} \sup_t \max_y \ell(t,y)$ , as  $r_i$  comes from a single mini-batch. The degree of tolerance is controlled by  $\beta$ : there is zero tolerance if  $\beta = 0$ , and we are minimizing  $\widehat{R}_{\mathbf{pu}}(g)$  if  $\beta = \pi_{\mathbf{p}} \sup_t \max_y \ell(t,y)$ . Otherwise if  $r_i < -\beta$ , we go along  $-\nabla_{\theta} r_i$  with a step size discounted by  $\gamma$  where  $0 \leq \gamma \leq 1$ , to make this mini-batch less overfitted. Algorithm 1 is insensitive to the choice of  $\gamma$ , if the optimization algorithm  $\mathcal A$  is adaptive such as [20] or [31].

#### <span id="page-4-0"></span>4 Theoretical analyses

In this section, we analyze the risk estimator (6) and its minimizer (all proofs are in Appendix B).

## 4.1 Bias and consistency

Fix g,  $\widetilde{R}_{\mathrm{pu}}(g) \geq \widehat{R}_{\mathrm{pu}}(g)$  for any  $(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}})$  but  $\widehat{R}_{\mathrm{pu}}(g)$  is unbiased, which implies  $\widetilde{R}_{\mathrm{pu}}(g)$  is biased in general. A fundamental question is then whether  $\widetilde{R}_{\mathrm{pu}}(g)$  is consistent. From now on, we prove this consistency. To begin with, partition all possible  $(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}})$  into  $\mathfrak{D}^+(g) = \{(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}) \mid \widehat{R}_{\mathrm{u}}^-(g) - \pi_{\mathrm{p}}\widehat{R}_{\mathrm{p}}^-(g) \geq 0\}$  and  $\mathfrak{D}^-(g) = \{(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}) \mid \widehat{R}_{\mathrm{u}}^-(g) - \pi_{\mathrm{p}}\widehat{R}_{\mathrm{p}}^-(g) < 0\}$ . Assume there are  $C_g > 0$  and  $C_\ell > 0$  such that  $\sup_{g \in \mathcal{G}} \|g\|_{\infty} \leq C_g$  and  $\sup_{|t| \leq C_g} \max_y \ell(t,y) \leq C_\ell$ .

<span id="page-4-3"></span>**Lemma 1.** The following three conditions are equivalent: (A) the probability measure of  $\mathfrak{D}^-(g)$  is non-zero; (B)  $\widetilde{R}_{pu}(g)$  differs from  $\widehat{R}_{pu}(g)$  with a non-zero probability over repeated sampling of  $(\mathcal{X}_p, \mathcal{X}_u)$ ; (C) the bias of  $\widetilde{R}_{pu}(g)$  is positive. In addition, by assuming that there is  $\alpha > 0$  such that  $R_n^-(g) \geq \alpha$ , the probability measure of  $\mathfrak{D}^-(g)$  can be bounded by

<span id="page-4-4"></span>
$$\Pr(\mathfrak{D}^{-}(g)) \le \exp(-2(\alpha/C_{\ell})^{2}/(\pi_{p}^{2}/n_{p}+1/n_{u})).$$
 (7)

Based on Lemma 1, we can show the exponential decay of the bias and also the consistency. For convenience, denote by  $\chi_{n_{\rm p},n_{\rm u}}=2\pi_{\rm p}/\sqrt{n_{\rm p}}+1/\sqrt{n_{\rm u}}$ .

<span id="page-5-2"></span>**Theorem 2** (Bias and consistency). Assume that  $R_{\rm n}^-(g) \ge \alpha > 0$  and denote by  $\Delta_g$  the right-hand side of Eq. (7). As  $n_{\rm p}, n_{\rm u} \to \infty$ , the bias of  $\widetilde{R}_{\rm pu}(g)$  decays exponentially:

$$0 \le \mathbb{E}_{\mathcal{X}_{\mathbf{p}}, \mathcal{X}_{\mathbf{u}}}[\widetilde{R}_{\mathbf{p}\mathbf{u}}(g)] - R(g) \le C_{\ell} \pi_{\mathbf{p}} \Delta_{g}. \tag{8}$$

Moreover, for any  $\delta > 0$ , let  $C_{\delta} = C_{\ell} \sqrt{\ln(2/\delta)/2}$ , then we have with probability at least  $1 - \delta$ ,

$$|\widetilde{R}_{pu}(g) - R(g)| \le C_{\delta} \cdot \chi_{n_p, n_p} + C_{\ell} \pi_p \Delta_q, \tag{9}$$

and with probability at least  $1 - \delta - \Delta_q$ ,

<span id="page-5-9"></span><span id="page-5-4"></span><span id="page-5-1"></span><span id="page-5-0"></span>
$$|\widetilde{R}_{\text{pu}}(g) - R(g)| \le C_{\delta} \cdot \chi_{n_{\text{p}}, n_{\text{y}}}.$$
(10)

Either (9) or (10) in Theorem 2 indicates for fixed g,  $\widetilde{R}_{pu}(g) \to R(g)$  in  $\mathcal{O}_p(\pi_p/\sqrt{n_p} + 1/\sqrt{n_u})$ . This convergence rate is optimal according to the *central limit theorem* [32], which means the proposed estimator is a biased yet optimal estimator to the risk.

## 4.2 Mean squared error

After introducing the bias,  $\widehat{R}_{pu}(g)$  tends to overestimate R(g). It is not a *shrinkage estimator* [33, 34] so that its *mean squared error* (MSE) is not necessarily smaller than that of  $\widehat{R}_{pu}(g)$ . However, we can still characterize this reduction in MSE.

<span id="page-5-5"></span>**Theorem 3** (MSE reduction). It holds that  $\mathrm{MSE}(\widetilde{R}_{\mathrm{pu}}(g)) < \mathrm{MSE}(\widehat{R}_{\mathrm{pu}}(g))$ , if and only if

$$\int_{(\mathcal{X}_{\mathbf{p}}, \mathcal{X}_{\mathbf{u}}) \in \mathfrak{D}^{-}(g)} (\widehat{R}_{\mathbf{p}\mathbf{u}}(g) + \widetilde{R}_{\mathbf{p}\mathbf{u}}(g) - 2R(g)) (\widehat{R}_{\mathbf{u}}^{-}(g) - \pi_{\mathbf{p}}\widehat{R}_{\mathbf{p}}^{-}(g)) \,\mathrm{d}F(\mathcal{X}_{\mathbf{p}}, \mathcal{X}_{\mathbf{u}}) > 0, \tag{11}$$

where  $dF(\mathcal{X}_p, \mathcal{X}_u) = \prod_{i=1}^{n_p} p_p(x_i^p) dx_i^p \cdot \prod_{i=1}^{n_u} p(x_i^u) dx_i^u$ . Eq. (11) is valid, if the following conditions are met: (a)  $\Pr(\mathfrak{D}^-(g)) > 0$ ; (b)  $\ell$  satisfies Eq. (3); (c)  $R_n^-(g) \geq \alpha > 0$ ; (d)  $n_u \gg n_p$ , such that we have  $R_u^-(g) - \widehat{R}_u^-(g) \leq 2\alpha$  almost surely on  $\mathfrak{D}^-(g)$ . In fact, given these four conditions, we have for any  $0 \leq \beta \leq C_\ell \pi_p$ ,

<span id="page-5-10"></span>
$$MSE(\widehat{R}_{pu}(g)) - MSE(\widetilde{R}_{pu}(g)) \ge 3\beta^{2} Pr\{\widetilde{R}_{pu}(g) - \widehat{R}_{pu}(g) > \beta\}.$$
(12)

The assumption (d) in Theorem 3 is explained as follows. Since U data can be much cheaper than P data in practice, it would be natural to assume  $n_{\rm u}$  is much larger and grows much faster than  $n_{\rm p}$ , hence  $\Pr\{R_{\rm u}^-(g) - \widehat{R}_{\rm u}^-(g) \geq \alpha\}/\Pr\{\widehat{R}_{\rm p}^-(g) - R_{\rm p}^-(g) \geq \alpha/\pi_{\rm p}\} \propto \exp(n_{\rm p} - n_{\rm u})$  asymptotically. This means the contribution of  $\mathcal{X}_{\rm u}$  is negligible for making  $(\mathcal{X}_{\rm p}, \mathcal{X}_{\rm u}) \in \mathfrak{D}^-(g)$  so that  $\Pr(\mathfrak{D}^-(g))$  exhibits exponential decay mainly in  $n_{\rm p}$ . As  $\Pr\{R_{\rm u}^-(g) - \widehat{R}_{\rm u}^-(g) \geq 2\alpha\}$  has stronger exponential decay in  $n_{\rm u}$  than  $\Pr\{R_{\rm u}^-(g) - \widehat{R}_{\rm u}^-(g) \geq \alpha\}$  as well as  $n_{\rm u} \gg n_{\rm p}$ , we made the assumption (d).

#### 4.3 Estimation error

While Theorems 2 and 3 addressed the use of (6) for evaluating the risk, we are likewise interested in its use for training classifiers. In what follows, we analyze the estimation error  $R(\widetilde{g}_{pu}) - R(g^*)$ , where  $g^*$  is the true risk minimizer in  $\mathcal{G}$ , i.e.,  $g^* = \arg\min_{g \in \mathcal{G}} R(g)$ . As a common practice [28], assume that  $\ell(t,y)$  is Lipschitz continuous in t for all  $|t| \leq C_g$  with a Lipschitz constant  $L_\ell$ .

<span id="page-5-7"></span>**Theorem 4** (Estimation error bound). Assume that (a)  $\inf_{g \in \mathcal{G}} R_n^-(g) \ge \alpha > 0$  and denote by  $\Delta$  the right-hand side of Eq. (7); (b)  $\mathcal{G}$  is closed under negation, i.e.,  $g \in \mathcal{G}$  if and only if  $-g \in \mathcal{G}$ . Then, for any  $\delta > 0$ , with probability at least  $1 - \delta$ ,

<span id="page-5-8"></span>
$$R(\widetilde{g}_{\mathrm{pu}}) - R(g^*) \le 16L_{\ell}\pi_{\mathrm{p}}\mathfrak{R}_{n_{\mathrm{p}},p_{\mathrm{p}}}(\mathcal{G}) + 8L_{\ell}\mathfrak{R}_{n_{\mathrm{u}},p}(\mathcal{G}) + 2C_{\delta}' \cdot \chi_{n_{\mathrm{p}},n_{\mathrm{u}}} + 2C_{\ell}\pi_{\mathrm{p}}\Delta, \tag{13}$$

where  $C'_{\delta} = C_{\ell} \sqrt{\ln(1/\delta)/2}$ , and  $\mathfrak{R}_{n_{\mathrm{p}},p_{\mathrm{p}}}(\mathcal{G})$  and  $\mathfrak{R}_{n_{\mathrm{u}},p}(\mathcal{G})$  are the Rademacher complexities of  $\mathcal{G}$  for the sampling of size  $n_{\mathrm{p}}$  from  $p_{\mathrm{p}}(x)$  and of size  $n_{\mathrm{u}}$  from p(x), respectively.

<span id="page-5-6"></span><span id="page-5-3"></span><sup>&</sup>lt;sup>5</sup>Here, MSE(·) is over repeated sampling of  $(\mathcal{X}_{D}, \mathcal{X}_{U})$ .

<sup>&</sup>lt;sup>6</sup>This can be derived as  $n_p$ ,  $n_u \to \infty$  by applying the *central limit theorem* to the two differences and then  $L'H\hat{o}pital's rule$  to the ratio of *complementary error functions* [32].

Theorem 4 ensures that learning with (6) is also consistent: as  $n_{\rm p}, n_{\rm u} \to \infty$ ,  $R(\widetilde{g}_{\rm pu}) \to R(g^*)$  and if  $\ell$  satisfies (5), all optimizations are convex and  $\widetilde{g}_{\rm pu} \to g^*$ . For linear-in-parameter models with a bounded norm,  $\mathfrak{R}_{n_{\rm p},p_{\rm p}}(\mathcal{G}) = \mathcal{O}(1/\sqrt{n_{\rm p}})$  and  $\mathfrak{R}_{n_{\rm u},p}(\mathcal{G}) = \mathcal{O}(1/\sqrt{n_{\rm u}})$ , and thus  $R(\widetilde{g}_{\rm pu}) \to R(g^*)$  in  $\mathcal{O}_p(\pi_{\rm p}/\sqrt{n_{\rm p}}+1/\sqrt{n_{\rm u}})$ .

For comparison,  $R(\widehat{g}_{Du}) - R(g^*)$  can be bounded using a different proof technique [19]:

<span id="page-6-3"></span><span id="page-6-1"></span>
$$R(\widehat{g}_{pu}) - R(g^*) \le 8L_{\ell}\pi_{p}\mathfrak{R}_{n_{p},p_{p}}(\mathcal{G}) + 4L_{\ell}\mathfrak{R}_{n_{u},p}(\mathcal{G}) + 2C_{\delta} \cdot \chi_{n_{p},n_{u}}, \tag{14}$$

where  $C_{\delta} = C_{\ell} \sqrt{\ln(2/\delta)/2}$ . The differences of (13) and (14) are completely from the differences of the corresponding uniform deviation bounds, i.e., the following lemma and Lemma 8 of [19].

<span id="page-6-2"></span>**Lemma 5.** Under the assumptions of Theorem 4, for any  $\delta > 0$ , with probability at least  $1 - \delta$ ,

$$\sup_{g \in \mathcal{G}} |\widetilde{R}_{pu}(g) - R(g)| \le 8L_{\ell} \pi_{p} \mathfrak{R}_{n_{p}, p_{p}}(\mathcal{G}) + 4L_{\ell} \mathfrak{R}_{n_{u}, p}(\mathcal{G}) + C_{\delta}' \cdot \chi_{n_{p}, n_{u}} + C_{\ell} \pi_{p} \Delta.$$
 (15)

Notice that  $\widehat{R}_{pu}(g)$  is point-wise while  $\widetilde{R}_{pu}(g)$  is not due to the maximum, which makes Lemma 5 much more difficult to prove than Lemma 8 of [19]. The key trick is that after *symmetrization*, we employ  $|\max\{0,z\}-\max\{0,z'\}| \leq |z-z'|$ , making three differences of partial risks point-wise (see (18) in the proof). As a consequence, we have to use a different Rademacher complexity *with the absolute value inside the supremum* [35, 36], whose *contraction* makes the coefficients of (15) doubled compared with Lemma 8 of [19]; moreover, we have to assume  $\mathcal G$  is closed under negation to change back to the standard Rademacher complexity *without the absolute value* [28]. Therefore, the differences of (13) and (14) are mainly due to different proof techniques and cannot reflect the intrinsic differences of empirical risk minimizers.

## <span id="page-6-0"></span>5 Experiments

In this section, we compare PN, unbiased PU (uPU) and non-negative PU (nnPU) learning experimentally. We focus on training deep neural networks, as uPU learning usually does not overfit if a linear-in-parameter model is used [19] and nothing needs to be fixed.

Table 2 describes the specification of benchmark datasets. MNIST, 20News and CIFAR-10 have 10, 7 and 10 classes originally, and we constructed the P and N classes from them as follows: MNIST was preprocessed in such a way that 0, 2, 4, 6, 8 constitute the P class, while 1, 3, 5, 7, 9 constitute the N class; for 20News, 'alt.', 'comp.', 'misc.' and 'rec.' make up the P class, and 'sci.', 'soc.' and 'talk.' make up the N class; for CIFAR-10, the P class is formed by 'airplane', 'automobile', 'ship' and 'truck', and the N class is formed by 'bird', 'cat', 'deer', 'dog', 'frog' and 'horse'. The dataset epsilon has 2 classes and such a construction is unnecessary.

Three learning methods were set up as follows: (A) for PN,  $n_p=1,000$  and  $n_n=(\pi_n/2\pi_p)^2n_p$ ; (B) for uPU,  $n_p=1,000$  and  $n_u$  is the total number of training data; (C) for nnPU,  $n_p$  and  $n_u$  are exactly same as uPU. For uPU and nnPU, P and U data were dependent, because neither  $\widehat{R}_{pu}(g)$  in Eq. (2) nor  $\widetilde{R}_{pu}(g)$  in Eq. (6) requires them to be independent. The choice of  $n_n$  was motivated by [19] and may make nnPU potentially better than PN as  $n_u \to \infty$  (whether  $n_p < \infty$  or  $n_p \le n_u$ ).

The model for MNIST was a 6-layer multilayer perceptron (MLP) with ReLU [40] (more specifically, d-300-300-300-300-1). For epsilon, the model was similar while the activation was replaced with Softsign [41] for better performance. For 20News, we borrowed the pre-trained word embeddings from GloVe [42], and the model can be written as d-avg\_pool(word\_emb(d,300))-300-300-1,

Table 2: Specification of benchmark datasets, models, and optimition algorithms.

<span id="page-6-4"></span>

| Name          | # Train | # Test  | # Feature | $\pi_{\rm p}$ | Model $g(x; \theta)$      | Opt. alg. $\mathcal{A}$ |
|---------------|---------|---------|-----------|---------------|---------------------------|-------------------------|
| MNIST [29]    | 60,000  | 10,000  | 784       | 0.49          | 6-layer MLP with ReLU     | Adam [20]               |
| epsilon [37]  | 400,000 | 100,000 | 2,000     | 0.50          | 6-layer MLP with Softsign | Adam [20]               |
| 20News [38]   | 11,314  | 7,532   | 61,188    | 0.44          | 5-layer MLP with Softsign | AdaGrad [31]            |
| CIFAR-10 [39] | 50,000  | 10,000  | 3,072     | 0.40          | 13-layer CNN with ReLU    | Adam [20]               |

See http://yann.lecun.com/exdb/mnist/ for MNIST, https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html for epsilon, http://qwone.com/~jason/20Newsgroups/ for 20Newsgroups, and https://www.cs.toronto.edu/~kriz/cifar.html for CIFAR-10.

<span id="page-7-0"></span>![](_page_7_Figure_0.svg)

Figure 2: Experimental results of training deep neural networks.

where word\_emb(d,300) retrieves 300-dimensional word embeddings for all words in a document, avg\_pool executes average pooling, and the resulting vector is fed to a 4-layer MLP with Softsign. The model for CIFAR-10 was an *all convolutional net* [43]: (32\*32\*3)-[C(3\*3,96)]\*2-C(3\*3,96,2)-[C(3\*3,192)]\*2-C(3\*3,192,2)-C(3\*3,192)-C(1\*1,192)-C(1\*1,10)-1000-1000-1, where the input is a 32\*32 RGB image, C(3\*3,96) means 96 channels of 3\*3 convolutions followed by ReLU, [ $\cdot$ ]\*2 means there are two such layers, C(3\*3,96,2) means a similar layer but with stride 2, etc.; it is one of the best architectures for CIFAR-10. Batch normalization [44] was applied before hidden layers. Furthermore, the sigmoid loss  $\ell_{\rm sig}$  was used as the surrogate loss and an  $\ell_2$ -regularization was also added. The resulting objectives were minimized by Adam [20] on MNIST, epsilon and CIFAR-10, and by AdaGrad [31] on 20News; we fixed  $\beta = 0$  and  $\gamma = 1$  for simplicity.

The experimental results are reported in Figure 2, where means and standard deviations of training and test risks based on the same 10 random samplings are shown. We can see that uPU overfitted training data and nnPU fixed this problem. Additionally, given limited N data, nnPU outperformed PN on MNIST, epsilon and CIFAR-10 and was comparable to it on 20News. In summary, with the proposed non-negative risk estimator, we are able to use very flexible models given limited P data.

We further tried some cases where  $\pi_p$  is misspecified, in order to simulate PU learning in the wild, where we must suffer from errors in estimating  $\pi_p$ . More specifically, we tested nnPU learning by replacing  $\pi_p$  with  $\pi'_p \in \{0.8\pi_p, 0.9\pi_p, \dots, 1.2\pi_p\}$  and giving  $\pi'_p$  to the learning method, so that it would regard  $\pi'_p$  as  $\pi_p$  during the entire training process. The experimental setup was exactly same as before except the replacement of  $\pi_p$ .

The experimental results are reported in Figure 3, where means of test risks of nnPU based on the same 10 random samplings are shown, and the best test risks are identified (horizontal lines are the best mean test risks and vertical lines are the epochs when they were achieved). We can see that on MNIST, the more misspecification was, the worse nnPU performed, while under-misspecification hurt more than over-misspecification; on epsilon, the cases where  $\pi'_p$  equals to  $\pi_p$ ,  $1.1\pi_p$  and  $1.2\pi_p$ 

<span id="page-8-1"></span>![](_page_8_Figure_0.svg)

Figure 3: Experimental results given  $\pi'_{p} \in \{0.8\pi_{p}, 0.9\pi_{p}, \dots, 1.2\pi_{p}\}.$ 

were comparable, but the best was  $\pi_{\rm p}'=1.1\pi_{\rm p}$  rather than  $\pi_{\rm p}'=\pi_{\rm p}$ ; on 20News, these three cases became different, such that  $\pi_{\rm p}'=\pi_{\rm p}$  was superior to  $\pi_{\rm p}'=1.2\pi_{\rm p}$  but inferior to  $\pi_{\rm p}'=1.1\pi_{\rm p}$ ; at last on CIFAR-10,  $\pi_{\rm p}'=\pi_{\rm p}$  and  $\pi_{\rm p}'=1.1\pi_{\rm p}$  were comparable again, and  $\pi_{\rm p}'=1.2\pi_{\rm p}$  was the winner.

In all the experiments, we have fixed  $\beta=0$ , which may explain this phenomenon. Recall that uPU overfitted seriously on all the benchmark datasets, and note that the larger  $\pi'_p$  is, the more different nnPU is from uPU. Therefore, the replacement of  $\pi_p$  with some  $\pi'_p > \pi_p$  introduces additional bias of  $\widetilde{R}_{pu}(g)$  in estimating R(g), but it also pushes  $\widetilde{R}_{pu}(g)$  away from  $\widehat{R}_{pu}(g)$  and then pushes nnPU away from uPU. This may result in lower test risks given some  $\pi'_p$  slightly larger than  $\pi_p$  as shown in Figure 3. This is also why under-misspecified  $\pi'_p$  hurt more than over-misspecified  $\pi'_p$ .

All the experiments were done with *Chainer* [45], and our implementation based on it is available at https://github.com/kiryor/nnPUlearning.

## <span id="page-8-0"></span>6 Conclusions

We proposed a non-negative risk estimator for PU learning that follows and improves on the state-of-the-art unbiased risk estimators. No matter how flexible the model is, it will not go negative as its unbiased counterparts. It is more robust against overfitting when being minimized, and training very flexible models such as deep neural networks given limited P data becomes possible. We also developed a large-scale PU learning algorithm. Extensive theoretical analyses were presented, and the usefulness of our non-negative PU learning was verified by intensive experiments. A promising future direction is extending the current work to semi-supervised learning along [46].

#### Acknowledgments

GN and MS were supported by JST CREST JPMJCR1403 and GN was also partially supported by Microsoft Research Asia.

# References

- <span id="page-9-0"></span>[1] F. Denis. PAC learning from positive statistical queries. In *ALT*, 1998.
- <span id="page-9-1"></span>[2] F. De Comité, F. Denis, R. Gilleron, and F. Letouzey. Positive and unlabeled examples help learning. In *ALT*, 1999.
- <span id="page-9-2"></span>[3] F. Letouzey, F. Denis, and R. Gilleron. Learning from positive and unlabeled examples. In *ALT*, 2000.
- <span id="page-9-3"></span>[4] C. Elkan and K. Noto. Learning classifiers from only positive and unlabeled data. In *KDD*, 2008.
- <span id="page-9-4"></span>[5] G. Ward, T. Hastie, S. Barry, J. Elith, and J. Leathwick. Presence-only data and the EM algorithm. *Biometrics*, 65(2):554–563, 2009.
- <span id="page-9-5"></span>[6] C. Scott and G. Blanchard. Novelty detection: Unlabeled data definitely help. In *AISTATS*, 2009.
- <span id="page-9-6"></span>[7] G. Blanchard, G. Lee, and C. Scott. Semi-supervised novelty detection. *Journal of Machine Learning Research*, 11:2973–3009, 2010.
- <span id="page-9-7"></span>[8] C.-J. Hsieh, N. Natarajan, and I. S. Dhillon. PU learning for matrix completion. In *ICML*, 2015.
- <span id="page-9-8"></span>[9] X. Li, P. S. Yu, B. Liu, and S.-K. Ng. Positive unlabeled learning for data stream classification. In *SDM*, 2009.
- <span id="page-9-9"></span>[10] M. N. Nguyen, X. Li, and S.-K. Ng. Positive unlabeled leaning for time series classification. In *IJCAI*, 2011.
- <span id="page-9-10"></span>[11] B. Liu, W. S. Lee, P. S. Yu, and X. Li. Partially supervised classification of text documents. In *ICML*, 2002.
- <span id="page-9-11"></span>[12] X. Li and B. Liu. Learning to classify texts using positive and unlabeled data. In *IJCAI*, 2003.
- <span id="page-9-12"></span>[13] W. S. Lee and B. Liu. Learning with positive and unlabeled examples using weighted logistic regression. In *ICML*, 2003.
- <span id="page-9-13"></span>[14] B. Liu, Y. Dai, X. Li, W. S. Lee, and P. S. Yu. Building text classifiers using positive and unlabeled examples. In *ICDM*, 2003.
- <span id="page-9-14"></span>[15] M. C. du Plessis, G. Niu, and M. Sugiyama. Analysis of learning from positive and unlabeled data. In *NIPS*, 2014.
- <span id="page-9-15"></span>[16] M. C. du Plessis, G. Niu, and M. Sugiyama. Convex formulation for learning from positive and unlabeled data. In *ICML*, 2015.
- <span id="page-9-16"></span>[17] N. Natarajan, I. S. Dhillon, P. Ravikumar, and A. Tewari. Learning with noisy labels. In *NIPS*, 2013.
- <span id="page-9-17"></span>[18] G. Patrini, F. Nielsen, R. Nock, and M. Carioni. Loss factorization, weakly supervised learning and label noise robustness. In *ICML*, 2016.
- <span id="page-9-18"></span>[19] G. Niu, M. C. du Plessis, T. Sakai, Y. Ma, and M. Sugiyama. Theoretical comparisons of positiveunlabeled learning against positive-negative learning. In *NIPS*, 2016.
- <span id="page-9-19"></span>[20] D. P. Kingma and J. L. Ba. Adam: A method for stochastic optimization. In *ICLR*, 2015.
- <span id="page-9-20"></span>[21] E. Sansone, F. G. B. De Natale, and Z.-H. Zhou. Efficient training for positive unlabeled learning. *arXiv preprint arXiv:1608.06807*, 2016.
- <span id="page-9-21"></span>[22] J. C. Platt. Fast training of support vector machines using sequential minimal optimization. In B. Schölkopf, C. J. C. Burges, and A. J. Smola, editors, *Advances in Kernel Methods*, pages 185–208. MIT Press, 1999.
- <span id="page-9-22"></span>[23] C. S. Ong B. Williamson A. Menon, B. Van Rooyen. Learning from corrupted binary labels via classprobability estimation. In *ICML*, 2015.
- <span id="page-9-23"></span>[24] H. G. Ramaswamy, C. Scott, and A. Tewari. Mixture proportion estimation via kernel embedding of distributions. In *ICML*, 2016.
- <span id="page-9-24"></span>[25] S. Jain, M. White, and P. Radivojac. Estimating the class prior and posterior from noisy positives and unlabeled data. In *NIPS*, 2016.
- <span id="page-9-25"></span>[26] M. C. du Plessis, G. Niu, and M. Sugiyama. Class-prior estimation for learning from positive and unlabeled data. *Machine Learning*, 106(4):463–492, 2017.
- <span id="page-9-26"></span>[27] P. L. Bartlett, M. I. Jordan, and J. D. McAuliffe. Convexity, classification, and risk bounds. *Journal of the American Statistical Association*, 101(473):138–156, 2006.
- <span id="page-9-28"></span>[28] M. Mohri, A. Rostamizadeh, and A. Talwalkar. *Foundations of Machine Learning*. MIT Press, 2012.
- <span id="page-9-27"></span>[29] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner. Gradient-based learning applied to document recognition. *Proceedings of the IEEE*, 86(11):2278–2324, 1998.
- <span id="page-9-29"></span>[30] A. L. Yuille and A. Rangarajan. The concave-convex procedure (CCCP). In *NIPS*, 2001.

- <span id="page-10-0"></span>[31] J. Duchi, E. Hazan, and Y. Singer. Adaptive subgradient methods for online learning and stochastic optimization. *Journal of Machine Learning Research*, 12:2121–2159, 2011.
- <span id="page-10-1"></span>[32] K.-L. Chung. *A Course in Probability Theory*. Academic Press, 1968.
- <span id="page-10-2"></span>[33] C. Stein. Inadmissibility of the usual estimator for the mean of a multivariate normal distribution. In *Proc. 3rd Berkeley Symposium on Mathematical Statistics and Probability*, 1956.
- <span id="page-10-3"></span>[34] W. James and C. Stein. Estimation with quadratic loss. In *Proc. 4th Berkeley Symposium on Mathematical Statistics and Probability*, 1961.
- <span id="page-10-4"></span>[35] V. Koltchinskii. Rademacher penalties and structural risk minimization. *IEEE Transactions on Information Theory*, 47(5):1902–1914, 2001.
- <span id="page-10-5"></span>[36] P. L. Bartlett and S. Mendelson. Rademacher and Gaussian complexities: Risk bounds and structural results. *Journal of Machine Learning Research*, 3:463–482, 2002.
- <span id="page-10-9"></span>[37] G.-X. Yuan, C.-H. Ho, and C.-J. Lin. An improved GLMNET for l1-regularized logistic regression. *Journal of Machine Learning Research*, 13:1999–2030, 2012.
- <span id="page-10-10"></span>[38] K. Lang. Newsweeder: Learning to filter netnews. In *ICML*, 1995.
- <span id="page-10-11"></span>[39] A. Krizhevsky. Learning multiple layers of features from tiny images. Technical report, University of Toronto, 2009.
- <span id="page-10-6"></span>[40] V. Nair and G. E. Hinton. Rectified linear units improve restricted boltzmann machines. In *ICML*, 2010.
- <span id="page-10-7"></span>[41] X. Glorot and Y. Bengio. Understanding the difficulty of training deep feedforward neural networks. In *AISTATS*, 2010.
- <span id="page-10-8"></span>[42] J. Pennington, R. Socher, and C. D. Manning. GloVe: Global vectors for word representation. In *EMNLP*, 2014.
- <span id="page-10-12"></span>[43] J. T. Springenberg, A. Dosovitskiy, T. Brox, and M. Riedmiller. Striving for simplicity: The all convolutional net. In *ICLR*, 2015.
- <span id="page-10-13"></span>[44] S. Ioffe and C. Szegedy. Batch normalization: Accelerating deep network training by reducing internal covariate shift. In *ICML*, 2015.
- <span id="page-10-14"></span>[45] S. Tokui, K. Oono, S. Hido, and J. Clayton. Chainer: a next-generation open source framework for deep learning. In *Machine Learning Systems Workshop at NIPS*, 2015.
- <span id="page-10-15"></span>[46] T. Sakai, M. C. du Plessis, G. Niu, and M. Sugiyama. Semi-supervised classification based on classification from positive and unlabeled data. In *ICML*, 2017.
- <span id="page-10-16"></span>[47] C. McDiarmid. On the method of bounded differences. In J. Siemons, editor, *Surveys in Combinatorics*, pages 148–188. Cambridge University Press, 1989.
- <span id="page-10-17"></span>[48] M. Ledoux and M. Talagrand. *Probability in Banach Spaces: Isoperimetry and Processes*. Springer, 1991.
- <span id="page-10-18"></span>[49] S. Shalev-Shwartz and S. Ben-David. *Understanding Machine Learning: From Theory to Algorithms*. Cambridge University Press, 2014.
- <span id="page-10-19"></span>[50] V. N. Vapnik. *Statistical Learning Theory*. John Wiley & Sons, 1998.

## A Supplementary experimental results

Due to limited space, we considered the surrogate loss without the zero-one loss in Figure 1. Here, we include the zero-one loss and show the extended version of Figure 1 in Figure 4. In general, the curves of risks w.r.t.  $\ell_{01}$  look quite similar to (but less smooth than) those w.r.t.  $\ell_{\rm sig}$ . Therefore, the curves of risks w.r.t.  $\ell_{\rm sig}$  are more visually appealing as the illustrative experimental results.

<span id="page-11-1"></span>![](_page_11_Figure_2.svg)

Figure 4: The extended version of Figure 1.

## <span id="page-11-0"></span>**B** Proofs

In this appendix, we prove all the theoretical results in Section 4.

## **B.1** Proof of Lemma 1

Let

$$p_{\mathbf{p}}(\mathcal{X}_{\mathbf{p}}) = p_{\mathbf{p}}(x_{1}^{\mathbf{p}}) \cdots p_{\mathbf{p}}(x_{n_{\mathbf{p}}}^{\mathbf{p}}), \quad p(\mathcal{X}_{\mathbf{u}}) = p(x_{1}^{\mathbf{u}}) \cdots p(x_{n_{\mathbf{u}}}^{\mathbf{u}})$$

be the probability density functions of  $\mathcal{X}_p$  and  $\mathcal{X}_u$ . Then let  $F_p(\mathcal{X}_p)$  be the cumulative distribution function of  $\mathcal{X}_p$ ,  $F_u(\mathcal{X}_u)$  be that of  $\mathcal{X}_u$ , and

$$F(\mathcal{X}_{D}, \mathcal{X}_{U}) = F_{D}(\mathcal{X}_{D}) \cdot F_{U}(\mathcal{X}_{U})$$

be the joint cumulative distribution function of  $(\mathcal{X}_p, \mathcal{X}_u)$ . Given the above definitions, the measure of  $\mathfrak{D}^-(g)$  is defined by

$$\Pr(\mathfrak{D}^{-}(g)) = \int_{(\mathcal{X}_{p}, \mathcal{X}_{u}) \in \mathfrak{D}^{-}(g)} dF(\mathcal{X}_{p}, \mathcal{X}_{u}),$$

where  $\Pr$  denotes the probability. Since  $\widetilde{R}_{pu}(g)$  is identical to  $\widehat{R}_{pu}(g)$  on  $\mathfrak{D}^+(g)$  and different from  $\widehat{R}_{pu}(g)$  on  $\mathfrak{D}^-(g)$ , we have  $\Pr(\mathfrak{D}^-(g)) = \Pr\{\widetilde{R}_{pu}(g) \neq \widehat{R}_{pu}(g)\}$ . That is, the measure of  $\mathfrak{D}^-(g)$  is non-zero if and only if  $\widetilde{R}_{pu}(g)$  differs from  $\widehat{R}_{pu}(g)$  with a non-zero probability.

Based on the facts that  $\widehat{R}_{pu}(g)$  is unbiased and  $\widetilde{R}_{pu}(g) - \widehat{R}_{pu}(g) = 0$  on  $\mathfrak{D}^+(g)$ , we have

$$\begin{split} \mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g)] - R(g) &= \mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g) - \widehat{R}_{\mathrm{pu}}(g)] \\ &= \int_{(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}) \in \mathfrak{D}^{+}(g)} \widetilde{R}_{\mathrm{pu}}(g) - \widehat{R}_{\mathrm{pu}}(g) \, \mathrm{d}F(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}) \\ &+ \int_{(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}) \in \mathfrak{D}^{-}(g)} \widetilde{R}_{\mathrm{pu}}(g) - \widehat{R}_{\mathrm{pu}}(g) \, \mathrm{d}F(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}) \\ &= \int_{(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}) \in \mathfrak{D}^{-}(g)} \widetilde{R}_{\mathrm{pu}}(g) - \widehat{R}_{\mathrm{pu}}(g) \, \mathrm{d}F(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}). \end{split}$$

As a result,  $\mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g)] - R(g) > 0$  if and only if  $\int_{(\mathcal{X}_{\mathrm{p}},\mathcal{X}_{\mathrm{u}}) \in \mathfrak{D}^{-}(g)} \mathrm{d}F(\mathcal{X}_{\mathrm{p}},\mathcal{X}_{\mathrm{u}}) > 0$  due to the fact  $\widetilde{R}_{\mathrm{pu}}(g) - \widehat{R}_{\mathrm{pu}}(g) > 0$  on  $\mathfrak{D}^{-}(g)$ . That is, the bias of  $\widetilde{R}_{\mathrm{pu}}(g)$  is positive if and only if the measure of  $\mathfrak{D}^{-}(g)$  is non-zero.

We prove (7) by the method of bounded differences, for that

$$\mathbb{E}[\widehat{R}_{\mathbf{u}}^{-}(g) - \pi_{\mathbf{p}}\widehat{R}_{\mathbf{p}}^{-}(g)] = R_{\mathbf{u}}^{-}(g) - \pi_{\mathbf{p}}R_{\mathbf{p}}^{-}(g) = R_{\mathbf{n}}^{-}(g) \ge \alpha.$$

We have assumed that  $0 \le \ell(t,\pm 1) \le C_\ell$ , and thus the change of  $\widehat{R}_{\rm p}^-(g)$  will be no more than  $C_\ell/n_{\rm p}$  if some  $x_i^{\rm p} \in \mathcal{X}_{\rm p}$  is replaced, or the change of  $\widehat{R}_{\rm u}^-(g)$  will be no more than  $C_\ell/n_{\rm u}$  if some  $x_i^{\rm p} \in \mathcal{X}_{\rm u}$  is replaced. Subsequently, McDiarmid's inequality [47] implies

$$\begin{split} \Pr\{R_{\mathbf{n}}^{-}(g) - (\widehat{R}_{\mathbf{u}}^{-}(g) - \pi_{\mathbf{p}}\widehat{R}_{\mathbf{p}}^{-}(g)) & \geq \alpha\} \leq \exp\left(-\frac{2\alpha^{2}}{n_{\mathbf{p}}(C_{\ell}\pi_{\mathbf{p}}/n_{\mathbf{p}})^{2} + n_{\mathbf{u}}(C_{\ell}/n_{\mathbf{u}})^{2}}\right) \\ & = \exp\left(-\frac{2\alpha^{2}/C_{\ell}^{2}}{\pi_{\mathbf{p}}^{2}/n_{\mathbf{p}} + 1/n_{\mathbf{u}}}\right). \end{split}$$

Taking into account that

$$\begin{split} \Pr(\mathfrak{D}^{-}(g)) &= \Pr\{\widehat{R}_{\mathbf{u}}^{-}(g) - \pi_{\mathbf{p}}\widehat{R}_{\mathbf{p}}^{-}(g) < 0\} \\ &\leq \Pr\{\widehat{R}_{\mathbf{u}}^{-}(g) - \pi_{\mathbf{p}}\widehat{R}_{\mathbf{p}}^{-}(g) \leq R_{\mathbf{n}}^{-}(g) - \alpha\} \\ &= \Pr\{R_{\mathbf{n}}^{-}(g) - (\widehat{R}_{\mathbf{u}}^{-}(g) - \pi_{\mathbf{p}}\widehat{R}_{\mathbf{p}}^{-}(g)) \geq \alpha\}, \end{split}$$

we complete the proof.

#### **B.2** Proof of Theorem 2

It has been proven in Lemma 1 that

$$\mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g)] - R(g) = \int_{(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}) \in \mathfrak{D}^{-}(g)} \widetilde{R}_{\mathrm{pu}}(g) - \widehat{R}_{\mathrm{pu}}(g) \, \mathrm{d}F(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}),$$

and thus the exponential decay of the bias in (8) is obtained via

$$\mathbb{E}[\widetilde{R}_{pu}(g)] - R(g) \leq \sup_{(\mathcal{X}_{p}, \mathcal{X}_{u}) \in \mathfrak{D}^{-}(g)} (\widetilde{R}_{pu}(g) - \widehat{R}_{pu}(g)) \cdot \int_{(\mathcal{X}_{p}, \mathcal{X}_{u}) \in \mathfrak{D}^{-}(g)} dF(\mathcal{X}_{p}, \mathcal{X}_{u})$$

$$= \sup_{(\mathcal{X}_{p}, \mathcal{X}_{u}) \in \mathfrak{D}^{-}(g)} (\pi_{p} \widehat{R}_{p}^{-}(g) - \widehat{R}_{u}^{-}(g)) \cdot \Pr(\mathfrak{D}^{-}(g))$$

$$\leq C_{\ell} \pi_{p} \Delta_{q}.$$

The deviation bound (9) is due to

$$\begin{split} |\widetilde{R}_{\mathrm{pu}}(g) - R(g)| &\leq |\widetilde{R}_{\mathrm{pu}}(g) - \mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g)]| + |\mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g)] - R(g)| \\ &\leq |\widetilde{R}_{\mathrm{pu}}(g) - \mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g)]| + C_{\ell} \pi_{\mathrm{p}} \Delta_{g}. \end{split}$$

The change of  $\widetilde{R}_{pu}(g)$  will be no more than  $2C_\ell/n_p$  if some  $x_i^p \in \mathcal{X}_p$  is replaced, or it will be no more than  $C_\ell/n_u$  if some  $x_i^u \in \mathcal{X}_u$  is replaced, and McDiarmid's inequality gives us

$$\Pr\{|\widetilde{R}_{\mathrm{pu}}(g) - \mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g)]| \geq \epsilon\} \leq 2 \exp\left(-\frac{2\epsilon^2}{n_{\mathrm{p}}(2C_\ell\pi_{\mathrm{p}}/n_{\mathrm{p}})^2 + n_{\mathrm{u}}(C_\ell/n_{\mathrm{u}})^2}\right),$$

or equivalently, with probability at least  $1 - \delta$ ,

$$\begin{aligned} |\widetilde{R}_{\mathrm{pu}}(g) - \mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g)]| &\leq \sqrt{\frac{\ln(2/\delta)C_{\ell}^{2}}{2} \left(\frac{4\pi_{\mathrm{p}}^{2}}{n_{\mathrm{p}}} + \frac{1}{n_{\mathrm{u}}}\right)} \\ &\leq C_{\delta} \left(\frac{2\pi_{\mathrm{p}}}{\sqrt{n_{\mathrm{p}}}} + \frac{1}{\sqrt{n_{\mathrm{u}}}}\right) \\ &= C_{\delta} \cdot \chi_{n_{\mathrm{p}}, n_{\mathrm{u}}}. \end{aligned}$$

On the other hand, the deviation bound (10) is due to

$$|\widetilde{R}_{\mathrm{pu}}(g) - R(g)| \le |\widetilde{R}_{\mathrm{pu}}(g) - \widehat{R}_{\mathrm{pu}}(g)| + |\widehat{R}_{\mathrm{pu}}(g) - R(g)|,$$

where  $|\widetilde{R}_{\mathrm{pu}}(g) - \widehat{R}_{\mathrm{pu}}(g)| > 0$  with probability at most  $\Delta_g$ , and  $|\widehat{R}_{\mathrm{pu}}(g) - R(g)|$  shares the same concentration inequality with  $|\widetilde{R}_{\mathrm{pu}}(g) - \mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g)]|$ .

#### **B.3** Proof of Theorem 3

For convenience, let  $A=\pi_{\rm p}\widehat{R}_{\rm p}^+(g)$  and  $B=\widehat{R}_{\rm u}^-(g)-\pi_{\rm p}\widehat{R}_{\rm p}^-(g)$ , so that

$$R(g) = \mathbb{E}[A+B], \quad \widehat{R}_{pu}(g) = A+B, \quad \widetilde{R}_{pu}(g) = A+B_{+},$$

where  $B_+ = \max\{0, B\}$ . Subsequently, let R = R(g) for short, and then by definition,

$$\begin{aligned} \text{MSE}(\widehat{R}_{\text{pu}}(g)) &= \mathbb{E}[(A+B-R)^2] \\ &= \mathbb{E}[(A+B)^2] - 2R \cdot \mathbb{E}[A+B] + R^2, \\ \text{MSE}(\widetilde{R}_{\text{pu}}(g)) &= \mathbb{E}[(A+B_+ - R(g))^2] \\ &= \mathbb{E}[(A+B_+)^2] - 2R \cdot \mathbb{E}[A+B_+] + R^2. \end{aligned}$$

Hence,

$$\begin{aligned} \mathrm{MSE}(\widehat{R}_{\mathrm{pu}}(g)) - \mathrm{MSE}(\widetilde{R}_{\mathrm{pu}}(g)) &= \mathbb{E}[(A+B)^2] - \mathbb{E}[(A+B_+)^2] \\ &- 2R \cdot (\mathbb{E}[A+B] - \mathbb{E}[A+B_+]). \end{aligned}$$

The first part  $\mathbb{E}[(A+B)^2] - \mathbb{E}[(A+B_+)^2]$  can be rewritten as

$$\begin{split} \mathbb{E}[(A+B)^{2}] - \mathbb{E}[(A+B_{+})^{2}] &= \mathbb{E}[2A(B-B_{+}) + B^{2} - B_{+}^{2}] \\ &= \int_{(\mathcal{X}_{p}, \mathcal{X}_{u}) \in \mathfrak{D}^{+}(g)} 2A(B-B) + B^{2} - B^{2} \, \mathrm{d}F(\mathcal{X}_{p}, \mathcal{X}_{u}) \\ &+ \int_{(\mathcal{X}_{p}, \mathcal{X}_{u}) \in \mathfrak{D}^{-}(g)} 2A(B-0) + B^{2} - 0^{2} \, \mathrm{d}F(\mathcal{X}_{p}, \mathcal{X}_{u}) \\ &= \int_{(\mathcal{X}_{p}, \mathcal{X}_{u}) \in \mathfrak{D}^{-}(g)} 2AB + B^{2} \, \mathrm{d}F(\mathcal{X}_{p}, \mathcal{X}_{u}). \end{split}$$

The second part  $2R \cdot (\mathbb{E}[A+B] - \mathbb{E}[A+B_+])$  can be rewritten as

$$\begin{aligned} 2R \cdot (\mathbb{E}[A+B] - \mathbb{E}[A+B_+]) &= 2R \cdot \mathbb{E}[B-B_+] \\ &= 2R \cdot \int_{(\mathcal{X}_{\mathbf{p}}, \mathcal{X}_{\mathbf{u}}) \in \mathfrak{D}^+(g)} B - B \, \mathrm{d}F(\mathcal{X}_{\mathbf{p}}, \mathcal{X}_{\mathbf{u}}) \\ &+ 2R \cdot \int_{(\mathcal{X}_{\mathbf{p}}, \mathcal{X}_{\mathbf{u}}) \in \mathfrak{D}^-(g)} B - 0 \, \mathrm{d}F(\mathcal{X}_{\mathbf{p}}, \mathcal{X}_{\mathbf{u}}) \\ &= \int_{(\mathcal{X}_{\mathbf{p}}, \mathcal{X}_{\mathbf{u}}) \in \mathfrak{D}^-(g)} 2RB \, \mathrm{d}F(\mathcal{X}_{\mathbf{p}}, \mathcal{X}_{\mathbf{u}}). \end{aligned}$$

As a consequence,

$$MSE(\widehat{R}_{pu}(g)) - MSE(\widetilde{R}_{pu}(g)) = \int_{(\mathcal{X}_{p}, \mathcal{X}_{u}) \in \mathfrak{D}^{-}(g)} (2A + B - 2R)B \, dF(\mathcal{X}_{p}, \mathcal{X}_{u}),$$

which is exactly the left-hand side of (11) since  $\widetilde{R}_{pu}(g) = A$  on  $\mathfrak{D}^{-}(g)$ .

In order to prove the rest, it suffices to show that  $A - R \leq B$  on  $\mathfrak{D}^-(g)$ . By the assumption that  $\ell$  satisfies (3),

$$\begin{aligned} A - R &= A - \mathbb{E}[A] - \mathbb{E}[B] \\ &= \pi_{\mathbf{p}} \widehat{R}_{\mathbf{p}}^+(g) - \pi_{\mathbf{p}} R_{\mathbf{p}}^+(g) - \mathbb{E}[B] \\ &= \pi_{\mathbf{p}} R_{\mathbf{p}}^-(g) - \pi_{\mathbf{p}} \widehat{R}_{\mathbf{p}}^-(g) - \mathbb{E}[B]. \end{aligned}$$

Thus, with probability one,

$$\begin{split} A - R &= \pi_{\mathbf{p}} R_{\mathbf{p}}^{-}(g) - \pi_{\mathbf{p}} \widehat{R}_{\mathbf{p}}^{-}(g) - \mathbb{E}[B] + (\widehat{R}_{\mathbf{u}}^{-}(g) - \widehat{R}_{\mathbf{u}}^{-}(g)) + (R_{\mathbf{u}}^{-}(g) - R_{\mathbf{u}}^{-}(g)) \\ &= (\widehat{R}_{\mathbf{u}}^{-}(g) - \pi_{\mathbf{p}} \widehat{R}_{\mathbf{p}}^{-}(g)) - (R_{\mathbf{u}}^{-}(g) - \pi_{\mathbf{p}} R_{\mathbf{p}}^{-}(g)) - \mathbb{E}[B] + (R_{\mathbf{u}}^{-}(g) - \widehat{R}_{\mathbf{u}}^{-}(g)) \\ &= B - 2\mathbb{E}[B] + (R_{\mathbf{u}}^{-}(g) - \widehat{R}_{\mathbf{u}}^{-}(g)) \\ &\leq B, \end{split}$$

where we used the assumptions that  $\mathbb{E}[B] \geq \alpha$  and  $R_{\mathrm{u}}^-(g) - \widehat{R}_{\mathrm{u}}^-(g) \leq 2\alpha$  almost surely on  $\mathfrak{D}^-(g)$ . To sum up, we have established that

$$\int_{(\mathcal{X}_p,\mathcal{X}_u)\in\mathfrak{D}^-(g)} (2A+B-2R)B \, \mathrm{d}F(\mathcal{X}_p,\mathcal{X}_u) \geq 3 \int_{(\mathcal{X}_p,\mathcal{X}_u)\in\mathfrak{D}^-(g)} B^2 \, \mathrm{d}F(\mathcal{X}_p,\mathcal{X}_u).$$

Due to the fact that  $B^2>0$  on  $\mathfrak{D}^-(g)$  and the assumption that  $\Pr(\mathfrak{D}^-(g))>0$ , we know Eq. (11) is valid. Finally, for any  $0\leq\beta\leq C_\ell\pi_p$ , it is clear that

$$\{(\mathcal{X}_{p}, \mathcal{X}_{u}) \mid B < -\beta\} \subseteq \{(\mathcal{X}_{p}, \mathcal{X}_{u}) \mid B < 0\} = \mathfrak{D}^{-}(g),$$

and  $B<-\beta$  if and only if  $\widetilde{R}_{\mathrm{pu}}(g)-\widehat{R}_{\mathrm{pu}}(g)>\beta$ . These two facts imply that

$$\int_{(\mathcal{X}_{p},\mathcal{X}_{u})\in\mathfrak{D}^{-}(g)} B^{2} dF(\mathcal{X}_{p},\mathcal{X}_{u}) \geq \int_{(\mathcal{X}_{p},\mathcal{X}_{u})|B<-\beta} B^{2} dF(\mathcal{X}_{p},\mathcal{X}_{u})$$

$$\geq \beta^{2} \int_{(\mathcal{X}_{p},\mathcal{X}_{u})|B<-\beta} dF(\mathcal{X}_{p},\mathcal{X}_{u})$$

$$= \beta^{2} \Pr\{B<-\beta\}$$

$$= \beta^{2} \Pr\{\widetilde{R}_{pu}(g) - \widehat{R}_{pu}(g) > \beta\},$$

which proves (12) and the whole theorem.

#### B.4 Proof of Lemma 5

**Preliminary** An alternative definition of the Rademacher complexity will be used in the proof:

$$\mathfrak{R}'_{n,q}(\mathcal{G}) = \mathbb{E}_{\mathcal{X}} \mathbb{E}_{\sigma_1, \dots, \sigma_n} \left[ \sup_{g \in \mathcal{G}} \left| \frac{1}{n} \sum_{x_i \in \mathcal{X}} \sigma_i g(x_i) \right| \right].$$

For the sake of comparison, the one we have used in the statements of theoretical results is

$$\mathfrak{R}_{n,q}(\mathcal{G}) = \mathbb{E}_{\mathcal{X}} \mathbb{E}_{\sigma_1, \dots, \sigma_n} \left[ \sup_{g \in \mathcal{G}} \frac{1}{n} \sum_{x_i \in \mathcal{X}} \sigma_i g(x_i) \right].$$

This alternative version comes from [35, 36] of which authors are the pioneers of error bounds based on the Rademacher complexity. Without any composition,  $\mathfrak{R}'_{n,q}(\mathcal{G}) \geq \mathfrak{R}_{n,q}(\mathcal{G})$  for arbitrary  $\mathcal{G}$  and  $\mathfrak{R}'_{n,q}(\mathcal{G}) = \mathfrak{R}_{n,q}(\mathcal{G})$  if  $\mathcal{G}$  is closed under negation. However, with a composition

$$\ell \circ \mathcal{G} = \{\ell \circ g \mid g \in \mathcal{G}\}$$

where the loss  $\ell$  is non-negative, the Rademacher complexity of the *composite function class* would generally not satisfy  $\mathfrak{R}'_{n,q}(\ell \circ \mathcal{G}) = \mathfrak{R}_{n,q}(\ell \circ \mathcal{G})$  since  $\ell \circ \mathcal{G}$  is generally not closed under negation. Furthermore, a vital disagreement arises when considering the contraction principle or property: if  $\psi : \mathbb{R} \to \mathbb{R}$  is a Lipschitz continuous function with a Lipschitz constant  $L_{\psi}$  and satisfies  $\psi(0) = 0$ , we have

<span id="page-15-2"></span><span id="page-15-1"></span>
$$\mathfrak{R}_{n,q}(\psi \circ \mathcal{G}) \le L_{\psi} \mathfrak{R}_{n,q}(\mathcal{G}),$$
  
$$\mathfrak{R}'_{n,q}(\psi \circ \mathcal{G}) \le 2L_{\psi} \mathfrak{R}'_{n,q}(\mathcal{G}),$$

according to *Talagrand's contraction lemma* [48] and its extension [28, 49]. Here, for  $\mathfrak{R}_{n,q}(\psi \circ \mathcal{G})$  we can use Lemma 4.2 in [28] or Lemma 26.9 in [49] where  $\psi(0)=0$  is safely dropped, while for  $\mathfrak{R}'_{n,q}(\psi \circ \mathcal{G})$  we have to use the original Theorem 4.12 in [48] where  $\psi(0)=0$  is required. In fact, the name of the lemma is after that  $\psi$  is a contraction if  $\psi(0)=0$  and  $L_{\psi}=1$ .

**Proof** Firstly, we deal with the bias of  $\widetilde{R}_{pu}(g)$ :

$$\sup_{g \in \mathcal{G}} |\widetilde{R}_{pu}(g) - R(g)| \le \sup_{g \in \mathcal{G}} |\widetilde{R}_{pu}(g) - \mathbb{E}[\widetilde{R}_{pu}(g)]| + \sup_{g \in \mathcal{G}} |\mathbb{E}[\widetilde{R}_{pu}(g)] - R(g)| 
\le \sup_{g \in \mathcal{G}} |\widetilde{R}_{pu}(g) - \mathbb{E}[\widetilde{R}_{pu}(g)]| + C_{\ell} \pi_{p} \Delta, \tag{16}$$

where we followed the assumption that  $\inf_{g \in \mathcal{G}} R_n^-(g) \ge \alpha > 0$  and Theorem 2.

Secondly, we apply McDiarmid's inequality to the uniform deviation  $\sup_{g \in \mathcal{G}} |\widetilde{R}_{pu}(g) - \mathbb{E}[\widetilde{R}_{pu}(g)]|$  to get that with probability at least  $1 - \delta$ ,

$$\sup_{g \in \mathcal{G}} |\widetilde{R}_{pu}(g) - \mathbb{E}[\widetilde{R}_{pu}(g)]| - \mathbb{E}[\sup_{g \in \mathcal{G}} |\widetilde{R}_{pu}(g) - \mathbb{E}[\widetilde{R}_{pu}(g)]|] \le C'_{\delta} \cdot \chi_{n_{p}, n_{u}}.$$
 (17)

Notice that this concentration inequality is single-sided even though the uniform deviation itself is double-sided, which is different from the non-uniform deviation in Theorem 2.

Thirdly, we make symmetrization [50]. Suppose that  $(\mathcal{X}'_{D}, \mathcal{X}'_{U})$  is a ghost sample, then

$$\begin{split} \mathbb{E}[\sup_{g \in \mathcal{G}} |\widetilde{R}_{\mathrm{pu}}(g) - \mathbb{E}[\widetilde{R}_{\mathrm{pu}}(g)]|] &= \mathbb{E}_{(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}})}[\sup_{g \in \mathcal{G}} |\widetilde{R}_{\mathrm{pu}}(g) - \mathbb{E}_{(\mathcal{X}'_{\mathrm{p}}, \mathcal{X}'_{\mathrm{u}})}[\widetilde{R}_{\mathrm{pu}}(g)]|] \\ &\leq \mathbb{E}_{(\mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}), (\mathcal{X}'_{\mathrm{p}}, \mathcal{X}'_{\mathrm{u}})}[\sup_{g \in \mathcal{G}} |\widetilde{R}_{\mathrm{pu}}(g; \mathcal{X}_{\mathrm{p}}, \mathcal{X}_{\mathrm{u}}) - \widetilde{R}_{\mathrm{pu}}(g; \mathcal{X}'_{\mathrm{p}}, \mathcal{X}'_{\mathrm{u}})|], \end{split}$$

where we applied *Jensen's inequality* twice since the absolute value and the supremum are convex. By decomposing the difference  $|\widetilde{R}_{pu}(g; \mathcal{X}_p, \mathcal{X}_u) - \widetilde{R}_{pu}(g; \mathcal{X}_p', \mathcal{X}_u')|$ , we can know that

$$\begin{split} |\widetilde{R}_{pu}(g; \mathcal{X}_{p}, \mathcal{X}_{u}) - \widetilde{R}_{pu}(g; \mathcal{X}'_{p}, \mathcal{X}'_{u})| \\ &= |\pi_{p} \widehat{R}^{+}_{p}(g; \mathcal{X}_{p}) - \pi_{p} \widehat{R}^{+}_{p}(g; \mathcal{X}'_{p}) \\ &+ \max\{0, \widehat{R}^{-}_{u}(g; \mathcal{X}_{u}) - \pi_{p} \widehat{R}^{-}_{p}(g; \mathcal{X}_{p})\} - \max\{0, \widehat{R}^{-}_{u}(g; \mathcal{X}'_{u}) - \pi_{p} \widehat{R}^{-}_{p}(g; \mathcal{X}'_{p})\}| \\ &\leq \pi_{p} |\widehat{R}^{+}_{p}(g; \mathcal{X}_{p}) - \widehat{R}^{+}_{p}(g; \mathcal{X}'_{p})| + \pi_{p} |\widehat{R}^{-}_{p}(g; \mathcal{X}_{p}) - \widehat{R}^{-}_{p}(g; \mathcal{X}'_{p})| + |\widehat{R}^{-}_{u}(g; \mathcal{X}'_{u}) - \widehat{R}^{-}_{u}(g; \mathcal{X}'_{u})| \end{split}$$

where we employed  $|\max\{0,z\} - \max\{0,z'\}| \le |z-z'|$ . This decomposition results in

$$\mathbb{E}[\sup_{g \in \mathcal{G}} |\widehat{R}_{pu}(g) - \mathbb{E}[\widehat{R}_{pu}(g)]|] \leq \pi_{p} \mathbb{E}_{\mathcal{X}_{p}, \mathcal{X}_{p}'} [\sup_{g \in \mathcal{G}} |\widehat{R}_{p}^{+}(g; \mathcal{X}_{p}) - \widehat{R}_{p}^{+}(g; \mathcal{X}_{p}')|]$$

$$+ \pi_{p} \mathbb{E}_{\mathcal{X}_{p}, \mathcal{X}_{p}'} [\sup_{g \in \mathcal{G}} |\widehat{R}_{p}^{-}(g; \mathcal{X}_{p}) - \widehat{R}_{p}^{-}(g; \mathcal{X}_{p}')|]$$

$$+ \mathbb{E}_{\mathcal{X}_{p}, \mathcal{X}_{p}'} [\sup_{g \in \mathcal{G}} |\widehat{R}_{p}^{-}(g; \mathcal{X}_{u}) - \widehat{R}_{p}^{-}(g; \mathcal{X}_{p}')|].$$
(18)

Fourthly, we relax those expectations in (18) to Rademacher complexities. The original  $\ell$  may miss the origin, i.e.,  $\ell(0, y) \neq 0$ , with which we need to cope. Let

<span id="page-15-0"></span>
$$\tilde{\ell}(t,y) = \ell(t,y) - \ell(0,y)$$

be a *shifted loss* so that  $\tilde{\ell}(0,y)=0$ . Note that for all  $t,t'\in\mathbb{R}$  and  $y=\pm 1$ ,

$$\ell(t,y) - \ell(t',y) = \tilde{\ell}(t,y) - \tilde{\ell}(t',y).$$

Hence,

$$\begin{aligned} \widehat{R}_{p}^{+}(g; \mathcal{X}_{p}) - \widehat{R}_{p}^{+}(g; \mathcal{X}_{p}') &= (1/n_{p}) \sum_{x_{i} \in \mathcal{X}_{p}} \ell(g(x_{i}), +1) - (1/n_{p}) \sum_{x_{i}' \in \mathcal{X}_{p}'} \ell(g(x_{i}'), +1) \\ &= (1/n_{p}) \sum_{i=1}^{n_{p}} (\ell(g(x_{i}), +1) - \ell(g(x_{i}'), +1)) \\ &= (1/n_{p}) \sum_{i=1}^{n_{p}} (\tilde{\ell}(g(x_{i}), +1) - \tilde{\ell}(g(x_{i}'), +1)). \end{aligned}$$

This is already a standard form where we can attach Rademacher variables to every  $\tilde{\ell}(g(x_i), +1) - \tilde{\ell}(g(x_i'), +1)$ , and it is a routine work to show that

$$\mathbb{E}_{\mathcal{X}_{\mathsf{p}},\mathcal{X}_{\mathsf{p}}'}[\sup_{q\in\mathcal{G}}|\widehat{R}_{\mathsf{p}}^{+}(g;\mathcal{X}_{\mathsf{p}})-\widehat{R}_{\mathsf{p}}^{+}(g;\mathcal{X}_{\mathsf{p}}')|] \leq 2\mathfrak{R}_{n_{\mathsf{p}},p_{\mathsf{p}}}(\tilde{\ell}(\cdot,+1)\circ\mathcal{G}).$$

The other two expectations can be handled analogously. As a result, (18) can be reduced to

$$\mathbb{E}[\sup_{g \in \mathcal{G}} |\widetilde{R}_{pu}(g) - \mathbb{E}[\widetilde{R}_{pu}(g)]|] \leq 2\pi_{p} \mathfrak{R}'_{n_{p}, p_{p}}(\widetilde{\ell}(\cdot, +1) \circ \mathcal{G}) + 2\pi_{p} \mathfrak{R}'_{n_{p}, p_{p}}(\widetilde{\ell}(\cdot, -1) \circ \mathcal{G}) + 2\mathfrak{R}'_{n_{u}, p}(\widetilde{\ell}(\cdot, -1) \circ \mathcal{G}).$$
(19)

Finally, we transform the Rademacher complexities of composite function classes in (19) to those of the original function class. It is obvious that  $\tilde{\ell}$  shares the same Lipschitz constant  $L_{\ell}$  with  $\ell$ , and consequently

$$\mathfrak{R}'_{n_{\mathbf{p}},p_{\mathbf{p}}}(\tilde{\ell}(\cdot,+1)\circ\mathcal{G}) \leq 2L_{\ell}\mathfrak{R}'_{n_{\mathbf{p}},p_{\mathbf{p}}}(\mathcal{G}) = 2L_{\ell}\mathfrak{R}_{n_{\mathbf{p}},p_{\mathbf{p}}}(\mathcal{G}) 
\mathfrak{R}'_{n_{\mathbf{p}},p_{\mathbf{p}}}(\tilde{\ell}(\cdot,-1)\circ\mathcal{G}) \leq 2L_{\ell}\mathfrak{R}'_{n_{\mathbf{p}},p_{\mathbf{p}}}(\mathcal{G}) = 2L_{\ell}\mathfrak{R}_{n_{\mathbf{p}},p_{\mathbf{p}}}(\mathcal{G}) 
\mathfrak{R}'_{n_{\mathbf{p}},p}(\tilde{\ell}(\cdot,-1)\circ\mathcal{G}) \leq 2L_{\ell}\mathfrak{R}'_{n_{\mathbf{p}},p}(\mathcal{G}) = 2L_{\ell}\mathfrak{R}_{n_{\mathbf{p}},p}(\mathcal{G}),$$
(20)

<span id="page-16-1"></span><span id="page-16-0"></span>

where we used Talagrand's contraction lemma and the assumption that  $\mathcal{G}$  is closed under negation. Combining (16), (17), (19) and (20) finishes the proof of the uniform deviation bound (15).

#### **B.5** Proof of Theorem 4

Based on Lemma 5, the estimation error bound (13) is proven through

$$R(\widetilde{g}_{pu}) - R(g^*) = \left(\widetilde{R}_{pu}(\widetilde{g}_{pu}) - \widetilde{R}_{pu}(g^*)\right) + \left(R(\widetilde{g}_{pu}) - \widetilde{R}_{pu}(\widetilde{g}_{pu})\right) + \left(\widetilde{R}_{pu}(g^*) - R(g^*)\right)$$

$$\leq 0 + 2\sup_{g \in \mathcal{G}} |\widetilde{R}_{pu}(g) - R(g)|$$

$$\leq 16L_{\ell}\pi_{p}\mathfrak{R}_{n_{p},p_{p}}(\mathcal{G}) + 8L_{\ell}\mathfrak{R}_{n_{u},p}(\mathcal{G}) + 2C'_{\delta} \cdot \chi_{n_{p},n_{u}} + 2C_{\ell}\pi_{p}\Delta,$$

where  $\widetilde{R}_{\mathrm{pu}}(\widetilde{g}_{\mathrm{pu}}) \leq \widetilde{R}_{\mathrm{pu}}(g^*)$  by the definition of  $\widetilde{g}_{\mathrm{pu}}$ .