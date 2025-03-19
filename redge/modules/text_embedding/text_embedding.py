from sentence_transformers import SentenceTransformer

class TextEmbedding:
    """
    用于加载 bge-small-zh-v1.5 模型并生成文本嵌入向量。
    """

    def __init__(self, model_name="BAAI/bge-small-zh-v1.5", device="cpu"):
        """
        初始化 TextEmbedding 类
        :param model_name: 预训练的 embedding 模型
        :param device: 设备（"cpu" 或 "cuda"）
        """
        self.model = SentenceTransformer(model_name, device=device)

    def encode(self, texts, normalize=True):
        """
        生成文本的向量表示
        :param texts: 单个字符串或字符串列表
        :param normalize: 是否归一化向量
        :return: 生成的文本向量（NumPy 数组）
        """
        return self.model.encode(texts, normalize_embeddings=normalize)