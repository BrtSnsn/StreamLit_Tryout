# syntax=docker/dockerfile:1
FROM python:3.10-bullseye
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
COPY Orac_scrapper.py Orac_scrapper.py
COPY . /app/

RUN mkdir ~/.streamlit
RUN cp .streamlit/config.toml ~/.streamlit/config.toml
RUN cp .streamlit/credentials.toml ~/.streamlit/credentials.toml

CMD ["Orac_scrapper.py"]



# https://www.section.io/engineering-education/how-to-deploy-streamlit-app-with-docker/
# https://docs.streamlit.io/library/advanced-features/configuration
# http://localhost:8501

# de URL geprint zijn de url's geprint door de docker

# docker config files
# https://github.com/MarcSkovMadsen/awesome-streamlit/blob/master/devops/docker/Dockerfile.prod