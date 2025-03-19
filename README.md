pip install -r requirements.txt

python3 -m unittest redge.modules.text_embedding.text_embedding_unittest

python3 -m unittest redge.modules.doc_scanner.doc_scanner_unittest

python3 -m unittest redge.modules.doc_splitter.doc_splitter_unittest

python3 -m redge.core.rag.knowledge_builder
