# # import Sastrawi package
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# import swifter

# # create stemmer
# factory = StemmerFactory()
# stemmer = factory.create_stemmer()

# # stemmed
# def stemmed_wrapper(term):
#     return stemmer.stem(term)

# term_dict = {}

# for document in dataSB['textdata_normalized']:
#     for term in document:
#         if term not in term_dict:
#             term_dict[term] = ' '
            
# print(len(term_dict))