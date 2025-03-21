pip install -r requirements.txt

python3 -m unittest redge.modules.text_embedding.text_embedding_unittest
python3 -m unittest redge.modules.doc_scanner.doc_scanner_unittest
python3 -m unittest redge.modules.doc_splitter.doc_splitter_unittest

python3 -m redge.core.rag.knowledge_builder
python3 -m redge.core.rag.knowledge_query
python3 -m redge.core.rag.knowledge_qa

python3 -m redge.api.server
python3 -m redge.api.rag_client

curl -X POST "http://127.0.0.1:8000/query_stream" \
     -H "Content-Type: application/json" \
     -d '{"question": "中华人民共和国的基本法律有哪些？"}'

python3 -m redge.app.app