# Makefile for running university projects

.PHONY: all install topic_modeling sentiment_analysis_russia_ukraine sentiment_analysis_vat_increase pilkada_jateng

# Default target
all: install

# Install required libraries
install:
	pip install -r requirements.txt

# Run Topic Modeling and LDA of Prabowo Subianto's Inaugural Speech
topic_modeling:
	cd topic_modeling_dan_lda_pidato_perdana_prabowo_subianto && python main.py

# Run Sentiment Analysis of Russia vs Ukraine
sentiment_analysis_russia_ukraine:
	cd sentiment_analisis_rusia_vs_ukraine && python src/main.py

# Run Sentiment Analysis of the 12% VAT Increase
sentiment_analysis_vat_increase:
	cd sentiment_analisis_kenaikan_ppn_12_persen && TOKEN=$(TOKEN) python src/main.py

# Run Central Java 2024 Election
pilkada_jateng:
	cd pilkada_jateng_2024 && python src/main.py
