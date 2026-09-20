# HR RAG Evaluation & Trust Assurance

An end-to-end **Retrieval-Augmented Generation (RAG) evaluation project** focused on evaluating the reliability of an HR policy question-answering system.

The project goes beyond building a RAG pipeline. It evaluates individual components of the system—including **retrieval, context sufficiency, groundedness, retry behavior, answer relevance, and completeness**—and investigates how failures propagate across the pipeline.

A major focus is also **evaluator reliability**: testing whether LLM-based judges remain accurate and stable across boundary cases, repeated runs, and small context variations.

---

## Project Objective

The objective was to build and evaluate an HR-policy RAG system while answering several quality and trust questions:

* Did the retriever select the correct policy?
* Does the retrieved context actually contain enough information to answer the question?
* Does the generated answer remain grounded in the provided evidence?
* Can a stricter retry recover an initially ungrounded answer?
* Is the final answer relevant to the user's question?
* Is the answer sufficiently complete?
* Are LLM-based evaluators themselves reliable and stable?
* Do evaluation changes improve the system without causing regressions elsewhere?

The evaluation framework therefore treats the RAG system as a collection of separately measurable components rather than evaluating only the final answer.

---

## System Architecture

```text
User Question
      |
      v
Semantic Retrieval
      |
      v
CrossEncoder Reranking
      |
      v
Context Sufficiency Gate
      |
      +---- INSUFFICIENT ----> Abstain
      |
      v
Answer Generation
      |
      v
Groundedness Evaluation
      |
      +---- FAIL ----> Strict Retry Generation
      |                        |
      |                        v
      |                Groundedness Re-check
      |
      v
Final Answer
      |
      v
Relevance + Completeness Evaluation
```

---

## Evaluation Pipeline

### 1. Retrieval Evaluation

The retrieval system evolved through multiple stages:

* Keyword-based retrieval baseline
* Semantic embeddings
* Cosine-similarity retrieval
* Top-k retrieval
* CrossEncoder reranking
* Retrieval diagnostics
* Confidence and ranking-margin analysis
* Holdout evaluation

Semantic retrieval uses `all-MiniLM-L6-v2` sentence embeddings.

A CrossEncoder reranker was also evaluated using:

`cross-encoder/ms-marco-MiniLM-L6-v2`

An important finding was that the more sophisticated reranker did **not automatically improve task performance**.

On expected-policy cases:

| Retrieval Method         | Accuracy |
| ------------------------ | -------: |
| Embedding-only retrieval |   96.15% |
| Reranked retrieval       |   88.46% |

The reranker corrected some errors but introduced others, demonstrating why retrieval components should be evaluated empirically rather than assumed to improve performance.

---

### 2. Context Sufficiency Evaluation

Correct retrieval does not necessarily mean the retrieved context contains enough information to answer the user's question.

A dedicated **context sufficiency judge** therefore determines whether generation should proceed.

The system classifies context as:

```text
SUFFICIENT
```

or:

```text
INSUFFICIENT
```

If context is insufficient, the pipeline abstains rather than generating an unsupported answer.

The evaluation included:

* normal questions
* paraphrases
* insufficient-context questions
* out-of-scope questions
* conflicting cues
* irrelevant background information
* material conditions
* conditional questions
* unstated exclusions

For evaluation purposes, **INSUFFICIENT** was treated as the positive class because identifying cases where generation should be blocked is an important safety behavior.

---

## Sufficiency Metrics

In the documented 31-case benchmark run:

| Metric                         | Result |
| ------------------------------ | -----: |
| Sufficiency Accuracy           | 96.77% |
| Insufficient-Context Precision | 93.75% |
| Insufficient-Context Recall    |   100% |
| False Negatives                |      0 |

The confusion matrix was tracked explicitly rather than relying only on aggregate accuracy.

Because sufficiency is evaluated using an LLM judge, repeated runs showed variability on semantic boundary cases. Judge stability and regression behavior were therefore evaluated separately rather than assuming a single run represented deterministic performance.

---

## LLM Judge Stability Testing

One of the most important findings was that an LLM evaluator can itself become a source of uncertainty.

The project therefore evaluated the **judge as another model under test**.

Testing included:

* repeated identical judgments
* stability measurements
* context perturbation tests
* boundary-condition tests
* prompt/rubric experiments
* regression testing

For one difficult material-condition case, identical evaluations produced both `SUFFICIENT` and `INSUFFICIENT` decisions across repeated runs.

