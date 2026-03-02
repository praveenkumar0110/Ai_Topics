
# import fitz
# import cv2
# import numpy as np
# import pytesseract
# from PIL import Image
# import imagehash
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# import gc

# print("🔹 Loading AI Models...")

# text_model = SentenceTransformer('all-MiniLM-L6-v2')
# image_model = SentenceTransformer('clip-ViT-B-32')

# pdf_path = "CP.pdf"
# doc = fitz.open(pdf_path)

# visual_hashes = []
# page_images = []

# total_pages = len(doc)

# print(f"📄 Total Pages: {total_pages}")
# print("⚙ Stage 1: Extracting Hash + Image...\n")


# for i in range(total_pages):

#     page = doc.load_page(i)


#     pix = page.get_pixmap(dpi=150)

#     img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     pil_img = Image.fromarray(gray)

#     phash = imagehash.phash(pil_img)

#     visual_hashes.append(phash)
#     page_images.append(pil_img)

#     print(f"✅ Hash Extracted Page {i+1}")

#     del page, pix, img, gray
#     gc.collect()

# print("\n🔍 Stage 2: Finding Layout Similar Pages...\n")

# candidate_pairs = []

# for i in range(total_pages):
#     for j in range(i+1, total_pages):

#         hash_dist = visual_hashes[i] - visual_hashes[j]

#         if hash_dist < 25:  
#             candidate_pairs.append((i, j))

# print(f"📌 Candidate Pairs Found: {len(candidate_pairs)}")


# print("\n🧠 Stage 3: Running Image AI...\n")

# image_embeddings = {}

# for (i, j) in candidate_pairs:

#     if i not in image_embeddings:
#         image_embeddings[i] = image_model.encode([page_images[i]])[0]

#     if j not in image_embeddings:
#         image_embeddings[j] = image_model.encode([page_images[j]])[0]

# print("✅ Image Embeddings Ready")


# print("\n🧠 Stage 4: OCR + Text AI...\n")

# text_embeddings = {}
# duplicates = []

# for (i, j) in candidate_pairs:

#     img_sim = cosine_similarity(
#         image_embeddings[i].reshape(1,-1),
#         image_embeddings[j].reshape(1,-1)
#     )[0][0]

#     if img_sim > 0.85:

#         if i not in text_embeddings:
#             text_i = pytesseract.image_to_string(page_images[i])
#             text_embeddings[i] = text_model.encode(text_i)

#         if j not in text_embeddings:
#             text_j = pytesseract.image_to_string(page_images[j])
#             text_embeddings[j] = text_model.encode(text_j)

#         text_sim = cosine_similarity(
#             text_embeddings[i].reshape(1,-1),
#             text_embeddings[j].reshape(1,-1)
#         )[0][0]

#         hash_dist = visual_hashes[i] - visual_hashes[j]

#         final_score = (0.4 * text_sim) + (0.4 * img_sim) + (0.2 * (1 - hash_dist/64))

#         if final_score > 0.90:
#             duplicates.append((i+1, j+1, final_score))

# print("\n📢 Duplicate Pages Found:\n")  

# seen = set()

# for d in duplicates:
#     if (d[1], d[0]) not in seen:
#         print(f"Page {d[0]} ≈ Page {d[1]} | Score: {round(d[2],2)}")
#         seen.add((d[0], d[1]))



#Same Layout + differnt text not duplicate

import fitz
import cv2
import numpy as np
import pytesseract
from PIL import Image
import imagehash
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import gc
import re



text_model = SentenceTransformer('all-MiniLM-L6-v2')
image_model = SentenceTransformer('clip-ViT-B-32')

pdf_path = "CP.pdf"
doc = fitz.open(pdf_path)

'''
visual_hashes = [
  ff2a9c3d8e10a2b4,   # Page 1
  ff2a9c3d8e10a2b0,   # Page 2
  88aa33ff2211cc99,   # Page 3
  ff2a9c3d8e10a2b6,   # Page 4
  77bb44dd1122ee88    # Page 5
]
'''
visual_hashes = []
page_images = []

total_pages = len(doc)

