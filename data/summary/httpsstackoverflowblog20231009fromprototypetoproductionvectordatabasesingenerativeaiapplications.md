# Vector Databases and Generative AI

## Introduction
Since the rise of ChatGPT, the general public has realized that generative artificial intelligence (GenAI) could potentially transform our lives. The availability of large language models (LLMs) has also changed how developers build AI-powered applications and has led to the emergence of various new developer tools. Although vector databases have been around long before ChatGPT, they have become an integral part of the GenAI technology stack, as vector databases can address some of LLMs’ key limitations, such as hallucinations and lack of long-term memory.

## What are Vector Databases?
Vector databases store and provide access to structured and unstructured data, such as text or images, alongside their vector embeddings. Vector embeddings are the data’s numerical representation as a long list of numbers that captures the original data object’s semantic meaning. Usually, machine learning models are used to generate the vector embeddings.

Because similar objects are close together in vector space, the similarity of data objects can be calculated based on the distance between the data object’s vector embeddings. This opens the door to a new type of search technique called vector search that retrieves objects based on similarity. In contrast to traditional keyword-based search, semantic search offers a more flexible way to search for items.

## Use Cases and Benefits
While many traditional databases support storing vector embeddings to enable vector search, vector databases are AI-native, which means they are optimized to conduct lightning-fast vector searches at scale. Because vector search requires the calculation of the distances between the search query and every data object, a classical K-Nearest-Neighbor algorithm is computationally expensive. Vector databases use vector indexing to pre-calculate the distances to enable faster retrieval at query time. Thus, vector databases allow users to find and retrieve similar objects quickly at scale in production.

Traditionally, vector databases have been used in various applications in the search domain. However, with the rise of ChatGPT, it has become more apparent that vector databases can enhance LLMs’ capabilities.

### Enhancing LLMs with Vector Databases
Traditionally, vector databases are used to unlock natural-language searches. They enable semantic searches that are robust to different terminologies or even typos. Vector searches can be performed on and across any modalities, such as images, video, audio, or even their combinations. This, in turn, enables varied and powerful use cases for vector databases, even where traditional databases could not be used at all.

For example, vector databases are used in recommendation systems as a special use case of search. Also, Stack Overflow recently showcased how they used Weaviate to improve customer experiences with better search results.

With the rise of LLMs, vector databases have shown that they can enhance LLM capabilities by acting as an external memory. For example, enterprises use customized chatbots as a first line of customer support or as technical or financial assistants to improve customer experiences. But for a conversational AI to be successful, it needs to meet three criteria:

1. **Understand the user's intent** - General-purpose LLMs can cover this.
2. **Access relevant context** - This is where vector databases can come into play.
3. **Generate a coherent response** - This can be handled by the LLM.

### Rapid Prototyping with Vector Databases
Being able to rapidly prototype is important not only in a hackathon setting but to test out new ideas and derive faster decisions in any fast-paced environment. As an integral part of the technology stack, vector databases should help accelerate the development of GenAI applications. This section covers how vector databases enable developers to do rapid prototyping by addressing setup, vectorization, search, and results.

#### Setup
In our example, we use Weaviate as it is simple to get started with and only requires a few lines of code (not to mention that we are very familiar with it).

To enable rapid prototyping, vector databases are usually easy to set up in a few lines of code. In this example, the setup consists of connecting your Weaviate client to your vector database instance. If you use embedding models or LLMs from providers, such as OpenAI, Cohere, or Hugging Face, you will provide your API key in this step to enable their integrations.

#### Vectorization
Vector databases store and query vector embeddings that are generated from embedding models. That means data must be (manually or automatically) vectorized at import and query time. While you can use vector databases stand-alone (a.k.a. bring your own vectors), a vector database that enables rapid prototyping will take care of vectorization automatically so that you don’t have to write boilerplate code to vectorize your data and queries.

In this example, you define a data collection called MyCollection that provides the structure for your data within your vector database after the initial setup. In this step, you can configure further modules, such as a vectorizer that automatically vectorizes all data objects during import and query time (in this case, text2vec-openai). You can omit this line of code if you want to use the vector database standalone and provide your own vectors.