This demonstrated that a single evaluation result can hide **judge instability**, even when generation temperature is set to zero.

---

## Boundary and Adversarial Evaluation

The evaluation dataset intentionally included cases designed to expose weaknesses that normal questions may not reveal.

### Material Conditions

A question may introduce a condition not addressed by the retrieved policy.

Example:

```text
If I have unused annual leave, can I work remotely
two days per week with manager approval?
```

The Remote Work policy describes remote-work conditions but does not establish whether unused annual leave changes eligibility.

This tests whether the sufficiency judge notices the unsupported material condition.

### Irrelevant Background

Example:

```text
I currently work remotely.
How many weeks of paid parental leave are eligible employees entitled to?
```

The remote-work statement should not prevent the system from answering a parental-leave question when the relevant context is sufficient.

### Unstated Exclusions

Example:

```text
Can the company reimburse my personal vacation expenses?
```

The available policy describes **business expense claims**, but does not explicitly establish the treatment of personal vacation expenses.

This case was useful for testing both sufficiency and groundedness.

### Out-of-Scope Questions

Out-of-scope cases were included to test what happens when semantic retrieval still returns the nearest available policy even though no policy actually answers the question.

The downstream sufficiency gate acts as an important protection against this behavior.

---

## Groundedness Evaluation

Generated answers were evaluated for whether their **material claims were supported by the retrieved context**.

A major distinction identified during evaluation was:

> A plausible inference is not necessarily a grounded claim.

For example, a model may infer that personal vacation expenses are not reimbursable because the policy discusses business expenses.

That may sound reasonable, but the retrieved policy does not necessarily establish that exclusion.

The groundedness evaluator is therefore intended to detect unsupported extensions beyond the provided evidence.

---

## Retry Strategy

When the first generated answer fails groundedness evaluation, the pipeline performs a stricter retry.

The retry generator is instructed to remain tightly constrained to the retrieved context.

The regenerated answer is then evaluated again before being accepted.

In the documented benchmark run:

| Metric                  | Result |
| ----------------------- | -----: |
| First-Pass Groundedness | 93.33% |
| Retry Usage             |  6.67% |
| Retry Recovery          |   100% |

This allows groundedness failures to be measured separately from the effectiveness of the recovery mechanism.

---

## Answer Quality Evaluation

Groundedness alone does not guarantee that an answer is useful.

The project therefore evaluates two additional dimensions.

### Relevance

Does the answer actually address the user's question?

### Completeness

Does the answer contain the material information needed to answer the question?

Controlled evaluator tests included:

```text
Good answer
Relevance: PASS
Completeness: PASS
```

```text
Wrong-focus answer
Relevance: FAIL
Completeness: FAIL
```

```text
Relevant but incomplete answer
Relevance: PASS
Completeness: FAIL
```

This separation prevents different failure types from being collapsed into a single generic quality score.

---

## Final End-to-End Evaluation

The documented benchmark contained **31 evaluation cases** across multiple slices.

| Metric                         | Result |
| ------------------------------ | -----: |
| Retrieval Accuracy             | 74.19% |
| Sufficiency Accuracy           | 96.77% |
| First-Pass Groundedness        | 93.33% |
| Retry Usage                    |  6.67% |
| Retry Recovery                 |   100% |
| Answer Relevance               |   100% |
| Answer Completeness            |   100% |
| Insufficient-Context Precision | 93.75% |
| Insufficient-Context Recall    |   100% |

These values represent a documented benchmark run rather than a claim of deterministic performance across every repeated LLM-judge execution.

### Slice Analysis

| Category                       | Retrieval Accuracy | Sufficiency Accuracy |
| ------------------------------ | -----------------: | -------------------: |
| Normal                         |               100% |                 100% |
| Paraphrase                     |               100% |                  80% |
| Insufficient                   |                75% |                 100% |
| Out-of-Scope                   |                 0% |                 100% |
| Conflicting Cue / Insufficient |                50% |                 100% |
| Irrelevant Background          |               100% |                 100% |
| Material Condition Supported   |               100% |                 100% |
| Material Condition Unsupported |               100% |                 100% |
| Conditional                    |               100% |                 100% |

The low retrieval accuracy on out-of-scope questions reflects the behavior of nearest-neighbor retrieval: a candidate can still be returned when no correct policy exists.

The sufficiency layer successfully blocked those cases in the documented benchmark run.

---

## Regression Testing

Evaluation changes were not accepted simply because they fixed one failing example.

After modifying judge prompts or evaluation rubrics, focused regression tests were used to check whether previously working cases had degraded.

