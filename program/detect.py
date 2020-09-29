import collections
import time

import pandas as pd
import psycopg2
from nltk.corpus import stopwords
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

start = time.perf_counter()
content = {
    "value": " Experimental Physics I & II \"Junior Lab\" \" Physics \" MIT OpenCourseWare Subscribe to the OCW Newsletter Help \" Contact Us FIND COURSES Find courses by: Topic MIT Course Number Department Collections New Courses Most Visited Courses OCW Scholar Courses Audio/Video Lectures Online Textbooks Supplemental Resources OCW Highlights for High School MITx & Related OCW Courses Cross-Disciplinary Topic Lists Energy Entrepreneurship Environment Introductory Programming Life Sciences Transportation Translated Courses 繁體字 / Traditional Chinese Español / Spanish Türkçe / Turkish (비디오)한국 / Korean For Educators OCW Educator Portal Search for Instructor Insights Search for Teaching Materials OCW Collections Instructor Insights by Department MIT Courses about Teaching and Education K-12 OCW Highlights for High School MIT+K12 Videos Higher Ed Teaching Excellence at MIT MIT Undergraduate Curriculum Map Give Now Make a Donation Why Give? Our Supporters Other Ways to Contribute Shop OCW Become a Corporate Sponsor About About MIT OpenCourseWare Site Statistics OCW Stories News Search Tips X Exclude words from your search Put - in front of a word you want to leave out. For example, jaguar speed -car Search for an exact match Put a word or phrase inside quotes. For example, \"tallest building\". Search for wildcards or unknown words Put a * in your word or phrase where you want to leave a placeholder. For example, \"largest * in the world\". Search within a range of numbers Put .. between two numbers. For example, camera $50..$100. Combine searches Put \"OR\" between each search query. For example, marathon OR race. Home » Courses » Physics » Experimental Physics I & II \"Junior Lab\" Experimental Physics I & II \"Junior Lab\" Course Home Syllabus Schedule Summaries Readings Expectations and Grading Policy Ethics in Science and Education Instructor Insights Prof. Janet Conrad's Insights Prof. Gunther Roland's Insights Dr. Sean Robinson's Insights Atissa Banuazizi's Insights Student Insights Re-Designing \"Junior Lab\" Laboratory Safety and Regulations Lab Notebooks Experiments Photoelectric Effect Poisson Statistics Michelson Interferometer Compton Scattering The Franck-Hertz Experiment Relativistic Dynamics Pulsed NMR: Spin Echoes The Speed and Mean Life of Cosmic-Ray Muons Rutherford Scattering Optical Emission Spectra of Hydrogenic Atoms X-Ray Physics Johnson Noise and Shot Noise 21-cm Radio Astrophysics Optical Trapping Optical Pumping of Rubidium Vapor Mössbauer Spectroscopy Superconductivity Doppler-Free Laser Spectroscopy Quantum Information Processing Raman Spectroscopy Reports and Presentations Student Presentations Related Resources Download Course Materials Rubidium magnetometer. (Image by Sarah Hansen at MIT OpenCourseWare.) Instructor(s) Physics Department Faculty, Lecturers, and Technical Staff MIT Course Number 8.13-14 As Taught In Fall 2016 - Spring 2017 Level Undergraduate Cite This Course Ocean Wave Interaction with Ships and Offshore Energy Systems (13.022) Some Description Instructor(s) Prof. As Taught In Spring 2002 Course Number 2.24 Level Undergraduate/Graduate Features Lecture Notes, Student Work Need help getting started? Don't show me this again Don't show me this again Welcome! This is one of over 2,200 courses on OCW. Find materials for this course in the pages linked along the left. MIT OpenCourseWare is a free & open publication of material from thousands of MIT courses, covering the entire MIT curriculum. No enrollment or registration. Freely browse and use OCW materials at your own pace. There's no signup, and no start or end dates. Knowledge is your reward. Use OCW to guide your own life-long learning, or to teach others. We don't offer credit or certification for using OCW. Made for sharing. Download files for later. Send to friends and colleagues. Modify, remix, and reuse (just remember to cite OCW as the source.) Learn more at Get Started with MIT OpenCourseWare Course Description Course Features Instructor insights Course Highlights In this lab-based course, students develop and refine their science communication skills by writing papers in the style of Physical Review Letters and making professional-level oral presentations. Faculty collaborate with communication instructors to support students in developing these professional competencies, and their reflections about teaching the course may be found in the Instructor Insights section of this course site. Insights from students, teaching assistants, and an editor of Physical Review Letters are also available in this section. Course Description Junior Lab consists of two undergraduate courses in experimental physics. The course sequence is usually taken by Juniors (hence the name). Officially, the courses are called Experimental Physics I and II and are numbered 8.13 for the first half, given in the fall semester, and 8.14 for the second half, given in the spring. Each term, students do experiments on phenomena whose discoveries led to major advances in physics. In the process, they deepen their understanding of the relations between experiment and theory, mostly in atomic and nuclear physics. Other Versions Other OCW Versions Archived versions: 8.13-14 Experimental Physics I & II \"Junior Lab\" (Fall 2007) 8.13-14 Experimental Physics I & II \"Junior Lab\" (Fall 2004) 8.13 Experimental Physics I & II \"Junior Lab\" (Fall 2002) Related Content Course Collections See related courses in the following collections: Find Courses by Topic Physics > Atomic, Molecular, Optical Physics Gunther Roland, Janet Conrad, Sean Robinson, and Physics Department Faculty, Lecturers, and Technical Staff. 8.13-14 Experimental Physics I & II \"Junior Lab\". Fall 2016 - Spring 2017. Massachusetts Institute of Technology: MIT OpenCourseWare, https://ocw.mit.edu . License: Creative Commons BY-NC-SA . For more information about using these materials and the Creative Commons license, see our Terms of Use . Find Courses Find by Topic Find by Course Number Find by Department New Courses Most Visited Courses OCW Scholar Courses Audio/Video Courses Online Textbooks Instructor Insights Supplemental Resources MITx & Related OCW Courses Translated Courses For Educators Search for Instructor Insights Search for Teaching Materials Instructor Insights by Department MIT Courses about Teaching and Education Highlights for High School MIT+K12 Videos Teaching Excellence at MIT MIT Undergraduate Curriculum Map Give Now Make a Donation Why Give? Our Supporters Other Ways to Contribute Shop OCW Become a Corporate Sponsor About About OpenCourseWare Site Statistics OCW Stories News Press Releases Tools Help & FAQs Contact Us Site Map Privacy & Terms of Use RSS Feeds Our Corporate Supporters About MIT OpenCourseWare MIT OpenCourseWare makes the materials used in the teaching of almost all of MIT's subjects available on the Web, free of charge. With more than 2,400 courses available, OCW is delivering on the promise of open sharing of knowledge. Learn more » © 2001–2018 Massachusetts Institute of Technology Your use of the MIT OpenCourseWare site and materials is subject to our Creative Commons License and other terms of use . "}
