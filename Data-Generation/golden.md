# Generate Synthetic Test Data for LLM Applications (/guides/guides-using-synthesizer)





Manually curating test data can be time-consuming and often causes critical edge cases to be overlooked. With DeepEval's Synthesizer, you can quickly generate thousands of **high-quality synthetic goldens** in just minutes.

<Callout type="info">
  A `Golden` in DeepEval is similar to an `LLMTestCase`, but does not require an `actual_output` and `retrieval_context` at initialization. Learn more about Goldens in DeepEval [here](/docs/evaluation-datasets#create-an-evaluation-dataset).
</Callout>

This guide will show you how to best utilize the `Synthesizer` to create **synthetic goldens** that fit your use case, including:

* Customizing document chunking
* Managing golden complexity through evolutions
* Quality assuring generated synthetic goldens

### Key Steps in Data Synthetic Generation [#key-steps-in-data-synthetic-generation]

DeepEval leverages your knowledge base to create contexts, from which relevant and accurate synthetic goldens are generated. To begin, simply initialize the `Synthesizer` and provide a list of document paths that represent your knowledge base:

```python
from deepeval.synthesizer import Synthesizer

synthesizer = Synthesizer()
synthesizer.generate_goldens_from_docs(
    document_paths=['example.txt', 'example.docx', 'example.pdf',  'example.md', 'example.markdown', 'example.mdx'],
)
```

The `generate_goldens_from_docs` function follows several key steps to transform your documents into high-quality goldens:

1. **Document Loading**: Load and process your knowledge base documents for chunking.
2. **Document Chunking**: Split the documents into smaller, manageable chunks
3. **Context Generation**: Group similar chunks (using cosine similarity) to create meaningful
4. **Golden Generation**: Generate synthetic goldens from the created contexts.
5. **Evolution**: Evolve the synthetic goldens to increase complexity and capture edge cases.

<div
  style="{
  display: &#x22;flex&#x22;,
  alignItems: &#x22;center&#x22;,
  justifyContent: &#x22;center&#x22;,
}"
>
  <ImageDisplayer src="ASSETS.synthesizerOverview" alt="LangChain" />
</div>

Alternatively, if you already have pre-prepared contexts, you can generate goldens directly, skipping the first three steps:

```python
from deepeval.synthesizer import Synthesizer

synthesizer = Synthesizer()
synthesizer.generate_goldens_from_contexts(
    contexts=[
        ["The Earth revolves around the Sun.", "Planets are celestial bodies."],
        ["Water freezes at 0 degrees Celsius.", "The chemical formula for water is H2O."],
    ]
)
```

## Document Chunking [#document-chunking]

In DeepEval, documents are divided into **fixed-size chunks**, which are then used to generate contexts for your goldens. This chunking process is critical because it directly influences the quality of the contexts, which are used to generate synthetic goldens. You can control this process using the following parameters:

* `chunk_size`: Defines the size of each chunk in tokens. Default is 1024.
* `chunk_overlap`: Specifies the number of overlapping tokens between consecutive chunks. Default is 0 (no overlap).
* `max_contexts_per_document`: The maximum number of contexts generated per document. Default is 3.

<Callout type="note">
  DeepEval uses a token-based splitter, meaning that `chunk_size` and `chunk_overlap` are measured in tokens, not characters.
</Callout>

```python
from deepeval.synthesizer import Synthesizer

synthesizer = Synthesizer()
synthesizer.generate_goldens_from_docs(
    document_paths=['example.txt', 'example.docx', 'example.pdf',  'example.md', 'example.markdown', 'example.mdx'],
    chunk_size=1024,
    chunk_overlap=0
)
```

It's crucial to match the `chunk_size` and `chunk_overlap` settings to the characteristics of your knowledge base and the retriever being used. These chunks will form the context for your synthetic goldens, so proper alignment ensures that your generated test cases are reflective of real-world scenarios.

### Best Practices for Chunking [#best-practices-for-chunking]

1. **Impact on Retrieval:** The chunk size and overlap should ideally align with the settings of the retriever in your LLM pipeline. If your retriever expects smaller or larger chunks for efficient retrieval, adjust the chunking accordingly to prevent mismatch in how context is presented during the golden generation.
2. **Balance Between Chunk Size and Overlap:** For documents with interconnected content, a small overlap (e.g., 50-100 tokens) can ensure that key information isn't cut off between chunks. However, for long-form documents or those with distinct sections, a larger chunk size with minimal overlap might be more efficient.
3. **Consider Document Structure:** If your documents have natural breaks (e.g., chapters, sections, or headings), ensure your chunk size doesn't disrupt those. Customizing chunking for structured documents can improve the quality of the synthetic goldens by preserving context.

<Callout type="caution">
  If `chunk_size` is set too large or `chunk_overlap` too small for shorter documents, the synthesizer may raise an error. This occurs because the document must generate enough chunks to meet the `max_contexts_per_document` requirement.
</Callout>

To validate your chunking settings, calculate the number of chunks per document using the following formula:

<Equation formula="\text{Number of Chunks} = \left\lceil \frac{\text{Document Length} - \text{chunk\_overlap}}{\text{chunk\_size} - \text{chunk\_overlap}} \right\rceil" />

### Maximizing Coverage [#maximizing-coverage]

The maximum number of goldens generated is determined by multiplying `max_contexts_per_document` by `max_goldens_per_context`.

