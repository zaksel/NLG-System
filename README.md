# NLG-System
A natural language generation system to generate technical docs

This code uses [OpenAi gpt-2](https://github.com/openai/gpt-2)
and also [finetuning from nshepperd](https://github.com/nshepperd/gpt-2/tree/finetuning)
## Preprocessing

<details>
#### Download Model with:
Available are Modells "117M" and "354M" adjust output_dir in script!
> python 1Preprocessing\download_model.py 117M

#### Create encoder.json and vocab.bpe
Use subword nmt by Rico Sennrich to create new Byte Pair Encoding for your Language.
1. Place a .txt File you want to extract embeddings from in data/embedding
2. start process with
    > subword-nmt learn-joint-bpe-and-vocab --input data/embedding/yourfile.txt --output data/embedding/vocab.txt --write-vocabulary data/embedding/encoder.txt --separator Ġ --symbols 50257 -v
3. Reformat Output so it fits gpt-2
    > python 1Preprocessing/format_embeddings.py
4. Move encoder.json and vocab.bpe to your base language-model in directory models

#### Convert Trainingdata PDFs to single txt
1. Place PDFs in training/PDF
2. Clean PDFs with own rules (regex, str.replace) in pdf_to_txt.py
3. Use pdf_to_txt.py to parse PDFs to single txt-File (with Apache Tika)
    > python -W ignore 1Preprocessing/pdf_to_txt.py

#### Create .npz
If you don't want to encode your Trainingdata on every run, you can save it encoded with numpy savez and load from that file.
> python 1Preprocessing\pre_encode.py .\data\training\PDF .\data\training\trainingsdaten.npz --model_name ISW_Model
</details>
    
## Training (based on nshepperd)

## Backend (based on OpenAi)

## Frontend