During experimentation, stricter sufficiency prompts sometimes improved difficult unsupported-condition cases while causing valid conditional or irrelevant-background questions to fail.

Those regressions were treated as evidence against the modification.

This led to an important evaluation principle used throughout the project:

> Optimize system-level behavior, not individual test cases.

The project also used repeated evaluation and restoration of earlier code states to distinguish actual code regressions from variability introduced by LLM-based judges.

---

## Key Findings

### More sophisticated retrieval is not automatically better

CrossEncoder reranking introduced regressions despite being a more advanced retrieval component.

### Correct retrieval does not guarantee sufficient evidence

Retrieval correctness and context sufficiency need separate evaluation.

### Plausibility is different from groundedness

An answer can sound logically reasonable while extending beyond what the supplied evidence supports.

### LLM judges must also be evaluated

LLM-as-a-judge systems can show instability and boundary sensitivity.

### Aggregate metrics are not enough

Slice analysis exposed failure patterns hidden by overall accuracy.

### Regression testing matters

A prompt adjustment that fixes one case can silently break several previously correct cases.

### Abstention is a useful RAG behavior

When evidence is insufficient, refusing to generate can be more reliable than forcing an answer.

---

## Skills Demonstrated

* RAG evaluation and failure analysis
* LLM response evaluation
* Semantic retrieval and embedding-based search
* Cosine similarity and top-k retrieval
* CrossEncoder reranking
* Retrieval diagnostics and holdout testing
* Context sufficiency evaluation
* Groundedness and hallucination analysis
* LLM-as-a-judge evaluation
* Answer relevance and completeness evaluation
* Confusion matrices, precision, recall, and accuracy
* Slice-based evaluation
* Boundary and adversarial test design
* LLM judge stability testing
* Context perturbation testing
* Regression testing
* Prompt and evaluation-rubric refinement
* Safe abstention for insufficient context
* Retry and recovery evaluation
* Python-based evaluation pipelines

---

## Technology Stack

* Python
* SentenceTransformers
* `all-MiniLM-L6-v2`
* CrossEncoder
* `cross-encoder/ms-marco-MiniLM-L6-v2`
* scikit-learn
* NumPy
* Groq API
* LLM-based evaluation
* VS Code

---

## Repository Structure

Key files include:

| File                            | Purpose                                  |
| ------------------------------- | ---------------------------------------- |
| `rag_pipeline.py`               | End-to-end RAG pipeline orchestration    |
| `semantic_retriever.py`         | Embedding-based semantic retrieval       |
| `reranker.py`                   | CrossEncoder reranking                   |
| `context_judge.py`              | Context sufficiency evaluation           |
| `generator.py`                  | Context-based answer generation          |
| `strict_generator.py`           | Stricter retry generation                |
| `groundedness_judge.py`         | Groundedness evaluation                  |
| `answer_quality_judge.py`       | Relevance and completeness evaluation    |
| `evaluation_data.py`            | Evaluation dataset and expected outcomes |
| `evaluation_runner1.py`         | End-to-end evaluation harness            |
| `retrieval_diagnostics.py`      | Retrieval failure analysis               |
| `retrieval_holdout.py`          | Holdout retrieval testing                |
| `sufficiency_stability_test.py` | Repeated judge stability evaluation      |
| `sufficiency_boundary_test.py`  | Sufficiency boundary-case testing        |
| `sufficiency_rubric_test.py`    | Judge rubric and regression evaluation   |

Additional scripts contain focused experiments and diagnostics used during development.

---

## Limitations

This is a controlled personal evaluation project using a small synthetic HR policy knowledge base and a limited evaluation dataset.

The reported metrics represent performance on this project's test suite and **should not be interpreted as production-level or general RAG performance guarantees**.

The project also identified run-to-run variability in LLM-based sufficiency judgments, particularly around semantic boundary cases. For that reason, evaluator stability and regression behavior are treated as part of the evaluation problem itself.

The project prioritizes evaluation methodology, failure analysis, and diagnostic reasoning over maximizing a single benchmark score.

---

## About the Project

This project was developed as a practical exploration of **AI Evaluation, RAG Quality Assurance, and AI Trust Assurance**.

The primary goal was not simply to maximize a benchmark score, but to understand:

* where RAG systems fail,
* how those failures can be measured,
* whether evaluation mechanisms themselves are reliable,
* how failures propagate across pipeline stages,
* and how safeguards behave under difficult or ambiguous inputs.
