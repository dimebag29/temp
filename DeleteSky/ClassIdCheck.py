from transformers import SegformerForSemanticSegmentation

model = SegformerForSemanticSegmentation.from_pretrained("nvidia/segformer-b2-finetuned-ade-512-512")
id2label = model.config.id2label

# "sky" に対応するクラスIDを探す
for k, v in id2label.items():
    if 'sky' in v.lower():
        print(f'{v}: {k}')
