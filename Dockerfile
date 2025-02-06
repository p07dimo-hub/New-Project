## Χρήση του Python 3.9 ως βάση
FROM python:3.9

# Ορισμός του working directory μέσα στο container
WORKDIR /app

# Αντιγραφή του requirements.txt (με τις εξαρτήσεις) στον φάκελο της εφαρμογής
COPY requirements.txt requirements.txt

# Εγκατάσταση των απαιτούμενων Python βιβλιοθηκών
RUN pip install --no-cache-dir -r requirements.txt

# Αντιγραφή όλων των αρχείων στον φάκελο /app
COPY . .

# Εκτέλεση της Streamlit εφαρμογής όταν ξεκινά το container
CMD ["streamlit", "run", "Project.py", "--server.port=8501", "--server.address=0.0.0.0"]


