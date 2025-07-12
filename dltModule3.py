import dlt
import requests
from dlt.destinations import qdrant

# This is the helper function to read the data, annotated as a dlt resource
@dlt.resource
def zoomcamp_data():
    """Reads FAQ data from a URL and yields each document."""
    docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
    docs_response = requests.get(docs_url)
    docs_response.raise_for_status()  # Ensure the request was successful
    documents_raw = docs_response.json()

    for course in documents_raw:
        course_name = course['course']
        for doc in course['documents']:
            doc['course'] = course_name
            yield doc

# Define the destination for our pipeline (a local Qdrant folder)
qdrant_destination = qdrant(
  qd_path="db.qdrant",
)

# Create and run the dlt pipeline
pipeline = dlt.pipeline(
    pipeline_name="zoomcamp_pipeline",
    destination=qdrant_destination,
    dataset_name="zoomcamp_tagged_data"
)

# Run the pipeline with our data resource
load_info = pipeline.run(zoomcamp_data())

# Print the detailed trace of the last run
print(pipeline.last_trace)