<Callout type="tip">
  It's generally more efficient to increase `max_contexts_per_document` to enhance coverage across different sections of your documents, especially when dealing with large datasets or varied knowledge bases. This provides broader insights into your LLM's performance across a wider range of scenarios, which is crucial for thorough testing, particularly if computational resources are limited.
</Callout>

## Evolutions [#evolutions]

The synthesizer increases the complexity of synthetic data by evolving the input through various methods. Each input can undergo multiple evolutions, which are applied randomly. However, you can control how these evolutions are sampled by adjusting the following parameters:

* `evolutions`: A dictionary specifying the distribution of evolution methods to be used.
* `num_evolutions`: The number of evolution steps to apply to each generated input.

<Callout type="info">
  **Data evolution** was originally introduced by the developers of [Evol-Instruct and WizardML.](https://arxiv.org/abs/2304.12244). For those interested, here is a [great article](https://www.confident-ai.com/blog/the-definitive-guide-to-synthetic-data-generation-using-llms) on how `deepeval`'s synthesizer was built.
</Callout>

```python
from deepeval.synthesizer import Synthesizer

synthesizer = Synthesizer()
synthesizer.generate_goldens_from_docs(
    document_paths=['example.txt', 'example.docx', 'example.pdf',  'example.md', 'example.markdown', 'example.mdx'],
    num_evolutions=3,
    evolutions={
        Evolution.REASONING: 0.1,
        Evolution.MULTICONTEXT: 0.1,
        Evolution.CONCRETIZING: 0.1,
        Evolution.CONSTRAINED: 0.1,
        Evolution.COMPARATIVE: 0.1,
        Evolution.HYPOTHETICAL: 0.1,
        Evolution.IN_BREADTH: 0.4,
    }
)
```

DeepEval offers 7 types of evolutions: reasoning, multicontext, concretizing, constrained, comparative, hypothetical, and in-breadth evolutions.

* **Reasoning:** Evolves the input to require multi-step logical thinking.
* **Multicontext:** Ensures that all relevant information from the context is utilized.
* **Concretizing:** Makes abstract ideas more concrete and detailed.
* **Constrained:** Introduces a condition or restriction, testing the model's ability to operate within specific limits.
* **Comparative:** Requires a response that involves a comparison between options or contexts.
* **Hypothetical:** Forces the model to consider and respond to a hypothetical scenario.
* **In-breadth:** Broadens the input to touch on related or adjacent topics.

<Callout type="tip">
  While the other evolutions increase input complexity and test an LLM's ability to reason and respond to more challenging queries, in-breadth focuses on broadening coverage. Think of in-breadth as **horizontal expansion**, and the other evolutions as **vertical complexity**.
</Callout>

### Best Practices for Using Evolutions [#best-practices-for-using-evolutions]

To maximize the effectiveness of evolutions in your testing process, consider the following best practices:

1. **Align Evolutions with Testing Goals**: Choose evolutions based on what you're trying to evaluate. For reasoning or logic tests, prioritize evolutions like Reasoning and Comparative. For broader domain testing, increase the use of In-breadth evolutions.

2. **Balance Complexity and Coverage**: Use a mix of vertical complexity (e.g., Reasoning, Constrained) and horizontal expansion (e.g., In-breadth) to ensure a comprehensive evaluation of both deep reasoning and a broad range of topics.

3. **Start Small, Then Scale**: Begin with a smaller number of evolution steps (`num_evolutions`) and gradually increase complexity. This helps you control the challenge level without generating overly complex goldens.

4. **Target Edge Cases for Stress Testing**: To uncover edge cases, increase the use of Constrained and Hypothetical evolutions. These evolutions are ideal for testing your model under restrictive or unusual conditions.

5. **Monitor Evolution Distribution**: Regularly check the distribution of evolutions to avoid overloading test data with any single type. Maintain a balanced distribution unless you're focusing on a specific evaluation area.

### Accessing Evolutions [#accessing-evolutions]

You can access evolutions either from the DataFrame generated by the synthesizer or directly from the metadata of each golden:

```python
from deepeval.synthesizer import Synthesizer

# Generate goldens from documents
goldens = synthesizer.generate_goldens_from_docs(
  document_paths=['example.txt', 'example.docx', 'example.pdf',  'example.md', 'example.markdown', 'example.mdx'],
)

# Access evolutions through the DataFrame
goldens_dataframe = synthesizer.to_pandas()
goldens_dataframe.head()

# Access evolutions directly from a specific golden
goldens[0].additional_metadata["evolutions"]
```

## Qualifying Synthetic Goldens [#qualifying-synthetic-goldens]

Generating synthetic goldens can introduce noise, so it's essential to qualify and filter out low-quality goldens from the final dataset. Qualification occurs at three key stages in the synthesis process.

### Context Filtering [#context-filtering]

The first two qualification steps happen during **context generation**. Each chunk is randomly sampled for each context and scored based on the following criteria:

* **Clarity:** How clear and understandable the information is.
* **Depth:** The level of detail and insight provided.
* **Structure:** How well-organized and logical the content is.
* **Relevance:** How closely the content relates to the main topic.

<Callout type="note">
  Scores range from 0 to 1. To pass, a chunk must achieve an average score of at least 0.5. A maximum of 3 retries is allowed for each chunk if it initially fails.
</Callout>

Additional chunks are sampled using a cosine similarity threshold of 0.5 to form the final context, ensuring that only high-quality chunks are included in the context.

### Synthetic Input Filtering [#synthetic-input-filtering]

In the next stage, **synthetic inputs** are generated from the goldens. These inputs are evaluated and scored based on:

* **Self-containment**: The query is understandable and complete without needing additional external context or references.
* **Clarity**: The query clearly conveys its intent, specifying the requested information or action without ambiguity.

<Callout type="info">
  Similar to context filtering, these inputs are scored on a scale of 0 to 1, with a minimum passing threshold. Each input is allowed up to 3 retries if it doesn't meet the quality criteria.
</Callout>

### Accessing Quality Scores [#accessing-quality-scores]

You can access the quality scores from the synthesized goldens using the DataFrame or directly from each golden.

```python
from deepeval.synthesizer import Synthesizer

# Generate goldens from documents
goldens = synthesizer.generate_goldens_from_docs(
  document_paths=['example.txt', 'example.docx', 'example.pdf',  'example.md', 'example.markdown', 'example.mdx'],
)

# Access quality scores through the DataFrame
goldens_dataframe = synthesizer.to_pandas()
goldens_dataframe.head()

# Access quality scores directly from a specific golden
goldens[0].additional_metadata["synthetic_input_quality"]
goldens[0].additional_metadata["context_quality"]
```

## FAQs [#faqs]

<FAQs
  qas="[
  {
    question: &#x22;What is the DeepEval `Synthesizer`?&#x22;,
    answer: (
      <>
        The <code>Synthesizer</code> is DeepEval's tool for generating
        high-quality synthetic <code>Golden</code>s from your knowledge base.
        It chunks documents, builds contexts, generates input-output pairs,
        and evolves them into harder edge cases—producing thousands of test
        cases in minutes.
      </>
    ),
  },
  {
    question: &#x22;What is the difference between a Golden and an `LLMTestCase`?&#x22;,
    answer: (
      <>
        A <code>Golden</code> is similar to an <code>LLMTestCase</code> but
        doesn't require <code>actual_output</code> or{&#x22; &#x22;}
        <code>retrieval_context</code> at initialization. You generate
        goldens ahead of time, then run your application against them at
        evaluation time to fill in the actual outputs.
      </>
    ),
  },
  {
    question: &#x22;How does the `Synthesizer` generate goldens from documents?&#x22;,
    answer: (
      <>
        It loads your documents, chunks them, groups similar chunks into
        contexts using cosine similarity, generates synthetic goldens from
        each context, and finally evolves them to introduce complexity and
        edge cases. The whole pipeline runs from a single call to{&#x22; &#x22;}
        <code>generate_goldens_from_docs</code>.
      </>
    ),
  },
  {
    question: &#x22;What are evolutions in DeepEval?&#x22;,
    answer:
      &#x22;Evolutions are transformations applied to synthetic goldens to make them harder—rewriting them to be more reasoning-heavy, multi-step, comparative, or hypothetical. Evolutions surface edge cases that simple seed prompts won't trigger.&#x22;,
  },
  {
    question: &#x22;How does DeepEval qualify synthetic data quality?&#x22;,
    answer:
      &#x22;The Synthesizer scores both contexts and synthetic inputs at generation time. Contexts are judged on clarity, depth, structure, and relevance. Inputs are judged on self-containment and clarity. Each must clear a 0.5 threshold (with up to 3 retries) before being kept.&#x22;,
  },
  {
    question: &#x22;Can I generate goldens without documents?&#x22;,
    answer: (
      <>
        Yes. Pass your own contexts directly to{&#x22; &#x22;}
        <code>generate_goldens_from_contexts</code> to skip document loading,
        chunking, and context generation. This is useful when you've already
        curated the contexts you want to test against.
      </>
    ),
  },
  {
    question: &#x22;How do I access quality scores for synthetic goldens?&#x22;,
    answer: (
      <>
        Either via <code>synthesizer.to_pandas()</code> for a DataFrame view,
        or directly on each golden through{&#x22; &#x22;}
        <code>golden.additional_metadata[&#x22;context_quality&#x22;]</code> and{&#x22; &#x22;}
        <code>[&#x22;synthetic_input_quality&#x22;]</code>. Use these to filter
        low-quality goldens out of your final dataset.
      </>
    ),
  },
]"
/>

# Golden Synthesizer (/docs/golden-synthesizer)





`deepeval`'s `Synthesizer` offers a fast and easy way to generate high-quality **single and multi-turn goldens** for your evaluation datasets in just a few lines of code. This is especially helpful if:

* You don't have an evaluation dataset to start with
* You have a small dataset and wish to augment it with existing examples
* You have a knowledge base and want to create a dataset out of it

<Callout type="note">
  For single-turn generations, note that `deepeval`'s `Synthesizer` does **NOT** generate `actual_output`s for each golden. This is because `actual_output`s are meant to be generated by your LLM (application), not `deepeval`'s synthesizer.

  For multi-turn generations, `deepeval`'s `Synthesizer` also does not generation `turns`. Instead, you should go to the [`ConversationSimulator`](/docs/conversation-simulator) instead for the simulation of `turns`.
</Callout>

<details>
  <summary>
    Should you generate synthetic datasets?
  </summary>

  Synthesizing evaluation data is especially helpful if you don't have a prepared evaluation dataset, as it will **help you generate the initiate testing data you need** to get up and running with evaluation.

  However, you should aim to manually inspect and edit any synthetic data where possible.
</details>

## Quick Summary [#quick-summary]

The `Synthesizer` uses an LLM to first generate a series of inputs/scenarios, before evolving them to become more complex and realistic. These evolved inputs/scenarios are then used to create a list of synthetic goldens, which can be single or multi-turn and makes up your synthetic `EvaluationDataset`.

To begin generating goldens, paste in the following code:

<Tabs items="[&#x22;Single-Turn&#x22;, &#x22;Multi-Turn&#x22;]">
  <Tab value="Single-Turn">
    ```python title="main.py"
    from deepeval.synthesizer import Synthesizer

    synthesizer = Synthesizer()
    goldens = synthesizer.generate_goldens_from_docs(
        document_paths=['example.txt'], # Replace with your file
        include_expected_output=True
    )
    print(goldens)
    ```
  </Tab>

  <Tab value="Multi-Turn">
    ```python title="main.py"
    from deepeval.synthesizer import Synthesizer

    synthesizer = Synthesizer()
    conversational_goldens = synthesizer.generate_conversational_goldens_from_docs(
        document_paths=['example.txt'], # Replace with your file
        include_expected_outcome=True
    )
    print(conversational_goldens)
    ```
  </Tab>
</Tabs>

```bash
python main.py
```

Congratulations 🎉🥳! You've just generated your first set of synthetic goldens.

<Callout type="info">
  `deepeval`'s `Synthesizer` uses the data evolution method to generate large volumes of data across various complexity levels to make synthetic data more realistic. This method was originally introduced by the developers of [Evol-Instruct and WizardML.](https://arxiv.org/abs/2304.12244)

  For those interested, here is a [great article on how `deepeval`'s synthesizer was built.](https://www.confident-ai.com/blog/the-definitive-guide-to-synthetic-data-generation-using-llms)
</Callout>

## Create Your First Synthesizer [#create-your-first-synthesizer]

To start generating goldens for your `EvaluationDataset`, begin by creating a `Synthesizer` object:

```python
from deepeval.synthesizer import Synthesizer

synthesizer = Synthesizer()
```

There are **EIGHT** optional parameters when creating a `Synthesizer`:

* \[Optional] `async_mode`: a boolean which when set to `True`, enables **concurrent generation of goldens**. Defaulted to `True`.
* \[Optional] `model`: a string specifying which of OpenAI's GPT models to use for generation, **OR** [any custom LLM model](/docs/metrics-introduction#using-a-custom-llm) of type `DeepEvalBaseLLM`. Defaulted to <DefaultLLMModel />.
* \[Optional] `max_concurrent`: an integer that determines the maximum number of goldens that can be generated in parallel at any point in time. You can decrease this value if you're running into rate limit errors. Defaulted to `100`.
* \[Optional] `filtration_config`: an instance of type `FiltrationConfig` that allows you to [customize the degree of which goldens are filtered](#filtration-quality) during generation. Defaulted to the default `FiltrationConfig` values.
* \[Optional] `evolution_config`: an instance of type `EvolutionConfig` that allows you to [customize the complexity of evolutions applied](#evolution-complexity) during generation. Defaulted to the default `EvolutionConfig` values.
* \[Optional] `styling_config`: an instance of type `StylingConfig` that allows you to [customize the styles and formats](#styling-options) of **single-turn** generations. Defaulted to the default `StylingConfig` values.
* \[Optional] `conversational_styling_config`: an instance of type `ConversationalStylingConfig` that allows you to [customize the styles and formats](#styling-options) of **multi-turn** generations. Defaulted to the default `ConversationalStylingConfig` values.
* \[Optional] `cost_tracking`: a boolean which when set to `True`, will print the cost incurred by your LLM during golden synthesization.

<Callout type="note">
  The `filtration_config`, `evolution_config`, `styling_config`, and `conversational_styling_config` parameters allow you to customize the goldens being generated by your `Synthesizer`.

  In addition, the `model` for your `Synthesizer` will automatically be used for the `critic_model`s of the [`FiltrationConfig`](#filtration-quality) and [`ContextConstructionConfig`](/docs/synthesizer-generate-from-docs#customize-context-construction) **if the respective custom config instances are not provided**.
</Callout>

## Generate Your First Golden [#generate-your-first-golden]

Once you've created a `Synthesizer` object with the desired filtering parameters and models, you can begin generating goldens.

<Tabs items="[&#x22;Single-Turn&#x22;, &#x22;Multi-Turn&#x22;]">
  <Tab value="Single-Turn">
    ```python
    from deepeval.synthesizer import Synthesizer

    synthesizer = Synthesizer()
    goldens = synthesizer.generate_goldens_from_docs(
        document_paths=['example.txt', 'example.docx', 'example.pdf', 'example.md', 'example.markdown', 'example.mdx'],
        include_expected_output=True
    )
    print(goldens)
    ```

    In this example, we've used the `generate_goldens_from_docs` and `generate_conversational_goldens_from_docs` methods, which are two of the four generation methods offered by `deepeval`'s `Synthesizer`. The four methods include:

    * [`generate_goldens_from_docs()`](/docs/synthesizer-generate-from-docs): useful for generating goldens to evaluate your LLM application based on contexts extracted from your knowledge base in the form of documents.
    * [`generate_goldens_from_contexts()`](/docs/synthesizer-generate-from-contexts): useful for generating goldens to evaluate your LLM application based on a list of prepared context.
    * [`generate_goldens_from_scratch()`](/docs/synthesizer-generate-from-scratch): useful for generating goldens to evaluate your LLM application without relying on contexts from a knowledge base.
    * [`generate_goldens_from_goldens()`](/docs/synthesizer-generate-from-goldens): useful for generating goldens by augmenting a known set of goldens.

    <Callout type="tip">
      You might have noticed the `generate_goldens_from_docs()` is a superset of `generate_goldens_from_contexts()`, and `generate_goldens_from_contexts()` is a superset of `generate_goldens_from_scratch()`.

      This implies that if you want more control over context extraction, you should use `generate_goldens_from_contexts()`, but if you want `deepeval` to take care of context extraction as well, use `generate_goldens_from_docs()`.
    </Callout>
  </Tab>

  <Tab value="Multi-Turn">
    ```python
    from deepeval.synthesizer import Synthesizer

    synthesizer = Synthesizer()
    conversational_goldens = synthesizer.generate_conversational_goldens_from_docs(
        document_paths=['example.txt', 'example.docx', 'example.pdf', 'example.md', 'example.markdown', 'example.mdx'],
        include_expected_outcome=True
    )
    print(conversational_goldens)
    ```

    In this example, we've used the `generate_goldens_from_docs` and `generate_conversational_goldens_from_docs` methods, which are two of the four generation methods offered by `deepeval`'s `Synthesizer`. The four methods include:

    * [`generate_conversational_goldens_from_docs()`](/docs/synthesizer-generate-from-docs): useful for generating goldens to evaluate your LLM application based on contexts extracted from your knowledge base in the form of documents.
    * [`generate_conversational_goldens_from_contexts()`](/docs/synthesizer-generate-from-contexts): useful for generating goldens to evaluate your LLM application based on a list of prepared context.
    * [`generate_conversational_goldens_from_scratch()`](/docs/synthesizer-generate-from-scratch): useful for generating goldens to evaluate your LLM application without relying on contexts from a knowledge base.
    * [`generate_conversational_goldens_from_goldens()`](/docs/synthesizer-generate-from-goldens): useful for generating goldens by augmenting a known set of goldens.

    <Callout type="tip">
      You might have noticed the `generate_conversational_goldens_from_docs()` is a superset of `generate_conversational_goldens_from_contexts()`, and `generate_conversational_goldens_from_contexts()` is a superset of `generate_conversational_goldens_from_scratch()`.

      This implies that if you want more control over context extraction, you should use `generate_conversational_goldens_from_contexts()`, but if you want `deepeval` to take care of context extraction as well, use `generate_conversational_goldens_from_docs()`.
    </Callout>
  </Tab>
</Tabs>

Once generation is complete, you can also convert your synthetically generated goldens into a DataFrame:

```python
dataframe = synthesizer.to_pandas()
print(dataframe)
```

Here's an example of what the resulting DataFrame might look like for a single-turn generation:

| <div style="{width: &#x22;200px&#x22;}">input</div> | actual\_output | expected\_output | <div style="{width: &#x22;280px&#x22;}">context</div>                   | retrieval\_context | n\_chunks\_per\_context | context\_length | context\_quality | synthetic\_input\_quality | evolutions | source\_file |
| --------------------------------------------------- | -------------- | ---------------- | ----------------------------------------------------------------------- | ------------------ | ----------------------- | --------------- | ---------------- | ------------------------- | ---------- | ------------ |
| Who wrote the novel "1984"?                         | None           | George Orwell    | `["1984 is a dystopian novel published in 1949 by George Orwell."]`     | None               | 1                       | 60              | 0.5              | 0.6                       | None       | file1.txt    |
| What is the boiling point of water in Celsius?      | None           | 100°C            | `["Water boils at 100°C (212°F) under standard atmospheric pressure."]` | None               | 1                       | 55              | 0.4              | 0.9                       | None       | file2.txt    |
| ...                                                 | ...            | ...              | ...                                                                     | ...                | ...                     | ...             | ...              | ...                       | ...        | ...          |

And that's it! You now have access to a list of synthetic goldens generated using information from your knowledge base.

## Save Your Synthetic Dataset [#save-your-synthetic-dataset]

<Tabs items="[&#x22;Confident AI&#x22;, &#x22;Locally&#x22;]">
  <Tab value="Confident AI">
    To avoid losing any generated synthetic `Goldens`, you can push a dataset containing the generated goldens to Confident AI:

    ```python
    from deepeval.dataset import EvaluationDataset
    ...

    dataset = EvaluationDataset(goldens=synthesizer.synthetic_goldens)
    dataset.push(alias="My Generated Dataset")
    ```

    This keeps your dataset on the cloud and you'll be able to edit and version control it in one place. When you are ready to evaluate your LLM application using the generated goldens, simply pull the dataset from the cloud like how you would pull a GitHub repo:

    ```python
    from deepeval import evaluate
    from deepeval.dataset import EvaluationDataset
    from deepeval.metrics import AnswerRelevancyMetric
    ...

    dataset = EvaluationDataset()
    # Same alias as before
    dataset.pull(alias="My Generated Dataset")
    evaluate(dataset, metrics=[AnswerRelevancyMetric()])
    ```
  </Tab>

  <Tab value="Locally">
    Alternatively, you can use the `save_as()` method to save synthetic goldens locally:

    ```python
    synthesizer.save_as(
        # Type of file to save ('json' or 'csv')
        file_type='json',
        # Directory where the file will be saved
        directory="./synthetic_data"
    )
    ```

    The `save_as()` method supports the following parameters:

    * `file_type`: Specifies the format to save the data ('json' or 'csv')
    * `directory`: The folder path where the file will be saved
    * `file_name`: Optional custom filename without extension - when provided, the file will be saved as `{file_name}.{file_type}`
    * `quiet`: Optional boolean to suppress output messages about the save location

    By default, the method generates a timestamp-based filename (e.g., "20240523\_152045.json"). When you provide a custom filename with the `file_name` parameter, that name is used as the base filename and the extension is added according to the `file_type` parameter.

    For example, if you specify `file_type='json'` and `file_name='my_dataset'`, the file will be saved as "my\_dataset.json".

    ```python
    # Save as JSON with a custom filename my_dataset.json
    synthesizer.save_as(
        file_type='json',
        directory="./synthetic_data",
        file_name="my_dataset"
    )

    # Save as CSV with a custom filename my_dataset.csv
    synthesizer.save_as(
        file_type='csv',
        directory="./synthetic_data",
        file_name="my_dataset"
    )
    ```

    <Callout type="caution">
      Note that `file_name` should not contain any periods or file extensions, as these will be automatically added based on the `file_type` parameter.
    </Callout>
  </Tab>
</Tabs>

## Customize Your Generations [#customize-your-generations]

`deepeval`'s `Synthesizer`'s generation pipeline is made up of several components, which you can easily customize to determine the quality and style of the resulting generated goldens.

<Callout type="tip">
  You might find it useful to first [learn about all the different components and steps that make up the `Synthesizer` generation pipeline](#how-does-it-work).
</Callout>

### Filtration Quality [#filtration-quality]

You can customize the degree of which generated goldens are filtered away to ensure the quality of synthetic inputs by instantiating the `Synthesizer` with a `FiltrationConfig` instance.

```python
from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import FiltrationConfig

filtration_config = FiltrationConfig(
  critic_model="gpt-4.1",
  synthetic_input_quality_threshold=0.5
)

synthesizer = Synthesizer(filtration_config=filtration_config)
```

There are **THREE** optional parameters when creating a `FiltrationConfig`:

* \[Optional] `critic_model`: a string specifying which of OpenAI's GPT models to use to determine context `quality_score`s, **OR** [any custom LLM model](/docs/metrics-introduction#using-a-custom-llm) of type `DeepEvalBaseLLM`. Defaulted to the &#x2A;*model used in the `Synthesizer`**, else <DefaultLLMModel /> when initialized as a standalone instance.
* \[Optional] `synthetic_input_quality_threshold`: a float representing the minimum quality threshold for synthetic input generation. Inputs with `quality_score`s lower than the `synthetic_input_quality_threshold` will be rejected. Defaulted to `0.5`.
* \[Optional] `max_quality_retries`: an integer that specifies the number of times to retry synthetic input generation if it does not meet the required quality. Defaulted to `3`.

If the `quality_score` is still lower than the `synthetic_input_quality_threshold` after `max_quality_retries`, the golden with the highest `quality_score` will be used.

### Evolution Complexity [#evolution-complexity]

You can customize the evolution types and depth applied by instantiating the `Synthesizer` with an `EvolutionConfig` instance. You should customize the `EvolutionConfig` to vary the complexity of the generated goldens.

```python
from deepeval.synthesizer import synthesizer
from deepeval.synthesizer.config import EvolutionConfig

evolution_config = EvolutionConfig(
    evolutions={
        Evolution.REASONING: 1/4,
        Evolution.MULTICONTEXT: 1/4,
        Evolution.CONCRETIZING: 1/4,
        Evolution.CONSTRAINED: 1/4
    },
    num_evolutions=4
)

synthesizer = Synthesizer(evolution_config=evolution_config)
```

There are **TWO** optional parameters when creating an `EvolutionConfig`:

* \[Optional] `evolutions`: a dict with `Evolution` keys and sampling probability values, specifying the distribution of data evolutions to be used. Defaulted to all `Evolution`s with equal probability.
* \[Optional] `num_evolutions`: the number of evolution steps to apply to each generated input. This parameter controls the complexity and diversity of the generated dataset by iteratively refining and evolving the initial inputs. Defaulted to 1.

<Callout type="info">
  `Evolution` is an `ENUM` that specifies the different data evolution techniques you wish to employ to make synthetic `Golden`s more realistic. `deepeval`'s `Synthesizer` supports 7 types of evolutions, which are randomly sampled based on a defined distribution. You can apply multiple evolutions to each `Golden`, and later access the evolution sequence through the `Golden`'s additional metadata field.

  If used for RAG evaluation: Note that some evolution techniques do not necessarily require that the evolved input can be answered from the context. Currently, only these 4 types of evolutions stick to the context: `Evolution.MULTICONTEXT`, `Evolution.CONCRETIZING`, `Evolution.CONSTRAINED` and `Evolution.COMPARATIVE`.

  ```python
  from deepeval.synthesizer import Evolution

  available_evolutions = {
      Evolution.REASONING: 1/7,
      Evolution.MULTICONTEXT: 1/7, # sticks to the context
      Evolution.CONCRETIZING: 1/7, # sticks to the context
      Evolution.CONSTRAINED: 1/7, # sticks to the context
      Evolution.COMPARATIVE: 1/7, # sticks to the context
      Evolution.HYPOTHETICAL: 1/7,
      Evolution.IN_BREADTH: 1/7,
  }
  ```
</Callout>

### Styling Options [#styling-options]

You can customize the output style and format of any `input` and/or `expected_output` generated by instantiating the `Synthesizer` with a `StylingConfig` instance (for single-turn generations) and/or a `ConversationalStylingConfig` instance (for multi-turn generations).

<Tabs items="[&#x22;Single-Turn&#x22;, &#x22;Multi-Turn&#x22;]">
  <Tab value="Single-Turn">
    ```python
    from deepeval.synthesizer import Synthesizer
    from deepeval.synthesizer.config import StylingConfig

    styling_config = StylingConfig(
      input_format="Questions in English that asks for data in database.",
      expected_output_format="SQL query based on the given input",
      task="Answering text-to-SQL-related queries by querying a database and returning the results to users",
      scenario="Non-technical users trying to query a database using plain English.",
    )

    synthesizer = Synthesizer(styling_config=styling_config)
    ```

    There are **FOUR** optional parameters when creating a `StylingConfig`:

    * \[Optional] `input_format`: a string, which specifies the desired format of the generated `input`s in the synthesized goldens. Defaulted to `None`.
    * \[Optional] `expected_output_format`: a string, which specifies the desired format of the generated `expected_output`s in the synthesized goldens. Defaulted to `None`.
    * \[Optional] `task`: a string, representing the purpose of the LLM application you're trying to evaluate are tasked with. Defaulted to `None`.
    * \[Optional] `scenario`: a string, representing the setting of the LLM application you're trying to evaluate are placed in. Defaulted to `None`.

    The `scenario`, `task`, `input_format`, and/or `expected_output_format` parameters, if provided at all, are used to enforce the styles and formats of any generated goldens.
  </Tab>

  <Tab value="Multi-Turn">
    ```python
    from deepeval.synthesizer import Synthesizer
    from deepeval.synthesizer.config import ConversationalStylingConfig

    conversational_styling_config = ConversationalStylingConfig(
      scenario_format="Questions in English that asks for data in database.",
      expected_outcome_format="SQL query based on the given input",
      conversational_task="Answering text-to-SQL-related queries by querying a database and returning the results to users",
      scenario_context="Non-technical users trying to query a database using plain English.",
      participant_roles="A customer support agent and a non-technical end user.",
    )

    synthesizer = Synthesizer(conversational_styling_config=conversational_styling_config)
    ```

    There are **FIVE** optional parameters when creating a `ConversationalStylingConfig`:

    * \[Optional] `scenario_context`: a string, representing the setting of the LLM application you're trying to evaluate are placed in. Defaulted to `None`.
    * \[Optional] `conversational_task`: a string, representing the purpose of the LLM application you're trying to evaluate are tasked with. Defaulted to `None`.
    * \[Optional] `participant_roles`: a string, describing the roles of the participants involved in the conversation. Defaulted to `None`.
    * \[Optional] `scenario_format`: a string, which specifies the desired format of the generated conversation scenarios. Defaulted to `None`.
    * \[Optional] `expected_outcome_format`: a string, which specifies the desired format of the generated `expected_outcome`s in the synthesized `ConversationalGolden`s. Defaulted to `None`.

    The `scenario_context`, `conversational_task`, `participant_roles`, `scenario_format`, and/or `expected_outcome_format` parameters, if provided at all, are used to enforce the styles and formats of any generated conversational goldens.
  </Tab>
</Tabs>

## How Does it Work? [#how-does-it-work]

`deepeval`'s `Synthesizer` generation pipeline consists of four main steps:

1. **Input Generation**: Generate synthetic goldens `input`s with or without provided contexts.
2. **Filtration**: Filter away any initial synthetic goldens that don't meet the specified generation standards.
3. **Evolution**: Evolve the filtered synthetic goldens to increase complexity and make them more realistic.
4. **Styling**: Style the output formats of the `input`s and `expected_output`s of the evolved synthetic goldens.

This generation pipeline is the same for `generate_goldens_from_docs()`, `generate_goldens_from_contexts()`, and `generate_goldens_from_scratch()`.

<Callout type="tip">
  There are two steps not mentioned - the context construction step and expected output generation step.

  The **context construction step** [(which you can learn how it works here)](synthesizer-generate-from-docs#how-does-context-construction-work) happens before the initial generation step and the reason why the context construction step isn't mentioned is because it is only required if you're using the `generate_goldens_from_docs()` method.

  As for the **expected output generation step**, it's omitted because it is a trivial one-step process that simply happens right before the final styling step.
</Callout>

### Input Generation [#input-generation]

In the initial **input generation** step, `input`s of goldens are generated with or without provided contexts using an LLM. Provided contexts, which can be in the form of a list of strings or a list of documents, allow generated goldens to be grounded in information presented in your knowledge base.

### Filtration [#filtration]

<Callout type="note">
  The position of this step might be a surprise to many but, the filtration step happens so early on in the pipeline because `deepeval` assumes that goldens that pass the initial filtration step will not degrade in quality upon further evolution and styling.
</Callout>

In the **filtration** step, `input`s of generated goldens are subject to quality filtering. These synthetic `input`s are evaluated and assigned a quality score (0-1) by an LLM based on:

* **Self-containment**: The `input` is understandable and complete without needing additional external context or references.
* **Clarity**: The `input` clearly conveys its intent, specifying the requested information or action without ambiguity.

<div
  style="{
  display: &#x22;flex&#x22;,
  alignItems: &#x22;center&#x22;,
  justifyContent: &#x22;center&#x22;,
}"
>
  <ImageDisplayer src="ASSETS.generationFiltration" />
</div>

Any goldens that has a quality scores below the `synthetic_input_quality_threshold` will be re-generated. If the quality score still does not meet the required `synthetic_input_quality_threshold` after the allowed `max_quality_retries`, the most generation with the highest score is used. As a result, some generated `Goldens` in your final evaluation dataset may not meet the minimum input quality scores, but you will be guaranteed at least a golden regardless of its quality.

[Click here](#filtration-quality) to learn how to customize the `synthetic_input_quality_threshold` and `max_quality_retries` parameters.

### Evolution [#evolution]

In the **evolution** step, the `input`s of the filtered goldens are rewritten to make more complex and realistic, often times indistinguishable from human curated goldens. Each `input` is rewritten `num_evolutions` times, where each evolution is sampled from the `evolution` distribution which adds an additional layer of complexity to the rewritten `input`.

[Click here](#evolution-types-and-depth) To learn how to customize the `evolution` and `num_evolutions` parameters.

<Callout type="info">
  As an example, a golden might take the following evolutionary route when `num_evolutions` is set to 2 and `evolutions` is a dictionary containing `Evolution.IN_BREADTH`, `Evolution.COMPARATIVE`, and `Evolution.REASONING`, with sampling probabilities of 0.4, 0.2, and 0.4, respectively:

  <div
    style="{
  display: &#x22;flex&#x22;,
  alignItems: &#x22;center&#x22;,
  justifyContent: &#x22;center&#x22;,
}"
  >
    <ImageDisplayer src="ASSETS.evolutions" />
  </div>
</Callout>

### Styling [#styling]

<Callout type="tip">
  This might be useful to you if for example you want to generate goldens in another language, or have the `expected_output`s to be in SQL format for a text-sql use case.
</Callout>

In the final **styling** step, the `input`s and `expected_outputs` of each golden are rewritten into the desired formats and styles if required. This can be configured by setting the `scenario`, `task`, `input_format`, and `expected_output_format` parameters, and `deepeval` will use what you have provided to style goldens tailored to your use case at the end of the generation pipeline to ensure all synthetic data makes sense to you.

[Click here](#styling-options) to learn how to customize the format and style of the synthetic `input`s and `expected_output`s being generated.

## FAQs [#faqs]

<FAQs
  qas="[
  {
    question: &#x22;Does the `Synthesizer` generate `actual_outputs` for my goldens?&#x22;,
    answer: (
      <>
        No. The <code>Synthesizer</code> generates <code>input</code>s (and
        optionally <code>expected_output</code>s), but{&#x22; &#x22;}
        <code>actual_output</code>s are produced by your LLM application at
        evaluation time, not by <code>deepeval</code>.
      </>
    ),
  },
  {
    question: &#x22;Can the `Synthesizer` generate multi-turn turns?&#x22;,
    answer: (
      <>
        No. Multi-turn generation produces <code>ConversationalGolden</code>s
        without <code>turns</code> — use the{&#x22; &#x22;}
        <a href=&#x22;/docs/conversation-simulator&#x22;>ConversationSimulator</a> to
        simulate the actual <code>turns</code>.
      </>
    ),
  },
  {
    question: &#x22;Which `generate_goldens_from_*` method should I use?&#x22;,
    answer: (
      <>
        <code>generate_goldens_from_docs</code> is a superset of{&#x22; &#x22;}
        <a href=&#x22;/docs/synthesizer-generate-from-contexts&#x22;>
          generate_goldens_from_contexts
        </a>
        , which is a superset of{&#x22; &#x22;}
        <a href=&#x22;/docs/synthesizer-generate-from-scratch&#x22;>
          generate_goldens_from_scratch
        </a>
        . Use{&#x22; &#x22;}
        <a href=&#x22;/docs/synthesizer-generate-from-docs&#x22;>
          generate_goldens_from_docs
        </a>{&#x22; &#x22;}
        to let <code>deepeval</code> handle context extraction, or a
        lower-level method for more control.
      </>
    ),
  },
  {
    question: &#x22;How do I control the quality, complexity, and style of goldens?&#x22;,
    answer: (
      <>
        Pass a <code>FiltrationConfig</code> (input quality threshold),{&#x22; &#x22;}
        <code>EvolutionConfig</code> (complexity via evolutions), and{&#x22; &#x22;}
        <code>StylingConfig</code> (task, scenario, and output formats) when
        instantiating the <code>Synthesizer</code>.
      </>
    ),
  },
  {
    question: &#x22;Can my team generate goldens without code?&#x22;,
    answer: (
      <>
        Yes. On <a href=&#x22;https://www.confident-ai.com&#x22;>Confident AI</a> you
        can connect your knowledge bases and run the generation pipeline
        no-code — tweak filtration, evolutions, and styling, experiment with
        variations, and collaborate on the resulting dataset as a team.
      </>
    ),
  },
]"
/>