print(f"Total Pages: {total_pages}")
print(" Stage 1: Extracting Hash + Image...\n")
#Each page process pannrom for layout hash
for i in range(total_pages):

    page = doc.load_page(i)
    #page --->image
    #dpi means imahe quality 150 is good for ocr and ai  
    pix = page.get_pixmap(dpi=150)

    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    
    '''
    PDF Page
   ↓
Pixel bytes (flat)
   ↓ frombuffer
Number array
   ↓ reshape
3D Image Matrix pixel
   ↓
AI usable image
    '''
    # color removal 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #PIl Format NumPy array → PIL Image
    pil_img = Image.fromarray(gray)

    phash = imagehash.phash(pil_img)

    visual_hashes.append(phash)
    # gray image store panrom for ocr and ai
    page_images.append(pil_img)

    print(f" Hash Extracted Page {i+1}")

    del page, pix, img, gray
    gc.collect()


print("\n Stage 2: Finding Layout Similar Pages...\n")

candidate_pairs = []
'''
candidate_pairs = [
  (0,2),
  (1,3),
  (2,4)
]
'''
# Layout match  

for i in range(total_pages):
    for j in range(i+1, total_pages):
    
        hash_dist = visual_hashes[i] - visual_hashes[j]

        if hash_dist < 25:
            candidate_pairs.append((i, j))

print(f" Candidate Pairs Found: {len(candidate_pairs)}")


print("\n Stage 3: Running Image AI...\n")


#Page image → AI vector

image_embeddings = {}
'''
image_embeddings = {
   0: vector0,
   1: vector1,
   2: vector2,
   3: vector3,
   4: vector4
}
'''

for (i, j) in candidate_pairs:

    if i not in image_embeddings:
        image_embeddings[i] = image_model.encode([page_images[i]])[0]

    if j not in image_embeddings:
        image_embeddings[j] = image_model.encode([page_images[j]])[0]

print(" Image Embeddings Ready")


def extract_product_lines(text):
    lines = text.split("\n")
    product_lines = []

    for line in lines:
        if len(line.strip()) > 5:
            #letter and number mix---add
            if re.search(r'[A-Z]+\d+|\d+[A-Z]+', line):
                product_lines.append(line.strip())

    return product_lines


print("\n Stage 4: OCR + Text AI + Product Check...\n")

text_embeddings = {}

'''
text_embeddings = {
  0: vector0,
  2: vector2
}
'''

duplicates = []

for (i, j) in candidate_pairs:
#coseine similaritycompare image
    img_sim = cosine_similarity(
        image_embeddings[i].reshape(1,-1),
        image_embeddings[j].reshape(1,-1)
    )[0][0]

    if img_sim > 0.85:
        # if ima_sim 0.96 then ocr goes and text similarity and product check panrom

        text_i = pytesseract.image_to_string(page_images[i])
        text_j = pytesseract.image_to_string(page_images[j])

        if i not in text_embeddings:
            text_embeddings[i] = text_model.encode(text_i)

        if j not in text_embeddings:
            text_embeddings[j] = text_model.encode(text_j)

        text_sim = cosine_similarity(
            text_embeddings[i].reshape(1,-1),
            text_embeddings[j].reshape(1,-1)
        )[0][0]

        # PRODUCT COMPARISON
        prod_i = extract_product_lines(text_i)
        prod_j = extract_product_lines(text_j)
#easy comparre 
        set_i = set(prod_i)
        set_j = set(prod_j)
#& = Intersection
        common = set_i & set_j
#how many percentage of product lines match panrom same product / total products
        product_overlap = len(common) / max(len(set_i), 1)

        # Layout similarity exact match panrom
        hash_dist = visual_hashes[i] - visual_hashes[j]
        layout_sim = 1 - (hash_dist / 64)

    
        final_score = (
            0.3 * text_sim +
            0.3 * img_sim +
            0.2 * layout_sim +
            0.2 * product_overlap
        )

        
        if final_score > 0.90 and product_overlap > 0.6:
            duplicates.append((i+1, j+1, final_score))


print("\nExact Duplicate Pages Found:\n")

seen = set()

for d in duplicates:
    if (d[1], d[0]) not in seen:
        print(f"Page {d[0]} ≈ Page {d[1]} | Score: {round(d[2],2)}")
        seen.add((d[0], d[1]))