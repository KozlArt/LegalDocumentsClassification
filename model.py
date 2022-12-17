import pandas as pd
import numpy as np
from tqdm import tqdm

import re

import spacy
from spacy.lang.ru.examples import sentences

from tika import parser

from typing import Tuple
from io import BytesIO
import os
import argparse
import re
import shutil
import pdfkit
import fitz



def search_for_text(lines, search_str):
    """
    Search for the search string within the document lines
    """
    for line in lines:
        # Find all matches within one line
        results = re.findall(search_str, line, flags = re.IGNORECASE)
        # In case multiple matches within one line
        for result in results:
            yield result

def highlight_matching_data(page, matched_values):
    """
    Highlight matching values
    """
    matches_found = 0
    # Loop throughout matching values
    for val in matched_values:
        matches_found += 1
        matching_val_area = page.searchFor(val)
        # print("matching_val_area",matching_val_area)
        highlight = None

        highlight = page.addHighlightAnnot(matching_val_area)
        
        # To change the highlight colar
        # highlight.setColors({"stroke":(0,0,1),"fill":(0.75,0.8,0.95) })
        # highlight.setColors(stroke = fitz.utils.getColor('white'), fill = fitz.utils.getColor('red'))
        # highlight.setColors(colors= fitz.utils.getColor('red'))
        highlight.update()
    return matches_found

def highlight_matching_data(page, matched_values, color):
    """
    Highlight matching values
    """
    matches_found = 0
    # Loop throughout matching values
    for val in matched_values:
        if len(val) < 15 or len(val.split()) < 3: 
            continue
        matches_found += 1
        matching_val_area = page.searchFor(val)
        # print("matching_val_area",matching_val_area)
        highlight = None

        highlight = page.addHighlightAnnot(matching_val_area)

        if color == "main":
            highlight.setColors({"stroke":(0.66, 0.92, 0.70)})
        elif color == "secondааааа":
            highlight.setColors({"stroke":(0.61, 0.87, 0.92)})
        elif color == "warn" or color == "second":
            highlight.setColors({"stroke":(0.96, 0.75, 0.77)})  
        
        highlight.update()
    return matches_found

def process_data(input_file: str, output_file: str, search_str: str, color: str):
    pdfDoc = fitz.open(input_file)
    output_buffer = BytesIO()
    total_matches = 0

    for pg in range(pdfDoc.pageCount):

        page = pdfDoc[pg]
        page_lines = page.getText("text").split('\n')
        matched_values = search_for_text(page_lines, search_str)

        matches_found = highlight_matching_data(
                    page, matched_values, color)

        total_matches += matches_found

    # Save to output
    pdfDoc.save(output_buffer)
    pdfDoc.close()
    # Save the output buffer to the output file
    with open(output_file, mode='wb') as f:
        f.write(output_buffer.getbuffer())