value = content['value']
length = len(value.split(" "))
print("{:-<40} {}".format("* length of the material ", length))
""" Connect to the PostgreSQL database server and get all urls """
conn = None
# material_val_query=material_val_query = "select material_contents.value,oer_materials.id,material_contents.type,material_contents.language from \
#         material_contents,oer_materials where material_contents.type!='translation' and extension='plain' and \
#         oer_materials.word_count>" + str(length - 50) + " and oer_materials.word_count<" + str(length + 50) + \
#                      "and oer_materials.id=material_contents.material_id"
material_val_query = "select material_contents.value,oer_materials.id,material_contents.type," \
                     "material_contents.language,record_id, features_public.value from material_contents," \
                     "oer_materials,features_public where material_contents.type!='translation' and "\
                    "extension='plain' and oer_materials.word_count>" + str(length - 50) + " and " \
                    "oer_materials.word_count<" + \
                     str(length + 50) + "and oer_materials.id=material_contents.material_id and features_" \
                    "public.record_id=oer_materials.id order by oer_materials.id "

material_wiki_query = "select record_id, features_public.value, oer_materials.language from features_public, " \
                      "oer_materials where features_public.record_id = oer_materials.id and " \
                      "oer_materials.word_count>" + str(length - 50) + " and oer_materials.word_count<" + str(
    length + 50) + " order by oer_materials.id "
try:
    # print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(host="localhost", database="x5db", user="postgres", password="hayleys")
    cur = conn.cursor()
    cur.execute(material_val_query)
    docs = cur.fetchall()
    cur.close()
    print("{:-<40} {:.2f} s".format("* Time elapsed - query 0 ", (time.perf_counter() - start)))

    corpus = [(i[0]['value'], i[1], i[2], i[3]) for i in docs]
    df1 = pd.DataFrame([[i[0], len(i[0].split(" ")), i[1], i[2], i[3]] for i in corpus])
    a = list(df1.sort_values(2)[1].values)  # lengths
    b = list(df1.sort_values(2)[0].values)  # values
    c = list(df1.sort_values(2)[2].values)  # material_ids
    data = [(i[4],i[5]) for i in docs]

    # cur = conn.cursor()
    # cur.execute(material_wiki_query)
    # print("{:-<40} {:.2f} s".format("* Time elapsed - query 1 execute ", (time.perf_counter() - start)))
    # data = cur.fetchall()
    # print("{:-<40} {:.2f} s".format("* Time elapsed - query 1 fetch ", (time.perf_counter() - start)))
    # cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        # print('Database connection closed.')

ids = []
lengths = []
wiki = []
for row in data:
    temp = []
    num = row[1]["value"]
    dicTemp = collections.defaultdict(float)
    # f = {}
    for i in range(len(num)):
        temp.append(num[i]["name"])
        temp.append(num[i]["cosine"])
    for k in range(0, len(temp), 2):
        dicTemp[temp[k]] = temp[k + 1]
    wiki.append(dicTemp)
    # lengths.append(len(row[2]["value"]))
    ids.append(row[0])
sw = stopwords.words("english")

wiki_vectorizer = DictVectorizer(sparse=True)
wiki_transform = wiki_vectorizer.fit_transform(wiki)
print("{:-<40} {:.2f} s".format("* Time Elapsed WIKI transform ", (time.perf_counter() - start)))
sim_wiki = cosine_similarity(wiki_transform[-1], wiki_transform, dense_output=True)
print("{:-<40} {:.2f} s".format("* Time Elapsed WIKI similarity ", (time.perf_counter() - start))
      )
tf_vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words=sw)
tf_transform = tf_vectorizer.fit_transform(b + [value])
print("{:-<40} {:.2f} s".format("* Time Elapsed TF transform ", (time.perf_counter() - start)))
sim_tf = cosine_similarity(tf_transform[-1], tf_transform, dense_output=True)
print("{:-<40} {:.2f} s".format("* Time Elapsed TF similarity ", (time.perf_counter() - start))
      )
print("{:-<40} {}".format("* TF transform shape ", tf_transform.shape))
print("{:-<40} {}".format("* WIKI transform shape ", wiki_transform.shape))
print("{:-<40} {}".format("* matching document count ", str(len(docs))))
print("{:-<40} {}".format("* Validity (TF vs WIKI) ", c == ids))

# print([i for i in sim[0] if i > 0.8])
# print(len([i for i in sim[0] if i > 0.8]))
print("{:-<40} {:.2f} s".format("* Total time elapsed ", (time.perf_counter() - start)))