#### Populating Data
To populate the data collection MyCollection, import data objects in batches, as shown below. The data objects are vectorized automatically with the defined vectorizer.

#### Searching
The key use of vector databases is to enable semantic similarity search. In this example, once the vector database is set up and populated, you can retrieve data from it based on the similarity to the search query ("My query here"). If you defined a vectorizer in the previous step, it will also vectorize the query and retrieve data closest to it in the vector space.

### Hybrid Search
However, lexical and semantic search are not mutually exclusive concepts. Vector databases also store the original data objects alongside their vector embeddings. This not only eliminates the need for a secondary database to host your original data objects but also enables keyword-based searches (BM25). The combination of keyword-based search and vector search as a hybrid search can improve search results. For example, Stack Overflow has implemented hybrid search with Weaviate to achieve better search results.

### Integration with LLMs
Because vector databases have become an integral part of the GenAI technology stack, they must be tightly integrated with the other components. For example, an integration between a vector database and an LLM will relieve developers from having to write separate pieces of boilerplate code to retrieve information from the vector database and then to feed it to the LLM. Instead, it will enable developers to do this in just a few lines of code.

### Production Considerations
For example, Weaviate’s modular ecosystem enables you to integrate state-of-the-art generative models from providers, such as OpenAI, Cohere, or Hugging Face, by defining a generative module (in this case, generative-openai). This enables you to extend the semantic search query (with the .with_generate() method) to a retrieval-augmented generative query. The .with_near_text() method first retrieves the relevant context for the property some_text, which is then used in the prompt "Summarize {some_text} in a tweet".

Although it is easy to build impressive prototypes for GenAI applications, moving them to production comes with its own challenges regarding deployment and access management. This section discusses concepts that you need to take into consideration when moving GenAI solutions from prototype to production successfully.

### Scalability
While the amount of data in a prototype may not even require the search capabilities of a full-blown vector database, the amount of handled data can be drastically different in production. To anticipate the amount of data in production, vector databases must be able to scale into billions of data objects according to various needs, such as maximum ingestion, largest possible dataset size, maximum of queries per second, etc.

### Vector Indexing
To enable lightning-fast vector searches at scale, vector databases use vector indexing. Vector indexing is what sets vector databases apart from other vector-capable databases that support vector search but are not optimized for it. For example, Weaviate uses hierarchical navigable small world (HNSW) algorithms for vector indexing in combination with product quantization on compressed vectors to unlock reduced memory usage and lightning-fast vector search even with filters. It typically performs nearest-neighbor searches of millions of objects in less than 100ms.

### Deployment and Access Management
A vector database should be able to address different deployment requirements of various production environments. For example, Stack Overflow required a vector database that had to be open-source and not hosted so that it could be run on their existing Azure infrastructure.

To address such requirements, different vector databases come with different deployment options:

- **Self-hosted**
- **Cloud-based**
- **Open-source**

### Data Protection
While choosing the right deployment infrastructure is an essential part of ensuring data protection, access management, and resource isolation are as important to meet compliance regulations and ensure data protection. E.g., if user A uploads a document, only user A should be able to interact with it. Weaviate uses a multi-tenancy concept allows you to comply with regulatory data handling requirements (e.g., GDPR).

### Conclusion
This article provides an overview of vector databases and their use cases. It highlights the importance of vector databases in improving search and enhancing LLM capabilities by giving them access to an external knowledge database to generate factually accurate results.

The article also showcases how vector databases can enable rapid prototyping of GenAI applications. Aside from an easy setup, vector databases can help developers if they handle vectorization of data automatically at import and query time, enable better search not only with vector search but in addition to keyword-based searches, and seamlessly integrate with other components of the technology stack. Additionally, the article discusses how vector databases can support enterprises in moving these prototypes to production by addressing concerns of scalability, deployment, and data protection.

If you are interested in using an open-source vector database for your GenAI application, head over to Weaviate’s Quickstart Guide and try it out yourself.