class DocClassifier:
    def __init__(self, nlp, embed, classifier) -> None:
        self.nlp = nlp
        self.embed = embed
        self.classifier = classifier

    def get_text_from_file(self, path: str) -> str:
        parsed = parser.from_file(path)
        return parsed["content"]

    def split_to_paragraphs(self, text: str) -> list:
        return re.split(r"\n[\t ]*\d\.*\d*\.*\d*\.*\d*\.*", text)

    def delete_rubbish(self, text: str, lower=True) -> str:
        doc = self.nlp(text)
        res = [x.text for x in doc if not x.is_punct and not x.is_space]
        if lower:
            return " ".join(res).lower()
        else:
            return " ".join(res)

    def preprocess(self, text: str, lower=True) -> list:
        paragraphs = self.split_to_paragraphs(text)

        for i, line in enumerate(paragraphs):
            paragraphs[i] = self.delete_rubbish(line, lower=lower)

        return paragraphs

    def get_embeddings(self, paragraphs: list) -> list:
        embeddings = []
        for text in paragraphs:
            embeddings.append(self.embed.encode(text))

        return embeddings

    def predict_proba(self, path: str, is_path=True) -> np.array:
        if is_path:
            text = self.get_text_from_file(path)
        else:
            text = path
        paragraphs = self.preprocess(text)
        embeddings = self.get_embeddings(paragraphs)
        res = np.zeros(5)
        for emb in embeddings:
            res += self.classifier.predict_proba([emb])[0]
        return res

    def get_dict(self, path: str, is_path=True) -> dict:
        if is_path:
            text = self.get_text_from_file(path)
        else:
            text = path

        paragraphs = self.preprocess(text)
        embeddings = self.get_embeddings(paragraphs)
        #paragraphs = np.array(self.preprocess(text, lower=False))
        paragraphs = paragraphs = self.split_to_paragraphs(self.get_text_from_file(path))
        paragraphs = [i.rstrip(" ").lstrip(" ") for i in paragraphs]
        paragraphs = [i.replace("(", "\(") for i in paragraphs if "("]
        paragraphs = [i.replace(")", "\)") for i in paragraphs if ")"]
        paragraphs = np.array(paragraphs)
        res = np.zeros(5)
        probs = []
        for emb in embeddings:
            pred = self.classifier.predict_proba([emb])[0]
            probs.append(pred)
            res += pred
        probs = np.array(probs)
        res = res / np.sum(res)

        main_cat_ind = np.argmax(res)
        second_cat_ind = np.argsort(res, axis=0)[-2]

        main_cat = self.classifier.classes_[main_cat_ind]
        second_cat = self.classifier.classes_[second_cat_ind]

        main_cat_prob = res[main_cat_ind]
        second_cat_prob = res[second_cat_ind]

        main_best_sent = paragraphs[np.argsort(probs[:,main_cat_ind], axis=0)][::-1][0:min(6, int(0.4*len(paragraphs)))]
        second_best_sent = paragraphs[np.argsort(probs[:,second_cat_ind], axis=0)][::-1][0:min(6, int(0.4*len(paragraphs)))]

        sent_warnings = []
        for j, prob in enumerate(probs):
            for i, p in enumerate(prob):
                 if i != main_cat_ind and (i != second_cat_ind or main_cat_prob > 0.6) and p > 0.7:
                    sent_warnings.append(paragraphs[j])

        if main_cat_prob > 0.6:
            output = {
                "main_class": {
                    "prob": main_cat_prob,
                    "class": main_cat,
                    "top_quotes":list(main_best_sent),
                    },
                "second_class": None
                }
        else:
            output = {
                "main_class": {
                    "prob": main_cat_prob,
                    "class": main_cat,
                    "top_quotes": list(main_best_sent),
                    },
                "second_class": {
                    "prob": second_cat_prob,
                    "class": second_cat,
                    "top_quotes": list(second_best_sent),
                    }
                }

        return output
    
    def convert_to_pdf(self, path:str) -> None:
        if path.split(".")[-1] == 'pdf':
            shutil.copyfile(path, "./output.pdf")
        else:
            with open("./tmp.txt", 'w') as f:
                f.write(self.get_text_from_file(path))
            opt = {
                    'encoding': 'UTF-8',
                    'enable-local-file-access': True
                }
            pdfkit.from_file("./tmp.txt", "./output.pdf", options=opt)
            
            

    def pdf_viz(self, path:str) -> None:
        self.convert_to_pdf(path)
        out = self.get_dict("./output.pdf")

        for text in out["main_class"]["top_quotes"]:
            lines = text.split("\n")
            lines = [i for i in lines if i != "" and i!= " "]
            print(lines)
            for line in lines:
                process_data("./output.pdf", "./output.pdf", line, color= "main")

        if out["second_class"] is not None:
            for text in out["second_class"]["top_quotes"]:
                lines = text.split("\n")
                lines = [i for i in lines if i != "" and i!= " "]
                for line in lines:
                    process_data("./output.pdf", "./output.pdf", line, color= "second")
        
