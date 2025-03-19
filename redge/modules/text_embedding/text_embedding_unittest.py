import unittest
import numpy as np

from redge.modules.text_embedding.text_embedding import TextEmbedding

class TestTextEmbedding(unittest.TestCase):
    """
    测试 TextEmbedding 类是否能够正确生成文本向量。
    """

    @classmethod
    def setUpClass(cls):
        """在所有测试前加载模型"""
        cls.encoder = TextEmbedding()

    def test_embedding_output_shape(self):
        """测试向量维度是否正确"""
        texts = ["测试文本"]
        embeddings = self.encoder.encode(texts)
        self.assertEqual(embeddings.shape, (1, 512))

    def test_embedding_consistency(self):
        """测试相同文本生成的向量是否一致"""
        text = ["一致性测试"]
        embedding1 = self.encoder.encode(text)
        embedding2 = self.encoder.encode(text)
        self.assertTrue(np.allclose(embedding1, embedding2, atol=1e-5))

    def test_multiple_sentences(self):
        """测试多个文本的向量化"""
        texts = ["你好", "世界", "文本嵌入"]
        embeddings = self.encoder.encode(texts)
        self.assertEqual(embeddings.shape, (3, 512))

if __name__ == "__main__":
    unittest.main()