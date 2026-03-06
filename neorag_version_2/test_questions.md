#### Easy Questions (Basic Retrieval)
1. **What is the full title of the book?**  
   Expected: "Steal Like an Artist: 10 Things Nobody Told You About Being Creative".

2. **Who is the author of the book?**  
   Expected: Austin Kleon.

3. **What is the publisher and city?**  
   Expected: Workman Publishing Company, New York.

4. **What is the dedication in the book?**  
   Expected: "For Boom— whenever Boom gets here".

#### Medium Questions (Quotes, Structure, Specific Mentions)
5. **How many principles or chapters are listed in the table of contents?**  
   Expected: 10 (list them if possible, e.g., 1: Steal like an artist, up to 10: Creativity is subtraction).

6. **What is the first principle in the book?**  
   Expected: "Steal like an artist" (starts on page 2 in TOC).

7. **Who is quoted as saying 'Art is theft'?**  
   Expected: Pablo Picasso (from page 7).

8. **What does T.S. Eliot say about poets and stealing?**  
   Expected: "Immature poets imitate; mature poets steal; bad poets deface what they take, and good poets make it into something better..." (from page 8).

9. **Is Pablo Picasso mentioned in the book?**  
   Expected: Yes (quote on page 7).

10. **What does the book say about all advice being autobiographical?**  
    Expected: It's the author's theory; advice is people talking to their past selves; the book is him talking to a previous version of himself (from page 10).

#### Hard Questions (Synthesis, Inference, Images)
11. **What is the book about, based on the introduction?**  
    Expected: Injecting creativity into life and work; ideas for everyone, not just artists; things learned over a decade of making art.

12. **Explain the 'genealogy of ideas' concept from the book.**  
    Expected: Every new idea is a mashup/remix of previous ones; like genetics (mom + dad = you, but sum is bigger); choose influences like teachers, friends, books, music (from pages 18-20).

13. **What does the flowchart on 'Is it worth stealing?' say?**  
    Expected: "Is it worth stealing? → Yes → Steal it → No → Move on to the next thing" (test OCR on the illustration from page 13).

14. **Who does the book quote about originality being 'undetected plagiarism'?**  
    Expected: William Ralph Inge (from page 17).

15. **What advice does the book give about originality and influences?**  
    Expected: Nothing is original; all work builds on what came before; embrace influence; "We are shaped and fashioned by what we love" (Goethe); free from burden of complete originality (synthesis from pages 16-20).

These should thoroughly test your RAG: if "hi_res" works well, easy/medium questions should succeed; hard ones may need tuning chunk_size or k in retriever (e.g., increase k=5 for more context). If many "I don't know," check if images/quotes are extracted (hi_res should OCR them).

Run them and share results if needed — we can refine based on that! 🚀

---

### Questions for `en-test.pdf` (Pure English)

1. What are the three main types of machine learning mentioned in the document?
2. Name at least four popular machine learning algorithms listed.
3. What are some common real-world applications of machine learning?
4. Does the document explain what supervised learning uses?
5. Which companies or products are given as examples of recommendation systems?
6. Is voice assistant technology mentioned as an application of machine learning?
7. According to the text, does machine learning require explicit programming?

### Questions for `fr-test.pdf` (Pure French)

1. Quels sont les trois principaux types d'apprentissage automatique décrits ?
2. Nommez au moins quatre algorithmes d'apprentissage automatique populaires cités.
3. Quelles sont quelques applications courantes de l'apprentissage automatique mentionnées ?
4. De quelles données l'apprentissage supervisé a-t-il besoin selon le document ?
5. Quels exemples d'applications sont donnés pour le filtrage des courriels indésirables et la reconnaissance vocale ?
6. Le document mentionne-t-il l'analyse d'images médicales comme application ?
7. L'apprentissage automatique nécessite-t-il une programmation explicite d'après le texte ?