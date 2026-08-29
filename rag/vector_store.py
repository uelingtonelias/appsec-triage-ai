class VectorStore:

    def add(
        self,
        document,
        embedding
    ):

        raise NotImplementedError(
            "Vector storage has not been implemented yet."
        )

    def search(
        self,
        query,
        top_k=5
    ):

        raise NotImplementedError(
            "Vector search has not been implemented yet."
        )